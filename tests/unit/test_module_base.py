"""
Unit tests verifying BaseModule lifecycle contract and methods.
"""
import asyncio
import pytest
from core.module_base import BaseModule

class ConcreteModule(BaseModule):
    async def start(self):
        self.status = "running"
        return {"status": "started"}

    async def stop(self):
        self.status = "stopped"
        return {"status": "stopped"}

    async def status_check(self):
        return {"status": self.status, "healthy": True}

    async def get_results(self):
        return {"metrics": 42}

def test_base_module_contract():
    async def _async_runner():
        cfg = {
            "id": "mod_999",
            "name": "test_module",
            "display_name": "Test Module",
            "category": "Network Security",
            "status": "enabled"
        }
        mod = ConcreteModule(cfg)
        assert mod.id == "mod_999"
        assert mod.name == "test_module"

        # Start
        res = await mod.start()
        assert res["status"] == "started"
        assert mod.status == "running"

        # Status check
        stat = await mod.status_check()
        assert stat["status"] == "running"
        assert stat["healthy"] is True

        # Get results
        results = await mod.get_results()
        assert results["metrics"] == 42

        # Configure
        conf_res = await mod.configure({"sample_key": "sample_val"})
        assert conf_res["status"] == "reconfigured"
        assert mod.config["sample_key"] == "sample_val"

        # Report
        rep = await mod.generate_report()
        assert rep["module"] == "Test Module"
        assert rep["results"]["metrics"] == 42

        # Stop
        stop_res = await mod.stop()
        assert stop_res["status"] == "stopped"
        assert mod.status == "stopped"

    asyncio.run(_async_runner())
