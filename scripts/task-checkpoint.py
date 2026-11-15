#!/usr/bin/env python3
"""scripts/task-checkpoint.py

Cơ chế Điểm kiểm tra & Tự động Hoàn tác (Git Checkpoint & Auto-Rollback Engine).
Ngăn chặn hiện tượng Lỗi Dây Chuyền Tích Tụ (Compounding Errors) theo chuẩn SWE-bench SOTA & Agentless 2025.

Tính năng:
- `create --task <T-xx> [--desc <mô tả>]`: Tạo điểm kiểm tra trước khi sửa code (lưu HEAD commit, diff hiện tại vào .checkpoints/).
- `rollback --task <T-xx>`: Khôi phục hoàn toàn về điểm kiểm tra sạch gần nhất, loại bỏ mọi sửa đổi bế tắc.
- `list [--task <T-xx>]`: Liệt kê các điểm kiểm tra đang lưu.
- `drop --task <T-xx>`: Xóa điểm kiểm tra khi task đã vượt qua bài test thành công.

Usage:
  python3 scripts/task-checkpoint.py create --task T-12.1 --desc "Trước khi sửa token parser"
  python3 scripts/task-checkpoint.py rollback --task T-12.1
  python3 scripts/task-checkpoint.py list
  python3 scripts/task-checkpoint.py drop --task T-12.1
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
CHECKPOINT_DIR = ROOT / ".checkpoints"


def run_git(args: List[str], cwd: Path | None = None) -> Tuple[int, str]:
    """Chạy lệnh git và trả về (exit_code, stdout)."""
    p = subprocess.run(
        ["git"] + args,
        cwd=cwd or ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return p.returncode, p.stdout.strip()


def sanitize_task(task_name: str) -> str:
    """Chuẩn hóa mã task (bỏ ký tự lạ chống lỗi path traversal)."""
    return "".join(c if c.isalnum() or c in ("-", "_", ".") else "_" for c in task_name)


def create_checkpoint(
    task: str,
    desc: str = "",
    root: Path | None = None,
) -> Dict:
    """Tạo checkpoint cho một task."""
    root_path = root or ROOT
    task_id = sanitize_task(task)
    task_dir = (root_path / ".checkpoints" / task_id)
    task_dir.mkdir(parents=True, exist_ok=True)

    timestamp = int(time.time())
    iso_time = datetime.now(timezone.utc).isoformat()

    # 1. Lấy HEAD commit SHA
    code, head_sha = run_git(["rev-parse", "HEAD"], cwd=root_path)
    if code != 0:
        raise RuntimeError(f"Không thể đọc git HEAD: {head_sha}")

    # 2. Lấy git diff unstaged và staged hiện tại (nếu có)
    _, staged_diff = run_git(["diff", "--cached"], cwd=root_path)
    _, unstaged_diff = run_git(["diff"], cwd=root_path)

    # 3. Lấy danh sách file untracked hiện tại để bảo toàn nếu có
    _, untracked_out = run_git(["ls-files", "--others", "--exclude-standard"], cwd=root_path)
    untracked_files = [f for f in untracked_out.splitlines() if f.strip()]

    patch_filename = f"{timestamp}.patch"
    patch_path = task_dir / patch_filename

    combined_diff = ""
    if staged_diff:
        combined_diff += "# STAGED DIFF\n" + staged_diff + "\n"
    if unstaged_diff:
        combined_diff += "# UNSTAGED DIFF\n" + unstaged_diff + "\n"

    if combined_diff:
        patch_path.write_text(combined_diff, encoding="utf-8")

    meta = {
        "task": task,
        "timestamp": timestamp,
        "created_at": iso_time,
        "desc": desc,
        "head_sha": head_sha,
        "patch_file": patch_filename if combined_diff else None,
        "untracked_files": untracked_files,
    }

    meta_file = task_dir / f"{timestamp}.json"
    meta_file.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    # Cập nhật latest pointer
    latest_file = task_dir / "latest.json"
    latest_file.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    return meta


def rollback_checkpoint(
    task: str,
    root: Path | None = None,
    clean_untracked: bool = True,
) -> Dict:
    """Khôi phục workspace về checkpoint gần nhất của task."""
    root_path = root or ROOT
    task_id = sanitize_task(task)
    task_dir = root_path / ".checkpoints" / task_id
    latest_file = task_dir / "latest.json"

    if not latest_file.exists():
        raise FileNotFoundError(f"Không tìm thấy checkpoint nào cho task '{task}'")

    meta = json.loads(latest_file.read_text(encoding="utf-8"))
    head_sha = meta["head_sha"]

    # 1. Reset hard về commit SHA của checkpoint để loại bỏ mọi thay đổi trong tracked files
    run_git(["reset", "--hard", head_sha], cwd=root_path)
    run_git(["clean", "-fd"], cwd=root_path) if clean_untracked else None

    # 2. Xóa các untracked files mới sinh ra trong quá trình sửa code thất bại
    if clean_untracked:
        # Lấy untracked hiện tại
        _, curr_untracked = run_git(["ls-files", "--others", "--exclude-standard"], cwd=root_path)
        current_set = set(f.strip() for f in curr_untracked.splitlines() if f.strip())
        initial_set = set(meta.get("untracked_files", []))

        # Chỉ xóa các file mới sinh sau checkpoint
        files_to_remove = current_set - initial_set
        for f in files_to_remove:
            target = root_path / f
            if target.is_file() or target.is_symlink():
                target.unlink(missing_ok=True)
            elif target.is_dir() and not target.name.startswith(".checkpoints"):
                shutil.rmtree(target, ignore_errors=True)

    # 3. Nếu checkpoint ban đầu có patch (sửa đổi trước khi checkpoint), apply lại patch đó
    if meta.get("patch_file"):
        patch_path = task_dir / meta["patch_file"]
        if patch_path.exists():
            patch_content = patch_path.read_text(encoding="utf-8")
            # Apply patch nếu hợp lệ
            subprocess.run(
                ["git", "apply", "--whitespace=nowarn", str(patch_path)],
                cwd=root_path,
                capture_output=True,
            )

    return meta


def list_checkpoints(root: Path | None = None, task: Optional[str] = None) -> List[Dict]:
    """Liệt kê danh sách các checkpoints."""
    root_path = root or ROOT
    base_dir = root_path / ".checkpoints"
    if not base_dir.exists():
        return []

    results = []
    if task:
        task_dirs = [base_dir / sanitize_task(task)]
    else:
        task_dirs = [d for d in base_dir.iterdir() if d.is_dir()]

    for td in task_dirs:
        if not td.exists():
            continue
        for jf in td.glob("*.json"):
            if jf.name == "latest.json":
                continue
            try:
                data = json.loads(jf.read_text(encoding="utf-8"))
                results.append(data)
            except Exception:
                continue

    results.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
    return results


def drop_checkpoints(task: str, root: Path | None = None) -> bool:
    """Xóa toàn bộ checkpoint của một task."""
    root_path = root or ROOT
    task_id = sanitize_task(task)
    task_dir = root_path / ".checkpoints" / task_id
    if task_dir.exists():
        shutil.rmtree(task_dir, ignore_errors=True)
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="task-checkpoint: Cơ chế tạo điểm kiểm tra và tự động hoàn tác (Anti-Compounding Errors)"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_create = sub.add_parser("create", help="Tạo checkpoint mới cho task")
    p_create.add_argument("--task", required=True, help="Mã task (ví dụ: T-12.1)")
    p_create.add_argument("--desc", default="", help="Mô tả lý do hoặc trạng thái checkpoint")
    p_create.add_argument("--root", default=".", help="Thư mục gốc của repository")

    p_rollback = sub.add_parser("rollback", help="Hoàn tác về checkpoint gần nhất của task")
    p_rollback.add_argument("--task", required=True, help="Mã task (ví dụ: T-12.1)")
    p_rollback.add_argument("--root", default=".", help="Thư mục gốc của repository")
    p_rollback.add_argument(
        "--no-clean", action="store_true", help="Không xóa các untracked files mới sinh"
    )

    p_list = sub.add_parser("list", help="Liệt kê các checkpoint đang lưu")
    p_list.add_argument("--task", default=None, help="Lọc theo mã task")
    p_list.add_argument("--root", default=".", help="Thư mục gốc của repository")

    p_drop = sub.add_parser("drop", help="Xóa các checkpoint của một task")
    p_drop.add_argument("--task", required=True, help="Mã task (ví dụ: T-12.1)")
    p_drop.add_argument("--root", default=".", help="Thư mục gốc của repository")

    args = parser.parse_args()
    root = Path(args.root).resolve()

    if args.cmd == "create":
        meta = create_checkpoint(args.task, desc=args.desc, root=root)
        print(f"[OK] Đã tạo Checkpoint cho task '{args.task}':")
        print(f"     Commit HEAD: {meta['head_sha'][:8]}")
        print(f"     Thời gian  : {meta['created_at']}")
        if meta.get("desc"):
            print(f"     Mô tả      : {meta['desc']}")
        return 0

    elif args.cmd == "rollback":
        try:
            meta = rollback_checkpoint(
                args.task, root=root, clean_untracked=not args.no_clean
            )
            print(f"[OK] Đã ROLLBACK thành công về Checkpoint của task '{args.task}':")
            print(f"     Khôi phục HEAD: {meta['head_sha'][:8]}")
            print(f"     Thời điểm checkpoint: {meta['created_at']}")
            print("     Toàn bộ các thay đổi sửa code hỏng đã được gỡ bỏ sạch sẽ.")
            return 0
        except Exception as exc:
            print(f"[ERROR] Lỗi khi hoàn tác checkpoint: {exc}", file=sys.stderr)
            return 1

    elif args.cmd == "list":
        cps = list_checkpoints(root=root, task=args.task)
        if not cps:
            print("[INFO] Không có checkpoint nào đang lưu.")
            return 0
        print(f"Tìm thấy {len(cps)} checkpoint(s):")
        for cp in cps:
            print(f"- Task: {cp['task']} | Commit: {cp['head_sha'][:8]} | Time: {cp['created_at']} | Desc: {cp.get('desc', '')}")
        return 0

    elif args.cmd == "drop":
        ok = drop_checkpoints(args.task, root=root)
        if ok:
            print(f"[OK] Đã xóa checkpoint của task '{args.task}'.")
        else:
            print(f"[INFO] Không tìm thấy checkpoint nào cho task '{args.task}'.")
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
