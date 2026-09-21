"""
Structured Debt Parser.
Học hỏi từ: ponytail (Thu hoạch nợ kỹ thuật có cấu trúc: debt, ceiling, upgrade).
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class DebtItem:
    file_path: str
    line_number: int
    shortcut: str
    ceiling: str
    upgrade_path: str
    raw_comment: str


class DebtParser:
    """Máy quét phân tích cú pháp nợ kỹ thuật có cấu trúc."""

    # Nhận diện cả # debt:, // debt:, /* debt:, <!-- debt:
    DEBT_PATTERN = re.compile(
        r"(?:#|//|/\*|<!--)\s*debt:\s*(?P<shortcut>.*?)\s*,\s*ceiling:\s*(?P<ceiling>.*?)\s*,\s*upgrade:\s*(?P<upgrade>.*?)(?:\*/|-->|$)",
        re.IGNORECASE
    )

    @classmethod
    def parse_line(cls, line: str, file_path: str, line_number: int) -> Optional[DebtItem]:
        """Phân tích một dòng mã nguồn xem có chứa thẻ nợ kỹ thuật không."""
        match = cls.DEBT_PATTERN.search(line)
        if match:
            return DebtItem(
                file_path=file_path,
                line_number=line_number,
                shortcut=match.group("shortcut").strip(),
                ceiling=match.group("ceiling").strip(),
                upgrade_path=match.group("upgrade").strip(),
                raw_comment=line.strip()
            )
        return None

    @classmethod
    def scan_file(cls, file_path: Path) -> List[DebtItem]:
        """Quét một file văn bản."""
        items: List[DebtItem] = []
        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
            for idx, line in enumerate(content.splitlines(), start=1):
                item = cls.parse_line(line, str(file_path), idx)
                if item:
                    items.append(item)
        except Exception:
            pass
        return items

    @classmethod
    def scan_directory(cls, dir_path: Path, exclude_dirs: Optional[List[str]] = None) -> List[DebtItem]:
        """Quét đệ quy toàn bộ thư mục mã nguồn."""
        excludes = set(exclude_dirs or [".git", "node_modules", ".venv", "__pycache__", "dist", "build", "tests", "scripts"])
        items: List[DebtItem] = []

        for p in dir_path.rglob("*"):
            if p.is_file():
                # Bỏ qua thư mục loại trừ
                if any(part in excludes for part in p.parts):
                    continue
                # Bỏ qua file nhị phân lớn
                if p.suffix.lower() in [".png", ".jpg", ".jpeg", ".zip", ".tar", ".gz", ".exe", ".dll", ".so", ".bin"]:
                    continue
                items.extend(cls.scan_file(p))

        return items
