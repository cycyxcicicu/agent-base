#!/usr/bin/env python3
"""
scripts/trojan-check.py
Cổng kiểm soát Ký Tự Vô Hình & Mã Độc Tàng Hình (Trojan Source & Invisible Smuggling Gate).

Mục tiêu cốt lõi:
1. Trojan Source (CVE-2021-42574): Ký tự điều khiển Unicode BiDi đảo ngược hướng đọc.
2. Zero-Width Spaces & Invisible Separators: Ký tự tàng hình (U+200B, U+200C, U+200D, U+FEFF).
3. Unicode Language Tags (U+E0000 - U+E007F): Mã hóa prompt injection tàng hình.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Danh sách mã Unicode BiDi điều hướng văn bản nguy hiểm (Trojan Source CVE-2021-42574)
BIDI_CHARS = {
    0x202A: "LRE (Left-to-Right Embedding)",
    0x202B: "RLE (Right-to-Left Embedding)",
    0x202D: "LRO (Left-to-Right Override)",
    0x202E: "RLO (Right-to-Left Override)",
    0x202C: "PDF (Pop Directional Formatting)",
    0x2066: "LRI (Left-to-Right Isolate)",
    0x2067: "RLI (Right-to-Left Isolate)",
    0x2068: "FSI (First Strong Isolate)",
    0x2069: "Pop Directional Isolate",
}

# Danh sách ký tự vô hình (Zero-Width & Invisible Characters)
ZERO_WIDTH_CHARS = {
    0x200B: "Zero-Width Space",
    0x200C: "Zero-Width Non-Joiner",
    0x200D: "Zero-Width Joiner",
    0x2060: "Word Joiner",
    0xFEFF: "Zero-Width No-Break Space",
    0x00AD: "Soft Hyphen",
    0x180E: "Mongolian Vowel Separator",
}

UNICODE_TAGS_RANGE = (0xE0000, 0xE007F)

CODE_EXTENSIONS = {
    ".py", ".java", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".kt",
    ".swift", ".c", ".cpp", ".h", ".cs", ".php", ".sh", ".sql", ".json", ".yml", ".yaml"
}


def _check_char_violation(file_path: Path, line_idx: int, col_idx: int, cp: int) -> str | None:
    """Kiểm tra mã codepoint đơn lẻ và trả về thông báo vi phạm nếu có."""
    if cp in BIDI_CHARS:
        desc = BIDI_CHARS[cp]
        return (
            f"{file_path}:{line_idx}:{col_idx} [TROJAN_SOURCE / CVE-2021-42574] "
            f"Ký tự BiDi độc hại U+{cp:04X} ({desc}) bị chặn cứng!"
        )

    if cp in ZERO_WIDTH_CHARS:
        desc = ZERO_WIDTH_CHARS[cp]
        return (
            f"{file_path}:{line_idx}:{col_idx} [INVISIBLE_CHARACTER] "
            f"Ký tự vô hình U+{cp:04X} ({desc}) bị chặn cứng!"
        )

    if UNICODE_TAGS_RANGE[0] <= cp <= UNICODE_TAGS_RANGE[1]:
        hidden_ascii = chr(cp - 0xE0000) if 0xE0020 <= cp <= 0xE007E else "?"
        return (
            f"{file_path}:{line_idx}:{col_idx} [UNICODE_LANGUAGE_TAG_INJECTION] "
            f"Ký tự tàng hình Tags Block U+{cp:04X} (ẩn ký tự '{hidden_ascii}') bị chặn cứng!"
        )

    return None


def scan_file_for_trojans(file_path: Path) -> list[str]:
    """Quét từng ký tự trong file để phát hiện BiDi và Zero-Width injection."""
    if not file_path.is_file():
        return []

    try:
        raw_bytes = file_path.read_bytes()
        if raw_bytes.startswith(b"\xef\xbb\xbf"):
            raw_bytes = raw_bytes[3:]
        text = raw_bytes.decode("utf-8", errors="replace")
    except Exception:
        return []

    violations: list[str] = []
    for line_idx, line in enumerate(text.splitlines(), 1):
        for col_idx, ch in enumerate(line, 1):
            err = _check_char_violation(file_path, line_idx, col_idx, ord(ch))
            if err:
                violations.append(err)

    return violations


def _collect_from_diff(changed_against: str) -> list[Path]:
    """Lấy danh sách file thay đổi từ git diff."""
    cmd = ["git", "diff", "--name-only", changed_against]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return []
    matched = []
    for line in res.stdout.splitlines():
        p = Path(line.strip())
        if p.is_file() and p.suffix.lower() in CODE_EXTENSIONS:
            matched.append(p)
    return matched


def _collect_from_paths(paths: list[str]) -> list[Path]:
    """Lấy danh sách file từ danh sách tham số đường dẫn."""
    matched = []
    for p_str in paths:
        p = Path(p_str)
        if p.is_file() and p.suffix.lower() in CODE_EXTENSIONS:
            matched.append(p)
        elif p.is_dir():
            matched.extend(f for f in p.rglob("*") if f.is_file() and f.suffix.lower() in CODE_EXTENSIONS)
    return matched


def _resolve_target_files(args: argparse.Namespace) -> list[Path]:
    """Xác định danh sách file mã nguồn cần quét."""
    if args.changed_against:
        return _collect_from_diff(args.changed_against)
    if args.paths:
        return _collect_from_paths(args.paths)

    results = []
    for dir_name in ("src", "scripts", "agents"):
        d = Path(dir_name)
        if d.exists():
            results.extend(f for f in d.rglob("*") if f.is_file() and f.suffix.lower() in CODE_EXTENSIONS)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Trojan Source & Invisible Smuggling Scanner")
    parser.add_argument("paths", nargs="*", help="File hoặc thư mục cần quét")
    parser.add_argument("--changed-against", help="Chỉ quét file thay đổi so với Git ref (vd: origin/develop)")
    args = parser.parse_args()

    files = _resolve_target_files(args)
    all_violations: list[str] = []
    for f in files:
        all_violations.extend(scan_file_for_trojans(f))

    if not all_violations:
        print(f"✅ [TROJAN SOURCE GATE] Đã quét {len(files)} file: 100% sạch, không chứa ký tự tàng hình.")
        sys.exit(0)

    print("❌ [TROJAN SOURCE GATE - PHÁT HIỆN MÃ ĐỘC TÀNG HÌNH]")
    for v in all_violations:
        print(f"  - {v}")
    print("\nCảnh báo: Phát hiện ký tự BiDi (CVE-2021-42574) hoặc ký tự vô hình có thể đánh lừa người review.")
    sys.exit(1)


if __name__ == "__main__":
    main()
