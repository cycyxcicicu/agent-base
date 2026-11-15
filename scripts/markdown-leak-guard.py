#!/usr/bin/env python3
"""
scripts/markdown-leak-guard.py
Cổng kiểm soát Rò Rỉ Dữ Liệu Qua Thẻ Ảnh Markdown & Kênh Ngầm (Markdown Exfiltration Guard).

Mục tiêu cốt lõi:
Ngăn chặn kỹ thuật tấn công Indirect Prompt Injection kết hợp Markdown Image Exfiltration:
Kẻ tấn công lừa Agent định dạng dữ liệu nhạy cảm (token, secret) vào query parameters của thẻ ảnh.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

MD_IMAGE_PATTERN = re.compile(r"!\[(.*?)\]\((https?://[^\)]+)\)", re.IGNORECASE)
HTML_IMAGE_PATTERN = re.compile(r"<img\s+[^>]*src=[\"'](https?://[^\"']+)[\"']", re.IGNORECASE)

SENSITIVE_PARAM_KEYWORDS = {
    "token", "secret", "key", "auth", "password", "jwt", "bearer",
    "apikey", "credential", "data", "leak", "exfil", "payload", "cookie"
}


def _check_url_query_leak(file_path: Path, line_no: int, url_str: str, tag_type: str) -> list[str]:
    """Kiểm tra tham số query trong URL ảnh xem có chứa kênh rò rỉ dữ liệu không."""
    violations: list[str] = []
    parsed = urlparse(url_str)
    qs = parse_qs(parsed.query)

    for param_key, param_vals in qs.items():
        pk_low = param_key.lower()
        if pk_low in SENSITIVE_PARAM_KEYWORDS or any(kw in pk_low for kw in SENSITIVE_PARAM_KEYWORDS):
            violations.append(
                f"{file_path}:{line_no} [{tag_type}_EXFILTRATION] "
                f"Phát hiện thẻ ảnh nhúng tham số nhạy cảm nghi vấn: '{url_str}'."
            )
        elif any(len(v) > 32 for v in param_vals):
            violations.append(
                f"{file_path}:{line_no} [SUSPICIOUS_IMAGE_PAYLOAD] "
                f"Phát hiện tham số ảnh có độ dài bất thường (>32 ký tự): '{url_str}'."
            )
    return violations


def _scan_line_for_images(file_path: Path, line_no: int, line: str) -> list[str]:
    """Quét các thẻ ảnh trong một dòng văn bản Markdown."""
    violations: list[str] = []
    for match in MD_IMAGE_PATTERN.finditer(line):
        violations.extend(_check_url_query_leak(file_path, line_no, match.group(2), "MARKDOWN_IMAGE"))

    for match in HTML_IMAGE_PATTERN.finditer(line):
        violations.extend(_check_url_query_leak(file_path, line_no, match.group(1), "HTML_IMG"))

    return violations


def audit_markdown_file(file_path: Path) -> list[str]:
    """Kiểm tra an toàn file tài liệu Markdown."""
    if not file_path.is_file() or "docs/research" in file_path.as_posix():
        return []

    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []

    violations: list[str] = []
    in_code_block = False

    for line_no, line in enumerate(content.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        violations.extend(_scan_line_for_images(file_path, line_no, line))

    return violations


def _collect_from_diff(changed_against: str) -> list[Path]:
    """Thu thập file markdown thay đổi từ git diff."""
    cmd = ["git", "diff", "--name-only", changed_against]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return []
    return [Path(l.strip()) for l in res.stdout.splitlines() if Path(l.strip()).is_file() and l.endswith(".md")]


def _collect_from_paths(paths: list[str]) -> list[Path]:
    """Thu thập file markdown từ danh sách đường dẫn truyền vào."""
    matched: list[Path] = []
    for p_str in paths:
        p = Path(p_str)
        if p.is_file() and p.suffix.lower() == ".md":
            matched.append(p)
        elif p.is_dir():
            matched.extend(f for f in p.rglob("*.md") if f.is_file())
    return matched


def _collect_from_default_dirs() -> list[Path]:
    """Thu thập file markdown từ các thư mục tài liệu mặc định."""
    results: list[Path] = []
    for d_name in ("doc", "docs", "tasks"):
        d = Path(d_name)
        if not d.exists():
            continue
        results.extend(f for f in d.rglob("*.md") if f.is_file())
    return results


def _resolve_markdown_files(args: argparse.Namespace) -> list[Path]:
    """Xác định danh sách file Markdown cần kiểm tra."""
    if args.changed_against:
        return _collect_from_diff(args.changed_against)
    if args.paths:
        return _collect_from_paths(args.paths)
    return _collect_from_default_dirs()


def main() -> None:
    parser = argparse.ArgumentParser(description="Markdown Image Exfiltration Guard")
    parser.add_argument("paths", nargs="*", help="File hoặc thư mục markdown cần quét")
    parser.add_argument("--changed-against", help="So sánh với commit/nhánh gốc (vd: origin/develop)")
    args = parser.parse_args()

    files = _resolve_markdown_files(args)
    all_violations: list[str] = []
    for f in files:
        all_violations.extend(audit_markdown_file(f))

    if not all_violations:
        print(f"✅ [MARKDOWN LEAK GUARD] Đã quét {len(files)} file Markdown: 100% an toàn.")
        sys.exit(0)

    print("❌ [MARKDOWN LEAK GUARD - PHÁT HIỆN KÊNH RÒ RỈ DỮ LIỆU]")
    for v in all_violations:
        print(f"  - {v}")
    print("\nCảnh báo: Phát hiện thẻ ảnh Markdown nhúng tham số ngoài máy trạm có thể tuồn dữ liệu bí mật.")
    sys.exit(1)


if __name__ == "__main__":
    main()
