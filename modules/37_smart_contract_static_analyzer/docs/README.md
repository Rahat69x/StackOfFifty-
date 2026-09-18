# Smart Contract Static Security Auditor (mod_037)

## Purpose & Features
Performs static AST security auditing for Solidity reentrancy bugs and integer anomalies

## Architecture
- `core/smart_contract_static_analyzer.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
