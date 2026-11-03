#!/usr/bin/env python3
"""
CLI Tool for Alibaba Open-Code-Review (OCR).
Cung cấp giao diện dòng lệnh cho Agent và Lập trình viên chạy Code Review độc lập,
hỗ trợ cả Chế độ Ủy thác (Delegation Mode) và Chế độ Kiểm định Tĩnh (Deterministic Static Scan).
Không cần cài đặt npm hay Go, chạy offline 100% trên mọi hệ điều hành.

Sử dụng:
    python scripts/ocr.py preview [paths...]
    python scripts/ocr.py rule [paths...]
    python scripts/ocr.py check <paths...>
    python scripts/ocr.py review [--from <ref>] [--to <ref>] [--commit <hash>]
"""

import argparse
import json
import os
import subprocess
import sys

# Đảm bảo xuất UTF-8 an toàn trên Windows console
if sys.platform == "win32":
    import io
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "buffer"):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Thêm thư mục gốc vào PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from agent_core.eval.code_reviewer import (
    CodeReviewer,
    ReviewComment,
    ReviewRuleResolver,
    FileExclusionFilter,
)


def get_git_changed_files(from_ref=None, to_ref=None, commit=None) -> list:
    """Lấy danh sách tệp thay đổi từ git."""
    try:
        if commit:
            cmd = ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit]
        elif from_ref and to_ref:
            cmd = ["git", "diff", "--name-only", f"{from_ref}...{to_ref}"]
        else:
            # Mặc định: staged, unstaged, và untracked files
            cmd_staged = ["git", "diff", "--name-only", "--cached"]
            cmd_unstaged = ["git", "diff", "--name-only"]
            cmd_untracked = ["git", "ls-files", "--others", "--exclude-standard"]

            files = set()
            for c in [cmd_staged, cmd_unstaged, cmd_untracked]:
                out = subprocess.check_output(c, stderr=subprocess.DEVNULL).decode("utf-8")
                for line in out.splitlines():
                    if line.strip():
                        files.add(line.strip())
            return sorted(list(files))

        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode("utf-8")
        return [line.strip() for line in out.splitlines() if line.strip()]
    except Exception:
        return []


def cmd_preview(args):
    files = args.paths
    if not files:
        files = get_git_changed_files(args.from_ref, args.to_ref, args.commit)

    reviewer = CodeReviewer()
    result = reviewer.preview(files)

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"=== Alibaba OCR Preview ===")
        print(f"Tổng số tệp: {result['total_files']}")
        print(f"Tệp cần review ({result['reviewable_count']}):")
        for f in result["reviewable_files"]:
            print(f"  [+] {f['path']}")
        print(f"Tệp bị loại trừ ({result['excluded_count']}):")
        for f in result["excluded_files"]:
            print(f"  [-] {f['path']} ({f['exclude_reason']})")


def cmd_rule(args):
    files = args.paths
    if not files:
        files = get_git_changed_files(args.from_ref, args.to_ref, args.commit)

    reviewer = CodeReviewer()
    preview = reviewer.preview(files)
    reviewable = [f["path"] for f in preview["reviewable_files"]]
    groups = reviewer.group_rules(reviewable)

    if args.format == "json":
        output = []
        for idx, (rule_file, file_list) in enumerate(groups.items(), start=1):
            output.append({
                "group_id": idx,
                "rule_doc": rule_file,
                "files": file_list,
            })
        print(json.dumps({"groups": output}, indent=2, ensure_ascii=False))
    else:
        print("=== Alibaba OCR Rule Mapping ===")
        for rule_file, file_list in groups.items():
            print(f"\n[Luật: {rule_file}]")
            for f in file_list:
                print(f"  - {f}")


def cmd_check(args):
    files = args.paths
    if not files:
        files = get_git_changed_files(args.from_ref, args.to_ref, args.commit)

    reviewer = CodeReviewer()
    preview = reviewer.preview(files)
    reviewable = [f["path"] for f in preview["reviewable_files"]]

    all_comments = []
    for path in reviewable:
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                comments = reviewer.analyze_source(path, content)
                all_comments.extend(comments)
            except Exception as e:
                print(f"Lỗi khi đọc file {path}: {e}", file=sys.stderr)

    if args.format == "json":
        print(json.dumps([c.to_dict() for c in all_comments], indent=2, ensure_ascii=False))
    else:
        report = reviewer.generate_report(all_comments, total_files=len(reviewable))
        print(report)

    # Nếu có lỗi critical/high -> exit code 1
    has_blocking = any(c.severity in ("critical", "high") for c in all_comments)
    sys.exit(1 if has_blocking else 0)


def cmd_review(args):
    cmd_check(args)


def main():
    parser = argparse.ArgumentParser(description="Alibaba Open-Code-Review CLI")
    subparsers = parser.add_subparsers(dest="command", help="Lệnh thực thi")

    # Preview sub-command
    p_prev = subparsers.add_parser("preview", help="Xem trước danh sách tệp được review và tệp bị loại trừ")
    p_prev.add_argument("paths", nargs="*", help="Danh sách tệp chỉ định")
    p_prev.add_argument("--from", dest="from_ref", help="Git from ref")
    p_prev.add_argument("--to", dest="to_ref", help="Git to ref")
    p_prev.add_argument("-c", "--commit", dest="commit", help="Commit hash")
    p_prev.add_argument("-f", "--format", choices=["text", "json"], default="text", help="Định dạng xuất")

    # Rule sub-command
    p_rule = subparsers.add_parser("rule", help="Ánh xạ và gom nhóm tệp theo bộ luật ngôn ngữ")
    p_rule.add_argument("paths", nargs="*", help="Danh sách tệp chỉ định")
    p_rule.add_argument("--from", dest="from_ref", help="Git from ref")
    p_rule.add_argument("--to", dest="to_ref", help="Git to ref")
    p_rule.add_argument("-c", "--commit", dest="commit", help="Commit hash")
    p_rule.add_argument("-f", "--format", choices=["text", "json"], default="text", help="Định dạng xuất")

    # Check / Review sub-command
    p_check = subparsers.add_parser("check", help="Chạy kiểm tra tĩnh và phân tích theo luật Alibaba")
    p_check.add_argument("paths", nargs="*", help="Danh sách tệp chỉ định")
    p_check.add_argument("--from", dest="from_ref", help="Git from ref")
    p_check.add_argument("--to", dest="to_ref", help="Git to ref")
    p_check.add_argument("-c", "--commit", dest="commit", help="Commit hash")
    p_check.add_argument("-f", "--format", choices=["text", "json"], default="text", help="Định dạng xuất")

    p_rev = subparsers.add_parser("review", help="Thực hiện quy trình review đầy đủ")
    p_rev.add_argument("paths", nargs="*", help="Danh sách tệp chỉ định")
    p_rev.add_argument("--from", dest="from_ref", help="Git from ref")
    p_rev.add_argument("--to", dest="to_ref", help="Git to ref")
    p_rev.add_argument("-c", "--commit", dest="commit", help="Commit hash")
    p_rev.add_argument("-f", "--format", choices=["text", "json"], default="text", help="Định dạng xuất")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "preview":
        cmd_preview(args)
    elif args.command == "rule":
        cmd_rule(args)
    elif args.command in ("check", "review"):
        cmd_review(args)


if __name__ == "__main__":
    main()
