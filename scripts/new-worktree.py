#!/usr/bin/env python3
"""
scripts/new-worktree.py
Create a git worktree and correctly named branch for one ticket.
Enforces branch naming: <type>/<ticket>-<slug>.

Usage:
  python scripts/new-worktree.py --ticket 12 --slug token-check [--type feature] [--base develop] [--root /path/to/worktrees]
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

VALID_TYPES = {'feature', 'bugfix', 'hotfix', 'fix', 'chore', 'refactor', 'docs', 'test', 'devops'}


def _detect_workspace_root(repo_path: Path) -> Path:
    home = Path.home().resolve()
    for cand in [repo_path, *list(repo_path.parents[:4])]:
        res = cand.resolve()
        if res == home or res == Path(res.anchor):
            break
        if (res / "platform-services").is_dir() or (res / "doc" / "features").is_dir() or (res / "docs" / "features").is_dir():
            return res
    return repo_path.resolve()


def main():
    parser = argparse.ArgumentParser(description="Create a worktree for a task.")
    parser.add_argument("--ticket", required=True, help="Ticket number (digits only, e.g. 12).")
    parser.add_argument("--slug", required=True, help="Short slug (e.g. token-check).")
    parser.add_argument("--type", default="feature", help="Branch type (default: feature).")
    parser.add_argument("--base", default="develop", help="Base branch (default: develop, or main for hotfix).")
    parser.add_argument("--root", default="", help="Custom worktree root directory (e.g. outside OneDrive).")
    args = parser.parse_args()

    if not re.match(r'^[0-9]+$', args.ticket):
        print(f"ERROR: --ticket must be a number, got '{args.ticket}'")
        sys.exit(2)

    if not re.match(r'^[a-z0-9][a-z0-9-]*$', args.slug):
        print(f"ERROR: --slug must be lowercase letters, digits and dashes, got '{args.slug}'")
        sys.exit(2)

    if args.type not in VALID_TYPES:
        print(f"ERROR: --type must be one of: {', '.join(sorted(VALID_TYPES))}")
        sys.exit(2)

    base = args.base
    if args.type == 'hotfix' and base == 'develop':
        base = 'main'

    try:
        repo_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip()
    except Exception:
        print("ERROR: not inside a git repository")
        sys.exit(2)

    # Check base branch exists
    res = subprocess.run(['git', '-C', repo_root, 'rev-parse', '--verify', '--quiet', f"{base}^{{commit}}"])
    if res.returncode != 0:
        print(f"ERROR: base branch '{base}' does not exist yet. Create it first (see agents/protocols/git-rules.md).")
        sys.exit(2)

    repo_path = Path(repo_root)
    name = repo_path.name
    if args.root:
        wt_root = Path(args.root).resolve()
    elif os.environ.get("WORKTREES_DIR"):
        wt_root = Path(os.environ["WORKTREES_DIR"]).expanduser().resolve()
    else:
        # Tự động nhận diện thư mục worktrees ngoài workspace
        sibling_wt = repo_path.parent / "worktrees"
        if sibling_wt.exists():
            wt_root = sibling_wt.resolve()
        elif (Path.home() / "Documents").exists():
            wt_root = (Path.home() / "Documents" / "worktrees").resolve()
        else:
            wt_root = (Path.home() / "worktrees").resolve()

    if 'onedrive' in str(wt_root).lower():
        print("WARNING: the worktree folder is inside OneDrive. Every worktree is a full checkout and OneDrive syncs it slowly. Prefer --root on another drive or folder.")

    type_word = {"feature": "feat", "bugfix": "fix"}.get(args.type, args.type)
    target_path = wt_root / f"{name}-T-{args.ticket}-{type_word}-{args.slug}"
    branch = f"{args.type}/{args.ticket}-{args.slug}"

    if target_path.exists():
        print(f"ERROR: worktree already exists: {target_path}")
        sys.exit(2)

    wt_root.mkdir(parents=True, exist_ok=True)
    cmd = ['git', '-C', repo_root, 'worktree', 'add', str(target_path), '-b', branch, base]
    res_wt = subprocess.run(cmd)
    if res_wt.returncode != 0:
        print("ERROR: git worktree add failed")
        sys.exit(2)

    # Tự động cấu hình Rules workspace, doc.workspace, info/exclude và cập nhật Worktree Registry
    wm_script = Path(__file__).resolve().parent / "worktree-manager.py"
    if wm_script.is_file():
        ws_root = _detect_workspace_root(repo_path)
        sync_env = {
            **os.environ,
            "WORKSPACE_ROOT": str(ws_root),
            "WORKTREES_DIR": str(wt_root),
        }
        print("\n🚀 Đang tự động đồng bộ Rules, doc.workspace & Sổ bộ Worktree...")
        if (ws_root / "doc" / "governance" / "standards").is_dir():
            subprocess.run([sys.executable, str(wm_script), "sync"], env=sync_env, check=False)
        else:
            subprocess.run(
                [sys.executable, str(wm_script), "inject", "--path", str(target_path), "--service", name, "--task", f"T-{args.ticket}"],
                env=sync_env,
                check=False,
            )

    print(f"\nWorktree: {target_path}")
    print(f"Branch:   {branch} (from {base})\n")
    print("Next: open that folder in the editor and let the agent edit files there.")
    print(f"Agents do not commit. When they finish, read the commit plan in the card tasks/<epic-folder>/T-{args.ticket}-{type_word}-{args.slug}.md and run it yourself.")
    print(f"Before opening a Merge Request: git rebase {base}, then python scripts/merge-gate.py --branch {branch} --card tasks/<epic-folder>/T-{args.ticket}-{type_word}-{args.slug}.md --base {base}")


if __name__ == '__main__':
    main()
