# Threat Intel STIX/TAXII Feed (mod_024)

## Purpose & Features
Ingests STIX/TAXII indicator feeds and matches active IOCs against platform logs

## Architecture
- `core/threat_intel_ingestion_feed.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
