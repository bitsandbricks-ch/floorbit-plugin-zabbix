"""The plugin is this repository's root; Floorbit (FLOORBIT_REF) is on PYTHONPATH."""
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def load(name):
    """One of the plugin's files as a module, loaded by path as Floorbit and the agent do."""
    modname = f"plugin_under_test_{name}"
    spec = importlib.util.spec_from_file_location(modname, ROOT / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[modname] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def plugin_root():
    return ROOT
