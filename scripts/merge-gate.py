#!/usr/bin/env python3
"""
scripts/merge-gate.py
Reject a branch that changes files outside the scope declared in its task card.

Hardened against bypasses:
- C1: Reads task card from the base branch (git show <base>:<card>) to prevent
      agents from widening scope_edit on their own feature branch.
- C2: Uses --no-renames in git diff to detect moves/renames of protected files.
- C3: Validates risk tickets (docs/risk/RK-*.md) ensuring Status: APPROVED,
      human approval statement, and prohibiting agent-authored risk approvals.

Usage:
  python scripts/merge-gate.py --branch feature/12-token-check --card tasks/T-12.md [--base develop]
"""

import sys
import re
import argparse
import subprocess
from pathlib import Path

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


def glob_to_regex(glob_str: str) -> str:
    g = glob_str.replace('\\', '/')
    sb = []
    i = 0
    n = len(g)
    while i < n:
        c = g[i]
        if c == '*':
            if i + 1 < n and g[i + 1] == '*':
                if i + 2 < n and g[i + 2] == '/':
                    sb.append('(?:.*/)?')
                    i += 3
                    continue
                else:
                    sb.append('.*')
                    i += 2
                    continue
            sb.append('[^/]*')
        elif c == '?':
            sb.append('[^/]')
        else:
            sb.append(re.escape(c))
        i += 1
    return '^' + ''.join(sb) + '$'


def test_match(filename: str, globs: list) -> bool:
    fn = filename.replace('\\', '/')
    for g in globs:
        pat = glob_to_regex(g)
        if re.match(pat, fn):
            return True
    return False


def parse_card_frontmatter(text: str):
    m = re.match(r'(?s)^---\n(.*?)\n---', text)
    if not m:
        return None, [], []

    task_id = None
    allow = []
    deny = []
    cur = None

    for line in m.group(1).splitlines():
        m_item = re.match(r'^\s+-\s+(.+)$', line)
        if m_item:
            v = m_item.group(1).strip().strip('"').strip("'")
            if cur == 'scope_edit':
                allow.append(v)
            elif cur == 'scope_deny':
                deny.append(v)
            continue
        m_key = re.match(r'^([a-z_]+):\s*(.*)$', line)
        if m_key:
            cur = m_key.group(1)
            if cur == 'id':
                task_id = m_key.group(2).strip()

    return task_id, allow, deny


