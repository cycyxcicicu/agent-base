# agent-base-diff.ps1
# Windows PowerShell wrapper for scripts/agent-base-diff.py
# Keep this file ASCII only.

$ErrorActionPreference = 'Stop'
$pyScript = Join-Path $PSScriptRoot 'agent-base-diff.py'
& python $pyScript @args
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
