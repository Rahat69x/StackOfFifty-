# Snort / Suricata IDS Rule Engine (mod_014)

## Purpose & Features
Parses and validates Snort and Suricata network intrusion signature rules for syntax and coverage

## Architecture
- `core/snort_suricata_ids_rule_engine.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
