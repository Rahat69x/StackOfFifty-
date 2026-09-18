# API Reference

The StackOfFifty REST API adheres to a standardized contract across all modules.

## Module Control
- `POST /api/modules/{id}/start`: Start module execution.
- `POST /api/modules/{id}/stop`: Halt module execution.
- `POST /api/modules/{id}/reload`: Hot-reload module in memory without restart.
- `GET /api/modules/{id}/status`: Query health and execution status.
- `GET /api/modules/{id}/results`: Fetch latest output and telemetry.
- `GET /api/modules/{id}/logs`: Query recent module logs.
- `POST /api/modules/{id}/configure`: Update runtime settings.
- `GET /api/modules/{id}/report`: Generate structured activity report.

## Platform Operations
- `GET /api/health`: Platform status, CPU/RAM telemetry, uptime.
- `GET /api/modules`: List all modules with category and status filters.
- `GET /api/modules/categories`: Retrieve 12 platform security categories.
- `GET /api/logs`: Query centralized system log stream.
- `GET /api/alerts`: Retrieve active security detections.
- `POST /api/alerts/{id}/resolve`: Mark an alert as resolved.
- `GET /api/config`: Read active platform configuration.
- `POST /api/config/update`: Modify configuration at runtime.
