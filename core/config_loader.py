"""
Configuration loader for AegisCore master and module-specific configurations.
"""
import json
import os
import re
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigLoader:
    """Manages loading, parsing, environment substitution, and hot-updates of configuration."""
    _instance: Optional["ConfigLoader"] = None
    _config: Dict[str, Any] = {}
    _config_path: Path = Path("platform.config.json")

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_path: str = "platform.config.json"):
        self._config_path = Path(config_path)
        if not self._config:
            self.load()

    def _substitute_env_vars(self, data: Any) -> Any:
        """Recursively replace ${VAR_NAME} with environment variable values."""
        if isinstance(data, dict):
            return {k: self._substitute_env_vars(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._substitute_env_vars(item) for item in data]
        elif isinstance(data, str):
            pattern = re.compile(r"\$\{([^}]+)\}")
            matches = pattern.findall(data)
            for match in matches:
                env_val = os.environ.get(match, "")
                data = data.replace(f"${{{match}}}", env_val)
            return data
        return data

    def load(self) -> Dict[str, Any]:
        """Read and parse the master configuration file."""
        if not self._config_path.exists():
            # Fallback to default structure
            self._config = {
                "platform": {"name": "AegisCore", "version": "1.0.0"},
                "modules": []
            }
            return self._config

        with open(self._config_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        self._config = self._substitute_env_vars(raw)
        return self._config

    def get_config(self) -> Dict[str, Any]:
        """Return the cached active configuration."""
        if not self._config:
            self.load()
        return self._config

    def get_module_config(self, module_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve configuration for a specific module by id."""
        for mod in self.get_config().get("modules", []):
            if mod.get("id") == module_id:
                # Merge per-module config file if present
                cfg_path = mod.get("config_path")
                if cfg_path and Path(cfg_path).exists():
                    try:
                        with open(cfg_path, "r", encoding="utf-8") as f:
                            override = json.load(f)
                            return {**mod, **override}
                    except Exception:
                        pass
                return mod
        return None

    def update_platform_config(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Safely apply runtime updates to platform configuration."""
        # Read raw json without env substitution to preserve tokens
        with open(self._config_path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        def recursive_update(base: dict, u: dict):
            for k, v in u.items():
                if isinstance(v, dict) and k in base and isinstance(base[k], dict):
                    recursive_update(base[k], v)
                else:
                    base[k] = v

        recursive_update(raw, updates)

        with open(self._config_path, "w", encoding="utf-8") as f:
            json.dump(raw, f, indent=2)

        return self.load()

config_loader = ConfigLoader()