def main():
    parser = argparse.ArgumentParser(description="Check branch file changes against task card scope.")
    parser.add_argument("--branch", required=True, help="Feature branch name.")
    parser.add_argument("--card", required=True, help="Task card path (e.g. tasks/T-12.md).")
    parser.add_argument("--base", default="develop", help="Base integration branch (default: develop).")
    args = parser.parse_args()

    try:
        repo = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip()
    except Exception:
        print("ERROR: not inside a git repository")
        sys.exit(2)

    card_path = Path(args.card)
    card_rel = card_path.as_posix().lstrip('./')

    # -------------------------------------------------------------------------
    # C1 Fix: Read task card from base branch to prevent tamper in feature branch
    # -------------------------------------------------------------------------
    base_card_text = None
    try:
        base_card_text = subprocess.check_output(
            ['git', '-C', repo, 'show', f"{args.base}:{card_rel}"],
            text=True, encoding='utf-8', stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        base_card_text = None

    worktree_card_text = None
    if card_path.exists():
        worktree_card_text = card_path.read_text(encoding='utf-8', errors='replace').replace('\r\n', '\n')
    else:
        try:
            worktree_card_text = subprocess.check_output(
                ['git', '-C', repo, 'show', f"{args.branch}:{card_rel}"],
                text=True, encoding='utf-8', stderr=subprocess.DEVNULL
            )
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # C1 / N1 Fix: Enforce that task cards MUST exist on base branch
    # -------------------------------------------------------------------------
    if not base_card_text:
        print(f"FAIL: Task card '{card_rel}' does not exist on base branch '{args.base}'!")
        print(f"  Task cards define authorization boundaries (scope_edit) and MUST be committed/merged to '{args.base}' first.")
        print(f"  Agents on feature branches may NOT invent new task cards to authorize their own changes.")
        sys.exit(1)

    task_id, allow, deny = parse_card_frontmatter(base_card_text)
    # Check if the branch attempted to tamper with scope_edit or scope_deny
    if worktree_card_text:
        wt_id, wt_allow, wt_deny = parse_card_frontmatter(worktree_card_text)
        if sorted(wt_allow) != sorted(allow) or sorted(wt_deny) != sorted(deny):
            print(f"FAIL: Task card {card_rel} scope was tampered with on branch {args.branch}!")
            print(f"  Base {args.base} scope_edit: {allow}")
            print(f"  Branch modified scope_edit: {wt_allow}")
            print("  Agents may NOT widen their own scope. Scope changes must originate from base branch.")
            sys.exit(1)

    if not task_id:
        print("ERROR: card has no id")
        sys.exit(2)

    if not allow:
        print("FAIL: scope_edit is empty in the card. Architect or Orchestrator must declare the scope.")
        sys.exit(1)

    diff_range = f"{args.base}...{args.branch}"

    # -------------------------------------------------------------------------
    # C2 Fix: Use --no-renames to ensure git mv cannot hide source files
    # -------------------------------------------------------------------------
    try:
        raw_diff = subprocess.check_output(
            ['git', '-C', repo, '-c', 'core.quotepath=false', 'diff', '--name-only', '--no-renames', diff_range],
            text=True
        )
    except Exception:
        print(f"ERROR: git diff failed for {diff_range}")
        sys.exit(2)

    files = [f.strip().replace('\\', '/') for f in raw_diff.splitlines() if f.strip()]
    expected_card = f"tasks/{task_id}.md"
    violations = []

    for f in files:
        if f == expected_card:
            continue
        if re.match(rf"^docs/notes/inbox/{re.escape(task_id)}-.*\.md$", f):
            continue

        # ---------------------------------------------------------------------
        # C3 Fix: Risk tickets must be approved with verified human signer
        # ---------------------------------------------------------------------
        if re.match(r"^docs/risk/RK-.*\.md$", f):
            base_risk_text = ""
            try:
                base_risk_text = subprocess.check_output(
                    ['git', '-C', repo, 'show', f"{args.base}:{f}"],
                    text=True, encoding='utf-8', stderr=subprocess.DEVNULL
                )
            except Exception:
                base_risk_text = ""

            risk_file = Path(repo) / f
            risk_text = ""
            if risk_file.exists():
                risk_text = risk_file.read_text(encoding='utf-8', errors='replace')
            else:
                try:
                    risk_text = subprocess.check_output(
                        ['git', '-C', repo, 'show', f"{args.branch}:{f}"],
                        text=True, encoding='utf-8'
                    )
                except Exception:
                    pass

            if not risk_text:
                violations.append(f"MISSING RISK TICKET {f}")
                continue

            status_match = re.search(r'(?m)^Status:\s*(APPROVED|PENDING|REJECTED|EXPIRED)\b', risk_text)
            status = status_match.group(1) if status_match else "UNKNOWN"
            app_match = re.search(r'(?s)## Chấp thuận\s*\n+(.+?)(?:\n##|\Z)', risk_text)
            approval_body = app_match.group(1).strip() if app_match else ""
            has_human_signer = bool(re.search(r"(?i)(người\s+phê\s+duyệt|người\s+chấp\s+thuận|approved\s+by)\s*:\s*[^\n]+", risk_text))

            # -----------------------------------------------------------------
            # C3 Fix: An APPROVED risk ticket CANNOT be created on feature branch.
            # Approved exemptions must already exist on base branch (develop/main).
            # Feature branches may only introduce PENDING tickets for human review.
            # -----------------------------------------------------------------
            if status == "APPROVED":
                if not base_risk_text:
                    violations.append(
                        f"UNAUTHORIZED RISK APPROVAL {f}: Status is 'APPROVED' but ticket does not exist on base '{args.base}'. "
                        f"Feature branches cannot self-approve risk tickets. Approvals must originate on base branch by human."
                    )
                    continue

                base_status_match = re.search(r'(?m)^Status:\s*(APPROVED|PENDING|REJECTED|EXPIRED)\b', base_risk_text)
                base_status = base_status_match.group(1) if base_status_match else "UNKNOWN"
                if base_status != "APPROVED":
                    violations.append(
                        f"UNAUTHORIZED RISK STATUS ELEVATION {f}: Status was elevated to 'APPROVED' on feature branch. "
                        f"Approvals must be committed to base branch '{args.base}' by human."
                    )
                    continue

                if not approval_body or approval_body.startswith("(") or "để trống" in approval_body.lower():
                    violations.append(f"INVALID RISK TICKET {f}: Status is 'APPROVED' but lacks valid approval statement")
                    continue

                if not has_human_signer:
                    violations.append(f"UNVERIFIED RISK TICKET {f}: Lacks human signer field ('Người phê duyệt: <họ tên / email>').")
                    continue

            elif status == "PENDING":
                # Newly proposed risk tickets in PENDING state are allowed to be tracked on branch
                pass
            else:
                violations.append(f"INVALID RISK TICKET STATUS {f}: Status is '{status}', expected APPROVED or PENDING.")
                continue

            # Risk ticket file itself is validly processed
            continue

        if test_match(f, deny):
            violations.append(f"DENIED       {f}")
            continue
        if not test_match(f, allow):
            violations.append(f"OUT OF SCOPE {f}")

    print(f"Task {task_id}, branch {args.branch} vs {args.base}: {len(files)} changed file(s)")
    if violations:
        for v in violations:
            print(f"  {v}")
        print("FAIL: fix the branch, or ask the task owner to widen scope_edit in the base card.")
        sys.exit(1)

    print("PASS: all changed files are within scope.")
    sys.exit(0)


if __name__ == '__main__':
    main()
