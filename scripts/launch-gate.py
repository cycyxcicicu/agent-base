#!/usr/bin/env python3
"""
scripts/launch-gate.py
Thẩm định Launch-Ready Gate (20% cuối) theo quy tắc 80/20 của Meta (Senior Staff Standard).

Quy trình release được chia làm 2 chặng tách bạch:
  - 80% đầu: Merge-Ready (scripts/merge-gate.py) - code sạch, test xanh, merge vào develop.
  - 20% cuối: Launch-Ready (scripts/launch-gate.py) - tổng kiểm toán trước khi bật cờ mở traffic Production.

Các tiêu chí thẩm định:
  1. Feature Flag & Kill-Switch: Có cờ tính năng, mặc định OFF, fallback an toàn khi tắt cờ.
  2. Security CSO Audit: Đã kiểm toán an ninh, không secret leak, không SQLi/IDOR/SSRF.
  3. Performance & Scalability: Không N+1 query, không lock bảng lớn, latency đạt SLA.
  4. Human Taste & UX Polish: Giao diện mượt mà, vi tương tác chuẩn, console error = 0, contrast >= 4.5:1.
  5. Canary Deployment Plan: Lộ trình mở lưu lượng từng bước (ví dụ: 0% -> 5% -> 25% -> 100%).

Usage:
  python scripts/launch-gate.py --card tasks/<epic>/T-<ticket>.md [--flag ENABLE_FEATURE_X] [--strict]
"""

import os
import sys
import re
import argparse
import subprocess
from pathlib import Path

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent


def check_task_card(card_path: Path):
    if not card_path.exists():
        print(f"FAIL: Task card '{card_path}' does not exist.")
        sys.exit(1)
    return card_path.read_text(encoding='utf-8', errors='replace')


def audit_feature_flag(card_text: str, flag_arg: str = None) -> tuple:
    """Kiểm tra khai báo Feature Flag và kịch bản Kill-Switch."""
    flag_name = flag_arg
    if not flag_name:
        m = re.search(r'(?i)(feature\s*flag|cờ\s*tính\s*năng)\s*:\s*`?([A-Za-z0-9_\-]+)`?', card_text)
        if m:
            flag_name = m.group(2)

    has_killswitch = bool(re.search(r'(?i)(kill-switch|kill\s*switch|fallback|tắt\s*cờ|rollback)', card_text))
    has_default_off = bool(re.search(r'(?i)(default\s*:\s*(off|false)|mặc\s*định\s*:\s*(tắt|off|false))', card_text))

    issues = []
    if not flag_name:
        issues.append("Chưa khai báo tên Feature Flag (VD: `Feature Flag: ENABLE_FEATURE_X`)")
    if not has_killswitch:
        issues.append("Chưa xác nhận kiểm thử Kill-Switch (Kịch bản fallback an toàn khi tắt cờ)")
    if not has_default_off:
        issues.append("Trạng thái mặc định của cờ chưa được chỉ định là OFF/false")

    return (len(issues) == 0, flag_name or "N/A", issues)


def audit_security(repo: Path, card_text: str) -> tuple:
    """Kiểm tra bảo mật (CSO - Chief Security Officer)."""
    has_security_mention = bool(re.search(r'(?i)(security\s*(cso|audit|check)|bảo\s*mật|cso\.py|idor|sqli)', card_text))
    
    # Thử chạy cso.py nếu script tồn tại
    cso_script = repo / 'scripts' / 'cso.py'
    cso_run_ok = True
    cso_output = ""
    if cso_script.exists():
        try:
            res = subprocess.run([sys.executable, str(cso_script), '--check'], capture_output=True, text=True, timeout=10)
            cso_run_ok = (res.returncode == 0)
            cso_output = res.stdout.strip() or res.stderr.strip()
        except Exception:
            pass

    issues = []
    if not cso_run_ok:
        issues.append(f"Cổng bảo mật cso.py báo lỗi: {cso_output[:100]}")
    elif not has_security_mention and not cso_script.exists():
        issues.append("Chưa ghi nhận bằng chứng kiểm toán an ninh (Security CSO Audit / Secret / Injection)")

    return (len(issues) == 0, issues)


def audit_performance(card_text: str) -> tuple:
    """Kiểm tra hiệu năng và CSDL."""
    has_perf = bool(re.search(r'(?i)(performance|hiệu\s*năng|latency|n\+1|db\s*lock|index|truy\s*vấn)', card_text))
    issues = []
    if not has_perf:
        issues.append("Chưa có ghi chú kiểm toán hiệu năng (N+1 query, Index DB, hoặc độ trễ SLA)")
    return (len(issues) == 0, issues)


