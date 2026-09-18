# StackOfFifty C++20 Build Script (Windows PowerShell)
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "       Compiling StackOfFifty Native C++20 Server         " -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptPath

Write-Host "`n[*] Invoking MinGW-w64 C++20 Compiler (g++)..." -ForegroundColor Yellow
g++ -std=c++20 -O2 main.cpp -lws2_32 -liphlpapi -lpsapi -o stackoffifty_server.exe

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[+] Compilation SUCCESSFUL!" -ForegroundColor Green
    Write-Host "    Binary: $scriptPath\stackoffifty_server.exe" -ForegroundColor White
    $binSize = (Get-Item "stackoffifty_server.exe").Length / 1MB
    Write-Host "    Size  : $([math]::Round($binSize, 2)) MB" -ForegroundColor White
} else {
    Write-Host "`n[-] Compilation failed with code $LASTEXITCODE" -ForegroundColor Red
}
