#!/usr/bin/env python3
"""
scripts/safe-search.py
Công cụ tìm kiếm chuỗi văn bản thuần (Text Literal / i18n / Nhãn UI tiếng Việt).

Dành riêng cho các trường hợp MCP AST (xerj, graphify) không hỗ trợ:
- Tìm nhãn giao diện tiếng Việt (e.g. "Đang ẩn", "Xóa bộ lọc")
- Tìm mã lỗi dạng text (e.g. "ORDER-4027")
- Tìm khóa i18n trong file JSON / TSX / Properties

Bảo vệ Context Window tuyệt đối:
- Tự động giới hạn tối đa 10 kết quả (chống tràn context).
- Bỏ qua tự động thư mục rác (node_modules, target, dist, .git, build).
- Đầu ra chuẩn mực để Agent dùng tiếp công cụ bản địa `read_file`.
"""
import sys
import os
import argparse
import unicodedata
from pathlib import Path

IGNORED_DIRS = {
    "node_modules", "target", "dist", ".git", ".idea",
    ".vscode", "build", "coverage", ".next", "out",
    "vendor", ".gradle", "bin", "obj", "tmp"
}

DEFAULT_EXTS = {
    ".ts", ".tsx", ".js", ".jsx", ".java", ".py",
    ".json", ".html", ".vue", ".properties", ".sql", ".xml",
    ".md", ".txt", ".yaml", ".yml", ".adoc", ".sh"
}


def _normalize_exts(raw_ext: str | None) -> set[str]:
    if not raw_ext:
        return DEFAULT_EXTS
    exts = set()
    for part in raw_ext.split(","):
        cleaned = part.strip().lower()
        if cleaned:
            exts.add(cleaned if cleaned.startswith(".") else f".{cleaned}")
    return exts


def search_text(query: str, root_dir: Path, exts: set[str], limit: int = 10):
    if not root_dir.exists():
        print(f"LỖI: Thư mục không tồn tại: {root_dir}")
        return 1

    query_lower = unicodedata.normalize("NFC", query).lower()
    query_is_ascii = query_lower.isascii()
    matches = []

    def _scan_file(file_path: Path, display_path: str):
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as fp:
                for line_num, line in enumerate(fp, 1):
                    haystack = line.lower() if (query_is_ascii and line.isascii()) else unicodedata.normalize("NFC", line).lower()
                    if query_lower in haystack:
                        matches.append((display_path, line_num, line.strip()))
                        if len(matches) >= limit:
                            return True
        except Exception:
            pass
        return False

    if root_dir.is_file():
        _scan_file(root_dir, root_dir.name)
    else:
        for root, dirs, files in os.walk(root_dir):
            # Lọc bỏ các thư mục rác ngay từ walk và ưu tiên quét tài liệu hiện hành trước archive/
            dirs[:] = sorted(
                (d for d in dirs if d not in IGNORED_DIRS and not d.startswith(".")),
                key=lambda d: (1 if d.lower() in {"archive", "legacy"} else 0, d.lower()),
            )

            for f in sorted(files, key=str.lower):
                ext = os.path.splitext(f)[1].lower()
                if exts and ext not in exts:
                    continue

                file_path = Path(root) / f
                rel_path = file_path.relative_to(root_dir) if root_dir != Path(".") else file_path
                if _scan_file(file_path, str(rel_path)):
                    break

            if len(matches) >= limit:
                break

    print(f"🔍 Kết quả tìm kiếm cho: \"{query}\" (Giới hạn tối đa: {limit} dòng)")
    print("-" * 70)
    if not matches:
        print("Không tìm thấy kết quả nào phù hợp.")
        return 0

    for path, line_num, text in matches:
        # Cắt ngắn dòng quá dài để tránh vỡ định dạng
        clean_text = text if len(text) <= 120 else text[:117] + "..."
        print(f"{path}:{line_num}: {clean_text}")

    print("-" * 70)
    print("💡 [HƯỚNG DẪN AGENT]: Hãy dùng công cụ 'read_file' với phạm vi dòng cụ thể để xem chi tiết.")
    return 0

def main():
    parser = argparse.ArgumentParser(description="Tìm kiếm chuỗi văn bản thuần an toàn (chống tràn context).")
    parser.add_argument("-q", "--query", required=True, help="Chuỗi văn bản cần tìm")
    parser.add_argument("-d", "--dir", default=".", help="Thư mục bắt đầu tìm (mặc định: .)")
    parser.add_argument("-e", "--ext", help="Danh sách đuôi mở rộng, cách nhau bởi dấu phẩy (vd: .tsx,.ts)")
    parser.add_argument("-l", "--limit", type=int, default=10, help="Số dòng kết quả tối đa (mặc định: 10, max: 20)")

    args = parser.parse_args()

    limit = min(max(1, args.limit), 20)
    exts = _normalize_exts(args.ext)
    root_dir = Path(os.path.expanduser(args.dir)).resolve()

    return search_text(args.query, root_dir, exts, limit)

if __name__ == "__main__":
    sys.exit(main())