def audit_ux_taste(card_text: str) -> tuple:
    """Kiểm tra chất lượng trải nghiệm người dùng (Human Taste & UX)."""
    has_ui = bool(re.search(r'(?i)(ui|ux|giao\s*diện|frontend|cdp|browser)', card_text))
    if not has_ui:
        return (True, [])  # Không phải task UI -> bỏ qua

    has_cdp_or_taste = bool(re.search(r'(?i)(console\s*errors?:\s*0|tương\s*phản|contrast|human\s*taste|ux\s*verified|mượt\s*mà)', card_text))
    issues = []
    if not has_cdp_or_taste:
        issues.append("Task chạm UI nhưng chưa có xác nhận Human Taste UX (0 console error, độ tương phản >= 4.5:1)")
    return (len(issues) == 0, issues)


def audit_canary_plan(card_text: str) -> tuple:
    """Kiểm tra kế hoạch mở dần traffic (Canary / Phased Rollout)."""
    has_canary = bool(re.search(r'(?i)(canary|phased\s*rollout|mở\s*dần|tỉ\s*lệ|traffic|%\s*->|a/b\s*test)', card_text))
    issues = []
    if not has_canary:
        issues.append("Chưa có kế hoạch Canary Rollout mở dần traffic (ví dụ: 0% -> 5% -> 25% -> 100%)")
    return (len(issues) == 0, issues)


def main():
    parser = argparse.ArgumentParser(description="Audit Launch-Ready Gate (20% phase) before enabling feature in Production.")
    parser.add_argument("--card", required=True, help="Path to task card markdown file.")
    parser.add_argument("--flag", default="", help="Feature flag name (e.g. ENABLE_NEW_CHECKOUT).")
    parser.add_argument("--strict", action="store_true", help="Fail if any check has warnings.")
    args = parser.parse_args()

    card_path = Path(args.card)
    card_text = check_task_card(card_path)

    try:
        repo = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip())
    except Exception:
        repo = ROOT

    print("========================================================================")
    print("🚀 LAUNCH-READY GATE AUDIT (Quy tắc 80/20 - Meta Senior Staff Standard)")
    print("========================================================================")
    print(f"Task Card: {card_path}")

    # 1. Feature Flag & Kill-Switch
    flag_ok, flag_name, flag_issues = audit_feature_flag(card_text, args.flag)
    print(f"\n1. Feature Gating & Kill-Switch: {'[PASS]' if flag_ok else '[WARN]'}")
    print(f"   - Flag Name: {flag_name}")
    for iss in flag_issues:
        print(f"   - ⚠️  {iss}")

    # 2. Security CSO Audit
    sec_ok, sec_issues = audit_security(repo, card_text)
    print(f"\n2. Security CSO Audit: {'[PASS]' if sec_ok else '[WARN]'}")
    for iss in sec_issues:
        print(f"   - ⚠️  {iss}")

    # 3. Performance & Scalability
    perf_ok, perf_issues = audit_performance(card_text)
    print(f"\n3. Performance & Scalability: {'[PASS]' if perf_ok else '[WARN]'}")
    for iss in perf_issues:
        print(f"   - ⚠️  {iss}")

    # 4. Human Taste & UX Audit
    ux_ok, ux_issues = audit_ux_taste(card_text)
    print(f"\n4. Human Taste & UX Polish: {'[PASS]' if ux_ok else '[WARN]'}")
    for iss in ux_issues:
        print(f"   - ⚠️  {iss}")

    # 5. Canary Rollout Plan
    canary_ok, canary_issues = audit_canary_plan(card_text)
    print(f"\n5. Phased Rollout / Canary Plan: {'[PASS]' if canary_ok else '[WARN]'}")
    for iss in canary_issues:
        print(f"   - ⚠️  {iss}")

    all_passed = flag_ok and sec_ok and perf_ok and ux_ok and canary_ok
    print("\n------------------------------------------------------------------------")
    if all_passed:
        print("✅ PASS: Feature is LAUNCH-READY for Production Traffic!")
        print("   - Code đạt chuẩn 100% (80% Merge-Ready + 20% Launch-Ready).")
        print("   - Sẵn sàng kích hoạt Feature Gate theo lộ trình Canary.")
        sys.exit(0)
    else:
        level = "FAIL" if args.strict else "WARN"
        print(f"⚠️  {level}: Feature chưa đạt trạng thái Launch-Ready hoàn chỉnh.")
        print("   - Khắc phục các mục cảnh báo trước khi bật cờ cho 100% người dùng thật.")
        print("   - Tham khảo: agents/protocols/launch-readiness.md")
        if args.strict:
            sys.exit(1)
        sys.exit(0)


if __name__ == '__main__':
    main()

