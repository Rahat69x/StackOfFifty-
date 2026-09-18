# mTLS Enforcement Gateway (mod_021)

## Purpose & Features
Enforces mutual TLS client certificate validation and audits cipher suite negotiation

## Architecture
- `core/mtls_enforcement_gateway.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
