# DDoS Rate Mitigator & Flood Detector (mod_033)

## Purpose & Features
Detects SYN flood and UDP amplification anomalies, applying token-bucket mitigation

## Architecture
- `core/ddos_rate_mitigator.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
