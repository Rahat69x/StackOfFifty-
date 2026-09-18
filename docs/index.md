# AegisCore Platform Overview

**AegisCore** is an enterprise-grade cybersecurity defense and telemetry operations platform. It unifies 50 independent cybersecurity modules across 12 logical categories into a single control plane.

## Key Principles
1. **Modularity**: Every module extends `BaseModule` and functions independently.
2. **Configurability**: Zero code changes required for reconfiguration; all attributes are bound to `platform.config.json` and module JSON files.
3. **Extensibility**: Hot-reloading enables dynamic updates without server restarts.
4. **Defensive Rigor**: 100% focused on telemetry, log aggregation, anomaly detection, and compliance auditing.

## Architecture Layers
- **Presentation**: Next.js 14 App Router + Tailwind CSS.
- **REST API**: FastAPI + Pydantic v2 schemas + SlowAPI rate limiting.
- **Data & Caching**: PostgreSQL 15 / SQLite fallback + Redis 7 / In-memory fallback.
- **Security**: JWT tokens (15min/7d), bcrypt cost factor 12, RBAC (`admin`, `researcher`, `viewer`).
