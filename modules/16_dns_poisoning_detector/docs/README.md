# DNS Poisoning Detector (mod_016)

## Purpose & Features
Monitors recursive resolver responses, validates DNSSEC signatures, and detects cache spoofing

## Architecture
- `core/dns_poisoning_detector.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
