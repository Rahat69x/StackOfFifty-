# Security Policy

## Defensive Mandate
AegisCore is strictly designed as a defensive cybersecurity, telemetry, monitoring, and compliance platform. The generation, integration, or distribution of offensive payloads, keyloggers, rootkits, kernel backdoors, or weaponized exploits is fundamentally prohibited by design and architecture.

## Reporting a Vulnerability
If you discover a security vulnerability within AegisCore, please send an advisory report to `security@aegiscore.local`.

All security vulnerabilities will be promptly evaluated and addressed.

## Secure Configuration Principles
- **Never ship default passwords**: Admin credentials must be established at deployment time via `ADMIN_SEED_PASSWORD` or an interactive CLI prompt.
- **Principle of Least Privilege**: Access to modules is strictly enforced via Role-Based Access Control (`admin`, `researcher`, `viewer`).
- **Audit Trails**: All state changes and execution commands are logged immutably to the `audit_log` table.
