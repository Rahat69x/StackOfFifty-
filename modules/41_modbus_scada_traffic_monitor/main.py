"""
Module entry point for Modbus/SCADA Traffic Protocol Monitor.
"""
import sys
import json
from pathlib import Path
from typing import Dict, Any
from fastapi import FastAPI
import uvicorn

# Setup import paths for standalone or package execution
_pkg_dir = Path(__file__).resolve().parent
if str(_pkg_dir) not in sys.path:
    sys.path.insert(0, str(_pkg_dir))

try:
    from core.module_base import BaseModule
except (ImportError, ModuleNotFoundError):
    try:
        from .core.base import BaseModule
    except (ImportError, ValueError):
        from core.base import BaseModule

try:
    from .core.modbus_scada_traffic_monitor import ModbusSCADATrafficMonitorEngine
    from .api.routes import router, set_module
except (ImportError, ValueError):
    from core.modbus_scada_traffic_monitor import ModbusSCADATrafficMonitorEngine
    from api.routes import router, set_module

def load_default_config() -> Dict[str, Any]:
    cfg_file = Path(__file__).resolve().parent / "module.config.json"
    if cfg_file.exists():
        with open(cfg_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "id": "mod_041",
        "name": "modbus_scada_traffic_monitor",
        "display_name": "Modbus/SCADA Traffic Protocol Monitor",
        "category": "IoT & ICS Security",
        "status": "enabled"
    }

class Module(BaseModule):
    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_default_config()
        super().__init__(config)
        self.engine = ModbusSCADATrafficMonitorEngine(config.get("settings", {}))
        self.api_router = router
        set_module(self)
        self.logger.info(f"Initialized {self.display_name}")

    async def start(self) -> Dict[str, Any]:
        await self.engine.start()
        self.status = "running"
        self.emit_event("module_started", {"module_id": self.id, "name": self.name})
        self.logger.info(f"{self.display_name} activated")
        return {"status": "started", "module": self.name}

    async def stop(self) -> Dict[str, Any]:
        await self.engine.stop()
        self.status = "stopped"
        self.emit_event("module_stopped", {"module_id": self.id, "name": self.name})
        self.logger.info(f"{self.display_name} deactivated")
        return {"status": "stopped", "module": self.name}

    async def status_check(self) -> Dict[str, Any]:
        return {
            "module_id": self.id,
            "status": self.status,
            "is_active": self.engine.is_running
        }

    async def get_results(self) -> Dict[str, Any]:
        return self.engine.get_summary()

# Standalone Application Deployment
app = FastAPI(
    title="Modbus/SCADA Traffic Protocol Monitor",
    description="Deep inspection of Modbus TCP and DNP3 industrial automation network packet payloads",
    version="1.0.0"
)

default_module = Module(load_default_config())
set_module(default_module)
app.include_router(router)

@app.get("/")
async def root():
    return {
        "module": default_module.display_name,
        "status": default_module.status,
        "category": default_module.category,
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
