# new-worktree.ps1
# Create an isolated worktree and branch for one task, with a per-agent git identity.
#
# Usage:
#   powershell -File scripts/new-worktree.ps1 -Task T-012 [-Agent dev-a] [-Base main]
#
# The worktree is created next to the repo, in <repo-name>-worktrees/<Task>,
# so it stays outside the repository (and outside OneDrive if the repo is outside it).
# Kilo Agent Manager can create worktrees itself; use this script when working outside it.
# Keep this file ASCII only (Windows PowerShell 5.1 reads BOM-less scripts as ANSI).

param(
  [Parameter(Mandatory = $true)][string]$Task,
  [string]$Agent = 'dev',
  [string]$Base = 'main'
)

$ErrorActionPreference = 'Continue'

if ($Task -notmatch '^T-[A-Za-z0-9._-]+$') { Write-Host "ERROR: task id must look like T-012, got '$Task'"; exit 2 }

$root = (git rev-parse --show-toplevel)
if ($LASTEXITCODE -ne 0) { Write-Host 'ERROR: not inside a git repository'; exit 2 }
$root = $root.Trim()

git -C $root rev-parse --verify --quiet "$Base^{commit}" | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Host "ERROR: base branch '$Base' has no commits yet"; exit 2 }

$name = Split-Path $root -Leaf
$parent = Split-Path $root -Parent
$wtRoot = Join-Path $parent ($name + '-worktrees')
$path = Join-Path $wtRoot $Task
$branch = "feat/$Task"

if (Test-Path $path) { Write-Host "ERROR: worktree already exists: $path"; exit 2 }
New-Item -ItemType Directory -Force $wtRoot | Out-Null

git -C $root worktree add $path -b $branch $Base
if ($LASTEXITCODE -ne 0) { Write-Host 'ERROR: git worktree add failed'; exit 2 }

git -C $root config extensions.worktreeConfig true
git -C $path config --worktree user.name "$Agent (agent)"
git -C $path config --worktree user.email "$Agent@agents.local"

Write-Host ''
Write-Host "Worktree: $path"
Write-Host "Branch:   $branch (from $Base)"
Write-Host "Identity: $Agent (agent)"
Write-Host ''
Write-Host 'Next: open that folder in the editor, or point the agent at it.'
Write-Host "Before merging: powershell -File scripts/merge-gate.ps1 -Branch $branch -Card tasks/$Task.md"
exit 0
