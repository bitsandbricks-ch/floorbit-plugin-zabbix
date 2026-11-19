"""The manifest loads the way a Floorbit installing it from the Marketplace loads it."""
from conftest import ROOT
from floorbit.plugins import BUILTIN_ONLY, _load


def test_it_loads_as_an_official_plugin():
    spec = _load(ROOT, "official", "1.0")
    assert spec is not None and not spec.error, spec.error if spec else "no plugin.yaml"
    assert not [k for k in BUILTIN_ONLY if spec.manifest.get(k)]
    assert spec.manifest["version"] and spec.manifest.get("icon")
