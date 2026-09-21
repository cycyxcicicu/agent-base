# sync-adapters.ps1
# Windows PowerShell wrapper for scripts/sync-adapters.py
# Keep this file ASCII only.

param([switch]$Check)

$ErrorActionPreference = 'Stop'
$pyScript = Join-Path $PSScriptRoot 'sync-adapters.py'

$argsList = @()
if ($Check) { $argsList += '--check' }

& python $pyScript @argsList
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
