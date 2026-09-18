# Binary Unpacker & Heuristic Deobfuscator (mod_046)

## Purpose & Features
Analyzes obfuscated scripts (Base64, PowerShell) and identifies UPX packer layers

## Architecture
- `core/packed_code_deobfuscator.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
