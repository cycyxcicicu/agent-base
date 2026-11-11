#!/usr/bin/env python3
"""
scripts/task-gate.py

Cổng kiểm độ đầy đủ Task Card, Phản biện 3 Phương án, Tính toàn vẹn kiểm thử
(RH-1 / RH-4 / RH-10) và Khóa phạm vi phiên làm việc (Scope Lock - chuyển thể từ gstack /freeze & audit).

Usage:
  python3 scripts/task-gate.py audit --root . --card path/to/card.md [--changed-against develop] [--strict-ac] [--require-challenge]
  python3 scripts/task-gate.py set-scope --root . --mode plan [--card path/to/card.md]
  python3 scripts/task-gate.py set-scope --root . --mode implement --card path/to/card.md
  python3 scripts/task-gate.py clear-scope --root .

Exit codes:
  0: Đạt toàn bộ cổng kiểm
  1: Có lỗi thiếu AC / thiếu phản biện / vi phạm gate integrity
  2: Lỗi tham số hoặc đường dẫn không hợp lệ
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_core.workflow.diff_utils import collect_changed_line_diffs, matches  # noqa: E402
from agent_core.workflow.task_discovery import parse_task_frontmatter  # noqa: E402

SCOPE_FILENAME = ".agentbase-scope.json"
TEST_FILE_GLOBS = (
    "**/test/**",
    "**/tests/**",
    "**/*Test.java",
    "**/*Tests.java",
    "**/*.test.ts",
    "**/*.test.tsx",
    "**/*.spec.ts",
    "**/*.spec.tsx",
    "**/test_*.py",
)
SPEC_OR_CARD_GLOBS = ("doc/**/*.md", "docs/**/*.md", "tasks/**/*.md")

RH1_SKIP_ADD_RE = re.compile(
    r"(?:@Disabled\b|@Ignore\b|@pytest\.mark\.skip\b|\b(?:it|describe|test)\.(?:skip|only)\(|\bxit\(|\bxdescribe\(|@Skip\b|#\[ignore\])"
)
RH1_TEST_REMOVED_RE = re.compile(r"^\s*(?:@Test\b|def\s+test_\w+|(?:it|test)\s*\(|func\s+Test\w+)")
RH4_PLACEHOLDER_RE = re.compile(
    r"(?:\bTODO\b|\bFIXME\b|\bXXX\b|throw\s+new\s+UnsupportedOperationException|raise\s+NotImplementedError|\btodo!\(\)|\bunimplemented!\(\))"
)
RH10_AC_REMOVED_RE = re.compile(r"(?:\bAC-\d+\b|^\s*-\s+\[[ xX]\])")
CHALLENGE_EVIDENCE_RE = re.compile(
    r"(?:phương\s*án\s*(?:A|B|C|1|2|3)|3\s+phương\s*án|plan\s+approved|chấp\s+thuận\s+phương\s*án|khuyến\s*nghị|chốt\s+phương\s*án|cách\s+khắc\s+phục\s+rủi\s*ro)",
    re.IGNORECASE,
)


def parse_card_checklist(card_text: str) -> tuple[list[str], list[str]]:
    """Tách danh sách mục đã tick (`[x]`) và mục chưa xong (`[ ]`) trong Task Card."""
    done_items: list[str] = []
    pending_items: list[str] = []
    for line in card_text.splitlines():
        m = re.match(r"^\s*[-*]\s+\[([ xX])\]\s+(.+?)\s*$", line)
        if not m:
            continue
        mark, item = m.group(1), m.group(2).strip()
        if mark.lower() == "x":
            done_items.append(item)
        else:
            pending_items.append(item)
    return done_items, pending_items


def _has_ignore(line: str, rh_code: str) -> bool:
    return bool(re.search(rf"gate-ignore:\s*{re.escape(rh_code)}\s+\S{{3,}}", line))


def scan_gate_integrity(
    root: Path,
    changed_against: str | None = None,
) -> list[dict[str, str | int]]:
    """Quét diff hiện tại tìm các dấu hiệu gian lận / làm dở (RH-1, RH-4, RH-10)."""
    added_map, removed_map = collect_changed_line_diffs(root, changed_against=changed_against)
    findings: list[dict[str, str | int]] = []

    for rel, rows in added_map.items():
        is_test_file = matches(rel, TEST_FILE_GLOBS)
        is_doc_file = matches(rel, SPEC_OR_CARD_GLOBS)
        for line_no, text in rows:
            if is_test_file and RH1_SKIP_ADD_RE.search(text) and not _has_ignore(text, "RH-1"):
                findings.append({
                    "code": "RH-1",
                    "severity": "error",
                    "file": rel,
                    "line": line_no,
                    "message": "Thêm đánh dấu skip/disable test thay vì sửa cho xanh",
                })
            if (not is_test_file and not is_doc_file) and RH4_PLACEHOLDER_RE.search(text) and not _has_ignore(text, "RH-4"):
                findings.append({
                    "code": "RH-4",
                    "severity": "error",
                    "file": rel,
                    "line": line_no,
                    "message": "Để sót placeholder TODO/FIXME/NotImplemented trong mã nguồn sản phẩm",
                })

    for rel, rrows in removed_map.items():
        is_test_file = matches(rel, TEST_FILE_GLOBS)
        is_doc_file = matches(rel, SPEC_OR_CARD_GLOBS)
        if is_test_file:
            added_texts = {t.strip() for _, t in added_map.get(rel, [])}
            for line_no, text in rrows:
                if RH1_TEST_REMOVED_RE.search(text) and text.strip() not in added_texts:
                    findings.append({
                        "code": "RH-1",
                        "severity": "warn",
                        "file": rel,
                        "line": line_no,
                        "message": f"Xóa test case ({text.strip()[:60]}) — kiểm tra lại để tránh che lỗi",
                    })
        if is_doc_file:
            added_ac_tokens = set()
            for _, t in added_map.get(rel, []):
                added_ac_tokens.update(re.findall(r"\bAC-\d+\b", t))
            for line_no, text in rrows:
                if RH10_AC_REMOVED_RE.search(text):
                    # Bỏ qua chuyển trạng thái hợp lệ `- [ ] AC-1` -> `- [x] AC-1`
                    checked_variant = re.sub(r"^(\s*-\s+)\[ \]", r"\1[x]", text.strip())
                    added_strips = {t.strip() for _, t in added_map.get(rel, [])}
                    if checked_variant in added_strips:
                        continue
                    removed_acs = set(re.findall(r"\bAC-\d+\b", text))
                    if removed_acs and removed_acs.issubset(added_ac_tokens):
                        continue
                    findings.append({
                        "code": "RH-10",
                        "severity": "error",
                        "file": rel,
                        "line": line_no,
                        "message": f"Xóa tiêu chí/AC gốc khỏi tài liệu ({text.strip()[:70]}) — dấu hiệu tự sửa A/C theo code dở",
                    })

    return findings


def _check_challenge_presence(root: Path, card_path: Path | None, card_text: str) -> bool:
    if card_text and CHALLENGE_EVIDENCE_RE.search(card_text):
        return True
    if not card_path:
        return False
    card_id = card_path.stem.split("-")[0] if "-" in card_path.stem else card_path.stem
    for inbox_dir in (root / "doc" / "notes" / "inbox", root / "docs" / "notes" / "inbox"):
        if not inbox_dir.is_dir():
            continue
        for note in inbox_dir.rglob("*.md"):
            if card_id.lower() in note.name.lower():
                try:
                    if CHALLENGE_EVIDENCE_RE.search(note.read_text(encoding="utf-8", errors="ignore")):
                        return True
                except OSError:
                    pass
    return False


def audit_task(
    root: Path,
    card_path: Path | None = None,
    changed_against: str | None = None,
    strict_ac: bool = False,
    require_challenge: bool = False,
) -> tuple[int, list[str]]:
    lines: list[str] = []
    errors = 0

    card_text = ""
    if card_path:
        if not card_path.is_file():
            return 2, [f"LỖI: Không tìm thấy Task Card: {card_path}"]
        card_text = card_path.read_text(encoding="utf-8")
        meta = parse_task_frontmatter(card_text, card_path)
        done_items, pending_items = parse_card_checklist(card_text)
        total = len(done_items) + len(pending_items)
        lines.append(f"Task Card: {meta.get('id') or card_path.stem} | status={meta.get('status')} | checklist={len(done_items)}/{total} hoàn thành")
        if total == 0:
            lines.append("CẢNH BÁO [NO-AC-CHECKLIST]: Task Card chưa có checklist `- [ ] ...` để đo tiến độ từng mục.")
        elif pending_items:
            tag = "LỖI" if strict_ac else "CẢNH BÁO"
            if strict_ac:
                errors += 1
            lines.append(f"{tag} [AC-INCOMPLETE]: Còn {len(pending_items)} mục chưa hoàn thành:")
            for p in pending_items[:10]:
                lines.append(f"  - [ ] {p}")

        if require_challenge and not _check_challenge_presence(root, card_path, card_text):
            errors += 1
            lines.append("LỖI [MISSING-CHALLENGE]: Thiếu dấu vết Phản biện 3 Phương án hoặc `[x] Plan Approved` trong card/note.")

    try:
        integrity_findings = scan_gate_integrity(root, changed_against=changed_against)
    except ValueError as exc:
        return 2, [f"LỖI: {exc}"]

    for f in integrity_findings:
        sev_label = "LỖI" if f["severity"] == "error" else "cảnh báo"
        if f["severity"] == "error":
            errors += 1
        lines.append(f"{f['file']}:{f['line']}: [{f['code']}] {sev_label}: {f['message']}")

    if errors:
        lines.append(f"FAIL: Task Gate phát hiện {errors} lỗi cần xử lý trước khi báo xong.")
        return 1, lines
    lines.append("PASS: Task Gate đạt yêu cầu.")
    return 0, lines


def set_scope_lock(
    root: Path,
    mode: str,
    card_path: Path | None = None,
    allow: list[str] | None = None,
    deny: list[str] | None = None,
) -> Path:
    scope_edit = list(allow or [])
    scope_deny = list(deny or [])
    card_rel = ""
    card_id = ""
    if card_path:
        if not card_path.is_file():
            raise FileNotFoundError(f"Không tìm thấy Task Card: {card_path}")
        meta = parse_task_frontmatter(card_path.read_text(encoding="utf-8"), card_path)
        card_id = str(meta.get("id") or card_path.stem)
        try:
            card_rel = card_path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            card_rel = str(card_path.resolve())
        if not scope_edit:
            scope_edit = [str(x) for x in (meta.get("scope_edit") or []) if str(x).strip()]
        for d in (meta.get("scope_deny") or []):
            if str(d).strip() and str(d).strip() not in scope_deny:
                scope_deny.append(str(d).strip())

    payload = {
        "mode": mode,
        "card_id": card_id,
        "card_path": card_rel,
        "scope_edit": scope_edit,
        "scope_deny": scope_deny,
    }
    scope_file = root / SCOPE_FILENAME
    scope_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return scope_file


def main() -> int:
    ap = argparse.ArgumentParser(description="Task Gate, Gate Integrity (RH-1/4/10) và Scope Lock.")
    sub = ap.add_subparsers(dest="cmd")

    p_audit = sub.add_parser("audit", help="Kiểm độ đầy đủ AC, Phản biện & tính toàn vẹn test/spec")
    p_audit.add_argument("--root", default=".", help="Thư mục gốc dự án hoặc worktree")
    p_audit.add_argument("--card", default="", help="Đường dẫn tới Task Card .md")
    p_audit.add_argument("--changed-against", default=None, metavar="REF", help="So sánh diff với nhánh gốc (vd: develop)")
    p_audit.add_argument("--strict-ac", action="store_true", help="Thất bại (exit 1) nếu còn mục `- [ ]` chưa đánh dấu")
    p_audit.add_argument("--require-challenge", action="store_true", help="Bắt buộc có bằng chứng Phản biện 3 phương án / Plan Approved")

    p_set = sub.add_parser("set-scope", help="Khóa phạm vi Edit/Write theo pha Plan hoặc Implement")
    p_set.add_argument("--root", default=".", help="Thư mục gốc áp dụng scope lock")
    p_set.add_argument("--mode", choices=("plan", "implement"), required=True, help="plan: chặn sửa code; implement: khóa theo scope_edit")
    p_set.add_argument("--card", default="", help="Task Card nguồn để đọc scope_edit/scope_deny")
    p_set.add_argument("--allow", nargs="*", default=None, help="Danh sách glob được phép sửa")
    p_set.add_argument("--deny", nargs="*", default=None, help="Danh sách glob cấm sửa")

    p_clr = sub.add_parser("clear-scope", help="Gỡ bỏ file .agentbase-scope.json")
    p_clr.add_argument("--root", default=".", help="Thư mục gốc")

    # Hỗ trợ gọi không có subcommand: `task-gate.py --card ...` -> tương đương `audit`
    if len(sys.argv) > 1 and sys.argv[1] not in ("audit", "set-scope", "clear-scope", "-h", "--help"):
        sys.argv.insert(1, "audit")
    elif len(sys.argv) == 1:
        sys.argv.append("audit")

    args = ap.parse_args()
    root = Path(args.root).resolve()

    if args.cmd == "set-scope":
        card_p = (Path(args.card) if Path(args.card).is_absolute() else (root / args.card)) if args.card else None
        try:
            out = set_scope_lock(root, args.mode, card_path=card_p, allow=args.allow, deny=args.deny)
        except FileNotFoundError as exc:
            print(f"LỖI: {exc}")
            return 2
        print(f"[OK] Đã bật Scope Lock (mode={args.mode}) tại {out}")
        return 0

    if args.cmd == "clear-scope":
        sf = root / SCOPE_FILENAME
        if sf.exists():
            sf.unlink()
            print(f"[OK] Đã gỡ {sf}")
        else:
            print(f"[INFO] Không có {sf}")
        return 0

    card_p = (Path(args.card) if Path(args.card).is_absolute() else (root / args.card)) if args.card else None
    code, lines = audit_task(
        root=root,
        card_path=card_p,
        changed_against=args.changed_against,
        strict_ac=args.strict_ac,
        require_challenge=args.require_challenge,
    )
    for ln in lines:
        print(ln)
    return code


if __name__ == "__main__":
    sys.exit(main())

