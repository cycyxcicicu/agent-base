"""
Multi-format Document to Clean Markdown Converter.
Học hỏi từ: markitdown (Bóc tách dữ liệu có cấu trúc, bảng tính Excel OpenXML & JSON/CSV thành Markdown sạch).
"""

import csv
import json
import zipfile
import xml.etree.ElementTree as ET
from io import BytesIO
from pathlib import Path
from typing import Union, List, Dict, Any, Optional


class DocumentConverter:
    """Bộ chuyển đổi tài liệu đầu vào thành văn bản Markdown tối ưu cho LLM context."""

    @staticmethod
    def _escape_md_cell(val: Any) -> str:
        """Escape pipes and format newlines to maintain valid markdown table columns."""
        s = str(val) if val is not None else ""
        return s.replace("\r", "").replace("\n", "<br>").replace("|", "\\|")

    @staticmethod
    def _safe_parse_xml(xml_bytes: bytes) -> ET.Element:
        """Parse XML safely, blocking XXE entity expansion attacks."""
        if b"<!ENTITY" in xml_bytes:
            raise ValueError("Insecure XML: ENTITY declaration detected (XXE protection).")
        # Strip DOCTYPE if present without entities
        if b"<!DOCTYPE" in xml_bytes:
            import re
            xml_bytes = re.sub(rb"<!DOCTYPE[^>]*>", b"", xml_bytes)
        return ET.fromstring(xml_bytes)

    @classmethod
    def csv_to_markdown(cls, csv_content: str, delimiter: str = ",") -> str:
        """Chuyển đổi CSV / TSV thành bảng GitHub Flavored Markdown."""
        content = csv_content.strip()
        if not content:
            return ""

        import io
        reader = csv.reader(io.StringIO(content), delimiter=delimiter)
        rows = list(reader)
        if not rows:
            return ""

        header = [cls._escape_md_cell(c) for c in rows[0]]
        md_lines = [
            "| " + " | ".join(header) + " |",
            "| " + " | ".join(["---"] * len(header)) + " |"
        ]

        for row in rows[1:]:
            row_escaped = [cls._escape_md_cell(c) for c in row]
            row_padded = row_escaped + [""] * (len(header) - len(row_escaped))
            md_lines.append("| " + " | ".join(row_padded[:len(header)]) + " |")

        return "\n".join(md_lines)

    @classmethod
    def xlsx_to_markdown(cls, file_source: Union[str, Path, bytes, BytesIO]) -> str:
        """
        Bóc tách trực tiếp file Excel OpenXML (.xlsx) nhị phân thành bảng Markdown.
        Triển khai First Principles bằng zipfile và XML ElementTree chuẩn thư viện gốc Python,
        không phụ thuộc vào pandas hay openpyxl cồng kềnh.
        """
        if isinstance(file_source, (str, Path)):
            archive = zipfile.ZipFile(file_source, "r")
        elif isinstance(file_source, bytes):
            archive = zipfile.ZipFile(BytesIO(file_source), "r")
        else:
            archive = zipfile.ZipFile(file_source, "r")

        with archive:
            # 1. Đọc bảng xâu ký tự chia sẻ (sharedStrings.xml) nếu có
            shared_strings = []
            if "xl/sharedStrings.xml" in archive.namelist():
                tree = cls._safe_parse_xml(archive.read("xl/sharedStrings.xml"))
                # Namespace chuẩn spreadsheetml
                ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
                for si in tree.findall(".//s:si", ns) or tree.findall(".//si"):
                    text_parts = [t.text or "" for t in (si.findall(".//s:t", ns) or si.findall(".//t"))]
                    shared_strings.append("".join(text_parts))

            # 2. Tìm danh sách các sheet (sheet1.xml, ...)
            sheet_files = [f for f in archive.namelist() if f.startswith("xl/worksheets/sheet") and f.endswith(".xml")]
            if not sheet_files:
                return "*(File Excel không có dữ liệu sheet)*"

            output_sheets = []
            for sheet_file in sorted(sheet_files):
                sheet_tree = cls._safe_parse_xml(archive.read(sheet_file))
                ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
                rows = sheet_tree.findall(".//s:row", ns) or sheet_tree.findall(".//row")

                grid = []
                for row in rows:
                    cells = row.findall(".//s:c", ns) or row.findall(".//c")
                    row_data = []
                    for c in cells:
                        val_elem = c.find("s:v", ns) if c.find("s:v", ns) is not None else c.find("v")
                        cell_val = val_elem.text if val_elem is not None and val_elem.text else ""
                        # Nếu là shared string (t="s")
                        if c.get("t") == "s" and cell_val.isdigit():
                            idx = int(cell_val)
                            if 0 <= idx < len(shared_strings):
                                cell_val = shared_strings[idx]
                        row_data.append(cell_val)
                    if any(row_data):
                        grid.append(row_data)

                if grid:
                    sheet_name = Path(sheet_file).stem.capitalize()
                    header = [cls._escape_md_cell(c) for c in grid[0]]
                    md_lines = [
                        "| " + " | ".join(header) + " |",
                        "| " + " | ".join(["---"] * len(header)) + " |"
                    ]
                    for row in grid[1:]:
                        row_escaped = [cls._escape_md_cell(c) for c in row]
                        row_padded = row_escaped + [""] * (len(header) - len(row_escaped))
                        md_lines.append("| " + " | ".join(row_padded[:len(header)]) + " |")
                    md_table = "\n".join(md_lines)
                    output_sheets.append(f"### {sheet_name}\n\n{md_table}")

            return "\n\n".join(output_sheets)

    @staticmethod
    def json_to_markdown(data: Union[str, Dict, List]) -> str:
        """Chuyển đổi JSON thành Markdown có phân cấp rõ ràng."""
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception:
                return data

        if isinstance(data, list):
            if data and isinstance(data[0], dict):
                keys = list(data[0].keys())
                md_lines = [
                    "| " + " | ".join(keys) + " |",
                    "| " + " | ".join(["---"] * len(keys)) + " |"
                ]
                for item in data:
                    row = [str(item.get(k, "")) for k in keys]
                    md_lines.append("| " + " | ".join(row) + " |")
                return "\n".join(md_lines)
            else:
                return "\n".join([f"- {item}" for item in data])

        elif isinstance(data, dict):
            md_lines = []
            for k, v in data.items():
                if isinstance(v, (dict, list)):
                    md_lines.append(f"### {k}")
                    md_lines.append(f"```json\n{json.dumps(v, indent=2, ensure_ascii=False)}\n```")
                else:
                    md_lines.append(f"- **{k}**: {v}")
            return "\n".join(md_lines)

        return str(data)

    @classmethod
    def convert_file(cls, file_path: Union[str, Path]) -> str:
        """Tự động nhận diện định dạng file và chuyển đổi sang Markdown sạch."""
        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(f"Không tìm thấy file: {p}")

        ext = p.suffix.lower()
        if ext == ".xlsx":
            return cls.xlsx_to_markdown(p)
        elif ext in [".csv"]:
            return cls.csv_to_markdown(p.read_text(encoding="utf-8", errors="replace"))
        elif ext in [".tsv"]:
            return cls.csv_to_markdown(p.read_text(encoding="utf-8", errors="replace"), delimiter="\t")
        elif ext in [".json"]:
            return cls.json_to_markdown(p.read_text(encoding="utf-8", errors="replace"))
        elif ext in [".md", ".txt"]:
            return p.read_text(encoding="utf-8", errors="replace")
        else:
            return p.read_text(encoding="utf-8", errors="replace")
