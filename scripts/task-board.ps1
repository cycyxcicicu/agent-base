# task-board.ps1
# Windows PowerShell wrapper for scripts/task-board.py
# Keep this file ASCII only.

$ErrorActionPreference = 'Stop'
$pyScript = Join-Path $PSScriptRoot 'task-board.py'
& python $pyScript @args
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
