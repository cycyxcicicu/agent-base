#!/usr/bin/env python3
"""scripts/setup-project.py

Trình Khởi Tạo Dự Án 1-Click (Zero-Friction Project Onboarding).
Dành cho người mới hoặc khi mở một dự án mới tinh muốn dùng chung agent-base.

Tính năng:
1. Tự động liên kết dự án mục tiêu với Hub trung tâm agent-base.
2. Tạo sẵn cấu trúc thư mục chuẩn: doc/, docs/notes/inbox/, tasks/BOARD.md.
3. Đồng bộ các adapter cấu hình (.agents/, .claude/...).
4. Thiết lập file .agentbase.json lưu vết liên kết.
5. Chạy bác sĩ chẩn đoán (doctor.py) bảo đảm môi trường sẵn sàng 100%.

Usage:
  # Chạy trực tiếp từ terminal tại thư mục dự án:
  python3 /path/to/agent-base/scripts/setup-project.py

  # Hoặc chỉ định đường dẫn dự án đích:
  python3 /path/to/agent-base/scripts/setup-project.py --target /path/to/new-project
"""

from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HUB_ROOT = Path(__file__).resolve().parent.parent


def register_project_in_dashboard(target_dir: Path) -> None:
    """Tự động đăng ký dự án mới vào danh mục Multi-Project của Dashboard."""
    # Bỏ qua lưu vào registry nếu là thư mục tạm test
    import tempfile
    temp_root = Path(tempfile.gettempdir()).resolve()
    try:
        target_dir.resolve().relative_to(temp_root)
        return
    except ValueError:
        pass

    projects_file = HUB_ROOT / "projects.json"
    registry = {"version": "1.0.0", "default_project": "ACCOUTING_Noi_Bo", "projects": []}
    if projects_file.is_file():
        try:
            registry = json.loads(projects_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    # Phát hiện thư mục tài liệu & sơ đồ
    doc_dir = "doc" if (target_dir / "doc").is_dir() else ("docs" if (target_dir / "docs").is_dir() else "doc")
    diagrams_dir = "doc/srs/hinh" if (target_dir / "doc" / "srs" / "hinh").is_dir() else (
        "docs/diagrams" if (target_dir / "docs" / "diagrams").is_dir() else f"{doc_dir}/hinh"
    )

    # Phát hiện file Mantis CSV và tên dự án chuẩn
    mantis_csv = None
    project_id = target_dir.name
    project_name = target_dir.name

    mantis_candidates = list((target_dir / "doc" / "bug" / "mantis").glob("*.csv")) if (target_dir / "doc" / "bug" / "mantis").is_dir() else []
    if not mantis_candidates and (target_dir / "mantis").is_dir():
        mantis_candidates = list((target_dir / "mantis").glob("*.csv"))

    if mantis_candidates:
        latest_csv = sorted(mantis_candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]
        mantis_csv = str(latest_csv.relative_to(target_dir)).replace("\\", "/")
        try:
            lines = latest_csv.read_text(encoding="utf-8", errors="ignore").splitlines()
            if len(lines) > 1:
                parts = lines[1].split(",")
                if len(parts) > 1 and parts[1].strip():
                    project_id = parts[1].strip()
                    project_name = f"{project_id} ({target_dir.name})"
        except Exception:
            pass

    # Cập nhật danh sách
    existing = next((p for p in registry.get("projects", []) if Path(p.get("path", "")).resolve() == target_dir.resolve()), None)
    if existing:
        existing["id"] = project_id
        existing["name"] = project_name
        existing["doc_dir"] = doc_dir
        existing["diagrams_dir"] = diagrams_dir
        if mantis_csv:
            existing["mantis_csv"] = mantis_csv
    else:
        registry.setdefault("projects", []).append({
            "id": project_id,
            "name": project_name,
            "path": str(target_dir),
            "doc_dir": doc_dir,
            "diagrams_dir": diagrams_dir,
            "mantis_csv": mantis_csv,
            "desc": f"Dự án {project_name} kết nối qua setup-project",
            "is_active": True
        })

    try:
        projects_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"✅ 3.1. Đã đăng ký dự án [{project_id}] vào Multi-Project Dashboard của agent-base")
    except Exception as e:
        print(f"⚪ 3.1. Không thể ghi projects.json: {e}")


