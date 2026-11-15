#!/usr/bin/env python3
"""
scripts/dependency-guard.py
Cổng kiểm soát Mã Độc Gói Phụ Thuộc (Dependency Poisoning & Supply Chain Guard).

Mục tiêu cốt lõi:
1. Malicious Lifecycle Hooks: Phát hiện script tiền/hậu cài đặt trong `package.json`.
2. Dependency Confusion & Untrusted Registries: Phát hiện `--extra-index-url` lạ.
3. Untrusted Repositories: Phát hiện repository HTTP lạ trong `pom.xml`.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SUSPICIOUS_LIFECYCLE_SCRIPTS = {"preinstall", "postinstall", "install"}
MALICIOUS_SCRIPT_COMMANDS = [
    re.compile(r"\b(curl|wget|fetch)\b", re.I),
    re.compile(r"\b(bash|sh|zsh|python|node)\s+-(?:c|e)\b", re.I),
    re.compile(r"\bbase64\b", re.I),
    re.compile(r"\b(nc|netcat|ncat)\b", re.I),
]


def _check_hook_command(file_path: Path, hook: str, cmd_str: str) -> str | None:
    """Kiểm tra câu lệnh trong lifecycle hook xem có mã độc không."""
    for pat in MALICIOUS_SCRIPT_COMMANDS:
        if pat.search(cmd_str):
            return (
                f"{file_path} [MALICIOUS_LIFECYCLE_HOOK] Script '{hook}' "
                f"chứa lệnh đáng ngờ: '{cmd_str}'."
            )
    return None


def audit_package_json(file_path: Path) -> list[str]:
    """Kiểm tra an toàn file package.json."""
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{file_path}: Lỗi đọc định dạng JSON ({exc})"]

    scripts = data.get("scripts", {})
    if not isinstance(scripts, dict):
        return []

    violations: list[str] = []
    for hook in SUSPICIOUS_LIFECYCLE_SCRIPTS:
        if hook not in scripts:
            continue
        err = _check_hook_command(file_path, hook, str(scripts[hook]))
        if err:
            violations.append(err)
    return violations


def audit_requirements_txt(file_path: Path) -> list[str]:
    """Kiểm tra an toàn file requirements.txt."""
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []

    violations: list[str] = []
    for line_no, line in enumerate(content.splitlines(), 1):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if "--extra-index-url" in s and not any(k in s for k in ("pypi.org", "python.org")):
            violations.append(
                f"{file_path}:{line_no} [UNTRUSTED_REGISTRY] Phát hiện --extra-index-url lạ: '{s}'!"
            )
        if re.search(r"^https?://.*(?:\.whl|\.tar\.gz|\.zip)", s):
            violations.append(
                f"{file_path}:{line_no} [UNVERIFIED_BINARY_URL] Cài gói trực tiếp từ URL lạ: '{s}'!"
            )
    return violations


def audit_pom_xml(file_path: Path) -> list[str]:
    """Kiểm tra an toàn file pom.xml."""
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []

    violations: list[str] = []
    for m in re.findall(r"<url>(http://[^<]+)</url>", content, re.I):
        violations.append(
            f"{file_path} [INSECURE_MAVEN_REPO] Phát hiện repository HTTP không an toàn: '{m}'!"
        )
    return violations


def audit_dependency_file(file_path: Path) -> list[str]:
    """Phân loại và kiểm tra file phụ thuộc tương ứng."""
    if not file_path.is_file():
        return []
    name = file_path.name.lower()
    if name == "package.json":
        return audit_package_json(file_path)
    if "requirements" in name and name.endswith(".txt"):
        return audit_requirements_txt(file_path)
    if name == "pom.xml":
        return audit_pom_xml(file_path)
    return []


def _resolve_files_from_diff(base_ref: str) -> list[Path]:
    """Lấy danh sách file phụ thuộc thay đổi so với base_ref."""
    cmd = ["git", "diff", "--name-only", base_ref]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return []
    return [Path(line.strip()) for line in res.stdout.splitlines() if line.strip()]


def _resolve_target_files(args: argparse.Namespace) -> list[Path]:
    """Xác định danh sách các file cấu hình phụ thuộc cần quét."""
    if args.changed_against:
        return _resolve_files_from_diff(args.changed_against)
    if args.paths:
        return [Path(p) for p in args.paths if Path(p).is_file()]

    results: list[Path] = []
    for p in Path.cwd().glob("**/package.json"):
        if "node_modules" not in str(p):
            results.append(p)
    results.extend(Path.cwd().glob("**/requirements*.txt"))
    results.extend(Path.cwd().glob("**/pom.xml"))
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Dependency Poisoning & Supply Chain Guard")
    parser.add_argument("paths", nargs="*", help="File quản lý gói cần quét")
    parser.add_argument("--changed-against", help="So sánh với commit/nhánh gốc (vd: origin/develop)")
    args = parser.parse_args()

    files = _resolve_target_files(args)
    all_violations: list[str] = []
    for f in files:
        all_violations.extend(audit_dependency_file(f))

    if not all_violations:
        print("✅ [DEPENDENCY GUARD] Các file quản lý gói phụ thuộc 100% an toàn.")
        sys.exit(0)

    print("❌ [DEPENDENCY GUARD - PHÁT HIỆN RỦI RO CHUỖI CUNG ỨNG]")
    for v in all_violations:
        print(f"  - {v}")
    print("\nCảnh báo: Vi phạm tiêu chuẩn an toàn chuỗi cung ứng theo §4 AGENTS.md.")
    sys.exit(1)


if __name__ == "__main__":
    main()
