# PE/ELF Binary Static Analyzer (mod_020)

## Purpose & Features
Inspects PE/ELF headers, section hashes, import address tables, and suspicious API imports

## Architecture
- `core/pe_binary_static_analyzer.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
