"""Kiểm thử scripts/srs-check.py bằng đặc tả giả (không dùng dữ liệu dự án)."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

try:
    from test_diagram_describe import mxfile, page
except ImportError:  # chạy bằng python -m unittest tests.test_srs_check
    from tests.test_diagram_describe import mxfile, page

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "srs-check.py"

GOOD = """# SRS — Đặt hàng

| Trường | Giá trị |
|---|---|
| Mã | UC-01 |

## 1. Bối cảnh
Hệ thống phải cho phép khách đặt hàng khi còn tồn kho.

## 2. Tác nhân
- Khách hàng

## 3. Use-case
### 3.1 Đặt hàng
Khách chọn sản phẩm rồi bấm đặt.

**Tiêu chí chấp nhận (A/C)**
| A/C | Nội dung |
|---|---|
| AC-01 | Khi tồn kho đủ thì tạo đơn |
| AC-02 | Khi hết hàng thì trả lỗi 400 trong 2 giây |

## 4. Sơ đồ
![Hoạt động đặt hàng](hinh/hoat-dong.png)

| Bước | Làn | Hành động |
|---|---|---|
| 1.1 | Khách | Bấm đặt |
| 1.2 | Hệ thống | Kiểm tra tồn kho |

Không thêm bảng.

## 5. Yêu cầu phi chức năng
Đặt hàng phải hoàn tất trong 2 giây ở mức 100 người dùng đồng thời.

## 6. Kiểm thử
| ID | Name | A/C ref |
|---|---|---|
| HP_01 | Đặt thành công | AC-01 |
| EC_01 | Hết hàng | AC-02 |

