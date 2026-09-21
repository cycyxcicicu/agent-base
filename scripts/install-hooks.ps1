# install-hooks.ps1
# Windows PowerShell wrapper for scripts/install-hooks.py
# Keep this file ASCII only.

$ErrorActionPreference = 'Stop'
$pyScript = Join-Path $PSScriptRoot 'install-hooks.py'
& python $pyScript @args
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
