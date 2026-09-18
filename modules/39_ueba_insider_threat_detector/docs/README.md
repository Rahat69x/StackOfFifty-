# UEBA Behavioral Threat Detector (mod_039)

## Purpose & Features
Correlates user activity baselines to flag off-hours logins and privilege escalation spikes

## Architecture
- `core/ueba_insider_threat_detector.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
