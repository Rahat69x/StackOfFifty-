"""
Dynamic module loader, hot-reloader, and lifecycle catalog for StackOfFifty.
"""
import importlib
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from core.module_base import BaseModule
from core.logger import get_logger
from core.config_loader import config_loader

logger = get_logger("module_registry")

class ModuleRegistry:
    """Dynamic registry managing all cybersecurity modules."""
    _instance: Optional["ModuleRegistry"] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ModuleRegistry, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_path: str = "platform.config.json"):
        if not getattr(self, "_initialized", False):
            self.config_path = config_path
            self.modules: Dict[str, BaseModule] = {}
            self.config: Dict[str, Any] = config_loader.get_config()
            self._initialized = True

    def reload_master_config(self):
        """Reload platform.config.json and refresh configuration."""
        self.config = config_loader.load()

    def load_all(self):
        """Iterate through configured modules and load all marked as enabled."""
        self.reload_master_config()
        loaded_count = 0
        for mod_config in self.config.get("modules", []):
            if mod_config.get("status") == "enabled":
                try:
                    self._load_module(mod_config)
                    loaded_count += 1
                except Exception as e:
                    logger.error(f"Failed to load module {mod_config.get('id')} ({mod_config.get('name')}): {e}")
        logger.info(f"Loaded {loaded_count} active modules into registry.")

    def _load_module(self, mod_config: Dict[str, Any]):
        """Load or reload a single module class dynamically."""
        cfg_path = mod_config.get("config_path")
        merged_config = dict(mod_config)
        if cfg_path and Path(cfg_path).exists():
            try:
                with open(cfg_path, "r", encoding="utf-8") as f:
                    module_cfg = json.load(f)
                merged_config.update(module_cfg)
            except Exception as e:
                logger.warning(f"Could not load override config for {mod_config.get('id')}: {e}")

        raw_entry = merged_config.get("entry_point", "")
        # Normalize entry point to module import string: e.g. "modules/01_honeypot/main.py" -> "modules.01_honeypot.main"
        entry = raw_entry.replace("/", ".").replace("\\", ".")
        if entry.endswith(".py"):
            entry = entry[:-3]

        # Ensure cwd is on sys.path
        cwd_str = str(Path.cwd().resolve())
        if cwd_str not in sys.path:
            sys.path.insert(0, cwd_str)

        if entry in sys.modules:
            module_lib = importlib.reload(sys.modules[entry])
        else:
            module_lib = importlib.import_module(entry)

        if not hasattr(module_lib, "Module"):
            raise AttributeError(f"Module entry point {entry} does not define a 'Module' class.")

        module_class = getattr(module_lib, "Module")
        instance = module_class(merged_config)
        self.modules[merged_config["id"]] = instance
        logger.info(f"Successfully registered module: {instance.id} ({instance.display_name})")

    def get(self, module_id: str) -> Optional[BaseModule]:
        """Retrieve an active module instance by its ID."""
        return self.modules.get(module_id)

    def list_all(self) -> List[Dict[str, Any]]:
        """List summary info for all currently instantiated modules."""
        return [
            {
                "id": m.id,
                "name": m.name,
                "display_name": m.display_name,
                "category": m.category,
                "status": m.status,
                "permission_level": m.config.get("permission_level", "viewer"),
                "lab_only": m.config.get("lab_only", False)
            }
            for m in self.modules.values()
        ]

    def list_all_catalog(self) -> List[Dict[str, Any]]:
        """Return catalog of all 50 modules from configuration with active execution state."""
        catalog = []
        for mod in self.config.get("modules", []):
            mod_id = mod.get("id")
            active_inst = self.modules.get(mod_id)
            item = dict(mod)
            item["is_loaded"] = active_inst is not None
            if active_inst:
                item["runtime_status"] = active_inst.status
            else:
                item["runtime_status"] = "unloaded"
            catalog.append(item)
        return catalog

    def reload(self, module_id: str) -> Optional[BaseModule]:
        """Hot-reload a single module without restarting the platform."""
        self.reload_master_config()
        for mod in self.config.get("modules", []):
            if mod.get("id") == module_id:
                self._load_module(mod)
                logger.info(f"Hot-reloaded module: {module_id}")
                return self.modules.get(module_id)
        raise ValueError(f"Module ID {module_id} not found in configuration.")

    def disable(self, module_id: str):
        """Unload and disable a module from active memory."""
        if module_id in self.modules:
            del self.modules[module_id]
            logger.info(f"Disabled/unloaded module: {module_id}")

module_registry = ModuleRegistry()
