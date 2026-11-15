#!/usr/bin/env python3
"""tests/test_handoff_validate.py

Unit test cho công cụ scripts/handoff-validate.py (Kiểm chuẩn hợp đồng bàn giao giữa các agent).
"""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location("handoff_validate", str(ROOT / "scripts" / "handoff-validate.py"))
handoff_validate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(handoff_validate)


class TestHandoffValidate(unittest.TestCase):
    def test_valid_handoff_note(self):
        content = """---
task: T-12.1
role: dev
status: done
summary: Chuẩn hóa hàm normalize_payload, 46/46 test OK
tags: [auth, jwt]
---

# Bàn giao T-12.1

## Bằng chứng kiểm chứng
Đã chạy: `python3 -m unittest tests/test_auth.py`
Kết quả: 46 tests passed in 0.12s. Exit code: 0.

## Thay đổi mã nguồn
- `src/auth.py`: Thêm hàm sanitize token.

## Điều agent sau cần biết
Lưu ý token format mới có prefix Bearer.
"""
        with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            ok, errs = handoff_validate.validate_handoff_note(temp_path, strict_proof=True)
            self.assertTrue(ok)
            self.assertEqual(len(errs), 0)
        finally:
            temp_path.unlink(missing_ok=True)

    def test_invalid_handoff_missing_frontmatter(self):
        content = "# Just a markdown without frontmatter"
        with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            ok, errs = handoff_validate.validate_handoff_note(temp_path)
            self.assertFalse(ok)
            self.assertTrue(any("Frontmatter" in e for e in errs))
        finally:
            temp_path.unlink(missing_ok=True)

    def test_done_status_missing_verification_proof(self):
        content = """---
task: T-12.2
role: dev
status: done
summary: Sửa xong nhưng quên viết proof
---

# Bàn giao T-12.2
Chỉ có chữ mà không có mục Bằng chứng kiểm chứng.
"""
        with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            ok, errs = handoff_validate.validate_handoff_note(temp_path)
            self.assertFalse(ok)
            self.assertTrue(any("Bằng chứng kiểm chứng" in e for e in errs))
        finally:
            temp_path.unlink(missing_ok=True)

    def test_proof_with_placeholder_rejected(self):
        content = """---
task: T-12.3
role: dev
status: done
summary: Bằng chứng chứa TODO
---

# Bàn giao T-12.3

## Bằng chứng kiểm chứng
TODO: sẽ kiểm tra sau khi merge.
"""
        with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            ok, errs = handoff_validate.validate_handoff_note(temp_path)
            self.assertFalse(ok)
            self.assertTrue(any("placeholder" in e for e in errs))
        finally:
            temp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
