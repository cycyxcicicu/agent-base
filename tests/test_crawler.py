"""tests/test_crawler.py

Unit test cho công cụ scripts/crawl_jina_assets.py
"""

from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch

from scripts.research_tools.crawl_jina_assets import (
    extract_image_urls,
    extract_internal_links,
    sanitize_filename,
)


class TestCrawler(unittest.TestCase):

    def test_sanitize_filename(self):
        self.assertEqual(sanitize_filename("valid_name"), "valid_name")
        self.assertEqual(sanitize_filename("name/with\\invalid:chars*?"), "name_with_invalid_chars")
        self.assertEqual(sanitize_filename("   spaced  name   "), "spaced_name")

    def test_extract_image_urls(self):
        sample_md = """
# Tiêu đề
Đây là ảnh markdown: ![Mô tả 1](images/diag1.png "title")
Đây là ảnh absolute: ![Mô tả 2](https://example.com/assets/logo.svg)
Đây là thẻ HTML img: <img src="/static/chart.jpg" alt="Thống kê">
        """
        base_url = "https://example.com/docs/page.html"
        extracted = extract_image_urls(sample_md, base_url)

        self.assertEqual(len(extracted), 3)
        urls = [item[2] for item in extracted]
        self.assertIn("https://example.com/docs/images/diag1.png", urls)
        self.assertIn("https://example.com/assets/logo.svg", urls)
        self.assertIn("https://example.com/static/chart.jpg", urls)

    def test_extract_internal_links(self):
        sample_md = """
[Link ngoài](https://google.com/search)
[Link nội bộ 1](https://example.com/sub/page1.html)
[Link nội bộ tương đối](/sub/page2.html)
[Link neo](#section)
        """
        base_url = "https://example.com/index.html"
        links = extract_internal_links(sample_md, "example.com", base_url)

        self.assertEqual(len(links), 2)
        self.assertIn("https://example.com/sub/page1.html", links)
        self.assertIn("https://example.com/sub/page2.html", links)


if __name__ == "__main__":
    unittest.main()

