# Credential Leak & Breach Monitor (mod_032)

## Purpose & Features
Monitors known public breach corpuses and dumps for exposed corporate email credentials

## Architecture
- `core/credential_leak_monitor.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
