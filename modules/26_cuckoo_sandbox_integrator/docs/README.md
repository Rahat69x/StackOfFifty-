# Automated Sandbox Report Parser (mod_026)

## Purpose & Features
Parses behavioral execution summaries from isolated sandboxes and extracts IOCs

## Architecture
- `core/cuckoo_sandbox_integrator.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
