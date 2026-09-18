# AegisCore Windows PowerShell Add Module Script
param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$DisplayName,

    [Parameter(Mandatory=$false, Position=1)]
    [string]$Category = "Network Security",

    [Parameter(Mandatory=$false, Position=2)]
    [string]$PermissionLevel = "researcher"
)

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$rootPath = Split-Path -Parent $scriptPath
Set-Location $rootPath

python scripts\add_module.py "$DisplayName" "$Category" "$PermissionLevel"
