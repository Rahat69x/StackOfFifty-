# Deployment Guide

AegisCore supports dual deployment pathways: local standalone execution and Docker container orchestration.

## 1. Local Development (Zero-Config)
```bash
# Setup platform and initialize database
python scripts/setup.py

# Start FastAPI Backend (Port 8000)
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Start Next.js 14 SOC Dashboard (Port 3000)
cd dashboard
npm run dev
```

## 2. Docker Compose Orchestration
```bash
# Production deployment with Postgres, Redis, and Nginx
docker-compose up -d

# Development mode
docker-compose -f docker-compose.dev.yml up -d
```
