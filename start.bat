@echo off
title AegisCore Platform Launcher
echo =======================================================
echo          Launching AegisCore Platform
echo =======================================================

echo [1/2] Starting FastAPI Backend on port 8000...
start "AegisCore Backend API" cmd /k "cd /d %~dp0 && uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 2 /nobreak >nul

echo [2/2] Starting Next.js SOC Dashboard on port 3000...
start "AegisCore SOC Dashboard" cmd /k "cd /d %~dp0dashboard && npm run dev"

echo.
echo [+] Services started!
echo     - API:       http://localhost:8000/docs
echo     - Dashboard: http://localhost:3000
echo.
start http://localhost:3000
