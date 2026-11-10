"""Kiểm thử scripts/glossary-check.py (Domain Glossary & diff-scoped terminology guard)."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "glossary-check.py"

GLOSSARY = {
    "version": "1.0.0",
    "exclude": ["**/archive/**", "**/GLOSSARY.json"],
    "terms": [
        {
            "id": "ui-status-term",
            "preferred": "Trạng thái",
            "forbidden": ["Tình trạng đơn", "Tình trạng"],
            "include": ["doc/**/*.md", "frontend/**/*.tsx"],
            "reason": "Thống nhất dùng 'Trạng thái' theo bảng thuật ngữ dự án",
        },
        {
            "id": "ui-tracking-term",
            "preferred": "Mã vận đơn",
            "forbidden": ["Tracking Number", "Số tracking"],
            "include": ["frontend/**/*.tsx"],
            "reason": "Nhãn UI tiếng Việt chuẩn là 'Mã vận đơn'",
        },
    ],
}


class TestGlossaryCheck(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="glossary-")
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)

    def _write(self, rel: str, text: str):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def _git(self, *args: str):
        r = subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stderr)

    def _run(self, *extra: str):
        r = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), *extra],
                           capture_output=True, text=True, encoding="utf-8")
        return r.returncode, r.stdout + r.stderr

    def test_missing_glossary_passes_gracefully(self):
        code, out = self._run()
        self.assertEqual(code, 0, out)
        self.assertIn("Chưa cấu hình GLOSSARY.json", out)

    def test_detects_forbidden_term_and_allows_ignore_with_reason(self):
        self._write("doc/architecture/GLOSSARY.json", json.dumps(GLOSSARY, ensure_ascii=False))
        self._write("frontend/Page.tsx", 'export const label = "Tình trạng đơn";\n')
        code, out = self._run()
        self.assertEqual(code, 1, out)
        self.assertIn("[ui-status-term]", out)
        self.assertIn("Trạng thái", out)

        self._write("frontend/Page.tsx", '// glossary-ignore: ui-status-term giữ tên nhãn API cũ\nexport const label = "Tình trạng đơn";\n')
        code2, out2 = self._run()
        self.assertEqual(code2, 0, out2)
        self.assertIn("1 bỏ qua có lý do", out2)

    def test_changed_against_scans_only_new_or_uncommitted_lines_not_legacy(self):
        self._git("init", "-q", "-b", "develop")
        self._git("config", "user.email", "t@example.com")
        self._git("config", "user.name", "Tester")
        self._write("doc/architecture/GLOSSARY.json", json.dumps(GLOSSARY, ensure_ascii=False))
        self._write("frontend/Legacy.tsx", 'export const old = "Tình trạng";\n')
        self._git("add", "-A")
        self._git("commit", "-q", "-m", "base")

        # File sửa mới (kể cả chưa commit trong worktree) dùng chuẩn -> PASS
        self._git("checkout", "-q", "-b", "feature/uc06")
        self._write("frontend/NewComp.tsx", 'export const title = "Mã vận đơn";\n')
        code, out = self._run("--changed-against", "develop")
        self.assertEqual(code, 0, out)

        # Thêm dòng sai chuẩn chưa commit -> FAIL ngay ở dòng đó, không bắt lỗi file Legacy cũ
        self._write("frontend/NewComp.tsx", 'export const title = "Tracking Number";\n')
        code2, out2 = self._run("--changed-against", "develop")
        self.assertEqual(code2, 1, out2)
        self.assertIn("frontend/NewComp.tsx:1", out2)
        self.assertNotIn("Legacy.tsx", out2)


if __name__ == "__main__":
    unittest.main()

