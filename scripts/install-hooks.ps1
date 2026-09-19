# install-hooks.ps1
# Enable the shared git hooks in .githooks/ for this clone (all worktrees share the setting).
#
# Usage: powershell -File scripts/install-hooks.ps1
# Keep this file ASCII only (Windows PowerShell 5.1 reads BOM-less scripts as ANSI).

$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot

git -C $root config core.hooksPath .githooks
if ($LASTEXITCODE -ne 0) { Write-Host 'ERROR: git config failed. Is this a git repository?'; exit 1 }

Write-Host ('core.hooksPath = ' + (git -C $root config --get core.hooksPath))
Write-Host 'Hooks enabled: pre-commit, commit-msg, pre-push.'
Write-Host 'Rules: agents/protocols/git-rules.md'
Write-Host 'Note: hooks only recognise agents whose git user.name ends with "(agent)" (scripts/new-worktree.ps1 sets that).'
exit 0
