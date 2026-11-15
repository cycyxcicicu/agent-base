#!/usr/bin/env python3
"""tests/test_skill_mechanisms.py

Unit test cho bộ định tuyến kỹ năng (skill-router) và cổng kiểm chứng thực chất (skill-adherence-check).
"""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_spec_router = importlib.util.spec_from_file_location("skill_router", str(ROOT / "scripts" / "skill-router.py"))
skill_router = importlib.util.module_from_spec(_spec_router)
_spec_router.loader.exec_module(skill_router)

_spec_adh = importlib.util.spec_from_file_location("skill_adherence", str(ROOT / "scripts" / "skill-adherence-check.py"))
skill_adherence = importlib.util.module_from_spec(_spec_adh)
_spec_adh.loader.exec_module(skill_adherence)


class TestSkillMechanisms(unittest.TestCase):
    def test_skill_router_ranking(self):
        mock_skills = [
            {
                "name": "jpa-patterns",
                "path": "skills/jpa-patterns",
                "description": "JPA Hibernate entity relationships N+1 optimization",
                "rules_checklist": ["Entity Design", "FetchType.LAZY"],
                "raw_text": "jpa-patterns JPA Hibernate entity relationships N+1 optimization",
            },
            {
                "name": "ui-ux-pro-max",
                "path": "skills/ui-ux-pro-max",
                "description": "Design system tailwind CSS react component",
                "rules_checklist": ["Contrast", "Spacing"],
                "raw_text": "ui-ux-pro-max Design system tailwind CSS react component",
            },
        ]
        results = skill_router.route_skills("cần tối ưu truy vấn N+1 của hibernate trong entity", mock_skills, top_k=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1]["name"], "jpa-patterns")

    def test_skill_adherence_valid_proof(self):
        valid_note = """---
task: T-50
role: dev
skills: [jpa-patterns]
status: done
---

# Bàn giao T-50

## Bằng chứng áp dụng kỹ năng
Đã áp dụng quy tắc FetchType.LAZY và @BatchSize từ jpa-patterns tại file `src/model/Order.java#L45`.
"""
        with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(valid_note)
            p = Path(f.name)

        try:
            ok, errs = skill_adherence.audit_skill_adherence(p)
            self.assertTrue(ok)
            self.assertEqual(len(errs), 0)
        finally:
            p.unlink(missing_ok=True)

    def test_skill_adherence_missing_file_line(self):
        invalid_note = """---
task: T-51
role: dev
skills: [jpa-patterns]
status: done
---

# Bàn giao T-51

## Bằng chứng áp dụng kỹ năng
Em đã áp dụng jpa-patterns rất cẩn thận nhưng không ghi dòng code nào.
"""
        with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(invalid_note)
            p = Path(f.name)

        try:
            ok, errs = skill_adherence.audit_skill_adherence(p)
            self.assertFalse(ok)
            self.assertTrue(any("dòng code" in e for e in errs))
        finally:
            p.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
