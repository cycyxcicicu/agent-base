# new-worktree.ps1
# Windows PowerShell wrapper for scripts/new-worktree.py
# Keep this file ASCII only.

param(
  [Parameter(Mandatory = $true)][string]$Ticket,
  [Parameter(Mandatory = $true)][string]$Slug,
  [string]$Type = 'feature',
  [string]$Base = 'develop',
  [string]$Root = ''
)

$ErrorActionPreference = 'Stop'
$pyScript = Join-Path $PSScriptRoot 'new-worktree.py'

$argsList = @('--ticket', $Ticket, '--slug', $Slug, '--type', $Type, '--base', $Base)
if ($Root -ne '') { $argsList += '--root'; $argsList += $Root }

& python $pyScript @argsList
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
