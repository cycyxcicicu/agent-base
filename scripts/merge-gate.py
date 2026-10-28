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

- Cỡ thay đổi (PR nguyên tử): cảnh báo khi số dòng đổi vượt ngưỡng (mặc định 600, không tính lockfile, build, card, ghi chú).
  Đổi ngưỡng bằng --max-lines N, biến môi trường MERGE_GATE_MAX_LINES, hoặc dòng `Giới hạn dòng thay đổi | N` trong PROJECT.md.
  Mặc định chỉ CẢNH BÁO; thêm --strict-size để biến thành FAIL.

Usage:
  python scripts/merge-gate.py --branch feature/12-token-check --card tasks/T-12.md [--base develop] [--max-lines 400] [--strict-size]
"""

import os
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

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MAX_LINES = 600
# Không tính vào cỡ thay đổi: file sinh ra hoặc khóa phụ thuộc, thư mục build, card và ghi chú bàn giao.
SIZE_IGNORE_GLOBS = [
    '**/package-lock.json', '**/pnpm-lock.yaml', '**/yarn.lock', '**/poetry.lock', '**/Pipfile.lock', '**/composer.lock',
    '**/Cargo.lock', '**/go.sum', 'build/**', 'dist/**', '**/*.min.js', '**/*.map', 'tasks/**', 'docs/notes/inbox/**',
]


def read_max_lines(repo: str, cli_value) -> int:
    """Thứ tự ưu tiên: --max-lines, biến môi trường, PROJECT.md, mặc định."""
    if cli_value:
        return cli_value
    env = os.environ.get('MERGE_GATE_MAX_LINES', '').strip()
    if env.isdigit() and int(env) > 0:
        return int(env)
    project = Path(repo) / 'PROJECT.md'
    if project.exists():
        m = re.search(r'Giới hạn dòng thay đổi\s*\|\s*(\d+)', project.read_text(encoding='utf-8', errors='replace'))
        if m and int(m.group(1)) > 0:
            return int(m.group(1))
    return DEFAULT_MAX_LINES


def count_changed_lines(repo: str, diff_range: str):
    """Tổng dòng thêm + xóa của các file tính vào cỡ thay đổi. Trả về (tổng, danh sách file lớn nhất)."""
    try:
        out = subprocess.check_output(
            ['git', '-C', repo, '-c', 'core.quotepath=false', 'diff', '--numstat', '--no-renames', diff_range],
            text=True, encoding='utf-8')
    except Exception:
        return 0, []
    total, per_file = 0, []
    for line in out.splitlines():
        parts = line.split('\t')
        if len(parts) != 3 or not (parts[0].isdigit() and parts[1].isdigit()):
            continue  # file nhị phân ("-\t-\tname")
        name = parts[2].replace('\\', '/')
        if test_match(name, SIZE_IGNORE_GLOBS):
            continue
        n = int(parts[0]) + int(parts[1])
        total += n
        per_file.append((n, name))
    per_file.sort(reverse=True)
    return total, per_file[:3]


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
        line_clean = re.sub(r'#.*$', '', line)
        m_item = re.match(r'^\s+-\s+(.+)$', line_clean)
        if m_item:
            v = m_item.group(1).strip().strip('"').strip("'")
            if not v:
                continue
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


def check_files_in_scope(files: list, allow: list, deny: list) -> list:
    """Return a list of violations for changed files against allow/deny patterns."""
    violations = []
    for f in files:
        if test_match(f, deny):
            violations.append(f"DENIED       {f}")
        elif not test_match(f, allow):
            violations.append(f"OUT OF SCOPE {f}")
    return violations


def main():
    parser = argparse.ArgumentParser(description="Check branch file changes against task card scope.")
    parser.add_argument("--branch", required=True, help="Feature branch name.")
    parser.add_argument("--card", required=True, help="Task card path (e.g. tasks/T-12.md).")
    parser.add_argument("--base", default="develop", help="Base integration branch (default: develop).")
    parser.add_argument("--max-lines", type=int, default=0, help="Ngưỡng số dòng thay đổi (xem đầu file).")
    parser.add_argument("--strict-size", action="store_true", help="Vượt ngưỡng thì FAIL thay vì chỉ cảnh báo.")
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
        print("FAIL: scope_edit is empty in the card. Architect or Lead must declare the scope.")
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
    # Card may live at tasks/T-n.md or in its epic folder tasks/<epic-folder>/T-n.md.
    card_re = re.compile(rf"^tasks/(?:[^/]+/)?{re.escape(task_id)}\.md$")
    violations = []

    for f in files:
        if card_re.match(f) or f == "tasks/BOARD.md":
            continue
        if re.match(rf"^docs/notes/inbox/(?:{re.escape(task_id)}/|{re.escape(task_id)}[\.-]).*\.md$", f):
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

    total_lines, biggest = count_changed_lines(repo, diff_range)
    limit = read_max_lines(repo, args.max_lines)
    if total_lines > limit:
        top = ", ".join(f"{name} ({n})" for n, name in biggest)
        level = "FAIL" if args.strict_size else "WARN"
        print(f"{level}: {total_lines} dòng thay đổi, vượt ngưỡng {limit}. Lớn nhất: {top}.")
        print("  Chia thành PR nguyên tử (50 đến vài trăm dòng, một thay đổi logic): agents/protocols/atomic-changes.md")
        if args.strict_size:
            sys.exit(1)

    print("PASS: all changed files are within scope.")
    # Tự động cập nhật Bảng điều khiển & Sơ đồ lộ trình nếu script tồn tại
    try:
        dash_script = ROOT / 'scripts' / 'generate-dashboard.py'
        # Chỉ cập nhật khi cổng chạy trên chính dự án chứa script này (không đụng bảng điều khiển của repo khác)
        if dash_script.exists() and Path(repo).resolve() == ROOT.resolve():
            subprocess.run([sys.executable, str(dash_script)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass
    sys.exit(0)


if __name__ == '__main__':
    main()
