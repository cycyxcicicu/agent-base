# convert-docs.ps1
# Wrapper script for converting source documents (PDF, DOCX, XLSX, PPTX, Images) to Markdown for BA.
#
# Usage:
#   powershell -File scripts/convert-docs.ps1 -All
#   powershell -File scripts/convert-docs.ps1 -File docs/source/spec.docx
#   powershell -File scripts/convert-docs.ps1 -File docs/source/mockup.png -EnableOcr
#   powershell -File scripts/convert-docs.ps1 -All -EnableOcr -Model "gpt-4o"
#
# Keep this file ASCII only (Windows PowerShell 5.1 reads BOM-less scripts as ANSI).

param(
  [string]$File = '',
  [switch]$All,
  [switch]$EnableOcr,
  [string]$Model = 'gpt-4o',
  [string]$BaseUrl = ''
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$pyScript = Join-Path $PSScriptRoot 'convert-docs.py'

$argsList = @()
if ($File -ne '') {
  $argsList += '--file'
  $argsList += $File
} elseif ($All) {
  $argsList += '--all'
} else {
  Write-Host "Please specify -File <path> or -All"
  Write-Host "Examples:"
  Write-Host "  powershell -File scripts/convert-docs.ps1 -All"
  Write-Host "  powershell -File scripts/convert-docs.ps1 -File docs/source/mockup.png -EnableOcr"
  exit 1
}

if ($EnableOcr) {
  $argsList += '--enable-ocr'
}
if ($Model -ne '') {
  $argsList += '--model'
  $argsList += $Model
}
if ($BaseUrl -ne '') {
  $argsList += '--base-url'
  $argsList += $BaseUrl
}

# Delegating dependency check and conversion directly to python
& python $pyScript @argsList
if ($LASTEXITCODE -ne 0) {
  Write-Host "convert-docs failed with exit code $LASTEXITCODE"
  exit $LASTEXITCODE
}
