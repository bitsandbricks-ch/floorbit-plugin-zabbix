"""The agent's part: runs on the local agent in the hall, checks each service's TCP port and sends
how many answered. Only counts leave the hall (``privacy: aggregate`` in plugin.yaml)."""
import socket

from floorbit.plugins.agent import AgentPlugin as Base

TIMEOUT = 3


def parse_targets(text):
    """``[(name, host, port)]`` from the lines of the Services setting; bad lines skipped."""
    out = []
    for line in str(text or '').splitlines():
        name, sep, rest = line.partition('=')
        host, colon, port = rest.strip().rpartition(':')
        if sep and name.strip() and colon and host and port.isdigit() and 0 < int(port) < 65536:
            out.append((name.strip(), host.strip('[]'), int(port)))
    return out


def answers(host, port):
    try:
        with socket.create_connection((host, port), timeout=TIMEOUT):
            return True
    except (OSError, ValueError):     # ValueError: a name too long for DNS, or one with a NUL in it
        return False


class AgentPlugin(Base):
    def start(self):
        self.targets = parse_targets(self.settings.get('targets'))
        self.interval = max(5, int(self.settings.get('interval') or 30))
        if not self.targets:
            self.ctx.health('off', 'No services set.')
            return
        self.ctx.thread(self.loop, name='example-check')

    def tick(self):
        down = [name for name, host, port in self.targets if not answers(host, port)]
        up = len(self.targets) - len(down)
        self.ctx.send('status', {'up': up, 'total': len(self.targets)})
        self.ctx.gauge('services_down', len(down))
        # Health may name a service, never its address.
        self.ctx.health('ok' if not down else 'warning' if up else 'error',
                        f'{up} of {len(self.targets)} up' + (f', down: {", ".join(down)}' if down else ''))
        return up, down

    def loop(self):
        while not self.ctx.stopping.is_set():
            # Two agents in one hall (VRRP): only the primary checks, so nothing is counted twice.
            # Nothing restarts this thread: an error that left it would stop the checks until the
            # agent restarts. Say it and try again next round.
            try:
                if self.ctx.primary():
                    self.tick()
                else:
                    self.ctx.health('ok', 'Standby: the primary agent checks the services')
            except Exception as exc:  # noqa: BLE001
                self.ctx.health('error', f'a round failed: {type(exc).__name__}: {exc}'[:300])
                self.ctx.error(f'a round failed: {type(exc).__name__}: {exc}')
            self.ctx.stopping.wait(self.interval)

    def check(self):
        """One line for ``python -m floorbit_agent check``."""
        up, down = self.tick()
        return f'{up} of {up + len(down)} services up'
