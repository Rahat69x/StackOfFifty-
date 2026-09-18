# MITRE ATT&CK & CVE Vulnerability Correlator (mod_036)

## Purpose & Features
Correlates CVE identifiers with MITRE ATT&CK enterprise tactics, techniques, and procedures (TTPs)

## Architecture
- `core/cve_mitre_vuln_correlator.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
