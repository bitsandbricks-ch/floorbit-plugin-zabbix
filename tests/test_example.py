"""The example plugin: the agent part against a port on localhost, the hosted part's widget."""
import socket

import pytest
from conftest import load
from floorbit.plugins.agent import MemoryContext
from floorbit.plugins.base import PluginError

SENDS = {"sends": {"status": {"privacy": "aggregate", "latest": True}}}


@pytest.fixture
def listening():
    server = socket.socket()
    server.bind(("127.0.0.1", 0))
    server.listen()
    yield server.getsockname()[1]
    server.close()


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def test_service_lines():
    m = load("agent")
    assert m.parse_targets("dns = 192.0.2.53:53\nbad\nweb=[2001:db8::1]:443\nx = host:99999") == [
        ("dns", "192.0.2.53", 53), ("web", "2001:db8::1", 443)]


def test_it_counts_what_answers_and_sends_only_counts(listening):
    m = load("agent")
    ctx = MemoryContext("example", {"targets": f"up = 127.0.0.1:{listening}\ndown = 127.0.0.1:{free_port()}"}, SENDS)
    plugin = m.AgentPlugin(ctx)
    plugin.targets = m.parse_targets(ctx.settings["targets"])
    assert plugin.tick() == (1, ["down"])
    assert ctx.sent == [("status", {"up": 1, "total": 2})]
    assert ctx.health_.report()["status"] == "warning"
    # The agent refuses an address in an aggregate kind before it leaves the hall.
    with pytest.raises(PluginError):
        ctx.send("status", {"up": 1, "first": "192.0.2.53"})


def test_the_widget_shows_what_the_agent_sent():
    m = load("plugin")

    class Ctx:
        def __init__(self):
            self.state = {}

        def set_state(self, key, value):
            self.state[key] = value

    plugin = m.Plugin.__new__(m.Plugin)
    plugin.ctx = Ctx()
    assert plugin.widget_summary()["value"] == "-"
    assert plugin.agent_status({"name": "Hall A"}, {"up": 2, "total": 3}) == {"kept": True}
    widget = plugin.widget_summary()
    assert widget["value"] == "2 / 3" and widget["tone"] == "warn" and widget["sub"] == "from Hall A"


def test_a_round_that_breaks_does_not_stop_the_checks(monkeypatch):
    m = load("agent")
    ctx = MemoryContext("example", {}, {"sends": {}})
    plugin = m.AgentPlugin(ctx)
    plugin.interval = 0
    rounds = []

    def tick():
        rounds.append(1)
        if len(rounds) == 1:
            raise KeyError("surprise")
        ctx.stopping.set()

    monkeypatch.setattr(plugin, "tick", tick)
    plugin.loop()
    assert len(rounds) == 2
    assert any("a round failed" in e["error"] for e in ctx.health_.report()["errors"])


def test_a_name_dns_cannot_take_is_down_not_an_error():
    m = load("agent")
    assert m.answers("a" * 300 + ".example.com", 80) is False
    assert m.answers("bad\0name", 80) is False
