#!/usr/bin/env python3
"""
scripts/test-integrity-check.py
Cổng kiểm định Độ Toàn Vẹn Kiểm Thử & Chống Gian Lận (Test Integrity & Anti-Gaming Gate).

Mục tiêu cốt lõi:
1. Test Dilution / Tampering: Âm thầm xóa bỏ hoặc giảm số lượng assertions trong bài test cũ.
2. Vacuous / Trivial Asserts: Chèn assert vô nghĩa (assert True) để kéo test xanh giả tạo.
3. Skip Annotations: Đánh dấu skip/Disabled lên test case để trốn kiểm thử.
4. Empty Test Bodies: Khai báo hàm test rỗng không có logic kiểm tra thực chất.
"""

import argparse
import ast
import os
import re
import subprocess
import sys
from pathlib import Path

TRIVIAL_ASSERT_PATTERNS = [
    re.compile(r"^\s*assert\s+(True|1\s*==\s*1|True\s*==\s*True)\s*(?:,.*)?$", re.I),
    re.compile(r"^\s*(?:self\.)?assertTrue\s*\(\s*(?:true|1\s*==\s*1)\s*\)\s*;?$", re.I),
    re.compile(r"^\s*(?:self\.)?assertFalse\s*\(\s*(?:false)\s*\)\s*;?$", re.I),
    re.compile(r"^\s*(?:self\.)?assertEquals?\s*\(\s*([a-zA-Z0-9_]+)\s*,\s*\1\s*\)\s*;?$", re.I),
    re.compile(r"^\s*expect\s*\(\s*true\s*\)\s*\.to(?:Be|Equal)\s*\(\s*true\s*\)\s*;?$", re.I),
]

SKIP_ANNOTATIONS_PATTERNS = [
    re.compile(r"@(?:unittest\.)?skip\b"),
    re.compile(r"@pytest\.mark\.skip\b"),
    re.compile(r"@Disabled\b"),
    re.compile(r"@Ignore\b"),
    re.compile(r"\b(?:it|test|describe)\.skip\s*\("),
    re.compile(r"\bxit\s*\("),
    re.compile(r"\bxdescribe\s*\("),
]

ASSERT_KEYWORDS = [
    "assert ", "assert\t", "self.assert", "assertTrue", "assertFalse", "assertEqual",
    "assertEquals", "assertNotEqual", "assertIn", "assertNotIn", "assertIsNone",
    "assertIsNotNone", "assertRaises", "assertThat", "expect(", "should.", "assert_that"
]

VALID_CODE_EXTS = {".py", ".java", ".ts", ".js", ".kt", ".go", ".rs", ".cs"}
META_TEST_FIXTURE_FILES = {"test_adversarial_defense.py", "test_task_gate.py"}


def count_assertions_in_text(content: str) -> int:
    """Đếm số lượng câu lệnh kiểm chứng thực chất trong mã nguồn test."""
    count = 0
    for line in content.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", "//", "/*", "*")):
            continue
        if any(pat.search(s) for pat in TRIVIAL_ASSERT_PATTERNS):
            continue
        if any(kw in s for kw in ASSERT_KEYWORDS):
            count += 1
    return count


def _inspect_func_node(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    """Kiểm tra từng hàm test xem có rỗng hoặc chứa assert True không."""
    if not (node.name.startswith("test_") or node.name.endswith("_test")):
        return []

    issues: list[str] = []
    stmts = [
        s for s in node.body
        if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value, str))
    ]
    if not stmts or (len(stmts) == 1 and isinstance(stmts[0], ast.Pass)):
        issues.append(f"Hàm test '{node.name}' có thân rỗng mà không có assertion!")

    for s in node.body:
        if isinstance(s, ast.Assert) and isinstance(s.test, ast.Constant) and s.test.value is True:
            issues.append(f"Hàm test '{node.name}' chứa lệnh assert True vô nghĩa!")
    return issues


def inspect_python_test_ast(code: str) -> list[str]:
    """Phân tích AST Python để tìm hàm test rỗng hoặc assert vô nghĩa."""
    try:
        tree = ast.parse(code)
    except Exception:
        return []

    issues: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            issues.extend(_inspect_func_node(node))
    return issues


