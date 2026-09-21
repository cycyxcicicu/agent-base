# merge-gate.ps1
# Windows PowerShell wrapper for scripts/merge-gate.py
# Keep this file ASCII only.

param(
  [Parameter(Mandatory = $true)][string]$Branch,
  [Parameter(Mandatory = $true)][string]$Card,
  [string]$Base = 'develop'
)

$ErrorActionPreference = 'Stop'
$pyScript = Join-Path $PSScriptRoot 'merge-gate.py'

& python $pyScript --branch $Branch --card $Card --base $Base
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
