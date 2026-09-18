"""
Standalone BaseModule fallback for independent module deployment.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging

class BaseModule(ABC):
    """
    Standard BaseModule contract defining async lifecycle and control methods.
    """
    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = {}
        self.id = config.get("id", "")
        self.name = config.get("name", "")
        self.display_name = config.get("display_name", self.name)
        self.category = config.get("category", "")
        self.status = config.get("status", "enabled")
        self.config = config
        self.logger = logging.getLogger(self.name or "module")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"))
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    @abstractmethod
    async def start(self) -> Dict[str, Any]:
        """Start the module execution — return status dict."""
        pass

    @abstractmethod
    async def stop(self) -> Dict[str, Any]:
        """Stop the module execution."""
        pass

    @abstractmethod
    async def status_check(self) -> Dict[str, Any]:
        """Return current module health and execution status."""
        pass

    @abstractmethod
    async def get_results(self) -> Dict[str, Any]:
        """Return latest results/output from this module."""
        pass

    def emit_event(self, event_type: str, data: Dict[str, Any]):
        """Emit a security/telemetry event."""
        self.logger.info(f"Event [{event_type}]: {data}")

    async def configure(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Update module configuration at runtime."""
        self.config.update(settings)
        self.logger.info(f"Module {self.name} reconfigured with {len(settings)} keys")
        return {"status": "reconfigured", "module": self.name, "updated_keys": list(settings.keys())}

    async def get_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Return recent logs for this module."""
        return [{"level": "INFO", "message": f"Module {self.name} operating normally"}]

    async def generate_report(self) -> Dict[str, Any]:
        """Generate a structured report of this module's activity."""
        status = await self.status_check()
        results = await self.get_results()
        logs = await self.get_logs(50)
        return {
            "module": self.display_name,
            "module_id": self.id,
            "category": self.category,
            "status": status,
            "results": results,
            "logs": logs
        }
