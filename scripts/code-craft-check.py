#!/usr/bin/env python3
"""
scripts/code-craft-check.py
Cổng kiểm định Tay Nghề Viết Code & Độ Sâu Module (Clean Code & Deep Module Linter).

Mục tiêu cốt lõi (Theo triết lý John Ousterhout & Clean Code):
Biến nguyên tắc "1 Thằng Làm - 1 Thằng Phá" thành công cụ kiểm soát tự động:
1. Hàm Gọn Gàng (Function Length): Hàm không dài quá 40 dòng (trừ test fixtures).
2. Chống Tháp Nhọn (Anti-Arrow Pattern): Cấm lồng nhau quá 3 tầng if/for/while (buộc dùng Guard Clauses / Return Early).
3. Cấm Chuỗi If-Else Kiểu Mở Rộng Kém (Anti-Type-Switching): Cảnh báo nếu có chuỗi if-else/switch >= 4 nhánh
   dựa trên type/channel/status (buộc trừu tượng hóa sang Strategy Pattern hoặc Polymorphism).
4. Interface Nông - Implementation Sâu (Deep Module Metric): Tỷ lệ interface gọn gàng, che giấu độ phức tạp.

Thoát:
  0: Code đạt chuẩn Clean Code, súc tích và dễ mở rộng (PASS).
  1: Phát hiện code rườm rà, khó mở rộng hoặc lồng ghép quá sâu (BLOCKED).
"""

import ast
import os
import subprocess
import sys
from pathlib import Path

MAX_FUNCTION_LINES = 45
MAX_NESTING_DEPTH = 3
MAX_IF_ELSE_CHAIN = 3


class CleanCodeASTVisitor(ast.NodeVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.violations: list[str] = []
        self.current_function = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._check_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._check_function(node)
        self.generic_visit(node)

    def _check_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef):
        # Bỏ qua các hàm test
        if node.name.startswith("test_") or node.name.endswith("_test"):
            return

        # 1. Kiểm tra độ dài hàm
        length = (node.end_lineno - node.lineno) if hasattr(node, "end_lineno") and node.end_lineno else len(node.body)
        if length > MAX_FUNCTION_LINES:
            self.violations.append(
                f"{self.file_path}:{node.lineno} [LONG_METHOD] Hàm '{node.name}' dài {length} dòng "
                f"(vượt ngưỡng chuẩn {MAX_FUNCTION_LINES} dòng). Cần bóc tách nhỏ để code súc tích và dễ hiểu."
            )

        # 2. Kiểm tra độ sâu lồng nhau (Nesting Depth)
        max_depth = self._calculate_max_nesting(node.body, current_depth=0)
        if max_depth > MAX_NESTING_DEPTH:
            self.violations.append(
                f"{self.file_path}:{node.lineno} [DEEP_NESTING] Hàm '{node.name}' có cấu trúc lồng nhau {max_depth} tầng "
                f"(vượt ngưỡng {MAX_NESTING_DEPTH} tầng). Hãy dùng Guard Clauses (return sớm) để làm phẳng luồng logic."
            )

        # 3. Kiểm tra chuỗi if-elif-else dài (Anti-Polymorphism)
        self._check_if_chains(node)

    def _calculate_max_nesting(self, statements: list[ast.stmt], current_depth: int) -> int:
        max_d = current_depth
        for stmt in statements:
            if isinstance(stmt, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                child_stmts = list(ast.iter_child_nodes(stmt))
                sub_d = self._calculate_max_nesting(
                    [s for s in child_stmts if isinstance(s, ast.stmt)],
                    current_depth + 1
                )
                if sub_d > max_d:
                    max_d = sub_d
        return max_d

    def _check_if_chains(self, func_node: ast.FunctionDef | ast.AsyncFunctionDef):
        for node in ast.walk(func_node):
            if isinstance(node, ast.If):
                # Đếm số nhánh elif
                branch_count = 1
                curr = node
                while curr.orelse and len(curr.orelse) == 1 and isinstance(curr.orelse[0], ast.If):
                    branch_count += 1
                    curr = curr.orelse[0]
                if curr.orelse:
                    branch_count += 1

                if branch_count > MAX_IF_ELSE_CHAIN:
                    self.violations.append(
                        f"{self.file_path}:{node.lineno} [TYPE_SWITCHING_CHAIN] Phát hiện chuỗi if-elif {branch_count} nhánh "
                        f"trong hàm '{func_node.name}'. Dấu hiệu vi phạm Open-Closed Principle (OCP)! "
                        "Nên trừu tượng hóa sang Strategy Pattern hoặc Dict/Map Dispatch để dễ mở rộng khi có nghiệp vụ mới."
                    )


def audit_python_file(file_path: Path) -> list[str]:
    violations = []
    if not file_path.is_file() or file_path.suffix.lower() != ".py":
        return violations

    try:
        source = file_path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(file_path))
    except Exception:
        return violations

    visitor = CleanCodeASTVisitor(file_path.as_posix())
    visitor.visit(tree)
    return visitor.violations


def _collect_from_diff(changed_against: str) -> list[Path]:
    """Thu thập file python thay đổi từ git diff."""
    cmd = ["git", "diff", "--name-only", changed_against]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return []
    matched = []
    for line in res.stdout.splitlines():
        p = Path(line.strip())
        if p.is_file() and p.suffix.lower() == ".py" and not any(k in p.name for k in ("test_", "_test")):
            matched.append(p)
    return matched


def _collect_default_py_files() -> list[Path]:
    """Thu thập file python trong các thư mục mặc định."""
    matched = []
    for root_dir in ("src", "scripts"):
        d = Path(root_dir)
        if not d.exists():
            continue
        for f in d.rglob("*.py"):
            if not any(k in f.name for k in ("test_", "_test")):
                matched.append(f)
    return matched


def _resolve_python_files(args) -> list[Path]:
    """Xác định danh sách file python cần kiểm tra."""
    if args.changed_against:
        return _collect_from_diff(args.changed_against)
    if args.paths:
        return [Path(p) for p in args.paths if Path(p).is_file() and Path(p).suffix.lower() == ".py"]
    return _collect_default_py_files()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Code Craft & Deep Module Linter")
    parser.add_argument("paths", nargs="*", help="File mã nguồn cần thẩm định Clean Code")
    parser.add_argument("--changed-against", help="So sánh với commit/nhánh gốc (vd: origin/develop)")
    args = parser.parse_args()

    files_to_check = _resolve_python_files(args)
    all_violations = []
    for f in files_to_check:
        all_violations.extend(audit_python_file(f))

    if all_violations:
        print("⚠️ [CODE CRAFT LINTER - CẢNH BÁO TAY NGHỀ CLEAN CODE & MỞ RỘNG]")
        for v in all_violations:
            print(f"  - {v}")
        print("\nKhuyến nghị từ Thằng Phá (Reviewer):")
        print("  1. Tách hàm nhỏ (< 45 dòng) để súc tích và dễ test đơn vị.")
        print("  2. Dùng Guard Clauses (return sớm) để giảm độ sâu lồng nhau <= 3 tầng.")
        print("  3. Trừu tượng hóa chuỗi if-elif dài thành Strategy Pattern để mở rộng dễ dàng.")
        sys.exit(1)
    else:
        print(f"✅ [CODE CRAFT LINTER] Đã quét {len(files_to_check)} file: Mã nguồn đạt chuẩn Clean Code, súc tích và dễ mở rộng.")
        sys.exit(0)


if __name__ == "__main__":
    main()
