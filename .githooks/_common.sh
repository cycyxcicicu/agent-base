#!/bin/sh
# Shared helpers for the hooks in this folder. Sourced, not run directly.
# Rules: agents/protocols/git-rules.md (GitFlow + Conventional Commits, from the user's lecture).

# An "agent" is any git identity whose user.name ends with "(agent)".
# Such an identity may not commit. When the user asks an AI to commit, the tool asks the user to approve each command and the
# commit uses the user's own identity plus a Co-Authored-By trailer, so it is not blocked here.
is_agent() {
  name=$(git config user.name 2>/dev/null)
  case "$name" in
    *"(agent)") return 0 ;;
    *) return 1 ;;
  esac
}

# Shared long-lived branches: nobody commits or pushes to them directly, only through a Merge Request.
is_protected() {
  case "$1" in
    main|master|develop|release/*) return 0 ;;
    *) return 1 ;;
  esac
}

# <type>/<ticket>-<short-description>, or release/<version>.
valid_branch_name() {
  case "$1" in
    release/[0-9]*.[0-9]*.[0-9]*) return 0 ;;
  esac
  printf '%s' "$1" | grep -Eq '^(feature|bugfix|hotfix|fix|chore|refactor|docs|test|devops)/[0-9]+-[a-z0-9][a-z0-9-]*$'
}

fail() {
  echo "git-rules: $*" >&2
  exit 1
}
