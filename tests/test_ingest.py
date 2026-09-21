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
        """Kiểm chứng WebCleaner không xoá nhầm các thẻ có font-size:0.9em hoặc opacity:0.85."""
        html = (
            "<div>"
            "<span style='font-size:0.9em'>Văn bản 0.9em hợp lệ</span>"
            "<span style='font-size:0.875rem'>Văn bản 0.875rem hợp lệ</span>"
            "<span style='opacity:0.85'>Văn bản opacity 0.85 hợp lệ</span>"
            "<span style='opacity:.5'>Văn bản opacity .5 hợp lệ</span>"
            "<span style='font-size:0px'>Văn bản ẩn 0px</span>"
            "<span style='font-size: 0'>Văn bản ẩn 0</span>"
            "<span style='opacity:0'>Văn bản ẩn opacity 0</span>"
            "<span style='opacity:0.0'>Văn bản ẩn opacity 0.0</span>"
            "</div>"
        )
        cleaned = WebCleaner.clean_html(html)
        self.assertIn("Văn bản 0.9em hợp lệ", cleaned)
        self.assertIn("Văn bản 0.875rem hợp lệ", cleaned)
        self.assertIn("Văn bản opacity 0.85 hợp lệ", cleaned)
        self.assertIn("Văn bản opacity .5 hợp lệ", cleaned)
        self.assertNotIn("Văn bản ẩn 0px", cleaned)
        self.assertNotIn("Văn bản ẩn 0", cleaned)
        self.assertNotIn("Văn bản ẩn opacity 0", cleaned)
        self.assertNotIn("Văn bản ẩn opacity 0.0", cleaned)

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


if __name__ == "__main__":
    unittest.main()
