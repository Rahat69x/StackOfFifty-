# IoT Device UPnP & mDNS Auditor (mod_044)

## Purpose & Features
Discovers and evaluates IoT devices exposing UPnP ports or advertising vulnerable mDNS services

## Architecture
- `core/upnp_mdns_iot_auditor.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