def _check_text_patterns(file_path: Path, content: str) -> list[str]:
    """Quét các dòng mã nguồn tìm trivial asserts và skip annotations."""
    violations: list[str] = []
    for line_no, line in enumerate(content.splitlines(), 1):
        s = line.strip()
        if not s or s.startswith(("#", "//", "/*", "*", '"""', "'''")):
            continue
        if s.startswith(('"', "'")) and s.endswith(('"', "'")):
            continue

        for pat in TRIVIAL_ASSERT_PATTERNS:
            if pat.search(s):
                violations.append(f"{file_path}:{line_no} [TRIVIAL_ASSERT] Assert vô nghĩa: '{s}'.")

        for pat in SKIP_ANNOTATIONS_PATTERNS:
            if pat.search(s):
                violations.append(f"{file_path}:{line_no} [TEST_SKIP_GAMING] Tag trốn test: '{s}'.")
    return violations


def _check_test_dilution(file_path: Path, new_content: str, base_ref: str) -> list[str]:
    """Kiểm tra xem số assertion có bị giảm so với bản gốc trong git không."""
    try:
        rel_path = file_path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        rel_path = file_path.name

    proc = subprocess.run(["git", "show", f"{base_ref}:{rel_path}"], capture_output=True, text=True)
    if proc.returncode != 0:
        return []

    old_count = count_assertions_in_text(proc.stdout)
    new_count = count_assertions_in_text(new_content)
    if new_count < old_count:
        return [
            f"{file_path} [TEST_DILUTION] Số lượng assertion bị suy giảm ({old_count} -> {new_count}). "
            "Nghiêm cấm xóa bớt assertion trong bài test cũ để ép test xanh!"
        ]
    return []


def scan_file_integrity(file_path: Path, base_ref: str | None = None) -> list[str]:
    """Kiểm tra độ toàn vẹn của một file test."""
    if not file_path.is_file():
        return []

    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []

    violations = _check_text_patterns(file_path, content)
    if file_path.suffix == ".py":
        violations.extend(f"{file_path} [EMPTY_TEST] {issue}" for issue in inspect_python_test_ast(content))
    if base_ref:
        violations.extend(_check_test_dilution(file_path, content, base_ref))
    return violations


def _is_valid_test_file(p: Path) -> bool:
    """Xác định file có phải là file kiểm thử hợp lệ không."""
    if "__pycache__" in str(p) or p.suffix.lower() not in VALID_CODE_EXTS:
        return False
    if p.name in META_TEST_FIXTURE_FILES:
        return False
    return any(k in p.name.lower() for k in ("test", "spec"))


def _resolve_test_files(args: argparse.Namespace) -> list[Path]:
    """Xác định danh sách file test cần kiểm tra."""
    if args.changed_against:
        cmd = ["git", "diff", "--name-only", args.changed_against]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            return []
        return [Path(l.strip()) for l in res.stdout.splitlines() if Path(l.strip()).is_file() and _is_valid_test_file(Path(l.strip()))]

    if args.paths:
        return [Path(p) for p in args.paths if Path(p).is_file() and _is_valid_test_file(Path(p))]

    results: list[Path] = []
    for r_dir in ("tests", "src"):
        r = Path(r_dir)
        if r.exists():
            results.extend(f for f in r.rglob("*") if f.is_file() and _is_valid_test_file(f))
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Test Integrity & Anti-Gaming Gate")
    parser.add_argument("paths", nargs="*", help="Đường dẫn các file test cần kiểm tra")
    parser.add_argument("--changed-against", help="So sánh với commit/nhánh gốc (vd: origin/develop)")
    args = parser.parse_args()

    files = _resolve_test_files(args)
    all_violations: list[str] = []
    for f in files:
        all_violations.extend(scan_file_integrity(f, base_ref=args.changed_against))

    if not all_violations:
        print(f"✅ [TEST INTEGRITY GATE] Đã quét {len(files)} file test: 100% toàn vẹn và thực chất.")
        sys.exit(0)

    print("❌ [TEST INTEGRITY GATE - PHÁT HIỆN GIAN LẬN BÀI TEST]")
    for v in all_violations:
        print(f"  - {v}")
    print("\nQuy tắc AGENTS.md nghiêm cấm hạ thấp tiêu chuẩn kiểm thử để làm đẹp kết quả.")
    sys.exit(1)


if __name__ == "__main__":
    main()
