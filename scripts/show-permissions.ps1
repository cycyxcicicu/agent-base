# show-permissions.ps1
# Print the permission matrix of every role, read straight from agents/roles/*.md.
#
# Usage: powershell -File scripts/show-permissions.ps1
# Keep this file ASCII only (Windows PowerShell 5.1 reads BOM-less scripts as ANSI).

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$utf8 = New-Object System.Text.UTF8Encoding($false)

$rows = foreach ($f in (Get-ChildItem (Join-Path $root 'agents/roles') -Filter *.md | Sort-Object Name)) {
  $t = ([System.IO.File]::ReadAllText($f.FullName, $utf8)) -replace "`r`n", "`n"
  $m = [regex]::Match($t, '(?s)^---\n(.*?)\n---')
  if (-not $m.Success) { throw "$($f.Name): missing front matter" }
  $cur = $null
  $meta = @{}
  foreach ($line in ($m.Groups[1].Value -split "`n")) {
    if ($line -match '^\s+-\s+(.+)$') { if ($cur) { $meta[$cur] += @($matches[1].Trim().Trim('"')) }; continue }
    if ($line -match '^([a-z_]+):\s*(.*)$') {
      $cur = $matches[1]
      if ($matches[2].Trim() -ne '') { $meta[$cur] = $matches[2].Trim() } else { $meta[$cur] = @() }
    }
  }
  $allow = @($meta['edit_allow'] | Where-Object { $_ -ne 'docs/notes/inbox/**' })
  $web = 'deny'
  if ($meta.ContainsKey('web')) { $web = $meta['web'] }
  $ask = @($meta['bash_ask'])
  [pscustomobject]@{
    Role      = $meta['name']
    Mode      = $meta['mode']
    Bash      = $meta['bash']
    Web       = $web
    EditAllow = ($allow -join ', ')
    EditDeny  = (@($meta['edit_deny']) -join ', ')
    ExtraAsk  = ($ask -join ', ')
  }
}

$rows | Format-Table -AutoSize -Wrap | Out-String -Width 250
Write-Host 'Every role may also write its own handoff note in docs/notes/inbox/.'
Write-Host 'bash: none = no shell | readonly = git status/diff/log/show only | full = any command, except ask/deny lists in scripts/sync-adapters.ps1'
Write-Host 'web:  allow | ask | deny for webfetch, websearch and codesearch (default deny)'
exit 0
