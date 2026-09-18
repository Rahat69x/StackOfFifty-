# StackOfFifty Windows PowerShell Health Check Script
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$rootPath = Split-Path -Parent $scriptPath
Set-Location $rootPath

python scripts\health_check.py
