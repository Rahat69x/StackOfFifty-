# Firmware Image Static Auditor (mod_040)

## Purpose & Features
Scans firmware binaries for embedded private keys, hardcoded credentials, and known CVEs

## Architecture
- `core/firmware_binwalk_analyzer.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
