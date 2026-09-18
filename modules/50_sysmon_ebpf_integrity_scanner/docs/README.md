# System Call & Sysmon Telemetry Integrity Scanner (mod_050)

## Purpose & Features
Monitors Windows Sysmon and Linux auditd telemetry pipelines for tampering or log dropping

## Architecture
- `core/sysmon_ebpf_integrity_scanner.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
