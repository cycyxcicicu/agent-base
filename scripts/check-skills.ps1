# check-skills.ps1
# Windows PowerShell wrapper for scripts/check-skills.py
# Keep this file ASCII only.

param(
  [string]$Path = '',
  [string]$Registry = '',
  [switch]$Strict
)

$ErrorActionPreference = 'Stop'
$pyScript = Join-Path $PSScriptRoot 'check-skills.py'

$argsList = @()
if ($Path -ne '') { $argsList += '--path'; $argsList += $Path }
if ($Registry -ne '') { $argsList += '--registry'; $argsList += $Registry }
if ($Strict) { $argsList += '--strict' }

& python $pyScript @argsList
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
