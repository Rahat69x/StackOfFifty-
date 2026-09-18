# APT Threat Actor Campaign Matcher (mod_042)

## Purpose & Features
Maps incident observables against known Advanced Persistent Threat (APT) group signatures

## Architecture
- `core/apt_threat_actor_matcher.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
