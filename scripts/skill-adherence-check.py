#!/usr/bin/env python3
"""scripts/skill-adherence-check.py

Cổng Kiểm Tra Tính Thực Chứng Kỹ Năng (Verifiable Skill Adherence Gate).
Hiện thực hóa cơ chế RAE (Retrieval-Invoked Actual-Use Effect) để chống hiện tượng "Chém gió là đã áp dụng Skill".

Tính năng:
- Quét Handoff Note (`docs/notes/inbox/*.md`) hoặc Task Card.
- Phát hiện các kỹ năng mà Agent tuyên bố áp dụng (qua trường `skills: [...]` trong Frontmatter hoặc mục `## Kỹ năng đã áp dụng`).
- Kiểm tra tính thực chứng (Verifiable Proof):
  * Bắt buộc có mục `## Bằng chứng áp dụng kỹ năng` (Skill Proof).
  * Phải trích dẫn cụ thể tên quy tắc từ `SKILL.md` (ví dụ: `FetchType.LAZY`, `DTO validation`, `@BatchSize`).
  * Phải trích dẫn file và dòng code cụ thể đã áp dụng quy tắc đó (ví dụ: `src/main/Order.java#L45`).
- Nếu Agent tuyên bố dùng Skill nhưng không có bằng chứng dòng code cụ thể -> Trả về FAIL (Exit code 1).

Usage:
  python3 scripts/skill-adherence-check.py --note docs/notes/inbox/T-12.1-dev.md
  python3 scripts/skill-adherence-check.py --dir docs/notes/inbox/
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent

PLACEHOLDER_RE = re.compile(r"\b(?:todo|fixme|chưa\s+áp\s+dụng|đang\s+cập\s+nhật|xem\s+sau)\b", re.IGNORECASE)
FILE_LINE_RE = re.compile(r"(?:[\w\.\-\/]+\.(?:java|py|ts|tsx|js|go|rs|sql|xml|json|md))(?:\s*#\s*L?\d+|\s*:\s*\d+)", re.IGNORECASE)


def parse_frontmatter_skills(content: str) -> Tuple[List[str], str]:
    """Trích xuất danh sách skills từ YAML Frontmatter."""
    skills = []
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            raw_fm = parts[1]
            body = parts[2]
            for line in raw_fm.splitlines():
                line = line.strip()
                if line.startswith("skills:") or line.startswith("skill:"):
                    # Hỗ trợ dạng [skill1, skill2] hoặc chuỗi
                    val = line.split(":", 1)[1].strip()
                    val = val.strip("[]")
                    for s in val.split(","):
                        cleaned = s.strip().strip("'").strip('"')
                        if cleaned:
                            skills.append(cleaned)

    # Tìm thêm trong body nếu có mục: "Skill đã chọn & áp dụng: <tên>"
    m_body_skill = re.findall(r"(?:skill\s+(?:đã\s+chọn|áp\s+dụng)|kỹ\s+năng\s+sử\s+dụng)\s*[:=]\s*([a-zA-Z0-9_\-]+)", body, re.IGNORECASE)
    for s in m_body_skill:
        if s not in skills:
            skills.append(s)

    return skills, body


def audit_skill_adherence(note_path: Path) -> Tuple[bool, List[str]]:
    """Kiểm tra xem note có bằng chứng dòng code chứng minh việc áp dụng skill hay không."""
    errors = []
    if not note_path.exists() or not note_path.is_file():
        return False, [f"File không tồn tại: {note_path}"]

    try:
        content = note_path.read_text(encoding="utf-8")
    except Exception as exc:
        return False, [f"Không thể đọc file: {exc}"]

    declared_skills, body = parse_frontmatter_skills(content)
    if not declared_skills:
        # Không tuyên bố dùng skill cụ thể nào -> Bỏ qua kiểm tra
        return True, []

    # Tìm section Bằng chứng áp dụng kỹ năng
    proof_match = re.search(
        r"##\s*(?:bằng\s*chứng\s*áp\s*dụng\s*kỹ\s*năng|skill\s*(?:proof|adherence|evidence))(.*?)(?=##|\Z)",
        body,
        re.DOTALL | re.IGNORECASE,
    )

    if not proof_match:
        errors.append(
            f"Khai báo áp dụng skills {declared_skills} nhưng thiếu mục '## Bằng chứng áp dụng kỹ năng' (Skill Proof)!"
        )
        return False, errors

    proof_text = proof_match.group(1).strip()
    if not proof_text or len(proof_text) < 15:
        errors.append("Mục Bằng chứng áp dụng kỹ năng bị để trống hoặc quá sơ sài.")
        return False, errors

    if PLACEHOLDER_RE.search(proof_text):
        errors.append("Bằng chứng áp dụng kỹ năng chứa từ khóa né tránh / placeholder.")

    # Bắt buộc phải có trích dẫn tên file và dòng code cụ thể (e.g. Order.java#L45 hoặc User.py:30)
    has_file_line = bool(FILE_LINE_RE.search(proof_text))
    if not has_file_line:
        errors.append(
            "Bằng chứng kỹ năng thiếu trích dẫn file và dòng code cụ thể đã áp dụng quy tắc (ví dụ: `OrderController.java#L35`)."
        )

    # Kiểm tra xem tên của từng skill có được nhắc tới kèm quy tắc trong proof hay không
    for sk in declared_skills:
        if sk.lower() not in proof_text.lower():
            errors.append(f"Không tìm thấy bằng chứng giải trình cụ thể cho skill '{sk}'.")

    return len(errors) == 0, errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="skill-adherence-check: Cổng kiểm tra tính thực chứng khi Agent áp dụng Kỹ năng (Anti-Skill Hallucination)"
    )
    parser.add_argument("--note", help="Đường dẫn tới file note cần kiểm tra")
    parser.add_argument("--dir", default=None, help="Thư mục chứa các note cần kiểm tra (e.g. docs/notes/inbox/)")

    args = parser.parse_args()

    target_notes = []
    if args.note:
        target_notes.append(Path(args.note))
    elif args.dir:
        d = Path(args.dir)
        if d.is_dir():
            target_notes.extend(d.glob("**/*.md"))
    else:
        default_inbox = Path("docs/notes/inbox")
        if default_inbox.is_dir():
            target_notes.extend(default_inbox.glob("**/*.md"))

    if not target_notes:
        print("[INFO] Không tìm thấy note nào để kiểm tra.")
        return 0

    checked = 0
    failed = 0

    for note in target_notes:
        if note.name.upper() in ("README.MD", "INDEX.MD", ".GITKEEP"):
            continue

        checked += 1
        ok, errs = audit_skill_adherence(note)
        if ok:
            print(f"[PASS] {note}")
        else:
            failed += 1
            print(f"[FAIL] {note}")
            for e in errs:
                print(f"       - {e}")

    print("-" * 60)
    print(f"Tổng kết: Kiểm tra {checked} note(s) | Hợp lệ: {checked - failed} | Lỗi: {failed}")
    return 1 if failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
