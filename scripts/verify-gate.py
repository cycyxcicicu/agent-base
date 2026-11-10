#!/usr/bin/env python3
"""
scripts/verify-gate.py

Cổng kiểm tổng hợp 3-trong-1 (hard-check + glossary-check + task-gate) và Stop Hook tin cậy
(chuyển thể từ `gstack-verify-gate` sang Python thuần).

Hai chế độ sử dụng:
  1. Chạy trực tiếp trước khi kết thúc task / tạo MR:
     python3 scripts/verify-gate.py run --root . --changed-against develop --card <card.md> [--strict-ac] [--require-challenge]
  2. Chạy ở Claude Code `Stop` hook (đọc JSON stdin, chặn exit 2 nếu dự án đã bật
     `<!-- agentbase:verify: <cmd> -->` trong CLAUDE.md VÀ người dùng đã xác thực `--trust`;
     nếu chưa khai báo hoặc chưa `--trust` thì fail-open exit 0 để không kẹt các repo khác).
     python3 scripts/verify-gate.py --trust --root .
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
DEFAULT_TRUST_FILE = Path.home() / ".agentbase" / "verify-gate-trust.tsv"
VERIFY_LINE_RE = re.compile(r"^\s*(?:<!--\s*)?agentbase:verify:\s*(.+?)\s*(?:-->)?\s*$")


def extract_verify_command(project_root: Path) -> str:
    claude_md = project_root / "CLAUDE.md"
    if not claude_md.is_file():
        return ""
    for line in claude_md.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = VERIFY_LINE_RE.match(line)
        if m:
            return m.group(1).strip().strip("`")
    return ""


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_trust_map(trust_file: Path) -> dict[str, str]:
    if not trust_file.is_file():
        return {}
    mapping: dict[str, str] = {}
    for line in trust_file.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "\t" not in line:
            continue
        p, h = line.split("\t", 1)
        if p.strip() and h.strip():
            mapping[p.strip()] = h.strip()
    return mapping


def record_trust(project_root: Path, cmd: str, trust_file: Path = DEFAULT_TRUST_FILE) -> Path:
    trust_file.parent.mkdir(parents=True, exist_ok=True)
    mapping = load_trust_map(trust_file)
    mapping[str(project_root.resolve())] = _sha256(cmd)
    tmp = trust_file.with_suffix(".tmp")
    lines = [f"{k}\t{v}\n" for k, v in sorted(mapping.items())]
    tmp.write_text("".join(lines), encoding="utf-8")
    try:
        os.chmod(tmp, 0o600)
    except OSError:
        pass
    tmp.replace(trust_file)
    return trust_file


def run_bundle(
    root: Path,
    changed_against: str | None = None,
    card: str = "",
    strict_ac: bool = False,
    require_challenge: bool = False,
) -> int:
    steps: list[tuple[str, list[str]]] = []

    hc_cmd = [sys.executable, str(SCRIPTS_DIR / "hard-check.py"), "--root", str(root)]
    if changed_against:
        hc_cmd.extend(["--changed-against", changed_against, "--diff-lines"])
    steps.append(("hard-check", hc_cmd))

    gc_cmd = [sys.executable, str(SCRIPTS_DIR / "glossary-check.py"), "--root", str(root)]
    if changed_against:
        gc_cmd.extend(["--changed-against", changed_against])
    steps.append(("glossary-check", gc_cmd))

    tg_cmd = [sys.executable, str(SCRIPTS_DIR / "task-gate.py"), "audit", "--root", str(root)]
    if changed_against:
        tg_cmd.extend(["--changed-against", changed_against])
    if card:
        tg_cmd.extend(["--card", card])
    if strict_ac:
        tg_cmd.append("--strict-ac")
    if require_challenge:
        tg_cmd.append("--require-challenge")
    steps.append(("task-gate", tg_cmd))

    overall_rc = 0
    for label, cmd in steps:
        print(f"=== [{label}] ===")
        res = subprocess.run(cmd, cwd=str(root), text=True, encoding="utf-8")
        if res.returncode != 0 and overall_rc == 0:
            overall_rc = res.returncode
    return overall_rc


def run_stop_hook(project_root: Path, trust_file: Path = DEFAULT_TRUST_FILE) -> int:
    # Đọc stdin Stop hook payload (tránh chặn đệ quy khi stop_hook_active=True)
    raw = ""
    if not sys.stdin.isatty():
        try:
            raw = sys.stdin.read()
        except Exception:
            raw = ""
    if raw.strip():
        try:
            payload = json.loads(raw)
            if payload.get("stop_hook_active"):
                return 0
            if payload.get("cwd"):
                project_root = Path(os.path.expanduser(str(payload["cwd"]))).resolve()
        except Exception:
            pass

    cmd = extract_verify_command(project_root)
    if not cmd:
        return 0
    trusted = load_trust_map(trust_file).get(str(project_root.resolve()))
    if trusted != _sha256(cmd):
        return 0

    proc = subprocess.run(cmd, cwd=str(project_root), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8")
    if proc.returncode != 0:
        sys.stderr.write(f"[verify-gate] Lệnh kiểm tra `{cmd}` thất bại (exit {proc.returncode}):\n{(proc.stdout or '')[-1500:]}\n")
        sys.stderr.flush()
        return 2
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Cổng kiểm tổng hợp & Stop Hook tin cậy.")
    sub = ap.add_subparsers(dest="subcmd")

    p_run = sub.add_parser("run", help="Chạy 3 cổng hard-check + glossary-check + task-gate")
    p_run.add_argument("--root", default=".", help="Thư mục gốc dự án/worktree")
    p_run.add_argument("--changed-against", default=None, metavar="REF", help="Nhánh gốc so sánh diff (vd: develop)")
    p_run.add_argument("--card", default="", help="Task Card .md")
    p_run.add_argument("--strict-ac", action="store_true")
    p_run.add_argument("--require-challenge", action="store_true")

    p_hook = sub.add_parser("hook", help="Chạy chế độ Claude Stop hook")
    p_hook.add_argument("--root", default=".")
    p_hook.add_argument("--trust-file", default=str(DEFAULT_TRUST_FILE))

    ap.add_argument("--trust", action="store_true", help="Ghi dấu tin cậy lệnh `agentbase:verify:` trong CLAUDE.md của --root")
    ap.add_argument("--root", default=".", help="Thư mục gốc dự án khi chạy --trust")
    ap.add_argument("--trust-file", default=str(DEFAULT_TRUST_FILE))

    args = ap.parse_args()
    if args.trust:
        ws = Path(args.root).resolve()
        cmd = extract_verify_command(ws)
        if not cmd:
            print(f"LỖI: Chưa tìm thấy dòng `<!-- agentbase:verify: <lệnh> -->` trong {ws / 'CLAUDE.md'}")
            return 2
        tf = record_trust(ws, cmd, trust_file=Path(args.trust_file))
        print(f"[OK] Đã xác thực tin cậy `{cmd}` cho {ws} tại {tf}")
        return 0

    if args.subcmd == "hook":
        return run_stop_hook(Path(args.root).resolve(), trust_file=Path(args.trust_file))

    if args.subcmd == "run":
        return run_bundle(
            root=Path(args.root).resolve(),
            changed_against=args.changed_against,
            card=args.card,
            strict_ac=args.strict_ac,
            require_challenge=args.require_challenge,
        )

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
