# Cryptographic Key Storage Auditor (mod_030)

## Purpose & Features
Audits BIP-39 / BIP-44 key derivation parameters and evaluates hardware enclave isolation

## Architecture
- `core/crypto_wallet_auditor.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
