# StackOfFifty Native C++ Platform Launcher
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "      Launching StackOfFifty (Native C++20 Engine)        " -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptPath

if (-not (Test-Path "$scriptPath\stackoffifty_server.exe")) {
    Write-Host "`n[*] Binary not found. Compiling stackoffifty_server.exe..." -ForegroundColor Yellow
    g++ -std=c++20 -O2 main.cpp -lws2_32 -liphlpapi -lpsapi -o stackoffifty_server.exe
}

Write-Host "`n[1/2] Starting Native C++ REST API Server (Port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$scriptPath'; Write-Host 'StackOfFifty C++20 Server Active' -ForegroundColor Green; .\stackoffifty_server.exe"

Start-Sleep -Seconds 2

Write-Host "[2/2] Starting Next.js SOC Dashboard (Port 3000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$scriptPath\dashboard'; Write-Host 'StackOfFifty SOC Dashboard Active' -ForegroundColor Cyan; npm run dev"

Write-Host "`n[+] StackOfFifty Native C++ Platform is LIVE!" -ForegroundColor Green
Write-Host "    - C++ Server & API Docs: http://localhost:8000/api/health" -ForegroundColor White
Write-Host "    - All 50 C++ Modules   : http://localhost:8000/api/modules" -ForegroundColor White
Write-Host "    - SOC Web Dashboard    : http://localhost:3000" -ForegroundColor White

Start-Sleep -Seconds 1
Start-Process "http://localhost:3000"
