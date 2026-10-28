# scripts/setup-skills.ps1
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
python "$root\scripts\setup-skills.py" @args
