import sys
from pathlib import Path
import asyncio
import pytest

# Ensure module directory is in sys.path for standalone pytest
_mod_dir = Path(__file__).resolve().parent.parent
if str(_mod_dir) not in sys.path:
    sys.path.insert(0, str(_mod_dir))

def get_module_class():
    try:
        import importlib
        mod_pkg = importlib.import_module("modules.02_password_strength_auditor.main")
        return getattr(mod_pkg, "Module")
    except (ImportError, ModuleNotFoundError):
        import main
        return getattr(main, "Module")

def test_password_strength_auditor_lifecycle():
    async def _run():
        Module = get_module_class()
        config = {
            "id": "mod_002",
            "name": "password_strength_auditor",
            "display_name": "Password Strength Auditor",
            "category": "Cryptography & Auth",
            "status": "enabled"
        }
        mod = Module(config)
        start_res = await mod.start()
        assert start_res["status"] == "started"
        status_res = await mod.status_check()
        assert status_res["is_active"] is True
        summary = await mod.get_results()
        assert isinstance(summary, dict)
        stop_res = await mod.stop()
        assert stop_res["status"] == "stopped"

    asyncio.run(_run())

def test_password_strength_auditor_engine_functionality():
    Module = get_module_class()
    mod = Module()
    assert hasattr(mod, "engine")
    assert mod.engine is not None
    summary = mod.engine.get_summary()
    assert isinstance(summary, dict)
