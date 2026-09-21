"""
Design Token & Contrast Linter.
Học hỏi từ: ui-ux-pro-max-skill (validate-tokens.cjs & WCAG 2.1 Contrast).
"""

import re
import math
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class LintIssue:
    line_number: int
    rule: str
    message: str
    matched_text: str


class TokenLinter:
    """Linter quét các vi phạm thẩm mỹ và token trong code giao diện."""

    HEX_COLOR_PATTERN = re.compile(r"#(?:[0-9a-fA-F]{3,4}){1,2}\b")
    HARDCODED_PX_PATTERN = re.compile(r"(?<![\w-])([1-9]\d{2,}|[5-9]\d)px\b")

    @classmethod
    def lint_file_content(cls, content: str, file_path: str = "") -> List[LintIssue]:
        issues: List[LintIssue] = []

        # Không quét chính file định nghĩa tokens
        if "tokens" in file_path.lower() or "colors" in file_path.lower():
            return issues

        for idx, line in enumerate(content.splitlines(), start=1):
            line_str = line.strip()
            if line_str.startswith("//") or line_str.startswith("#") or line_str.startswith("/*"):
                continue

            # 1. Bắt màu Hex hardcoded (Bắt buộc dùng CSS variable hoặc Tailwind class)
            for hex_match in cls.HEX_COLOR_PATTERN.finditer(line):
                issues.append(LintIssue(
                    line_number=idx,
                    rule="no_hardcoded_hex",
                    message="Hardcoded hex color vi phạm token system (hãy dùng CSS variable / Tailwind token)",
                    matched_text=hex_match.group(0)
                ))

            # 2. Bắt kích thước px lớn bất thường (trên 50px mà không dùng rem / clamp)
            for px_match in cls.HARDCODED_PX_PATTERN.finditer(line):
                issues.append(LintIssue(
                    line_number=idx,
                    rule="no_large_hardcoded_px",
                    message="Kích thước pixel cố định lớn gây vỡ responsive (hãy dùng rem hoặc clamp)",
                    matched_text=px_match.group(0)
                ))

        return issues

    @staticmethod
    def calculate_contrast(hex1: str, hex2: str) -> float:
        """Tính toán tỷ lệ tương phản màu WCAG 2.1 giữa 2 mã màu Hex."""
        def _get_luminance(hex_str: str) -> float:
            hex_str = hex_str.lstrip("#")
            if len(hex_str) == 3:
                hex_str = "".join([c * 2 for c in hex_str])
            r, g, b = [int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
            # Gamma correction
            rgb = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
            return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]

        try:
            l1 = _get_luminance(hex1)
            l2 = _get_luminance(hex2)
            lighter = max(l1, l2)
            darker = min(l1, l2)
            return round((lighter + 0.05) / (darker + 0.05), 2)
        except Exception:
            return 1.0

    @classmethod
    def is_wcag_aa_compliant(cls, hex_fg: str, hex_bg: str, is_large_text: bool = False) -> bool:
        """Kiểm tra độ tương phản có đạt chuẩn WCAG 2.1 AA không (Normal >= 4.5, Large >= 3.0)."""
        ratio = cls.calculate_contrast(hex_fg, hex_bg)
        min_ratio = 3.0 if is_large_text else 4.5
        return ratio >= min_ratio

    @classmethod
    def is_wcag_aaa_compliant(cls, hex_fg: str, hex_bg: str, is_large_text: bool = False) -> bool:
        """Kiểm tra độ tương phản có đạt chuẩn WCAG 2.1 AAA không (Normal >= 7.0, Large >= 4.5)."""
        ratio = cls.calculate_contrast(hex_fg, hex_bg)
        min_ratio = 4.5 if is_large_text else 7.0
        return ratio >= min_ratio

