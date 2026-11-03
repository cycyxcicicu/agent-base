#!/bin/sh
# install-hooks.sh
# Enable shared git hooks in .githooks/ for Linux / macOS / WSL.
#
# Usage: ./scripts/install-hooks.sh

set -e

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "$ROOT_DIR" ]; then
  echo "ERROR: Not a git repository." >&2
  exit 1
fi

git -C "$ROOT_DIR" config core.hooksPath .githooks
chmod +x "$ROOT_DIR"/.githooks/* 2>/dev/null || true

echo "core.hooksPath = $(git -C "$ROOT_DIR" config --get core.hooksPath)"
echo "Hooks enabled: pre-commit, commit-msg, pre-push."
echo "Rules: agents/protocols/git-rules.md"
exit 0
