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

    # Chỉ quét file mã nguồn/cấu hình có cú pháp comment được parser hỗ trợ.
    SOURCE_SUFFIXES = {
        ".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
        ".sh", ".ps1", ".html", ".go", ".rs", ".java", ".kt",
        ".cs", ".rb", ".php", ".sql", ".yml", ".yaml", ".toml",
        ".ini", ".cfg",
    }
    SOURCE_FILENAMES = {"makefile", "dockerfile", "containerfile", "jenkinsfile"}

    GENERATED_DIRS = {
        ".git", ".kilo", ".agents", ".claude", ".codex", ".gemini",
        ".idea", ".vscode", ".venv", "node_modules", "dist", "build",
        "__pycache__", "docs", "tasks", "tests", "scripts",
    }

    # Nhận diện cả # debt:, // debt:, /* debt:, <!-- debt:, -- debt:, ; debt:
    DEBT_PATTERN = re.compile(
        r"(?:#|//|/\*|<!--|--|;)\s*debt:\s*(?P<shortcut>.*?)\s*,\s*ceiling:\s*(?P<ceiling>.*?)\s*,\s*upgrade:\s*(?P<upgrade>.*?)(?:\*/|-->|$)",
        re.IGNORECASE
    )

    # Thẻ dị dạng chỉ nhận khi bắt đầu dòng comment, tránh khớp câu văn mô tả cú pháp.
    GENERIC_DEBT_PATTERN = re.compile(
        r"^\s*(?:#|//|/\*|<!--|--|;)\s*debt:\s*(?P<content>.*?)(?:\*/|-->|$)",
        re.IGNORECASE
    )

    @classmethod
    def is_source_file(cls, file_path: Path) -> bool:
        name = file_path.name.lower()
        return (
            file_path.suffix.lower() in cls.SOURCE_SUFFIXES
            or any(name == base or name.startswith(f"{base}.") for base in cls.SOURCE_FILENAMES)
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

        # Phát hiện thẻ nợ dị dạng thiếu trường (malformed debt tags)
        gen_match = cls.GENERIC_DEBT_PATTERN.search(line)
        if gen_match:
            raw_text = gen_match.group("content").strip()
            return DebtItem(
                file_path=file_path,
                line_number=line_number,
                shortcut=raw_text or "[EMPTY SHORTCUT]",
                ceiling="[MALFORMED: THIẾU CEILING]",
                upgrade_path="[MALFORMED: THIẾU UPGRADE]",
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
        """Quét đệ quy mã nguồn; bỏ qua tài liệu, adapter sinh tự động và build output.

        GENERATED_DIRS luôn được áp dụng; exclude_dirs chỉ bổ sung thêm, không thay thế.
        Chỉ xét các thành phần bên trong dir_path để tên thư mục cha không làm rỗng kết quả.
        """
        excludes = cls.GENERATED_DIRS | set(exclude_dirs or [])
        items: List[DebtItem] = []

        for p in dir_path.rglob("*"):
            if not p.is_file():
                continue
            try:
                rel_parents = p.relative_to(dir_path).parts[:-1]
            except ValueError:
                rel_parents = p.parts[:-1]
            if any(part in excludes for part in rel_parents):
                continue
            if not cls.is_source_file(p):
                continue
            items.extend(cls.scan_file(p))

        return items
