# MFA Authentication Guard (mod_012)

## Purpose & Features
Validates RFC 6238 TOTP codes, enforces MFA policies, and protects against brute-force

## Architecture
- `core/mfa_authentication_guard.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
