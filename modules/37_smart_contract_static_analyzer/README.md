# Smart Contract Static Security Auditor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)

## Description
Performs static AST security auditing for Solidity reentrancy bugs and integer anomalies

* **Category**: `Advanced Research`
* **Module ID**: `mod_037`
* **Version**: `1.0.0`

## Features
- **Defensive Telemetry & Operations**: Engineered for enterprise defensive security operations and research.
- **Asynchronous Lifecycle Control**: Non-blocking asynchronous `start()`, `stop()`, and `status_check()` operations.
- **FastAPI REST API**: Native OpenAPI-compliant endpoints (`/smart_contract_static_analyzer/status`).
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
│   └── smart_contract_static_analyzer.py       # Core engine and domain logic
├── tests/
│   └── test_smart_contract_static_analyzer.py     # Automated lifecycle & engine unit tests
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
   git clone https://github.com/<your-username>/smart_contract_static_analyzer.git
   cd smart_contract_static_analyzer
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Linux / macOS:
   source venv/bin/activate
   # Windows:
   .\venv\Scripts\Activate.ps1
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
- `GET /smart_contract_static_analyzer/status`: Current execution metrics and telemetry summary
- `GET /docs`: Interactive OpenAPI documentation

## License
Distributed under the MIT License. See [LICENSE](LICENSE) for more details.
