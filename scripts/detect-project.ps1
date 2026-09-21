# detect-project.ps1
# Windows PowerShell wrapper for scripts/detect-project.py
# Keep this file ASCII only.

param(
  [string]$Path = "",
  [switch]$FillProjectMd
)

$ErrorActionPreference = 'Stop'
$pyScript = Join-Path $PSScriptRoot 'detect-project.py'

$argsList = @()
if ($Path -ne "") { $argsList += '--path'; $argsList += $Path }
if ($FillProjectMd) { $argsList += '--fill-project-md' }

& python $pyScript @argsList
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
