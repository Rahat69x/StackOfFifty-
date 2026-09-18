# Process Injection & Memory Auditor (mod_047)

## Purpose & Features
Scans running processes for unbacked memory pages (PAGE_EXECUTE_READWRITE) and hollowed PE headers

## Architecture
- `core/process_memory_dumper_auditor.py`: Implementation logic.
- `api/routes.py`: Endpoints.
- `main.py`: `BaseModule` integration.
