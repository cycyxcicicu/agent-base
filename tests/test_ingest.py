import unittest
from agent_core.ingest.doc_converter import DocumentConverter
from agent_core.ingest.web_cleaner import WebCleaner


class TestIngestModules(unittest.TestCase):
    def test_csv_to_markdown(self):
        csv_data = "name,role,status\nAlice,Architect,Active\nBob,Dev,Active"
        md = DocumentConverter.csv_to_markdown(csv_data)
        self.assertIn("| name | role | status |", md)
        self.assertIn("| Alice | Architect | Active |", md)

    def test_json_to_markdown_table(self):
        json_list = [
            {"id": "T-01", "name": "Auth Cookie"},
            {"id": "T-02", "name": "Dashboard"}
        ]
        md = DocumentConverter.json_to_markdown(json_list)
        self.assertIn("| id | name |", md)
        self.assertIn("| T-01 | Auth Cookie |", md)

    def test_web_cleaner(self):
        raw_html = (
            "<html>"
            "<head><script>alert('spam')</script><style>.bad {color:red}</style></head>"
            "<body>"
            "<h1>Tiêu Đề Trang</h1>"
            "<p>Nội dung quan trọng của bài viết.</p>"
            "<div style='display:none'>văn bản ẩn không được xuất hiện</div>"
            "<span hidden>văn bản ẩn khác</span>"
            "<iframe src='tracker.com'></iframe>"
            "</body>"
            "</html>"
        )
        cleaned = WebCleaner.clean_html(raw_html)
        self.assertNotIn("alert('spam')", cleaned)
        self.assertNotIn("tracker.com", cleaned)
        self.assertNotIn("văn bản ẩn", cleaned)
        self.assertIn("# Tiêu Đề Trang", cleaned)
        self.assertIn("Nội dung quan trọng của bài viết.", cleaned)

    def test_web_cleaner_table(self):
        table_html = (
            "<table>"
            "<tr><th>Endpoint</th><th>Method</th></tr>"
            "<tr><td>/auth/login</td><td>POST</td></tr>"
            "</table>"
        )
        cleaned = WebCleaner.clean_html(table_html)
        self.assertIn("| Endpoint | Method |", cleaned)
        self.assertIn("| /auth/login | POST |", cleaned)

    def test_xlsx_to_markdown(self):
        import zipfile
        import io

        # Tạo file Excel (.xlsx) tối thiểu trong bộ nhớ để test bóc tách First Principles
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            # Shared strings
            shared_strings_xml = (
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="3" uniqueCount="3">'
                '<si><t>Project</t></si>'
                '<si><t>AgentBase</t></si>'
                '<si><t>A "q"</t></si>'
                '</sst>'
            )
            zf.writestr("xl/sharedStrings.xml", shared_strings_xml)

            # Sheet1
            sheet_xml = (
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
                '<sheetData>'
                '<row r="1"><c r="A1" t="s"><v>0</v></c></row>'
                '<row r="2"><c r="A2" t="s"><v>1</v></c></row>'
                '<row r="3"><c r="A3" t="s"><v>2</v></c></row>'
                '</sheetData>'
                '</worksheet>'
            )
            zf.writestr("xl/worksheets/sheet1.xml", sheet_xml)

        zip_buffer.seek(0)
        md = DocumentConverter.xlsx_to_markdown(zip_buffer)
        self.assertIn("| Project |", md)
        self.assertIn("| AgentBase |", md)
        self.assertIn('| A "q" |', md)

    def test_csv_to_markdown_pipe_and_newline_escape(self):
        csv_data = 'name,notes\nAlice,"A | B | C"\nBob,"Line 1\nLine 2"'
        md = DocumentConverter.csv_to_markdown(csv_data)
        # Check pipes are escaped
        self.assertIn(r"A \| B \| C", md)
        # Check newlines are converted to <br>
        self.assertIn("Line 1<br>Line 2", md)

    def test_xlsx_xxe_protection(self):
        import zipfile
        import io

        xxe_xml = (
            '<?xml version="1.0"?>'
            '<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>'
            '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<si><t>&xxe;</t></si>'
            '</sst>'
        )
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            zf.writestr("xl/sharedStrings.xml", xxe_xml)
            zf.writestr("xl/worksheets/sheet1.xml", "<worksheet/>")

        zip_buffer.seek(0)
        with self.assertRaises(ValueError):
            DocumentConverter.xlsx_to_markdown(zip_buffer)

    def test_web_cleaner_font_size_and_opacity_decimals(self):
        """Kiểm chứng WebCleaner không xoá nhầm các thẻ có font-size:0.9em, opacity:0.85, aria-hidden='false'."""
        html = (
            "<div>"
            "<span style='font-size:0.9em'>Văn bản 0.9em hợp lệ</span>"
            "<span style='font-size:0.875rem'>Văn bản 0.875rem hợp lệ</span>"
            "<span style='opacity:0.85'>Văn bản opacity 0.85 hợp lệ</span>"
            "<span style='opacity:.5'>Văn bản opacity .5 hợp lệ</span>"
            "<span aria-hidden='false'>Văn bản aria-hidden false hợp lệ</span>"
            "<span style='font-size:0px'>Văn bản ẩn 0px</span>"
            "<span style='font-size: 0'>Văn bản ẩn 0</span>"
            "<span style='font-size:0.0'>Văn bản ẩn 0.0</span>"
            "<span style='font-size:0.0px'>Văn bản ẩn 0.0px</span>"
            "<span style='opacity:0'>Văn bản ẩn opacity 0</span>"
            "<span style='opacity:0.0'>Văn bản ẩn opacity 0.0</span>"
            "<span aria-hidden='true'>Văn bản ẩn aria-hidden true</span>"
            "</div>"
        )
        cleaned = WebCleaner.clean_html(html)
        self.assertIn("Văn bản 0.9em hợp lệ", cleaned)
        self.assertIn("Văn bản 0.875rem hợp lệ", cleaned)
        self.assertIn("Văn bản opacity 0.85 hợp lệ", cleaned)
        self.assertIn("Văn bản opacity .5 hợp lệ", cleaned)
        self.assertIn("Văn bản aria-hidden false hợp lệ", cleaned)
        self.assertNotIn("Văn bản ẩn 0px", cleaned)
        self.assertNotIn("Văn bản ẩn 0", cleaned)
        self.assertNotIn("Văn bản ẩn 0.0", cleaned)
        self.assertNotIn("Văn bản ẩn 0.0px", cleaned)
        self.assertNotIn("Văn bản ẩn opacity 0", cleaned)
        self.assertNotIn("Văn bản ẩn opacity 0.0", cleaned)
        self.assertNotIn("Văn bản ẩn aria-hidden true", cleaned)

    def test_web_cleaner_table_markdown_newlines(self):
        """Kiểm chứng các hàng trong bảng Markdown được nối bằng \\n đơn, không bị tách bởi \\n\\n."""
        table_html = (
            "<table>"
            "<tr><th>Cột 1</th><th>Cột 2</th></tr>"
            "<tr><td>Giá trị A</td><td>Giá trị B</td></tr>"
            "<tr><td>Giá trị C</td><td>Giá trị D</td></tr>"
            "</table>"
        )
        cleaned = WebCleaner.clean_html(table_html)
        expected_table = (
            "| Cột 1 | Cột 2 |\n"
            "| --- | --- |\n"
            "| Giá trị A | Giá trị B |\n"
            "| Giá trị C | Giá trị D |"
        )
        self.assertIn(expected_table, cleaned)

    def test_web_cleaner_pre_tag_code_block(self):
        """Kiểm chứng thẻ <pre> được bao bọc trong code block Markdown và không bị dính liền với nội dung sau."""
        html = (
            "<div>"
            "<pre>code x=1</pre><a href='/docs'>link text</a>"
            "</div>"
        )
        cleaned = WebCleaner.clean_html(html)
        self.assertIn("```\ncode x=1\n```", cleaned)
        self.assertIn("link text", cleaned)
        self.assertNotIn("code x=1link text", cleaned)


