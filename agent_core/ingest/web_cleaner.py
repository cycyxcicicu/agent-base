"""
Web DOM & Semantic Accessibility Cleaner.
Học hỏi từ: webcmd (Lọc sạch HTML rác, chiết xuất cấu trúc tinh gọn cho AI).
"""

import re
from html import unescape
from typing import Dict


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

    # Thẻ HTML mở hoặc đóng: (1) '/' nếu là thẻ đóng, (2) tên thẻ, (3) chuỗi thuộc tính (giá trị có thể chứa '>'
    # khi nằm trong dấu nháy), (4) '/' nếu là thẻ tự đóng.
    _TAG = re.compile(
        r"<(/?)([a-zA-Z][a-zA-Z0-9:-]*)((?:\s+[^\s\"'<>/=]+(?:\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s\"'<>=`]+))?)*)\s*(/?)>"
    )
    _ATTR = re.compile(r"([^\s\"'<>/=]+)(?:\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s\"'<>=`]+)))?")
    _VOID_TAGS = frozenset(
        "area base br col embed hr img input link meta param source track wbr".split()
    )

    # Số bằng 0 (0, 00, 0.0, .0) kèm đơn vị tuỳ chọn; KHÔNG khớp 0.9em, 10px, 0.05em.
    _ZERO_NUMBER = re.compile(r"^[+-]?(?=[0.])0*(?:\.0+)?(?:px|pt|em|rem|ex|ch|vw|vh|%)?$")
    _WHITE = re.compile(r"^(?:white|#fff(?:fff)?(?:ff)?|rgba?\(\s*255\s*,\s*255\s*,\s*255\s*(?:,\s*[\d.]+\s*)?\))$")
    _OFFSCREEN = re.compile(r"^-\s*\d{4,}(?:px|em|rem|vw|vh|%)?$")

    @classmethod
    def _parse_attrs(cls, attr_text: str) -> Dict[str, str]:
        attrs: Dict[str, str] = {}
        for m in cls._ATTR.finditer(attr_text or ""):
            value = m.group(2) if m.group(2) is not None else (m.group(3) if m.group(3) is not None else m.group(4))
            attrs[m.group(1).lower()] = "" if value is None else value
        return attrs

    @classmethod
    def _style_declarations(cls, style: str) -> Dict[str, str]:
        decls: Dict[str, str] = {}
        for part in style.split(";"):
            if ":" not in part:
                continue
            name, value = part.split(":", 1)
            value = re.sub(r"\s*!important\s*$", "", value.strip(), flags=re.IGNORECASE)
            decls[name.strip().lower()] = value.strip().lower()
        return decls

    @classmethod
    def _is_hidden(cls, attrs: Dict[str, str]) -> bool:
        """Phần tử có bị giấu khỏi người xem (nhưng vẫn nằm trong DOM để đánh lừa AI) hay không."""
        # Thuộc tính boolean `hidden` (đứng riêng, KHÔNG phải chữ 'hidden' trong giá trị của class/id/title).
        if "hidden" in attrs:
            return True
        if attrs.get("aria-hidden", "").strip().lower() == "true":
            return True
        style = attrs.get("style")
        if not style:
            return False
        d = cls._style_declarations(style)
        if d.get("display") == "none" or d.get("visibility") == "hidden":
            return True
        if "font-size" in d and cls._ZERO_NUMBER.match(d["font-size"]):
            return True
        if "opacity" in d and cls._ZERO_NUMBER.match(d["opacity"]):
            return True
        # Chữ đặt ngoài màn hình.
        for prop in ("left", "top", "text-indent", "margin-left", "margin-top"):
            if prop in d and cls._OFFSCREEN.match(d[prop]):
                return True
        # Chữ ngụy trang: màu chữ trùng màu nền.
        color = d.get("color")
        background = d.get("background-color") or d.get("background")
        if color and background and cls._WHITE.match(color) and cls._WHITE.match(background):
            return True
        return False

    # Thẻ bị đóng ngầm khi gặp thẻ mở cùng tên ngay sau nó (<p>a<p>b, <li>a<li>b, <td>a<td>b ...).
    _IMPLICIT_CLOSE = frozenset({"p", "li", "dt", "dd", "option", "tr", "td", "th"})

    @classmethod
    def _strip_hidden_elements(cls, html: str) -> str:
        """Xoá phần tử ẩn cùng toàn bộ nội dung bên trong (kể cả thẻ cùng tên lồng nhau).

        Quét một lượt duy nhất với ngăn xếp các phần tử đang mở nên độ phức tạp tuyến tính O(n),
        an toàn với trang có hàng chục nghìn thẻ ẩn không đóng."""
        out = []
        pos = 0
        stack = []            # tên các phần tử đang mở (chưa đóng)
        open_count = {}       # tên -> số phần tử đang mở trong stack
        hidden_at = None      # chỉ số trong stack của phần tử ẩn ngoài cùng; None nếu đang ở vùng hiển thị

        def pop_until(name: str) -> None:
            nonlocal hidden_at
            while stack:
                top = stack.pop()
                open_count[top] -= 1
                if top == name:
                    break
            if hidden_at is not None and len(stack) <= hidden_at:
                hidden_at = None

        for m in cls._TAG.finditer(html):
            if hidden_at is None:
                out.append(html[pos:m.start()])
            pos = m.end()
            closing, raw_name, attr_text, self_close = m.group(1), m.group(2), m.group(3), m.group(4)
            name = raw_name.lower()
            was_hidden = hidden_at is not None

            if closing:
                if open_count.get(name, 0) > 0:
                    pop_until(name)
                if not was_hidden:
                    out.append(m.group(0))
                continue

            # Thẻ mở cùng tên nằm ngay trên đỉnh ngăn xếp => thẻ trước được đóng ngầm.
            if name in cls._IMPLICIT_CLOSE and stack and stack[-1] == name:
                pop_until(name)
                was_hidden = hidden_at is not None

            is_void = name in cls._VOID_TAGS or bool(self_close)
            if was_hidden:
                if not is_void:
                    stack.append(name)
                    open_count[name] = open_count.get(name, 0) + 1
                continue

            if cls._is_hidden(cls._parse_attrs(attr_text)):
                if not is_void:
                    hidden_at = len(stack)
                    stack.append(name)
                    open_count[name] = open_count.get(name, 0) + 1
                continue

            out.append(m.group(0))
            if not is_void:
                stack.append(name)
                open_count[name] = open_count.get(name, 0) + 1

        if hidden_at is None:
            out.append(html[pos:])
        return "".join(out)

    _CELL_OPEN = re.compile(r"<(td|th)\b[^>]*>", re.IGNORECASE)
    _CELL_CLOSE = {
        "td": re.compile(r"</td\s*>", re.IGNORECASE),
        "th": re.compile(r"</th\s*>", re.IGNORECASE),
    }

    @classmethod
    def _cells(cls, row: str) -> list:
        """Nội dung các ô <td>/<th> của một hàng, quét tuyến tính."""
        cells = []
        pos = 0
        while True:
            m = cls._CELL_OPEN.search(row, pos)
            if not m:
                break
            c = cls._CELL_CLOSE[m.group(1).lower()].search(row, m.end())
            if not c:
                break
            cells.append(row[m.end():c.start()])
            pos = c.end()
        return cells

    @staticmethod
    def _sub_blocks(text: str, tag: str, repl) -> str:
        """Thay từng khối <tag ...>nội dung</tag> (không lồng, thẻ đóng đầu tiên thắng) bằng repl(nội dung).

        Tìm thẻ đóng bằng một lần quét tiến về phía trước nên độ phức tạp tuyến tính; khi không còn thẻ đóng
        thì dừng ngay (phần còn lại giữ nguyên, các thẻ mở thừa sẽ bị bóc ở bước sau)."""
        open_re = re.compile(rf"<{tag}\b[^>]*>", re.IGNORECASE)
        close_re = re.compile(rf"</{tag}\s*>", re.IGNORECASE)
        out = []
        pos = 0
        while True:
            m = open_re.search(text, pos)
            if not m:
                break
            c = close_re.search(text, m.end())
            if not c:
                break
            out.append(text[pos:m.start()])
            out.append(repl(text[m.end():c.start()]))
            pos = c.end()
        out.append(text[pos:])
        return "".join(out)

    @classmethod
    def clean_html(cls, html_content: str) -> str:
        """Loại bỏ toàn bộ mã rác khỏi trang web."""
        clean = html_content
        for pattern in cls.NOISY_TAGS:
            clean = re.sub(pattern, "", clean, flags=re.IGNORECASE)

        # Loại bỏ phần tử bị giấu (display:none, visibility:hidden, font-size:0, opacity:0, hidden, aria-hidden="true",
        # chữ đặt ngoài màn hình, chữ trùng màu nền) cùng nội dung bên trong.
        clean = cls._strip_hidden_elements(clean)

        # Chuyển đổi tiêu đề, đoạn văn, khối và danh sách thành Markdown (mỗi hàm đều quét tuyến tính).
        clean = cls._sub_blocks(clean, "h1", lambda inner: f"\n# {inner}\n")
        clean = cls._sub_blocks(clean, "h2", lambda inner: f"\n## {inner}\n")
        clean = cls._sub_blocks(clean, "h3", lambda inner: f"\n### {inner}\n")
        clean = cls._sub_blocks(clean, "p", lambda inner: f"\n{inner}\n")
        clean = cls._sub_blocks(clean, "div", lambda inner: f"\n{inner}\n")
        clean = re.sub(r"<br\s*\/?>", r"\n", clean, flags=re.IGNORECASE)
        clean = cls._sub_blocks(clean, "li", lambda inner: f"\n- {inner}")

        # Chuyển đổi các thẻ bảng <table> thành Markdown table
        def _table_replacer(table_inner: str) -> str:
            rows = []
            pos = 0
            row_re = re.compile(r"<tr\b[^>]*>", re.IGNORECASE)
            row_close = re.compile(r"</tr\s*>", re.IGNORECASE)
            while True:
                m = row_re.search(table_inner, pos)
                if not m:
                    break
                c = row_close.search(table_inner, m.end())
                if not c:
                    break
                rows.append(table_inner[m.end():c.start()])
                pos = c.end()
            if not rows:
                return ""
            md_table_rows = []
            for r_idx, row in enumerate(rows):
                cols = cls._cells(row)
                cols_clean = [re.sub(r"<[^>]+>", "", c).strip().replace("\n", " ") for c in cols]
                if not cols_clean:
                    continue
                md_table_rows.append("| " + " | ".join(cols_clean) + " |")
                if r_idx == 0:
                    md_table_rows.append("| " + " | ".join(["---"] * len(cols_clean)) + " |")
            return "\n\n" + "\n".join(md_table_rows) + "\n\n"

        clean = cls._sub_blocks(clean, "table", _table_replacer)

        # Chuyển đổi khối <pre> thành code block Markdown trước khi bóc thẻ HTML còn lại
        clean = cls._sub_blocks(clean, "pre", lambda inner: f"\n\n```\n{inner}\n```\n\n")

        # Bóc toàn bộ các thẻ HTML còn lại
        clean = re.sub(r"<[^>]+>", "", clean)

        # Giải mã ký tự HTML entities (&amp;, &lt;, ...)
        clean = unescape(clean)

        # Chuẩn hóa khoảng trắng và dòng trống
        lines = [line.strip() for line in clean.splitlines() if line.strip()]
        in_code_block = False
        result_lines = []
        for i, line in enumerate(lines):
            if line.startswith("```"):
                in_code_block = not in_code_block
                if i > 0 and not in_code_block:
                    result_lines.append("\n" + line)
                elif i > 0:
                    result_lines.append("\n\n" + line)
                else:
                    result_lines.append(line)
            elif in_code_block:
                result_lines.append("\n" + line)
            elif i > 0 and line.startswith("|") and lines[i - 1].startswith("|"):
                result_lines.append("\n" + line)
            else:
                if i > 0:
                    result_lines.append("\n\n" + line)
                else:
                    result_lines.append(line)
        return "".join(result_lines)
