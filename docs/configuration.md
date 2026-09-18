# Zero-Code Configuration

AegisCore adheres to the rule: **one config file change = the entire platform reflects it at runtime. No code edits. No rebuilds.**

## What to Change and How

| Target | Configuration Location | Key |
|---|---|---|
| Platform Name | `platform.config.json` | `platform.name` |
| Subtitle & Branding | `platform.config.json` | `platform.display_name` |
| Module Display Name | `module.config.json` | `display_name` |
| Move Module Category | `module.config.json` | `category` |
| Enable/Disable Module | `platform.config.json` | `status: "enabled"` or `"disabled"` |
| Toggle Authentication | `platform.config.json` | `features.enable_auth` |
| Toggle RBAC | `platform.config.json` | `features.enable_rbac` |
| Audit Logging | `platform.config.json` | `features.enable_audit_log` |
| Modify Ports | `module.config.json` | `ports: [...]` |
| Change Permission Level | `module.config.json` | `permission_level` |
