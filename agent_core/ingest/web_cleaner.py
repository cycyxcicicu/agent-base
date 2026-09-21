"""
Web DOM & Semantic Accessibility Cleaner.
Học hỏi từ: webcmd (Lọc sạch HTML rác, chiết xuất cấu trúc tinh gọn cho AI).
"""

import re
from html import unescape


class WebCleaner:
    """Loại bỏ thẻ rác, quảng cáo, tracking script để tạo ngữ cảnh sạch cho AI."""

    NOISY_TAGS = [
        r"<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>",
        r"<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>",
        r"<svg\b[^<]*(?:(?!<\/svg>)<[^<]*)*<\/svg>",
        r"<noscript\b[^<]*(?:(?!<\/noscript>)<[^<]*)*<\/noscript>",
        r"<!--[\s\S]*?-->",
        r"<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>",
    ]

    @classmethod
    def clean_html(cls, html_content: str) -> str:
        """Loại bỏ toàn bộ mã rác khỏi trang web."""
        clean = html_content
        for pattern in cls.NOISY_TAGS:
            clean = re.sub(pattern, "", clean, flags=re.IGNORECASE)

        # Chuyển đổi các thẻ tiêu đề thành Markdown
        clean = re.sub(r"<h1[^>]*>(.*?)<\/h1>", r"\n# \1\n", clean, flags=re.IGNORECASE)
        clean = re.sub(r"<h2[^>]*>(.*?)<\/h2>", r"\n## \1\n", clean, flags=re.IGNORECASE)
        clean = re.sub(r"<h3[^>]*>(.*?)<\/h3>", r"\n### \1\n", clean, flags=re.IGNORECASE)
        clean = re.sub(r"<p[^>]*>(.*?)<\/p>", r"\n\1\n", clean, flags=re.IGNORECASE)
        clean = re.sub(r"<li[^>]*>(.*?)<\/li>", r"\n- \1", clean, flags=re.IGNORECASE)

        # Chuyển đổi các thẻ bảng <table> thành Markdown table
        def _table_replacer(match):
            table_html = match.group(0)
            rows = re.findall(r"<tr[^>]*>(.*?)<\/tr>", table_html, flags=re.IGNORECASE | re.DOTALL)
            if not rows:
                return ""
            md_table_rows = []
            for r_idx, row in enumerate(rows):
                cols = re.findall(r"<(?:td|th)[^>]*>(.*?)<\/(?:td|th)>", row, flags=re.IGNORECASE | re.DOTALL)
                cols_clean = [re.sub(r"<[^>]+>", "", c).strip().replace("\n", " ") for c in cols]
                if not cols_clean:
                    continue
                md_table_rows.append("| " + " | ".join(cols_clean) + " |")
                if r_idx == 0:
                    md_table_rows.append("| " + " | ".join(["---"] * len(cols_clean)) + " |")
            return "\n\n" + "\n".join(md_table_rows) + "\n\n"

        clean = re.sub(r"<table\b[^>]*>.*?<\/table>", _table_replacer, clean, flags=re.IGNORECASE | re.DOTALL)

        # Bóc toàn bộ các thẻ HTML còn lại
        clean = re.sub(r"<[^>]+>", "", clean)

        # Giải mã ký tự HTML entities (&amp;, &lt;, ...)
        clean = unescape(clean)

        # Chuẩn hóa khoảng trắng và dòng trống
        lines = [line.strip() for line in clean.splitlines() if line.strip()]
        return "\n\n".join(lines)

