# Kernel Hook & Rootkit Hunter Scanner (mod_031)

## Purpose & Features
Audits system call tables, hidden processes, and kernel module signatures for rootkit indicators

## Architecture
- `core/rootkit_hunter_scanner.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
