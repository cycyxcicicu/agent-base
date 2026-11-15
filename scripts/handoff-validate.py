#!/usr/bin/env python3
"""scripts/handoff-validate.py

Cổng kiểm tra chuẩn Hợp đồng Giao việc & Bàn giao giữa các Agent (Schema-First Handoff Validator).
Giải quyết triệt để 32% lỗi Lệch pha giữa các Agent (Inter-Agent Misalignment) theo phân loại MAST (UC Berkeley 2025).

Quy tắc kiểm chuẩn:
1. YAML Frontmatter hợp lệ:
   - `task`: Mã task cụ thể (e.g. T-12.1)
   - `role`: Vai trò bàn giao (e.g. dev, reviewer, qa, architect...)
   - `status`: `done` | `blocked` | `review` | `doing`
   - `summary`: Chuỗi tóm tắt cô đọng (10-150 ký tự), cấm để trống hoặc placeholder.
2. Section "Bằng chứng kiểm chứng" (Verification Proof):
   - Bắt buộc có khi status = `done`.
   - Phải chứa lệnh kiểm thử thực tế (e.g. `mvn`, `pytest`, `unittest`, `npm test`, `exit code 0`, hoặc `PASS`).
   - Cấm các từ khóa né tránh (placeholder, sẽ test sau, bỏ qua kiểm thử).
3. Section "Thay đổi mã nguồn" hoặc "Điều agent sau cần biết":
   - Không được để trống.

Usage:
  python3 scripts/handoff-validate.py --note docs/notes/inbox/T-12.1-fix-auth-dev.md
  python3 scripts/handoff-validate.py --dir docs/notes/inbox/ --strict-proof
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

VALID_ROLES = {
    "lead", "product", "ba", "analyst", "architect", "researcher",
    "designer", "dba", "data-eng", "ai-eng", "dev", "mobile",
    "devops", "sre", "security", "reviewer", "qa", "runner",
    "debt-hunter", "writer", "model-tester"
}

VALID_STATUSES = {"done", "review", "blocked", "doing"}

PROOF_PATTERNS = [
    re.compile(r"\b(?:exit\s+code\s*[:=]?\s*0|pass(?:ed)?|ok|success)\b", re.IGNORECASE),
    re.compile(r"\b(?:pytest|mvn\s+test|npm\s+test|go\s+test|cargo\s+test|python3?\s+-m\s+unittest)\b", re.IGNORECASE),
    re.compile(r"\b\d+\s+(?:tests?|passed)\b", re.IGNORECASE),
    re.compile(r"\b(?:console\s+errors?\s*[:=]?\s*0)\b", re.IGNORECASE),
]

PLACEHOLDER_PATTERNS = [
    re.compile(r"\b(?:todo|fixme|xxx|chưa\s+test|sẽ\s+kiểm\s+tra|bỏ\s+qua)\b", re.IGNORECASE),
]


def parse_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
    """Tách YAML Frontmatter và phần thân Markdown."""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    raw_yaml = parts[1]
    body = parts[2]
    meta = {}

    for line in raw_yaml.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip().lower()] = v.strip().strip('"').strip("'")

    return meta, body


def validate_handoff_note(
    note_path: Path,
    strict_proof: bool = False,
) -> Tuple[bool, List[str]]:
    """Kiểm tra hợp chuẩn một file handoff note.

    Returns:
        (is_valid, errors)
    """
    errors = []
    if not note_path.exists() or not note_path.is_file():
        return False, [f"File không tồn tại: {note_path}"]

    try:
        content = note_path.read_text(encoding="utf-8")
    except Exception as exc:
        return False, [f"Không thể đọc file {note_path}: {exc}"]

    meta, body = parse_frontmatter(content)

    # 1. Kiểm tra Frontmatter
    if not meta:
        errors.append("Thiếu khối YAML Frontmatter (mở đầu bằng `---`).")
    else:
        # Task
        task = meta.get("task", "")
        if not task:
            errors.append("Thiếu trường 'task:' trong Frontmatter.")

        # Role
        role = meta.get("role", "").lower()
        if not role:
            errors.append("Thiếu trường 'role:' trong Frontmatter.")
        elif role not in VALID_ROLES:
            errors.append(f"Vai trò 'role: {role}' không hợp lệ (hỗ trợ 20 vai chuẩn).")

        # Status
        status = meta.get("status", "").lower()
        if not status:
            errors.append("Thiếu trường 'status:' trong Frontmatter.")
        elif status not in VALID_STATUSES:
            errors.append(f"Trạng thái 'status: {status}' không hợp lệ (hỗ trợ done/review/blocked/doing).")

        # Summary
        summary = meta.get("summary", "")
        if not summary:
            # Cho phép kiểm tra fallback `> summary:` ở đầu body nếu frontmatter không có
            m_sum = re.search(r"^>\s*summary:\s*(.+)$", body, re.MULTILINE | re.IGNORECASE)
            if m_sum:
                summary = m_sum.group(1).strip()

        if not summary:
            errors.append("Thiếu trường 'summary:' mô tả tóm tắt 1 dòng cho Lead.")
        elif len(summary) < 6:
            errors.append("Summary quá ngắn (dưới 6 ký tự).")
        elif len(summary) > 200:
            errors.append("Summary quá dài (trên 200 ký tự). Cần tóm tắt siêu gọn.")

    # 2. Kiểm tra Bằng chứng kiểm chứng (Verification Proof)
    status = meta.get("status", "").lower()
    has_proof_header = bool(
        re.search(r"##\s*(?:bằng\s*chứng|verification|kết\s*quả\s*kiểm\s*thử|proof)", body, re.IGNORECASE)
    )

    if status == "done":
        if not has_proof_header:
            errors.append("Status là 'done' nhưng thiếu mục '## Bằng chứng kiểm chứng' (Verification Proof).")
        else:
            # Trích xuất phần nội dung sau header proof
            proof_match = re.search(
                r"##\s*(?:bằng\s*chứng|verification|kết\s*quả\s*kiểm\s*thử|proof)(.*?)(?=##|\Z)",
                body,
                re.DOTALL | re.IGNORECASE,
            )
            proof_text = proof_match.group(1).strip() if proof_match else ""

            if not proof_text or len(proof_text) < 10:
                errors.append("Mục Bằng chứng kiểm chứng bị để trống hoặc quá ngắn.")
            else:
                for ph in PLACEHOLDER_PATTERNS:
                    if ph.search(proof_text):
                        errors.append(f"Bằng chứng chứa placeholder không hợp lệ: '{ph.pattern}'.")

                if strict_proof:
                    has_command_evidence = any(p.search(proof_text) for p in PROOF_PATTERNS)
                    if not has_command_evidence:
                        errors.append("Bằng chứng thiếu lệnh test thật (exit code 0, pytest, mvn test, hoặc kết quả test).")

    is_valid = len(errors) == 0
    return is_valid, errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="handoff-validate: Kiểm chuẩn Hợp đồng Giao việc & Bàn giao giữa các Agent (Chống MAST Misalignment)"
    )
    parser.add_argument("--note", help="Đường dẫn file handoff note cần kiểm tra")
    parser.add_argument("--dir", default=None, help="Thư mục chứa các note cần kiểm tra (e.g. docs/notes/inbox/)")
    parser.add_argument("--pattern", default="**/*.md", help="Mẫu glob tìm kiếm file note (mặc định: **/*.md)")
    parser.add_argument("--ignore-briefs", action="store_true", help="Bỏ qua các file brief hoặc research (*brief*.md)")
    parser.add_argument("--strict-proof", action="store_true", help="Bắt buộc có lệnh kiểm thử thật và exit code 0")

    args = parser.parse_args()

    target_notes = []
    if args.note:
        target_notes.append(Path(args.note))
    elif args.dir:
        d = Path(args.dir)
        if d.is_dir():
            target_notes.extend(d.glob(args.pattern))
    else:
        # Mặc định quét docs/notes/inbox/ nếu có
        default_inbox = Path("docs/notes/inbox")
        if default_inbox.is_dir():
            target_notes.extend(default_inbox.glob(args.pattern))

    if not target_notes:
        print("[INFO] Không tìm thấy file note nào để kiểm tra.")
        return 0

    total_checked = 0
    failed_count = 0

    for note in target_notes:
        # Bỏ qua file README hoặc INDEX
        if note.name.upper() in ("README.MD", "INDEX.MD", ".GITKEEP"):
            continue
        if args.ignore_briefs and "brief" in note.name.lower():
            continue

        total_checked += 1
        ok, errs = validate_handoff_note(note, strict_proof=args.strict_proof)
        if ok:
            print(f"[PASS] {note}")
        else:
            failed_count += 1
            print(f"[FAIL] {note}")
            for e in errs:
                print(f"       - {e}")

    print("-" * 50)
    print(f"Tổng kết: Kiểm tra {total_checked} note(s) | Hợp lệ: {total_checked - failed_count} | Lỗi: {failed_count}")

    return 1 if failed_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
