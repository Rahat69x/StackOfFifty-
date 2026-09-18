# Secure Web Bastion (mod_013)

## Purpose & Features
Audits HTTP security headers (CSP, HSTS, X-Frame-Options) and detects CORS misconfigurations

## Architecture
- `core/secure_web_bastion.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
