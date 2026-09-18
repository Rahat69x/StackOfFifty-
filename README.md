# AegisCore — Modular Cybersecurity Defense & Operations Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![Architecture](https://img.shields.io/badge/Defensive-100%25-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AegisCore** is an enterprise-grade, modular cybersecurity platform engineered strictly for defensive operations, threat intelligence aggregation, system telemetry inspection, log correlation, and compliance auditing.

The platform orchestrates 50 self-contained defensive modules connected to a high-performance central control layer through a standardized interface (`BaseModule`).

---

## Architecture Principles

1. **Strict Modularity**: Every module is an isolated unit of execution adhering to the async `BaseModule` contract.
2. **Zero-Code Configurability**: Every setting, name, permission level, and port is controlled from `platform.config.json` and module overrides.
3. **Dynamic Extensibility**: Modules can be hot-reloaded or added on the fly via the `add_module` utility without restarting the platform.
4. **Resilient Local Execution**: Features automatic zero-config fallbacks (SQLite + in-memory pub/sub) for instant local execution without external service dependencies.

---

## Quick Start

### 1. Automated Setup
Run the cross-platform setup script to initialize the environment, database schemas, and administrator credentials:

```bash
# Windows PowerShell
.\scripts\setup.ps1

# Or Python cross-platform
python scripts\setup.py
```

### 2. Run Backend API
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Run SOC Dashboard
```bash
cd dashboard
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to access the AegisCore SOC dashboard.

---

## Project Structure

```
AegisCore/
├── platform.config.json       # Master configuration (Single source of truth)
├── core/                      # Core runtime engine (Never modified per module)
│   ├── module_base.py         # BaseModule abstract class
│   ├── module_registry.py     # Dynamic loader and hot-reloader
│   ├── event_bus.py           # Pub/Sub event communication
│   ├── logger.py              # Centralized logging engine
│   ├── config_loader.py       # Configuration reader & validator
│   ├── auth/                  # JWT and RBAC enforcement
│   ├── database/              # SQLAlchemy 9-table schema & connection
│   └── security/              # Input sanitization & rate limiting
├── api/                       # FastAPI REST backend
│   ├── main.py                # Server entry point & CORS
│   └── routers/               # Module control, logs, alerts, reports, config
├── dashboard/                 # Next.js 14 SOC Dashboard
├── modules/                   # 50 Defensive Cybersecurity Modules
├── scripts/                   # Cross-platform CLI utilities (setup, add_module, health_check)
└── tests/                     # Unit, integration, security, and API test suites
```

---

## License
MIT License. Developed by AegisCore SecOps.
