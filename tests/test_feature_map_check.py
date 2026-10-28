"""Kiểm thử scripts/feature-map-check.py. Viết bằng unittest để CI chạy được."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "feature-map-check.py"

GOOD_MAP = """# Feature Map: Demo
Cập nhật: 2026-10-19

## F-01 Tìm kiếm tài liệu
- Khu vực: thanh bên trái
- Đường vào: Đăng nhập > Tài liệu
- Định vị: `[data-testid="doc-search"]`
- File nguồn: `src/features/docs/Search.tsx`
- Kiểm tra nhanh: gõ chữ ra danh sách lọc

## F-02 Hồ sơ (chưa kiểm)
- Khu vực: góc phải
- Đường vào: avatar > Hồ sơ
- Định vị: nút `role=button name="Hồ sơ"`
- File nguồn: `src/features/profile/`
- Kiểm tra nhanh: mở được trang hồ sơ
"""


class FeatureMapCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="fmcheck-")
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.write("src/features/docs/Search.tsx", '<input data-testid="doc-search" />\n')
        self.write("src/features/profile/Profile.tsx", "export const Profile = () => null;\n")
        self.write("docs/design/feature-map.md", GOOD_MAP)

    def write(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def run_check(self, *extra):
        r = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), *extra],
                           capture_output=True, text=True, encoding="utf-8")
        return r.returncode, r.stdout + r.stderr


class TestFeatureMapCheck(FeatureMapCase):
    def test_matching_map_passes_and_counts_unverified(self):
        code, out = self.run_check()
        self.assertEqual(code, 0, out)
        self.assertIn("1 mục còn `(chưa kiểm)`", out)

    def test_optional_sub_features_field_is_accepted(self):
        self.write("docs/design/feature-map.md",
                   GOOD_MAP.replace("- Kiểm tra nhanh: gõ chữ ra danh sách lọc\n",
                                    "- Tính năng phụ: lọc theo loại\n- Kiểm tra nhanh: gõ chữ ra danh sách lọc\n"))
        code, out = self.run_check()
        self.assertEqual(code, 0, out)

    def test_no_map_is_not_an_error(self):
        (self.root / "docs" / "design" / "feature-map.md").unlink()
        code, out = self.run_check()
        self.assertEqual(code, 0, out)
        self.assertIn("Chưa có", out)

    def test_missing_source_file_is_drift(self):
        (self.root / "src/features/docs/Search.tsx").unlink()
        code, out = self.run_check()
        self.assertEqual(code, 1, out)
        self.assertIn("không còn tồn tại", out)

    def test_stale_testid_is_drift(self):
        self.write("src/features/docs/Search.tsx", '<input data-testid="renamed" />\n')
        code, out = self.run_check()
        self.assertEqual(code, 1, out)
        self.assertIn('"doc-search" không còn xuất hiện', out)

    def test_testid_elsewhere_in_repo_is_only_a_warning(self):
        self.write("src/features/docs/Search.tsx", "export const S = 1;\n")
        self.write("src/shared/Input.tsx", '<input data-testid="doc-search" />\n')
        code, out = self.run_check()
        self.assertEqual(code, 0, out)
        self.assertIn("không nằm trong File nguồn", out)

    def test_missing_required_field(self):
        self.write("docs/design/feature-map.md", GOOD_MAP.replace("- Kiểm tra nhanh: gõ chữ ra danh sách lọc\n", ""))
        code, out = self.run_check()
        self.assertEqual(code, 1, out)
        self.assertIn('thiếu mục "Kiểm tra nhanh"', out)

    def test_duplicate_id(self):
        self.write("docs/design/feature-map.md", GOOD_MAP.replace("F-02", "F-01"))
        code, out = self.run_check()
        self.assertEqual(code, 1, out)
        self.assertIn("bị trùng", out)

    def test_directory_source_is_expanded(self):
        (self.root / "src/features/profile/Profile.tsx").unlink()
        code, out = self.run_check()
        self.assertEqual(code, 1, out)  # thư mục profile/ giờ rỗng
        self.assertIn("src/features/profile", out)


class TestChangedAgainst(FeatureMapCase):
    def git(self, *args):
        r = subprocess.run(["git", *args], cwd=self.root, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_new_ui_file_outside_map_is_warned(self):
        self.git("init", "-q", "-b", "develop")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "T")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "base")
        self.git("checkout", "-q", "-b", "feature/1-x")
        self.write("src/features/billing/Invoice.tsx", "export const Invoice = () => null;\n")
        self.write("src/features/billing/Invoice.test.tsx", "test('x', () => {});\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "change")
        code, out = self.run_check("--changed-against", "develop")
        self.assertEqual(code, 0, out)  # chỉ cảnh báo, không làm đỏ
        self.assertIn("src/features/billing/Invoice.tsx", out)
        self.assertNotIn("Invoice.test.tsx", out)


if __name__ == "__main__":
    unittest.main()