## 7. Câu hỏi mở
- [ ] Có giới hạn số lượng mỗi đơn không?
"""


class SrsCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = Path(self._tmp.name)
        (self.dir / "hinh").mkdir()
        (self.dir / "hinh" / "hoat-dong.png").write_bytes(b"png")

    def run_check(self, text, *args):
        f = self.dir / "UC-01-feat-dat-hang.md"
        f.write_text(text, encoding="utf-8")
        return subprocess.run([sys.executable, str(SCRIPT), str(f), *args], capture_output=True, text=True)


class TestSrsCheck(SrsCase):
    def test_complete_spec_passes_even_in_strict_mode(self):
        r = self.run_check(GOOD, "--strict")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("ĐẠT", r.stdout)

    def test_missing_required_section_is_an_error(self):
        r = self.run_check(GOOD.replace("## 5. Yêu cầu phi chức năng", "## 5. Ghi chú"))
        self.assertEqual(r.returncode, 1)
        self.assertIn("phi chức năng", r.stdout)

    def test_missing_image_file_is_an_error(self):
        r = self.run_check(GOOD.replace("hinh/hoat-dong.png", "hinh/khong-co.png"))
        self.assertEqual(r.returncode, 1)
        self.assertIn("ảnh sơ đồ không tồn tại", r.stdout)

    def test_acceptance_criterion_without_test_case_is_an_error(self):
        r = self.run_check(GOOD.replace("| EC_01 | Hết hàng | AC-02 |", "| EC_01 | Hết hàng | |"))
        self.assertEqual(r.returncode, 1)
        self.assertIn("AC-02 chưa có ca kiểm thử", r.stdout)

    def test_spec_without_any_diagram_is_an_error(self):
        r = self.run_check(GOOD.replace("![Hoạt động đặt hàng](hinh/hoat-dong.png)", "Chưa vẽ."))
        self.assertEqual(r.returncode, 1)
        self.assertIn("chưa có sơ đồ nào", r.stdout)

    def test_vague_word_warns_and_strict_fails(self):
        text = GOOD.replace("Khách chọn sản phẩm rồi bấm đặt.", "Giao diện phải trực quan và nhanh.")
        r = self.run_check(text)
        self.assertEqual(r.returncode, 0)
        self.assertIn("từ cảm tính", r.stdout)
        self.assertEqual(self.run_check(text, "--strict").returncode, 1)

    def test_numbers_make_a_measurable_sentence_acceptable(self):
        r = self.run_check(GOOD.replace("Khách chọn sản phẩm rồi bấm đặt.", "Trang phải phản hồi nhanh hơn 2 giây."))
        self.assertNotIn("từ cảm tính", r.stdout)

    def test_vague_words_in_open_questions_are_allowed(self):
        r = self.run_check(GOOD.replace("Có giới hạn số lượng mỗi đơn không?", "Giao diện có cần thân thiện hơn không?"))
        self.assertNotIn("từ cảm tính", r.stdout)

    def test_image_without_step_description_warns(self):
        text = GOOD.replace("| 1.1 | Khách | Bấm đặt |\n| 1.2 | Hệ thống | Kiểm tra tồn kho |\n", "")
        r = self.run_check(text)
        self.assertIn("chưa có mô tả hoạt động", r.stdout)

    def test_database_without_erd_warns(self):
        r = self.run_check(GOOD.replace("Không thêm bảng.", "Dữ liệu lưu trong cơ sở dữ liệu."))
        self.assertIn("ERD", r.stdout)

    def test_open_questions_not_last_warns(self):
        r = self.run_check(GOOD + "\n## 8. Rủi ro\nChưa có.\n")
        self.assertIn("câu hỏi mở nên là mục cuối", r.stdout)

    def test_machine_specific_file_link_warns_but_resolves(self):
        absolute = "file://" + str(self.dir / "hinh" / "hoat-dong.png")
        r = self.run_check(GOOD.replace("hinh/hoat-dong.png", absolute))
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("liên kết tuyệt đối theo máy", r.stdout)
        self.assertNotIn("ảnh sơ đồ không tồn tại", r.stdout)

    def test_erd_style_image_needs_only_some_explanation(self):
        text = GOOD.replace("Không thêm bảng.", "![ERD đơn hàng](hinh/erd.png)\n\n| Bảng | Cột chính | Quan hệ |\n|---|---|---|\n| orders | id | 1-n order_items |\n| order_items | order_id | n-1 orders |")
        (self.dir / "hinh" / "erd.png").write_bytes(b"png")
        r = self.run_check(text, "--strict")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_code_fences_and_html_comments_are_ignored(self):
        text = GOOD.replace("Không thêm bảng.", "Không thêm bảng.\n<!-- nhanh, mượt, trực quan -->\n```\nnhanh mượt\n```")
        self.assertEqual(self.run_check(text, "--strict").returncode, 0)


class TestSrsCheckWithDrawio(SrsCase):
    def link_drawio(self, content):
        (self.dir / "hinh" / "UC-01.drawio").write_text(content, encoding="utf-8")
        return GOOD + "\n"  # chèn dẫn tới nguồn vào mục sơ đồ

    def spec_with_drawio(self):
        return GOOD.replace("Không thêm bảng.", "Không thêm bảng.\n\nNguồn: [UC-01.drawio](hinh/UC-01.drawio)")

    def test_valid_drawio_source_is_accepted(self):
        (self.dir / "hinh" / "UC-01.drawio").write_text(mxfile(page("p1")), encoding="utf-8")
        r = self.run_check(self.spec_with_drawio(), "--strict")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_drawio_with_two_end_nodes_fails_the_spec(self):
        (self.dir / "hinh" / "UC-01.drawio").write_text(mxfile(page("p1", ends=2)), encoding="utf-8")
        r = self.run_check(self.spec_with_drawio())
        self.assertEqual(r.returncode, 1)
        self.assertIn("đúng một nút kết thúc", r.stdout)

    def test_missing_drawio_source_is_an_error(self):
        r = self.run_check(self.spec_with_drawio())
        self.assertEqual(r.returncode, 1)
        self.assertIn("file nguồn sơ đồ không tồn tại", r.stdout)


if __name__ == "__main__":
    unittest.main()
