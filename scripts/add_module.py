"""
Module scaffolding CLI for AegisCore.
Enables expanding the platform with new defensive modules (51, 52, 53...)
with zero manual configuration boilerplate.
"""
import sys
import json
import re
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

def slugify(text: str) -> str:
    slug = text.lower()
    slug = re.sub(r'[^a-z0-9]+', '_', slug).strip('_')
    return slug

def scaffold_module(display_name: str, category: str = "Network Security", permission_level: str = "researcher"):
    config_path = root_dir / "platform.config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        master_cfg = json.load(f)

    existing_modules = master_cfg.get("modules", [])
    next_idx = len(existing_modules) + 1
    mod_id = f"mod_{next_idx:03d}"
    mod_slug = slugify(display_name)
    folder_name = f"{next_idx:02d}_{mod_slug}"
    mod_dir = root_dir / "modules" / folder_name

    print(f"\n[*] Scaffolding new defensive module: {display_name}")
    print(f"    ID: {mod_id}")
    print(f"    Category: {category}")
    print(f"    Folder: modules/{folder_name}")

    # 1. Create directory structure
    for sub in ["core", "api", "tests", "docs"]:
        (mod_dir / sub).mkdir(parents=True, exist_ok=True)

    # 2. Create module.config.json
    mod_config = {
        "id": mod_id,
        "name": mod_slug,
        "display_name": display_name,
        "description": f"Automated defensive analysis module for {display_name}",
        "category": category,
        "version": "1.0.0",
        "author": "AegisCore SecOps",
        "status": "enabled",
        "permission_level": permission_level,
        "entry_point": f"modules.{folder_name}.main",
        "dependencies": [],
        "ports": [],
        "tags": [mod_slug, category.lower().replace(" ", "-"), "defensive"],
        "safe_mode": True,
        "lab_only": False,
        "docs_path": "docs/README.md",
        "settings": {}
    }
    with open(mod_dir / "module.config.json", "w", encoding="utf-8") as f:
        json.dump(mod_config, f, indent=2)

    # 3. Create core implementation file
    core_file = mod_dir / "core" / f"{mod_slug}.py"
    with open(core_file, "w", encoding="utf-8") as f:
        f.write(f'''"""
Core implementation logic for {display_name}.
"""
from typing import Dict, Any

class {display_name.replace(" ", "")}Engine:
    def __init__(self, settings: Dict[str, Any]):
        self.settings = settings
        self.is_running = False
        self.telemetry = []

    async def start(self):
        self.is_running = True

    async def stop(self):
        self.is_running = False

    def get_summary(self) -> Dict[str, Any]:
        return {{
            "is_active": self.is_running,
            "telemetry_count": len(self.telemetry)
        }}
''')

    # 4. Create api/routes.py
    api_file = mod_dir / "api" / "routes.py"
    with open(api_file, "w", encoding="utf-8") as f:
        f.write(f'''"""
API routes for {display_name}.
"""
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/{mod_slug}", tags=["{display_name}"])

module_instance = None

def set_module(mod):
    global module_instance
    module_instance = mod

@router.get("/status")
async def get_status():
    if not module_instance:
        raise HTTPException(status_code=503, detail="Module not initialized")
    return await module_instance.get_results()
''')

    # 5. Create main.py
    main_file = mod_dir / "main.py"
    with open(main_file, "w", encoding="utf-8") as f:
        f.write(f'''"""
Module entry point for {display_name}.
"""
from typing import Dict, Any
from core.module_base import BaseModule
from .core.{mod_slug} import {display_name.replace(" ", "")}Engine
from .api.routes import router, set_module

class Module(BaseModule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.engine = {display_name.replace(" ", "")}Engine(config.get("settings", {{}}))
        self.api_router = router
        set_module(self)

    async def start(self) -> Dict[str, Any]:
        await self.engine.start()
        self.status = "running"
        self.emit_event("module_started", {{"module_id": self.id, "name": self.name}})
        return {{"status": "started", "module": self.name}}

    async def stop(self) -> Dict[str, Any]:
        await self.engine.stop()
        self.status = "stopped"
        self.emit_event("module_stopped", {{"module_id": self.id, "name": self.name}})
        return {{"status": "stopped", "module": self.name}}

    async def status_check(self) -> Dict[str, Any]:
        return {{
            "module_id": self.id,
            "status": self.status,
            "is_active": self.engine.is_running
        }}

    async def get_results(self) -> Dict[str, Any]:
        return self.engine.get_summary()
''')

    # 6. Create docs/README.md
    with open(mod_dir / "docs" / "README.md", "w", encoding="utf-8") as f:
        f.write(f'''# {display_name} ({mod_id})

## Purpose & Features
Defensive cybersecurity module designed for {category} analysis.

## Architecture
- `core/{mod_slug}.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
''')

    # 7. Create requirements.txt
    with open(mod_dir / "requirements.txt", "w", encoding="utf-8") as f:
        f.write(f"# Dependencies for {display_name}\n")

    # 8. Create tests/test_<mod_slug>.py
    with open(mod_dir / "tests" / f"test_{mod_slug}.py", "w", encoding="utf-8") as f:
        f.write(f'''import importlib
import asyncio
import pytest

def test_{mod_slug}_lifecycle():
    async def _run():
        module_lib = importlib.import_module("modules.{folder_name}.main")
        Module = getattr(module_lib, "Module")
        config = {{
            "id": "{mod_id}",
            "name": "{mod_slug}",
            "display_name": "{display_name}",
            "category": "{category}",
            "status": "enabled"
        }}
        mod = Module(config)
        start_res = await mod.start()
        assert start_res["status"] == "started"
        status_res = await mod.status_check()
        assert status_res["is_active"] is True
        stop_res = await mod.stop()
        assert stop_res["status"] == "stopped"

    asyncio.run(_run())
''')

    # 9. Register in platform.config.json
    master_entry = {
        "id": mod_id,
        "name": mod_slug,
        "display_name": display_name,
        "category": category,
        "version": "1.0.0",
        "status": "enabled",
        "entry_point": f"modules.{folder_name}.main",
        "config_path": f"modules/{folder_name}/module.config.json",
        "docs_path": f"modules/{folder_name}/docs/README.md",
        "permission_level": permission_level,
        "lab_only": False
    }
    master_cfg["modules"].append(master_entry)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(master_cfg, f, indent=2)

    print(f"[+] Successfully scaffolded and registered {display_name} ({mod_id})!\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/add_module.py \"Module Display Name\" [Category] [Permission Level]")
        sys.exit(1)

    name = sys.argv[1]
    cat = sys.argv[2] if len(sys.argv) > 2 else "Network Security"
    perm = sys.argv[3] if len(sys.argv) > 3 else "researcher"
    scaffold_module(name, cat, perm)
