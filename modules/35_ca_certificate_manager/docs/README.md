# Internal PKI & Certificate Manager (mod_035)

## Purpose & Features
Manages internal Root/Intermediate CA certificates, CRLs, and automated expiration alarms

## Architecture
- `core/ca_certificate_manager.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
