# show-permissions.ps1
# Windows PowerShell wrapper for scripts/show-permissions.py
# Keep this file ASCII only.

$ErrorActionPreference = 'Stop'
$pyScript = Join-Path $PSScriptRoot 'show-permissions.py'
& python $pyScript @args
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
