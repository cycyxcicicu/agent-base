#!/usr/bin/env python3
"""
scripts/proof-check.py
CLI Kiểm tra tính toàn vẹn độc lập của Proof Bundle và các artifacts thực tế.
Tuân thủ đặc tả T-11 §5.

Mã thoát (Exit codes):
  0: Bằng chứng hợp lệ 100% và khớp băm SHA256
  1: Bị sửa đổi, thiếu tệp artifact hoặc vi phạm schema
  2: Lỗi tham số / tệp proof.json không tồn tại

Usage:
  python scripts/proof-check.py --bundle <path/to/proof.json> [--format text|json]
"""

from __future__ import annotations
import argparse
import hashlib
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

from agent_core.verification.proof import validate_proof_bundle


def check_proof(bundle_file: Path) -> Tuple[bool, List[str]]:
    if not bundle_file.is_file():
        return False, [f"Tệp proof không tồn tại: {bundle_file}"]

    try:
        data = json.loads(bundle_file.read_text(encoding="utf-8"))
    except Exception as e:
        return False, [f"Lỗi cú pháp JSON trong proof: {str(e)}"]

    errors = validate_proof_bundle(data)
    if errors:
        return False, errors

    # Kiểm tra thực tế từng artifact
    bundle_dir = bundle_file.parent
    artifacts = data.get("artifacts", [])

    for art in artifacts:
        p_rel = art.get("path_rel")
        expected_sha = art.get("sha256", "").lower()
        art_path = bundle_dir / p_rel

        if not art_path.is_file():
            errors.append(f"Thiếu tệp artifact trên đĩa: {p_rel}")
            continue

        try:
            with open(art_path, "rb") as f:
                actual_sha = hashlib.sha256(f.read()).hexdigest().lower()
            if actual_sha != expected_sha:
                errors.append(
                    f"Sai lệch băm SHA256 tại artifact '{p_rel}' (kỳ vọng: {expected_sha}, thực tế: {actual_sha})"
                )
        except Exception as e:
            errors.append(f"Không thể đọc tệp artifact '{p_rel}': {str(e)}")

    return len(errors) == 0, errors


def main():
    parser = argparse.ArgumentParser(description="CLI Kiểm chuẩn tính toàn vẹn của Proof Bundle")
    parser.add_argument("--bundle", required=True, help="Đường dẫn tới tệp proof.json cần kiểm tra")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Định dạng đầu ra")

    args = parser.parse_args()

    bundle_path = Path(args.bundle)
    if not bundle_path.is_file():
        # Thử ghép với ROOT nếu cần
        bundle_path = ROOT / args.bundle
        if not bundle_path.is_file():
            sys.stderr.write(f"Lỗi: Không tìm thấy tệp proof tại: {args.bundle}\n")
            sys.exit(2)

    is_valid, errors = check_proof(bundle_path)

    if args.format == "json":
        out = {
            "bundle": str(bundle_path),
            "valid": is_valid,
            "error_count": len(errors),
            "errors": errors,
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        if is_valid:
            print(f"✅ Bằng chứng hợp lệ 100%: {bundle_path.name}")
        else:
            print(f"❌ Phát hiện {len(errors)} lỗi toàn vẹn trong proof:")
            for err in errors:
                print(f"  - {err}")

    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
