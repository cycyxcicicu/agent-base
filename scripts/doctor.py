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
    errors = 0

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
    print(f"  {check_mark(env_example.exists())} Mẫu cấu hình môi trường (.env.example): {'Có sẵn' if env_example.exists() else 'Thiếu'}")

    # Hook git chỉ có tác dụng khi core.hooksPath trỏ vào .githooks. Đây là cấu hình cục bộ, không đi kèm khi clone,
    # nên bản clone mới không có hook mà không ai biết. Chỉ cảnh báo (không tính là lỗi); bỏ qua trên CI.
    if (ROOT_DIR / ".git").exists() and not os.environ.get("CI"):
        try:
            hooks_path = subprocess.run(
                ["git", "-C", str(ROOT_DIR), "config", "--get", "core.hooksPath"], capture_output=True, text=True
            ).stdout.strip()
        except Exception:
            hooks_path = ""
        hooks_on = hooks_path.replace("\\", "/").rstrip("/").endswith(".githooks")
        if hooks_on:
            print("  ✅ Hook git (core.hooksPath): đã bật")
        else:
            print("  ⚠️ Hook git (core.hooksPath): CHƯA BẬT trên bản clone này. Chạy: python scripts/install-hooks.py")

    # --------------------------------------------------------------------------
    # MỤC 3: KIỂM TRA NHỮNG GÌ SẼ THIẾU KHI TẢI VỀ MÁY MỚI (VÀ CÁCH XỬ LÝ)
    # --------------------------------------------------------------------------
    print("\n3️⃣ KIỂM TRA CÁC TỆP CẤU HÌNH CỤC BỘ (LOCAL SECRETS & COOKIES):")
    real_env = ROOT_DIR / ".env"
    user_home_env = Path.home() / ".gemini" / ".env"
    agent_home_env = Path.home() / ".agent-base" / ".env"

    has_env = real_env.exists() or user_home_env.exists() or agent_home_env.exists()
    is_onedrive = any(cloud in str(ROOT_DIR).lower() for cloud in ["onedrive", "dropbox", "google drive", "box sync"])

    if user_home_env.exists():
        print(f"  {info_mark(True)} Tệp môi trường: ĐÃ CÓ AN TOÀN NGOÀI ONEDRIVE ({user_home_env})")
    elif agent_home_env.exists():
        print(f"  {info_mark(True)} Tệp môi trường: ĐÃ CÓ AN TOÀN NGOÀI ONEDRIVE ({agent_home_env})")
    elif real_env.exists():
        if is_onedrive:
            print(f"  ⚠️ Tệp môi trường: ĐANG NẰM TRONG ONEDRIVE ({real_env}) - NGUY CƠ RÒ RỈ TOKEN ĐỒNG BỘ!")
        else:
            print(f"  {info_mark(True)} Tệp môi trường (.env): ĐÃ CÓ CỤC BỘ")
    else:
        print(f"  {info_mark(False)} Tệp môi trường (.env): CHƯA CÓ (Bình thường trên máy mới)")

    # --------------------------------------------------------------------------
    # MỤC 4: KIỂM TRA KHO KỸ NĂNG & QUARANTINE (SKILLS & AGENT RUNTIME)
    # --------------------------------------------------------------------------
    print("\n4️⃣ KIỂM TRA KHO KỸ NĂNG & QUARANTINE (SKILLS & AGENT RUNTIME):")
    local_config = ROOT_DIR / "skills.config.local.json"
    config_file = local_config if local_config.exists() else (ROOT_DIR / "skills.config.json")
    skills_dir = ROOT_DIR / ".agents" / "skills"
    has_config = config_file.exists() or bool(os.environ.get("SKILLS_QUARANTINE_DIR"))
    quarantine_ok = False
    quarantine_desc = "Chưa cấu hình"
    skills_count = 0

    if has_config:
        try:
            import json
            cfg_data = json.loads(config_file.read_text(encoding="utf-8")) if config_file.exists() else {}
            q_dir = os.environ.get("SKILLS_QUARANTINE_DIR") or cfg_data.get("quarantine_dir", "")
            if q_dir:
                p_q = Path(q_dir).expanduser()
                if p_q.exists():
                    quarantine_ok = True
                    quarantine_desc = str(p_q)
                else:
                    quarantine_desc = f"{p_q} (Thư mục không tồn tại trên máy này)"
        except Exception:
            pass

    if skills_dir.exists():
        skills_count = len([d for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()])

    if quarantine_ok and skills_count >= 20:
        print(f"  ✅ Kho kỹ năng: Đã sẵn sàng ({skills_count} skills tại {skills_dir.name}/, kho quarantine: {quarantine_desc})")
    elif os.environ.get("CI") and skills_count >= 20:
        # Máy chủ CI không có kho kiểm dịch (nó nằm trên máy người dùng) nên chỉ cảnh báo, không làm đỏ CI.
        print(f"  ⚠️ Kho kỹ năng: có {skills_count} skills trong {skills_dir.name}/ nhưng không có kho quarantine ({quarantine_desc}); bỏ qua trong CI.")
    else:
        errors += 1
        print(f"  ❌ Kho kỹ năng: CHƯA SẴN SÀNG ({skills_count} skills trong .agents/skills, cần tối thiểu 20; quarantine: {quarantine_desc})")
        print("     👉 BẮT BUỘC CHẠY THIẾT LẬP TRƯỚC KHI DÙNG AGENT:")
        print("        - Windows (PowerShell): .\\setup.ps1 (hoặc: python scripts/setup-skills.py)")
        print("        - macOS / Linux:        ./setup.sh  (hoặc: python3 scripts/setup-skills.py)")

    # --------------------------------------------------------------------------
    # MỤC 5: HƯỚNG DẪN CẤU HÌNH DÀNH CHO NGƯỜI DÙNG MỚI
    # --------------------------------------------------------------------------
    print("\n5️⃣ HƯỚNG DẪN CẤU HÌNH & VẬN HÀNH:")
    if not has_env:
        print("  💡 CHẾ ĐỘ HOÀN TOÀN TỰ CHỦ (OFFLINE / ZERO CONFIG):")
        print("     - Hệ thống agent-base sẵn sàng hoạt động 100% không bắt buộc token API bên ngoài.")
        print("     - Toàn bộ các chức năng kỹ nghệ cốt lõi dưới đây VẪN CHẠY HOÀN TOÀN TỰ ĐỘNG:")
        print("       * Đồ thị phân rã Tracer-Bullet DAG & Tìm đường biên Frontier (`agent_core/workflow/`)")
        print("       * Quét phòng thủ Red-teaming 7 véc-tơ & Giải mã Deobfuscator (`agent_core/eval/`)")
        print("       * Hệ thống Design Tokens & Kiểm định độ tương phản WCAG 2.1 AA/AAA (`agent_core/design/`)")
        print("       * Sổ cái nợ kỹ thuật DebtLedger & Cổng chặn Pre-Commit Gate (`agent_core/debt/`)")
        print("       * Bóc tách bảng tính Excel (.xlsx nhị phân) và làm sạch Web rác (`agent_core/ingest/`)")
        print("       * Toàn bộ 20 vai trò Agent & các kịch bản mô phỏng đa tác tử (`agents/roles/`)")
        print("     - Khi cần kết nối API LLM thật, sao chép `.env.example` thành `.env` để cấu hình key.")
    else:
        print("  🎉 Máy hiện tại đã có cấu hình thông tin xác thực cục bộ!")

    if not py_ok:
        errors += 1
    if not has_gitignore:
        errors += 1

    # --------------------------------------------------------------------------
    # MỤC 6: CHẠY THỬ NGHIỆM CHỨNG THỰC LÕI NỘI BỘ (SANITY SELF-CHECK)
    # --------------------------------------------------------------------------
    print("\n6️⃣ KIỂM TRA SỨC KHỎE CÁC MÔ-ĐUN KỸ NGHỆ (CORE HEALTH CHECK):")
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
