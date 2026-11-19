"""The plugin is this repository's root; Floorbit (FLOORBIT_REF) is on PYTHONPATH."""
import importlib.util
import sys
from pathlib import Path

import pytest
import yaml
from floorbit.plugins.base import HttpClient

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = yaml.safe_load((ROOT / "plugin.yaml").read_text())


def load(name):
    """One of the plugin's files as a module, loaded by path as Floorbit and the agent do."""
    modname = f"plugin_under_test_{name}"
    spec = importlib.util.spec_from_file_location(modname, ROOT / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[modname] = module
    spec.loader.exec_module(module)
    return module


class Context:
    """What Floorbit hands plugin.py (floorbit/plugins/base.py, Context), for the areas this plugin
    uses: its settings with the manifest's defaults, its log and an HTTP client."""

    def __init__(self, settings):
        self.id = MANIFEST["id"]
        defaults = {s["key"]: s["default"] for s in MANIFEST.get("settings") or [] if "default" in s}
        self.settings = {**defaults, **settings}
        self.lines = []

    def log(self, message):
        self.lines.append(str(message))

    def http(self, base_url="", *, verify=None, timeout=10, auth=None, headers=None):
        if verify is None:
            verify = self.settings.get("verify_ssl", True)
        return HttpClient(base_url, verify=verify, timeout=min(float(timeout), 60), auth=auth,
                          headers=headers, log=self.log)


@pytest.fixture
def make():
    """make(**settings) -> the plugin's hosted part, as Floorbit (or the agent) runs it."""
    module = load("plugin")
    return lambda **settings: module.Plugin(Context(settings))


@pytest.fixture
def plugin_root():
    return ROOT
