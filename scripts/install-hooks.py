#!/usr/bin/env python3
"""
scripts/install-hooks.py
Enable shared git hooks in .githooks/ for this repository clone.

Usage:
  python scripts/install-hooks.py
"""

import sys
import subprocess
from pathlib import Path

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


def main():
    root = Path(__file__).resolve().parent.parent
    res = subprocess.run(['git', '-C', str(root), 'config', 'core.hooksPath', '.githooks'])
    if res.returncode != 0:
        print("ERROR: git config failed. Is this a git repository?")
        sys.exit(1)

    hooks_val = subprocess.check_output(['git', '-C', str(root), 'config', '--get', 'core.hooksPath'], text=True).strip()
    print(f"core.hooksPath = {hooks_val}")
    print("Hooks enabled: pre-commit, commit-msg, pre-push.")
    print("They enforce: <type>/<ticket>-<desc> branch names, <type>(scope): <summary> commits,")
    print("no direct commit or push on main/develop/release/*, no secrets, no agent commits.")
    print("Rules: agents/protocols/git-rules.md")


if __name__ == '__main__':
    main()
