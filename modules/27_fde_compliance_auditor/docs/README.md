# Full Disk Encryption Compliance Auditor (mod_027)

## Purpose & Features
Verifies BitLocker and LUKS volume encryption status and key backup compliance

## Architecture
- `core/fde_compliance_auditor.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
