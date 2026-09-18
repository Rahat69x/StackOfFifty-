# Behavioral Anomaly Detection Engine (mod_019)

## Purpose & Features
Applies statistical Z-score baseline modeling on authentication frequency and egress bandwidth

## Architecture
- `core/behavioral_anomaly_detector.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
