# Renaming & Customization

AegisCore requires zero code changes to rebrand or rename platform components.

## Renaming the Platform
Open `platform.config.json` and modify:
```json
{
  "platform": {
    "name": "YourPlatformName",
    "display_name": "YourPlatformName — Cybersecurity Operations Platform"
  }
}
```
The dashboard, API documentation, and logging components will immediately adopt the new brand identity.

## Renaming a Module
Open the target module's `module.config.json` and change:
```json
{
  "display_name": "New Module Title"
}
```
The change is instantly reflected in the dashboard catalog and API status reports without altering file structures or import paths.