class TestWebCleanerHiddenContent(unittest.TestCase):
    """Loại đúng chữ bị giấu mà không xoá nhầm nội dung hiển thị; xử lý HTML xấu trong thời gian tuyến tính."""

    @staticmethod
    def _clean(fragment: str) -> str:
        return WebCleaner.clean_html("<body>" + fragment + "</body>")

    def test_hidden_variants_are_removed(self):
        hidden = {
            "opacity:0 only property": '<p style="opacity:0">SECRET</p>',
            "opacity:0 !important": '<p style="opacity:0 !important">SECRET</p>',
            "opacity:0.0": '<p style="opacity:0.0">SECRET</p>',
            "opacity uppercase": '<p STYLE="OPACITY:0">SECRET</p>',
            "font-size:0": '<p style="font-size:0">SECRET</p>',
            "font-size:0.0": '<p style="font-size:0.0">SECRET</p>',
            "display:none !important": '<div style="display: none !important">SECRET</div>',
            "visibility:hidden": '<p style="visibility:hidden">SECRET</p>',
            "hidden attribute": "<div hidden>SECRET</div>",
            "hidden empty value": '<div hidden="">SECRET</div>',
            "aria-hidden true": '<div aria-hidden="true">SECRET</div>',
            "single quoted style": "<p style='opacity:0'>SECRET</p>",
            "offscreen left": '<p style="position:absolute;left:-9999px">SECRET</p>',
            "text-indent": '<p style="text-indent:-9999px">SECRET</p>',
            "white on white": '<p style="color:#fff;background:#fff">SECRET</p>',
            "nested same tag": '<div style="display:none"><div>a</div>SECRET</div>',
            "three levels": '<div style="display:none"><div><div>x</div>y</div>SECRET</div>',
            "nested span": "<span hidden><span>b</span>SECRET</span>",
        }
        for name, html in hidden.items():
            self.assertNotIn("SECRET", self._clean(html), name)

    def test_visible_content_is_kept(self):
        visible = {
            "font-size:0.9em": '<p style="font-size:0.9em">KEEP</p>',
            "font-size:.9em": '<p style="font-size:.9em">KEEP</p>',
            "font-size:0.05em": '<p style="font-size:0.05em">KEEP</p>',
            "font-size:10px": '<p style="font-size:10px">KEEP</p>',
            "font-size empty": '<p style="font-size:;color:red">KEEP</p>',
            "opacity:0.85": '<p style="opacity:0.85">KEEP</p>',
            "opacity:.5": '<p style="opacity:.5">KEEP</p>',
            "opacity:0.99": '<p style="opacity:0.99">KEEP</p>',
            "aria-hidden false": '<div aria-hidden="false">KEEP</div>',
            "class hidden-xs": '<div class="hidden-xs"><p>KEEP</p></div>',
            "id hidden-panel": '<div id="hidden-panel"><p>KEEP</p></div>',
            "title with word hidden": '<p title="hidden gem">KEEP</p>',
            "class overflow-hidden": '<div class="overflow-hidden"><h2>KEEP</h2></div>',
            "data-hidden": '<p data-hidden="x">KEEP</p>',
            "small negative left": '<p style="position:relative;left:-10px">KEEP</p>',
            "white text on dark": '<p style="color:#fff;background:#000">KEEP</p>',
            "gt sign inside attribute": '<p title="a > b" style="opacity:0.9">KEEP</p>',
            "hidden input then text": '<form><input type="hidden" name="a" value="1"><p>KEEP</p></form>',
        }
        for name, html in visible.items():
            self.assertIn("KEEP", self._clean(html), name)

    def test_text_after_a_hidden_block_is_kept(self):
        out = self._clean('<div style="display:none"><div><div>x</div>y</div>SECRET</div>AFTER')
        self.assertIn("AFTER", out)
        self.assertNotIn("SECRET", out)

    def test_implicit_end_tags_do_not_swallow_following_content(self):
        out = self._clean("<p hidden>SECRET<p>KEEP</p>")
        self.assertNotIn("SECRET", out)
        self.assertIn("KEEP", out)

    def test_linear_time_on_hostile_html(self):
        import time
        hostile = {
            "unclosed hidden p": "<p hidden>" * 10000 + "x",
            "unclosed table": "<table>" * 5000 + "x",
            "unclosed pre": "<pre>" * 5000 + "x",
            "unclosed td": "<table><tr>" + "<td>" * 20000 + "</tr></table>",
            "unclosed h1": "<h1>" * 20000,
            "unclosed div": "<div>" * 20000 + "x",
            "unclosed li": "<li>a" * 20000,
            "endless attributes": "<div " + "a " * 40000 + "<p>x",
        }
        for name, html in hostile.items():
            start = time.time()
            WebCleaner.clean_html(html)
            self.assertLess(time.time() - start, 3.0, f"{name} chạy quá chậm (nghi ngờ O(n^2))")

    def test_structure_is_preserved(self):
        out = self._clean(
            "<h1>T</h1><table><tr><th>A</th><th>B</th></tr><tr><td>1</td><td>2</td></tr></table>"
            "<ul><li>one</li></ul><pre>x=1</pre><a href='/x'>lk</a> tail"
        )
        self.assertIn("| A | B |\n| --- | --- |\n| 1 | 2 |", out)
        self.assertIn("```\nx=1\n```", out)
        self.assertNotIn("x=1lk", out)

    def test_preformatted_tag_is_not_mistaken_for_paragraph(self):
        out = self._clean("<pre>code</pre><p>para</p>")
        self.assertIn("```\ncode\n```", out)
        self.assertIn("para", out)


if __name__ == "__main__":
    unittest.main()
