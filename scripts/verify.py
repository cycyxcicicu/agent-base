#!/usr/bin/env python3
"""
scripts/verify.py
CLI Kiểm chứng thực thi chạy thật trên fixture cô lập (Bootstrap & Upgrade).
Tuân thủ đặc tả T-11 §5 và các yêu cầu R-10, R-14.

Mã thoát (Exit codes):
  0: Kiểm chứng PASS và xuất proof bundle thành công
  1: Kiểm chứng FAIL (có điều kiện hậu kiểm thất bại)
  2: Lỗi tham số đầu vào

Usage:
  python scripts/verify.py bootstrap --evidence-root <dir> [--keep-fixture]
  python scripts/verify.py upgrade --evidence-root <dir> [--keep-fixture]
"""

from __future__ import annotations
import argparse
import json
import os
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
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_core.verification.bootstrap import run_bootstrap_verification
from agent_core.verification.upgrade import run_upgrade_verification
from agent_core.verification.repro import run_repro_harness


def main():
    parser = argparse.ArgumentParser(description="CLI Kiểm chứng thực thi chạy thật trên fixture cô lập (Proof & Verification)")
    subparsers = parser.add_subparsers(dest="recipe", required=True)

    # Subcommand: bootstrap
    p_boot = subparsers.add_parser("bootstrap", help="Kiểm chứng quy trình cài đặt framework vào fixture trống")
    p_boot.add_argument("--evidence-root", required=True, help="Thư mục lưu trữ bằng chứng kiểm chứng (Proof)")
    p_boot.add_argument("--keep-fixture", action="store_true", help="Giữ lại fixture sau khi chạy (mặc định xóa)")

    # Subcommand: upgrade
    p_upg = subparsers.add_parser("upgrade", help="Kiểm chứng quy trình nâng cấp và giải quyết xung đột trên fixture")
    p_upg.add_argument("--evidence-root", required=True, help="Thư mục lưu trữ bằng chứng kiểm chứng (Proof)")
    p_upg.add_argument("--keep-fixture", action="store_true", help="Giữ lại fixture sau khi chạy (mặc định xóa)")

    # Subcommand: repro
    p_rep = subparsers.add_parser("repro", help="Tái hiện triệu chứng lỗi 2 lần độc lập có reset trạng thái")
    p_rep.add_argument("--recipe", required=True, help="Đường dẫn tệp JSON khai báo kịch bản tái hiện")
    p_rep.add_argument("--evidence-root", required=True, help="Thư mục lưu trữ bằng chứng kiểm chứng (Proof)")

    args = parser.parse_args()

    ev_root = Path(args.evidence_root)
    ev_root.mkdir(parents=True, exist_ok=True)

    if args.recipe == "bootstrap":
        print("🚀 Bắt đầu kiểm chứng thực tế recipe: BOOTSTRAP...")
        proof_path = run_bootstrap_verification(evidence_root=ev_root, keep_fixture=args.keep_fixture)
    elif args.recipe == "upgrade":
        print("🚀 Bắt đầu kiểm chứng thực tế recipe: UPGRADE...")
        proof_path = run_upgrade_verification(evidence_root=ev_root, keep_fixture=args.keep_fixture)
    elif args.recipe == "repro":
        recipe_path = Path(args.recipe)
        if not recipe_path.is_file():
            sys.stderr.write(f"Lỗi: Tệp recipe không tồn tại: {args.recipe}\n")
            sys.exit(2)
        recipe_data = json.loads(recipe_path.read_text(encoding="utf-8"))
        print(f"🚀 Bắt đầu tái hiện lỗi hai lần có reset theo recipe: {recipe_data.get('name', 'repro')}...")
        repro_res = run_repro_harness(recipe_data, evidence_root=ev_root)
        proof_path = repro_res.proof_path
    else:
        sys.exit(2)

    data = json.loads(proof_path.read_text(encoding="utf-8"))
    res = data.get("result", "inconclusive")
    icon = "✅ PASS" if res == "pass" else "❌ FAIL"

    print(f"\n=======================================================")
    print(f"KẾT QUẢ KIỂM CHỨNG [{args.recipe.upper()}]: {icon}")
    print(f"=======================================================")
    print(f"📄 Tệp proof bundle: {proof_path}")
    print(f"📊 Run ID: {data.get('run_id')}")
    print(f"🎯 Assertions:")
    for a in data.get("assertions", []):
        a_icon = "  * [PASS]" if a.get("passed") else "  * [FAIL]"
        print(f"{a_icon} {a.get('id')}: {a.get('observed')}")
    print(f"🧹 Cleanup performed: {data.get('cleanup', {}).get('clean')}\n")

    sys.exit(0 if res == "pass" else 1)


if __name__ == "__main__":
    main()
