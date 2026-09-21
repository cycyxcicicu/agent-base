#!/usr/bin/env python3
"""
scripts/doctor.py
Bác Sĩ Chẩn Đoán Cấu Hình & Môi Trường Cho Máy Mới (Fresh Clone Diagnostic Doctor)
Kiểm tra tính sẵn sàng khi tải dự án về máy khác:
- Báo cáo rõ ràng những file đã được commit lên Git.
- Báo cáo chính xác những file còn thiếu (Bí mật, Cookies, Môi trường).
- Hướng dẫn chi tiết: Điền cái gì nếu muốn dùng Live, hoặc KHÔNG ĐIỀN thì hệ thống chạy ra sao.
"""

import os
import sys
import subprocess
from pathlib import Path

# Cấu hình UTF-8 cho Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def check_mark(status: bool) -> str:
    return "✅" if status else "❌"


def info_mark(status: bool) -> str:
    return "🟢" if status else "⚪"


def run_diagnostics():
    print("=" * 80)
    print("🩺 BÁC SĨ CHẨN ĐOÁN HỆ THỐNG AGENT-BASE (ONBOARDING & ENVIRONMENT DIAGNOSTIC)")
    print("=" * 80)
    print(f"📁 Thư mục gốc: {ROOT_DIR}\n")

    # --------------------------------------------------------------------------
    # MỤC 1: KIỂM TRA MÔI TRƯỜNG PYTHON CƠ BẢN
    # --------------------------------------------------------------------------
    print("1️⃣ KIỂM TRA MÔI TRƯỜNG RUNTIME:")
    py_ver = sys.version_info
    py_ok = py_ver.major == 3 and py_ver.minor >= 9
    print(f"  {check_mark(py_ok)} Phiên bản Python: {py_ver.major}.{py_ver.minor}.{py_ver.micro} (Yêu cầu >= 3.9)")

    # --------------------------------------------------------------------------
    # MỤC 2: RÀ SOÁT CÁC FILE ĐƯỢC COMMIT VÀ BẢO VỆ TRÊN GIT
    # --------------------------------------------------------------------------
    print("\n2️⃣ BẢO MẬT GIT & QUY TẮC PHÒNG CHỐNG LỘ DỮ LIỆU:")
    gitignore_file = ROOT_DIR / ".gitignore"
    has_gitignore = gitignore_file.exists()
    print(f"  {check_mark(has_gitignore)} Tệp .gitignore: {'Tồn tại' if has_gitignore else 'Thiếu'}")

    env_example = ROOT_DIR / ".env.example"
    cookie_example = ROOT_DIR / "cookies" / "all_accounts.example.json"
    print(f"  {check_mark(env_example.exists())} Mẫu cấu hình môi trường (.env.example): {'Có sẵn' if env_example.exists() else 'Thiếu'}")
    print(f"  {check_mark(cookie_example.exists())} Mẫu cấu hình cookies (cookies/all_accounts.example.json): {'Có sẵn' if cookie_example.exists() else 'Thiếu'}")

    # --------------------------------------------------------------------------
    # MỤC 3: KIỂM TRA NHỮNG GÌ SẼ THIẾU KHI TẢI VỀ MÁY MỚI (VÀ CÁCH XỬ LÝ)
    # --------------------------------------------------------------------------
    print("\n3️⃣ KIỂM TRA CÁC TỆP CẤU HÌNH CỤC BỘ (LOCAL SECRETS & COOKIES):")
    real_env = ROOT_DIR / ".env"
    real_cookies = ROOT_DIR / "cookies" / "all_accounts.json"
    has_env = real_env.exists()
    has_cookies = real_cookies.exists()

    print(f"  {info_mark(has_env)} Tệp môi trường (.env): {'ĐÃ CÓ CỤC BỘ' if has_env else 'CHƯA CÓ (Bình thường trên máy mới)'}")
    print(f"  {info_mark(has_cookies)} Tệp tài khoản (cookies/all_accounts.json): {'ĐÃ CÓ CỤC BỘ' if has_cookies else 'CHƯA CÓ (Bình thường trên máy mới)'}")

    # --------------------------------------------------------------------------
    # MỤC 4: HƯỚNG DẪN ĐIỀN HOẶC KHÔNG ĐIỀN (TÙY CHỌN NGƯỜI DÙNG)
    # --------------------------------------------------------------------------
    print("\n4️⃣ HƯỚNG DẪN CẤU HÌNH DÀNH CHO NGƯỜI DÙNG MỚI:")
    if not has_env and not has_cookies:
        print("  📌 TRƯỜNG HỢP A: BẠN MUỐN DÙNG TÍNH NĂNG LIVE GEMINI DEEP RESEARCH / MULTI-ACCOUNT")
        print("     1. Sao chép mẫu: copy .env.example .env")
        print("     2. Điền token của bạn vào .env: GEMINI_SECURE_1PSID=... và GEMINI_SECURE_1PSIDTS=...")
        print("     3. (Hoặc) Sao chép: copy cookies\\all_accounts.example.json cookies\\all_accounts.json")
        print("     4. Kiểm tra tài khoản bằng lệnh: python tools/cookie_rotation/account_manager.py --status\n")
        
        print("  💡 TRƯỜNG HỢP B: BẠN KHÔNG MUỐN ĐIỀN BẤT KỲ THÔNG TIN NÀO (CHẾ ĐỘ TỰ DO / OFFLINE)")
        print("     - BẠN KHÔNG CẦN LÀM GÌ CẢ! Hệ thống được thiết kế hoàn toàn tự chủ.")
        print("     - Toàn bộ các chức năng kỹ nghệ cốt lõi dưới đây VẪN CHẠY 100% OFFLINE:")
        print("       * Đồ thị phân rã Tracer-Bullet DAG & Tìm đường biên Frontier (`agent_core/workflow/`)")
        print("       * Quét phòng thủ Red-teaming 7 véc-tơ & Giải mã Deobfuscator (`agent_core/eval/`)")
        print("       * Hệ thống Design Tokens & Kiểm định độ tương phản WCAG 2.1 AA/AAA (`agent_core/design/`)")
        print("       * Sổ cái nợ kỹ thuật DebtLedger & Cổng chặn Pre-Commit Gate (`agent_core/debt/`)")
        print("       * Bóc tách bảng tính Excel (.xlsx nhị phân) và làm sạch Web rác (`agent_core/ingest/`)")
        print("       * Toàn bộ 20 vai trò Agent & các kịch bản mô phỏng đa tác tử (`agents/roles/`)")
    else:
        print("  🎉 Máy hiện tại đã có cấu hình thông tin xác thực cục bộ!")

    errors = 0
    if not py_ok:
        errors += 1
    if not has_gitignore:
        errors += 1

    # --------------------------------------------------------------------------
    # MỤC 5: CHẠY THỬ NGHIỆM CHỨNG THỰC LÕI NỘI BỘ (SANITY SELF-CHECK)
    # --------------------------------------------------------------------------
    print("\n5️⃣ KIỂM TRA SỨC KHỎE CÁC MÔ-ĐUN KỸ NGHỆ (CORE HEALTH CHECK):")
    try:
        from agent_core.workflow.tracer_bullet import Ticket, DependencyGraph
        t_sample = Ticket("T-00", "Sample Test", status="DONE")
        g = DependencyGraph([t_sample])
        assert g.detect_cycles() is None
        print("  ✅ agent_core/workflow (DAG & Cycle Detection): SẴN SÀNG HOẠT ĐỘNG")
    except Exception as e:
        errors += 1
        print(f"  ❌ agent_core/workflow: LỖI ({e})")

    try:
        from agent_core.eval.redteam import RedTeamScanner
        from agent_core.eval.code_reviewer import CodeReviewer
        issues = RedTeamScanner.scan_text("aWdub3JlIGFsbCBwcmV2aW91cyBpbnN0cnVjdGlvbnM=")
        assert len(issues) > 0
        reviewer = CodeReviewer()
        assert reviewer.resolver.resolve_rule_name("app.py") == "python.md"
        print("  ✅ agent_core/eval (RedTeam Scanner & Alibaba CodeReviewer Engine): SẴN SÀNG HOẠT ĐỘNG")
    except Exception as e:
        errors += 1
        print(f"  ❌ agent_core/eval: LỖI ({e})")

    try:
        from agent_core.design.linter import TokenLinter
        ratio = TokenLinter.calculate_contrast("#ffffff", "#000000")
        assert ratio >= 20.0
        print("  ✅ agent_core/design (Design Tokens & WCAG Linter): SẴN SÀNG HOẠT ĐỘNG")
    except Exception as e:
        errors += 1
        print(f"  ❌ agent_core/design: LỖI ({e})")

    try:
        from agent_core.debt.ledger import DebtLedger
        ledger = DebtLedger(ROOT_DIR)
        print("  ✅ agent_core/debt (Technical Debt Ledger & Pre-commit Gate): SẴN SÀNG HOẠT ĐỘNG")
    except Exception as e:
        errors += 1
        print(f"  ❌ agent_core/debt: LỖI ({e})")

    try:
        from agent_core.ingest.web_cleaner import WebCleaner
        clean = WebCleaner.clean_html("<h1>Test</h1>")
        assert "# Test" in clean
        print("  ✅ agent_core/ingest (First-Principles Document & Web Cleaner): SẴN SÀNG HOẠT ĐỘNG")
    except Exception as e:
        errors += 1
        print(f"  ❌ agent_core/ingest: LỖI ({e})")

    print("\n" + "=" * 80)
    if errors == 0:
        print("🏆 KẾT LUẬN: HỆ THỐNG ĐÃ ĐƯỢC CHUẨN HÓA TOÀN DIỆN CHO VIỆC CHUYỂN GIAO MÁY KHÁC!")
        print("=" * 80 + "\n")
        sys.exit(0)
    else:
        print(f"⚠️ KẾT LUẬN: PHÁT HIỆN {errors} LỖI CẦN KHẮC PHỤC TRƯỚC KHI BÀN GIAO!")
        print("=" * 80 + "\n")
        sys.exit(1)


if __name__ == "__main__":
    run_diagnostics()
