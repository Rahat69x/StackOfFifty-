# Phishing Email Analyzer (mod_008)

## Purpose & Features
Inspects email headers, SPF/DKIM/DMARC records, homoglyphs, and URL reputations

## Architecture
- `core/phishing_email_analyzer.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
