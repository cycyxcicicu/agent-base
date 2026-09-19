# merge-gate.ps1
# Reject a branch that changes files outside the scope declared in its task card.
#
# Usage:
#   powershell -File scripts/merge-gate.ps1 -Branch feat/T-012 -Card tasks/T-012.md [-Base main]
#
# Exit codes: 0 = PASS, 1 = FAIL (scope violation), 2 = usage or setup error.
#
# The card must have a front matter block with:
#   id: T-012
#   scope_edit:
#     - src/auth/**
#   scope_deny:
#     - package.json
# scope_deny always wins. The card itself (tasks/<id>.md) is always allowed.
# Keep this file ASCII only (Windows PowerShell 5.1 reads BOM-less scripts as ANSI).

param(
  [Parameter(Mandatory = $true)][string]$Branch,
  [Parameter(Mandatory = $true)][string]$Card,
  [string]$Base = 'main'
)

$ErrorActionPreference = 'Continue'
$utf8 = New-Object System.Text.UTF8Encoding($false)

function ConvertTo-GlobRegex([string]$glob) {
  $g = $glob -replace '\\', '/'
  $sb = New-Object System.Text.StringBuilder
  $i = 0
  while ($i -lt $g.Length) {
    $c = $g[$i]
    if ($c -eq '*') {
      if (($i + 1 -lt $g.Length) -and ($g[$i + 1] -eq '*')) {
        if (($i + 2 -lt $g.Length) -and ($g[$i + 2] -eq '/')) { [void]$sb.Append('(.*/)?'); $i += 3 }
        else { [void]$sb.Append('.*'); $i += 2 }
        continue
      }
      [void]$sb.Append('[^/]*')
    } elseif ($c -eq '?') {
      [void]$sb.Append('[^/]')
    } else {
      [void]$sb.Append([regex]::Escape([string]$c))
    }
    $i++
  }
  return '^' + $sb.ToString() + '$'
}

function Test-Match([string]$file, [string[]]$globs) {
  foreach ($g in $globs) {
    if ($file -match (ConvertTo-GlobRegex $g)) { return $true }
  }
  return $false
}

if (-not (Test-Path $Card)) { Write-Host "ERROR: card not found: $Card"; exit 2 }
$text = ([System.IO.File]::ReadAllText((Resolve-Path $Card).Path, $utf8)) -replace "`r`n", "`n"
$m = [regex]::Match($text, '(?s)^---\n(.*?)\n---')
if (-not $m.Success) { Write-Host 'ERROR: card has no front matter'; exit 2 }

$id = $null
$allow = @()
$deny = @()
$cur = $null
foreach ($line in ($m.Groups[1].Value -split "`n")) {
  if ($line -match '^\s+-\s+(.+)$') {
    $v = $matches[1].Trim().Trim('"').Trim("'")
    if ($cur -eq 'scope_edit') { $allow += $v }
    elseif ($cur -eq 'scope_deny') { $deny += $v }
    continue
  }
  if ($line -match '^([a-z_]+):\s*(.*)$') {
    $cur = $matches[1]
    if ($cur -eq 'id') { $id = $matches[2].Trim() }
  }
}
if (-not $id) { Write-Host 'ERROR: card has no id'; exit 2 }
if ($allow.Count -eq 0) { Write-Host 'FAIL: scope_edit is empty in the card. Architect or Orchestrator must declare the scope.'; exit 1 }

$repo = (git rev-parse --show-toplevel)
if ($LASTEXITCODE -ne 0) { Write-Host 'ERROR: not inside a git repository'; exit 2 }
$repo = $repo.Trim()

$raw = git -C $repo -c core.quotepath=false diff --name-only "$Base...$Branch"
if ($LASTEXITCODE -ne 0) { Write-Host "ERROR: git diff failed for $Base...$Branch"; exit 2 }
$files = @($raw | Where-Object { $_ -and $_.Trim() -ne '' })

$cardPath = "tasks/$id.md"
$violations = @()
foreach ($f in $files) {
  $f = $f.Trim()
  if ($f -eq $cardPath) { continue }
  if (Test-Match $f $deny) { $violations += "DENIED       $f"; continue }
  if (-not (Test-Match $f $allow)) { $violations += "OUT OF SCOPE $f" }
}

Write-Host "Task $id, branch $Branch vs $Base: $($files.Count) changed file(s)"
if ($violations.Count -gt 0) {
  foreach ($v in $violations) { Write-Host "  $v" }
  Write-Host 'FAIL: fix the branch, or ask the task owner to widen scope_edit in the card.'
  exit 1
}
Write-Host 'PASS: all changed files are within scope.'
exit 0
