#!/bin/sh
# Shared helpers for the hooks in this folder. Sourced, not run directly.

PROTECTED_BRANCHES="main master integration"

# An "agent" is any git identity whose user.name ends with "(agent)".
# scripts/new-worktree.ps1 sets that identity per worktree.
is_agent() {
  name=$(git config user.name 2>/dev/null)
  case "$name" in
    *"(agent)") return 0 ;;
    *) return 1 ;;
  esac
}

is_protected() {
  for b in $PROTECTED_BRANCHES; do
    [ "$1" = "$b" ] && return 0
  done
  return 1
}

fail() {
  echo "git-rules: $*" >&2
  exit 1
}
