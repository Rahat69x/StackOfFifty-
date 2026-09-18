"""
Unit tests for module registry dynamic loading and catalog.
"""
import pytest
from core.module_registry import ModuleRegistry

def test_module_registry_loads_enabled_modules():
    registry = ModuleRegistry("platform.config.json")
    registry.load_all()
    assert len(registry.modules) >= 5

    # Check mod_001
    mod1 = registry.get("mod_001")
    assert mod1 is not None
    assert mod1.name == "honeypot_deception_sensor"

    # Check listing
    summary_list = registry.list_all()
    assert any(m["id"] == "mod_001" for m in summary_list)

    # Check catalog (all 50 modules)
    catalog = registry.list_all_catalog()
    assert len(catalog) >= 50
    assert any(m["id"] == "mod_001" and m["is_loaded"] is True for m in catalog)
    assert any(m["id"] == "mod_002" and m["is_loaded"] is True for m in catalog)