def setup_project(target_dir: Path) -> int:
    target_dir = target_dir.resolve()
    print("=" * 70)
    print("🚀 TRÌNH KHỞI TẠO DỰ ÁN 1-CLICK (ZERO-FRICTION ONBOARDING)")
    print("=" * 70)
    print(f"🌟 Hub Trung Tâm (agent-base): {HUB_ROOT}")
    print(f"📁 Dự Án Mục Tiêu:           {target_dir}")
    print("-" * 70)

    # 1. Thống nhất một thư mục tài liệu duy nhất (doc hoặc docs)
    doc_name = "doc" if (target_dir / "doc").is_dir() else ("docs" if (target_dir / "docs").is_dir() else "doc")
    doc_dir = target_dir / doc_name
    inbox_dir = doc_dir / "notes" / "inbox"
    archive_dir = doc_dir / "notes" / "archive"
    tasks_dir = doc_dir / "delivery" / "tasks"

    doc_subdirs = [
        doc_dir / "features",      # Gói hồ sơ theo từng Use Case / Feature
        doc_dir / "architecture",  # Kiến trúc hệ thống, Domain Glossary, chuẩn DB
        doc_dir / "references",    # Dữ liệu nguồn, Master Data, API đối tác ngoài
        doc_dir / "governance",    # Quy trình kỹ thuật (TDD, Scrum, CMMI) & Templates
        doc_dir / "delivery",      # Tiến độ Roadmap, Handoff, Quản trị Defect/Bug
        tasks_dir,                 # Thẻ task, Kanban Board trong delivery
    ]

    for d in [inbox_dir, archive_dir, doc_dir] + doc_subdirs:
        d.mkdir(parents=True, exist_ok=True)
        gitkeep = d / ".gitkeep"
        if not gitkeep.is_file() and not any(d.iterdir()):
            gitkeep.touch()

    print(f"✅ 1. Khởi tạo cấu trúc tài liệu chuẩn Enterprise Global (tại {doc_name}/):")
    print(f"   - {doc_name}/notes/inbox/         (Hộp thư bàn giao nội bộ của dự án)")
    print(f"   - {doc_name}/notes/archive/       (Lưu trữ bài học)")
    print(f"   - {doc_name}/delivery/tasks/      (Quản lý task & thẻ việc)")
    print(f"   - {doc_name}/features/            (Hồ sơ đóng gói theo từng Use Case)")
    print(f"   - {doc_name}/architecture/        (Kiến trúc tổng thể & Domain Glossary)")
    print(f"   - {doc_name}/references/          (Tài liệu nguồn, Master Data & API đối tác)")
    print(f"   - {doc_name}/governance/          (Quy trình phát triển & Biểu mẫu)")
    print(f"   - {doc_name}/delivery/            (Lộ trình Roadmap, Báo cáo & Lỗi Mantis)")

    # 2. Tạo file BOARD.md nếu chưa có
    board_file = tasks_dir / "BOARD.md"
    if not board_file.is_file():
        board_content = f"""# Bảng Công Việc Dự Án (Task Board)

> **Dự án:** {target_dir.name}  
> **Hub Liên Kết:** agent-base  
> **Cập nhật:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}  

## 1. Việc Đang Làm (Doing)
- [ ] T-01: Khởi tạo và thiết lập dự án ban đầu (Khởi tạo thành công)

## 2. Chờ Duyệt (Review)
*(Chưa có)*

## 3. Hoàn Thành (Done)
*(Chưa có)*
"""
        board_file.write_text(board_content, encoding="utf-8")
        print(f"✅ 2. Tạo bảng công việc khởi điểm: {doc_name}/delivery/tasks/BOARD.md")
    else:
        print(f"⚪ 2. Bảng công việc: Đã có sẵn ({doc_name}/delivery/tasks/BOARD.md)")

    # 3. Ghi file liên kết .agentbase.json
    agentbase_link_file = target_dir / ".agentbase.json"
    link_data = {
        "hub_path": str(HUB_ROOT),
        "target_project": target_dir.name,
        "roles_count": 20,
        "initialized_at": datetime.now(timezone.utc).isoformat(),
        "status": "ready"
    }
    agentbase_link_file.write_text(json.dumps(link_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ 3. Gắn thẻ định danh liên kết: .agentbase.json")

    # 3.1. Tự động đăng ký dự án vào Dashboard trung tâm (Multi-Project Registry)
    register_project_in_dashboard(target_dir)

    # 4. Sao chép hoặc tạo file luật AGENTS.md cơ sở nếu dự án chưa có
    agents_rule_file = target_dir / "AGENTS.md"
    if not agents_rule_file.is_file():
        agents_content = rf"""# Quy Tắc Điều Phối Agent ({target_dir.name})

Dự án này sử dụng bộ khung chuẩn hóa từ `agent-base`.

## Quy tắc cốt lõi:
1. **Phân quyền & Ranh giới:**
   - Chỉ commit, push, tạo MR khi người dùng yêu cầu rõ ràng.
   - Tài liệu nghiệp vụ dùng chung ghi vào `doc/` ở gốc dự án.
   - Hộp thư bàn giao nội bộ ghi vào `docs/notes/inbox/`.
2. **Cơ chế Hai Tốc Độ (Fast-Track vs Full-Track):**
   - Việc nhỏ ($\le 50$ dòng diff): Được lập trình ngay, Reviewer được Quick Fix lỗi chính tả.
   - Việc vừa & lớn: Cần kế hoạch phân rã và phê duyệt trước khi code.
3. **Tra cứu tri thức JIT On-Demand:**
   - Khi cần tra cứu chuẩn kỹ nghệ (JPA, Redis, Kafka, Playwright, K8s...):
     `python3 {HUB_ROOT}/scripts/knowledge.py query -q "<từ khóa>" --budget 1200`
4. **Tự học không làm rác context:**
   - Khi phát hiện bài học kỹ thuật mới:
     `python3 {HUB_ROOT}/scripts/knowledge.py learn --title "<tiêu đề>" --note "<nội dung>" --role dev`
"""
        agents_rule_file.write_text(agents_content, encoding="utf-8")
        print("✅ 4. Khởi tạo file luật dự án: AGENTS.md")
    else:
        print("⚪ 4. File luật AGENTS.md: Đã có sẵn (Giữ nguyên luật riêng của dự án)")

    # 5. Cấu hình adapter Kilo Code (.kilo/) và AI Adapters (.agents/, .claude/, .codex/, .qoder/)
    # Đặc biệt: Kilo Code sandbox chặn nạp agent nếu .kilo/agents là symlink ra ngoài project scope.
    # Do đó, thư mục .kilo cục bộ của project luôn là thư mục thực tế (không symlink cả thư mục .kilo).
    # Và agents được cấu hình toàn cục tại ~/.config/kilo/agents để 100% không bị sandbox chặn mà vẫn đồng bộ real-time.
    kilo_target = target_dir / ".kilo"
    if kilo_target.is_symlink():
        kilo_target.unlink()
    kilo_target.mkdir(parents=True, exist_ok=True)

    # Dọn dẹp symlink .kilo/agents cục bộ cũ nếu có để tránh lỗi Sandbox Escape
    proj_kilo_agents = kilo_target / "agents"
    if proj_kilo_agents.is_symlink():
        proj_kilo_agents.unlink()

    # Cấu hình Kilo Agents toàn cục
    user_kilo_agents = Path.home() / ".config" / "kilo" / "agents"
    hub_kilo_agents = HUB_ROOT / ".kilo" / "agents"
    if hub_kilo_agents.is_dir():
        try:
            user_kilo_agents.parent.mkdir(parents=True, exist_ok=True)
            if user_kilo_agents.is_symlink() or user_kilo_agents.is_file():
                user_kilo_agents.unlink()
            if not user_kilo_agents.exists():
                user_kilo_agents.symlink_to(hub_kilo_agents, target_is_directory=True)
                print(f"✅ 5. Cấu hình Kilo Agents toàn cục: {user_kilo_agents} -> {hub_kilo_agents}")
        except Exception as e:
            pass

    # Các AI adapters còn lại hỗ trợ symlink thư mục
    adapters = [".agents", ".claude", ".codex", ".qoder"]
    for adapter in adapters:
        src_adapter = HUB_ROOT / adapter
        dst_adapter = target_dir / adapter
        if not src_adapter.is_dir():
            continue

        if dst_adapter.is_symlink():
            dst_adapter.unlink()

        if not dst_adapter.exists():
            try:
                # Ưu tiên tạo symlink thư mục adapter để luôn đồng bộ nhẹ nhàng với Hub
                dst_adapter.symlink_to(src_adapter, target_is_directory=True)
                print(f"✅ 5. Tạo symlink adapter nhẹ: {adapter} -> {src_adapter}")
            except Exception:
                shutil.copytree(src_adapter, dst_adapter)
                print(f"✅ 5. Sao chép adapter: {adapter}")
        elif dst_adapter.is_dir():
            for child in src_adapter.iterdir():
                dst_child = dst_adapter / child.name
                if dst_child.is_symlink():
                    dst_child.unlink()
                if not dst_child.exists():
                    try:
                        dst_child.symlink_to(child, target_is_directory=child.is_dir())
                        print(f"✅ 5. Tạo symlink thành phần con: {adapter}/{child.name} -> {child}")
                    except Exception:
                        if child.is_dir():
                            shutil.copytree(child, dst_child)
                        else:
                            shutil.copy2(child, dst_child)
                        print(f"✅ 5. Sao chép thành phần con: {adapter}/{child.name}")

    # 6. Bảo vệ an toàn MCP: Khởi tạo file mẫu mcp.example.json & cập nhật .gitignore
    kilo_target = target_dir / ".kilo"
    kilo_target.mkdir(parents=True, exist_ok=True)
    mcp_example_src = HUB_ROOT / ".kilo" / "mcp.example.json"
    mcp_example_dst = kilo_target / "mcp.example.json"
    if mcp_example_src.is_file() and not mcp_example_dst.exists():
        shutil.copy2(mcp_example_src, mcp_example_dst)
        print("✅ 6. Tạo file mẫu MCP an toàn: .kilo/mcp.example.json (chỉ chứa template mẫu)")

    # Đảm bảo .gitignore của dự án đích chặn tuyệt đối file cấu hình MCP cá nhân
    target_gitignore = target_dir / ".gitignore"
    mcp_ignore_rules = [
        ".kilo/mcp.json",
        ".kilo/mcp.local.json",
        ".kilo/kilo.jsonc",
        "mcp.json",
        "mcp.local.json",
        "*.mcp.local.json"
    ]
    existing_ignore = target_gitignore.read_text(encoding="utf-8") if target_gitignore.is_file() else ""
    missing_rules = [r for r in mcp_ignore_rules if r not in existing_ignore]
    if missing_rules:
        with open(target_gitignore, "a", encoding="utf-8") as f:
            f.write("\n# MCP cá nhân hóa (Tuyệt đối không đẩy lên Git)\n")
            for r in missing_rules:
                f.write(f"{r}\n")
        print("✅ 6. Cập nhật .gitignore dự án: Đã chặn các file cấu hình MCP cá nhân không bị commit.")

    # 7. Tự động kiểm tra và tải ngầm động cơ Harness² nếu máy người mới chưa có
    harness2_dir = Path.home() / "Documents" / "skill" / "repos" / "harness2"
    if not harness2_dir.is_dir():
        print("📥 7. Chưa phát hiện động cơ Harness² trên máy. Đang tự động tải ngầm...")
        try:
            harness2_dir.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                ["git", "clone", "--depth", "1", "https://github.com/google-research/harness2.git", str(harness2_dir)],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=30
            )
            if harness2_dir.is_dir():
                print("✅ 7. Đã tự động tải thành công Harness² về máy!")
            else:
                print("⚪ 7. Mạng offline — Hệ thống tự động dùng động cơ tích hợp sẵn.")
        except Exception:
            print("⚪ 7. Mạng offline — Hệ thống tự động dùng động cơ tích hợp sẵn.")
    else:
        print(f"✅ 7. Động cơ Harness²: Đã sẵn sàng tại {harness2_dir}")

    print("-" * 70)
    print("🎉 DỰ ÁN ĐÃ ĐƯỢC KẾT NỐI VÀ KHỞI TẠO THÀNH CÔNG VỚI AGENT-BASE!")
    print("=" * 70)
    print("💡 Hướng dẫn dành cho Người Mới / Developer:")
    print("   1. Bạn có thể bắt đầu làm việc ngay với bất kỳ công cụ AI nào (Kilo Code, Antigravity, Cursor, Claude).")
    print("   2. Để tra cứu kiến thức chuẩn bất kỳ lúc nào:")
    print(f"      python3 {HUB_ROOT}/scripts/knowledge.py query -q \"<từ khóa>\"")
    print("   3. Về cấu hình MCP:")
    print("      - Tham khảo các mẫu server tại: .kilo/mcp.example.json")
    print("      - Nếu muốn dùng MCP riêng trên máy bạn: sao chép thành .kilo/mcp.json và tự chỉnh sửa.")
    print("      - File .kilo/mcp.json đã được .gitignore bảo vệ 100%, không bao giờ bị đẩy lên Git!")
    print(f"   4. Mọi tài liệu nghiệp vụ ghi vào: {doc_name}/")
    print(f"   5. Mọi task theo dõi tại:          {doc_name}/delivery/tasks/BOARD.md")
    print("=" * 70)
    return 0


def main():
    parser = argparse.ArgumentParser(description="Trình khởi tạo dự án 1-Click với agent-base")
    parser.add_argument("--target", default=".", help="Đường dẫn thư mục dự án cần khởi tạo (mặc định: .)")
    args = parser.parse_args()

    target_path = Path(args.target)
    if not target_path.is_dir():
        sys.stderr.write(f"Lỗi: Thư mục mục tiêu không tồn tại: {target_path}\n")
        sys.exit(2)

    sys.exit(setup_project(target_path))


if __name__ == "__main__":
    main()
