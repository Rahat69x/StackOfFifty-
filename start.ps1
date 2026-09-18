# AegisCore Platform Launcher for Windows PowerShell
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "         Launching AegisCore Platform                 " -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptPath

Write-Host "`n[1/2] Starting FastAPI Backend (Port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$scriptPath'; Write-Host 'Starting AegisCore Backend API...' -ForegroundColor Green; uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload"

Start-Sleep -Seconds 2

Write-Host "[2/2] Starting Next.js SOC Dashboard (Port 3000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$scriptPath\dashboard'; Write-Host 'Starting AegisCore Dashboard...' -ForegroundColor Cyan; npm run dev"

Write-Host "`n[+] AegisCore services launched in dedicated terminal windows!" -ForegroundColor Green
Write-Host "    - Backend API & Swagger: http://localhost:8000/docs" -ForegroundColor White
Write-Host "    - SOC Web Dashboard   : http://localhost:3000" -ForegroundColor White
Write-Host "`nOpening SOC Dashboard in browser..." -ForegroundColor Cyan
Start-Process "http://localhost:3000"
