# Adding New Defensive Modules

To add a new defensive capability (Module 51, 52, 53...), use the automated scaffolding utility.

## One-Command Scaffolding

```bash
# Windows PowerShell
.\scripts\add_module.ps1 "DNS Tunneling Detector" "Network Security" "researcher"

# Cross-platform Python
python scripts/add_module.py "DNS Tunneling Detector" "Network Security" "researcher"
```

## What Happens Automatically
1. Creates directory `modules/51_dns_tunneling_detector/` with `core/`, `api/`, `tests/`, `docs/`.
2. Generates `module.config.json` with metadata.
3. Generates `main.py` inheriting `BaseModule`.
4. Creates test suite in `tests/test_dns_tunneling_detector.py`.
5. Appends the registration into `platform.config.json`.
6. Dynamic hot-reload detects and exposes the new module live on the SOC dashboard without restarting the core platform.
