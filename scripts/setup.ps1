# StackOfFifty Windows PowerShell Setup Script
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "      StackOfFifty Platform Setup (PowerShell)           " -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$rootPath = Split-Path -Parent $scriptPath

Set-Location $rootPath

Write-Host "`n[*] Executing Python setup sequence..." -ForegroundColor Yellow
python scripts\setup.py $args

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[+] Setup completed successfully!" -ForegroundColor Green
} else {
    Write-Host "`n[-] Setup encountered an error." -ForegroundColor Red
}
