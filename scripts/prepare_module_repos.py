"""
Automation script to audit, test, document, and prepare all 50+ StackOfFifty defensive modules
as standalone, push-ready GitHub repositories.
"""
import os
import sys
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

BASE_MODULE_CONTENT = '''"""
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
'''

GITIGNORE_CONTENT = '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE / Editor files
.vscode/
.idea/
*.swp
*.swo

# OS generated files
.DS_Store
Thumbs.db
'''

LICENSE_CONTENT = '''MIT License

Copyright (c) 2026 StackOfFifty SecOps

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

def get_engine_info(mod_dir: Path, mod_slug: str):
    """Inspect core/ directory to find the engine class and file."""
    core_dir = mod_dir / "core"
    engine_file = None
    engine_class = None
    extra_imports = []

    # Priority to <slug>.py, else any py file other than base.py or __init__.py
    preferred = core_dir / f"{mod_slug}.py"
    candidates = [preferred] if preferred.exists() else []
    for f in core_dir.glob("*.py"):
        if f.name not in ("base.py", "__init__.py") and f not in candidates:
            candidates.append(f)

    for c in candidates:
        content = c.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r'class\s+([A-Za-z0-9_]+Engine)\b', content)
        if match:
            engine_class = match.group(1)
            engine_file = c.stem
            break
        match_any = re.search(r'class\s+([A-Za-z0-9_]+)\b', content)
        if match_any:
            engine_class = match_any.group(1)
            engine_file = c.stem
            break

    # Check for external dependencies in core files
    for f in core_dir.glob("*.py"):
        text = f.read_text(encoding="utf-8", errors="ignore")
        if "psutil" in text and "psutil>=5.9.0" not in extra_imports:
            extra_imports.append("psutil>=5.9.0")
        if "pyotp" in text and "pyotp>=2.9.0" not in extra_imports:
            extra_imports.append("pyotp>=2.9.0")
        if "cryptography" in text and "cryptography>=41.0.0" not in extra_imports:
            extra_imports.append("cryptography>=41.0.0")

    return engine_file or mod_slug, engine_class or "Engine", extra_imports

