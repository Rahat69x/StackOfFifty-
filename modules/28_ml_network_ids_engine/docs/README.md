# ML NetFlow Anomaly IDS Engine (mod_028)

## Purpose & Features
Analyzes NetFlow and IPFIX telemetry using Isolation Forest to identify exfiltration

## Architecture
- `core/ml_network_ids_engine.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
