# bootstrap-project.ps1
# Windows PowerShell wrapper for scripts/bootstrap-project.py
# Keep this file ASCII only.

$ErrorActionPreference = 'Stop'
$pyScript = Join-Path $PSScriptRoot 'bootstrap-project.py'
& python $pyScript @args
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