def prepare_module(mod_name: str):
    mod_dir = ROOT_DIR / "modules" / mod_name
    if not mod_dir.is_dir():
        return None

    cfg_path = mod_dir / "module.config.json"
    if not cfg_path.exists():
        return None

    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    mod_id = cfg.get("id", "")
    mod_slug = cfg.get("name", "")
    display_name = cfg.get("display_name", mod_slug.replace("_", " ").title())
    category = cfg.get("category", "Cybersecurity Operations")
    description = cfg.get("description", f"Defensive cybersecurity operations module for {display_name}")
    version = cfg.get("version", "1.0.0")

    fixes = []

    # 1. Ensure core/base.py exists
    core_dir = mod_dir / "core"
    core_dir.mkdir(parents=True, exist_ok=True)
    base_file = core_dir / "base.py"
    if not base_file.exists() or base_file.stat().st_size < 100:
        base_file.write_text(BASE_MODULE_CONTENT, encoding="utf-8")
        fixes.append("added core/base.py fallback")

    # 2. Get engine info
    engine_file, engine_class, extra_deps = get_engine_info(mod_dir, mod_slug)

    # 3. Update main.py
    main_py = mod_dir / "main.py"
    main_code = f'''"""
Module entry point for {display_name}.
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
    from .core.{engine_file} import {engine_class}
    from .api.routes import router, set_module
except (ImportError, ValueError):
    from core.{engine_file} import {engine_class}
    from api.routes import router, set_module

def load_default_config() -> Dict[str, Any]:
    cfg_file = Path(__file__).resolve().parent / "module.config.json"
    if cfg_file.exists():
        with open(cfg_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {{
        "id": "{mod_id}",
        "name": "{mod_slug}",
        "display_name": "{display_name}",
        "category": "{category}",
        "status": "enabled"
    }}

class Module(BaseModule):
    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_default_config()
        super().__init__(config)
        self.engine = {engine_class}(config.get("settings", {{}}))
        self.api_router = router
        set_module(self)
        self.logger.info(f"Initialized {{self.display_name}}")

    async def start(self) -> Dict[str, Any]:
        await self.engine.start()
        self.status = "running"
        self.emit_event("module_started", {{"module_id": self.id, "name": self.name}})
        self.logger.info(f"{{self.display_name}} activated")
        return {{"status": "started", "module": self.name}}

    async def stop(self) -> Dict[str, Any]:
        await self.engine.stop()
        self.status = "stopped"
        self.emit_event("module_stopped", {{"module_id": self.id, "name": self.name}})
        self.logger.info(f"{{self.display_name}} deactivated")
        return {{"status": "stopped", "module": self.name}}

    async def status_check(self) -> Dict[str, Any]:
        return {{
            "module_id": self.id,
            "status": self.status,
            "is_active": self.engine.is_running
        }}

    async def get_results(self) -> Dict[str, Any]:
        return self.engine.get_summary()

# Standalone Application Deployment
app = FastAPI(
    title="{display_name}",
    description="{description}",
    version="{version}"
)

default_module = Module(load_default_config())
set_module(default_module)
app.include_router(router)

@app.get("/")
async def root():
    return {{
        "module": default_module.display_name,
        "status": default_module.status,
        "category": default_module.category,
        "version": "{version}",
        "docs": "/docs"
    }}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
'''
    main_py.write_text(main_code, encoding="utf-8")
    fixes.append("updated main.py for standalone & runnable FastAPI app")

    # 4. Update api/routes.py
    api_dir = mod_dir / "api"
    api_dir.mkdir(parents=True, exist_ok=True)
    routes_py = api_dir / "routes.py"
    routes_code = f'''"""
API routes for {display_name}.
"""
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/{mod_slug}", tags=["{display_name}"])

module_instance = None

def set_module(mod):
    global module_instance
    module_instance = mod

def get_module():
    global module_instance
    if module_instance is None:
        try:
            import main
            if hasattr(main, "default_module"):
                module_instance = main.default_module
            elif hasattr(main, "Module"):
                module_instance = main.Module()
        except Exception:
            pass
    return module_instance

@router.get("/status")
async def get_module_status():
    mod = get_module()
    if not mod:
        raise HTTPException(status_code=503, detail="Module not initialized")
    return await mod.get_results()
'''
    routes_py.write_text(routes_code, encoding="utf-8")
    fixes.append("safeguarded api/routes.py module resolution")

    # 5. Update tests
    tests_dir = mod_dir / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    test_file = tests_dir / f"test_{mod_slug}.py"
    test_code = f'''import sys
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
        mod_pkg = importlib.import_module("modules.{mod_name}.main")
        return getattr(mod_pkg, "Module")
    except (ImportError, ModuleNotFoundError):
        import main
        return getattr(main, "Module")

def test_{mod_slug}_lifecycle():
    async def _run():
        Module = get_module_class()
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
        summary = await mod.get_results()
        assert isinstance(summary, dict)
        stop_res = await mod.stop()
        assert stop_res["status"] == "stopped"

    asyncio.run(_run())

def test_{mod_slug}_engine_functionality():
    Module = get_module_class()
    mod = Module()
    assert hasattr(mod, "engine")
    assert mod.engine is not None
    summary = mod.engine.get_summary()
    assert isinstance(summary, dict)
'''
    test_file.write_text(test_code, encoding="utf-8")
    fixes.append("updated tests for standalone & monorepo lifecycle validation")

    # 6. requirements.txt
    req_file = mod_dir / "requirements.txt"
    base_deps = [
        "fastapi>=0.100.0",
        "uvicorn[standard]>=0.22.0",
        "pydantic>=2.0.0",
        "pytest>=7.0.0",
        "httpx>=0.24.0"
    ]
    all_deps = base_deps + [d for d in extra_deps if d not in base_deps]
    req_file.write_text("\n".join(all_deps) + "\n", encoding="utf-8")
    fixes.append("configured complete requirements.txt")

    # 7. .gitignore
    gitignore_file = mod_dir / ".gitignore"
    gitignore_file.write_text(GITIGNORE_CONTENT, encoding="utf-8")

    # 8. .env.example
    env_example_file = mod_dir / ".env.example"
    env_content = f'''MODULE_NAME={mod_slug}
MODULE_PORT=8000
MODULE_HOST=0.0.0.0
LOG_LEVEL=INFO
DEBUG=false
SAFE_MODE=true
'''
    env_example_file.write_text(env_content, encoding="utf-8")

    # 9. LICENSE
    license_file = mod_dir / "LICENSE"
    license_file.write_text(LICENSE_CONTENT, encoding="utf-8")

    # 10. README.md
    readme_file = mod_dir / "README.md"
    readme_content = f'''# {display_name}

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)

## Description
{description}

* **Category**: `{category}`
* **Module ID**: `{mod_id}`
* **Version**: `{version}`

## Features
- **Defensive Telemetry & Operations**: Engineered for enterprise defensive security operations and research.
- **Asynchronous Lifecycle Control**: Non-blocking asynchronous `start()`, `stop()`, and `status_check()` operations.
- **FastAPI REST API**: Native OpenAPI-compliant endpoints (`/{mod_slug}/status`).
- **Configurable Settings**: Dynamic runtime configuration support via `module.config.json`.
- **Standalone & Monorepo Compatible**: Deployable as an independent microservice or integrated into central SOC platforms.

## Tech Stack
- **Python 3.10+**
- **FastAPI** — High-performance modern web framework for APIs
- **Uvicorn** — Lightning-fast ASGI web server
- **Pydantic** — Data validation and settings management
- **Pytest** — Automated testing framework

## Directory Structure
```
.
├── api/
│   └── routes.py              # FastAPI router and endpoint definitions
├── core/
│   ├── base.py                # Standalone BaseModule interface fallback
│   └── {engine_file}.py       # Core engine and domain logic
├── tests/
│   └── test_{mod_slug}.py     # Automated lifecycle & engine unit tests
├── .env.example               # Template environment configuration
├── .gitignore                 # Standard Python gitignore
├── LICENSE                    # MIT License
├── main.py                    # Application entrypoint & FastAPI app
├── module.config.json         # Module metadata & default configurations
├── README.md                  # Project documentation
└── requirements.txt           # Project dependencies
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/{mod_slug}.git
   cd {mod_slug}
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Linux / macOS:
   source venv/bin/activate
   # Windows:
   .\\venv\\Scripts\\Activate.ps1
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   ```bash
   cp .env.example .env
   ```

## Usage

### Run as Standalone Service
Start the FastAPI server with hot-reloading:
```bash
python main.py
```
Or directly with Uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive API documentation will be available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Run Automated Tests
Execute the test suite:
```bash
pytest
```

## API Endpoints
- `GET /`: Service status and metadata
- `GET /{mod_slug}/status`: Current execution metrics and telemetry summary
- `GET /docs`: Interactive OpenAPI documentation

## License
Distributed under the MIT License. See [LICENSE](LICENSE) for more details.
'''
    readme_file.write_text(readme_content, encoding="utf-8")
    fixes.append("generated root README.md, .gitignore, LICENSE, .env.example")

    # Clean local .pytest_cache if present
    pt_cache = mod_dir / ".pytest_cache"
    if pt_cache.exists():
        shutil.rmtree(pt_cache, ignore_errors=True)

    # 11. Run pytest inside module directory
    test_res = subprocess.run(
        [sys.executable, "-m", "pytest", "tests"],
        cwd=str(mod_dir),
        capture_output=True,
        text=True
    )
    passed = (test_res.returncode == 0)

    return {
        "name": mod_name,
        "display_name": display_name,
        "fixes": ", ".join(fixes),
        "test_status": "PASS" if passed else "FAIL",
        "push_ready": "Yes" if passed else "No",
        "output": test_res.stdout if not passed else ""
    }

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    if target:
        res = prepare_module(target)
        print(json.dumps(res, indent=2))
    else:
        # Run all
        modules = sorted([d.name for d in (ROOT_DIR / "modules").iterdir() if d.is_dir()])
        print(f"Discovered {len(modules)} modules to process.")
        results = []
        for m in modules:
            res = prepare_module(m)
            if res:
                results.append(res)
                # Print one-line status
                print(f"[{res['test_status']}] {res['name']}: {res['fixes']} | Test: {res['test_status']} | Push-ready: {res['push_ready']}")
        with open(ROOT_DIR / "scripts" / "preparation_results.json", "w", encoding="utf-8") as out:
            json.dump(results, out, indent=2)
