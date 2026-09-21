#!/usr/bin/env python3
"""
scripts/fetch-skills.py
Bộ Kéo & Cài Đặt Tự Động Kỹ Năng Đã Phê Duyệt (Skill Fetcher & Installer)
Đọc sổ đăng ký `agents/knowledge/skills.md`, kiểm tra các skill còn thiếu trong `.agents/skills/`
và tự động tải/sao chép từ nguồn phê duyệt vào dự án.

Sử dụng:
  python scripts/fetch-skills.py            # Kiểm tra và tải các skill còn thiếu
  python scripts/fetch-skills.py --status   # Chỉ kiểm tra trạng thái các skill
  python scripts/fetch-skills.py --force    # Tải lại toàn bộ đè lên bản cũ
"""

import os
import sys
import shutil
import tempfile
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

# Cấu hình UTF-8 cho Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT_DIR / ".agents" / "skills"
REGISTRY_FILE = ROOT_DIR / "agents" / "knowledge" / "skills.md"

# Bản đồ ánh xạ thư mục con bên trong các kho nguồn
SUBFOLDER_MAP = {
    "grilling": "skills/engineering/grilling",
    "writing-for-agents": "skills/productivity/writing-for-agents",
    "domain-modeling": "skills/engineering/domain-modeling",
    "codebase-design": "skills/engineering/codebase-design",
    "to-spec": "skills/engineering/to-spec",
    "to-tickets": "skills/engineering/to-tickets",
    "ponytail-debt": "skills/ponytail-debt",
    "architecture-decision-records": "skills/architecture-decision-records",
    "subagent-driven-development": "skills/subagent-driven-development",
    "systematic-debugging": "skills/systematic-debugging",
    "open-code-review": "skills/open-code-review",
    "i-have-adhd": "skills/i-have-adhd",
}

# Bản đồ ánh xạ nguồn kiểm dịch cục bộ (nếu có trên máy dev)
LOCAL_QUARANTINE_MAP = {
    "diagram-design": Path("D:/skills-quarantine/diagram-design"),
    "grilling": Path("D:/skills-quarantine/pocock-skills/skills/engineering/grilling"),
    "writing-for-agents": Path("D:/skills-quarantine/pocock-skills/skills/productivity/writing-for-agents"),
    "domain-modeling": Path("D:/skills-quarantine/pocock-skills/skills/engineering/domain-modeling"),
    "codebase-design": Path("D:/skills-quarantine/pocock-skills/skills/engineering/codebase-design"),
    "to-spec": Path("D:/skills-quarantine/pocock-skills/skills/engineering/to-spec"),
    "to-tickets": Path("D:/skills-quarantine/pocock-skills/skills/engineering/to-tickets"),
    "ponytail-debt": Path("D:/skills-quarantine/ponytail/skills/ponytail-debt"),
    "architecture-decision-records": Path("D:/skills-quarantine/ECC/skills/architecture-decision-records"),
    "subagent-driven-development": Path("D:/skills-quarantine/superpowers/skills/subagent-driven-development"),
    "systematic-debugging": Path("D:/skills-quarantine/superpowers/skills/systematic-debugging"),
    "ui-ux-pro-max": Path("D:/skills-quarantine/ui-ux-pro-max-skill"),
    "open-code-review": Path("D:/skills-quarantine/open-code-review/skills/open-code-review"),
    "i-have-adhd": Path("D:/skills-quarantine/i-have-adhd/skills/i-have-adhd"),
    "plan-ceo-review": Path("D:/skills-quarantine/gstack/plan-ceo-review"),
    "plan-eng-review": Path("D:/skills-quarantine/gstack/plan-eng-review"),
    "cso": Path("D:/skills-quarantine/gstack/cso"),
    "ship": Path("D:/skills-quarantine/gstack/ship"),
    "archify": Path("D:/skills-quarantine/archify/archify"),
    "archify-review": Path("D:/skills-quarantine/archify/.agents/skills/archify-review"),
    "swarm-orchestration": Path("D:/skills-quarantine/ruflo/.agents/skills/swarm-orchestration"),
    "sparc-methodology": Path("D:/skills-quarantine/ruflo/.agents/skills/sparc-methodology"),
    "careful": Path("D:/skills-quarantine/gstack/careful"),
    "browse": Path("D:/skills-quarantine/gstack/browse"),
    "qa-web": Path("D:/skills-quarantine/gstack/qa"),
    "office-hours": Path("D:/skills-quarantine/gstack/office-hours"),
    "investigate": Path("D:/skills-quarantine/gstack/investigate"),
    "devex-review": Path("D:/skills-quarantine/gstack/devex-review"),
}




def parse_registry() -> List[Dict[str, str]]:
    """Đọc và bóc tách bảng kỹ năng đã duyệt từ agents/knowledge/skills.md."""
    if not REGISTRY_FILE.exists():
        print(f"❌ Không tìm thấy sổ đăng ký: {REGISTRY_FILE}")
        return []

    lines = REGISTRY_FILE.read_text(encoding="utf-8", errors="replace").splitlines()
    skills = []
    in_table = False

    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) < 6:
            continue
        name = parts[0]
        url = parts[1]
        version = parts[2]
        if name in ["Skill", "---", ":---"]:
            continue
        if name and not name.startswith("-"):
            skills.append({
                "name": name,
                "url": url,
                "version": version
            })
    return skills


def fetch_skill(skill_info: Dict[str, str], force: bool = False) -> bool:
    name = skill_info["name"]
    url = skill_info["url"]
    target_dir = SKILLS_DIR / name

    # Nếu là bản chắt lọc tự viết nội bộ
    if "Tự viết" in url or not url.startswith("http"):
        if (target_dir / "SKILL.md").exists():
            print(f"  ✨ [{name}] Bản chuẩn chắt lọc nội bộ đã sẵn sàng tại .agents/skills/{name}")
            return True
        print(f"  ⚠️ [{name}] Bản tự viết nội bộ chưa có tại .agents/skills/{name}. Vui lòng kiểm tra.")
        return False

    if target_dir.exists() and (target_dir / "SKILL.md").exists() and not force:
        print(f"  ✅ [{name}] Đã có sẵn tại .agents/skills/{name}")
        return True

    print(f"  📥 [{name}] Đang nạp từ nguồn: {url}...")

    # 1. Kiểm tra nguồn kiểm dịch cục bộ trước (Nhanh & Không tốn mạng)
    local_src = LOCAL_QUARANTINE_MAP.get(name)
    if local_src and local_src.exists() and (local_src / "SKILL.md").exists():
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(local_src, target_dir, dirs_exist_ok=True)
        print(f"  ✨ [{name}] Đã sao chép thành công từ kho nội bộ: {local_src}")
        return True

    # 2. Tải qua Git Clone nếu là remote URL
    if url.startswith("http"):
        with tempfile.TemporaryDirectory() as tmp_dir:

            tmp_path = Path(tmp_dir)
            try:
                # Clone shallow với độ sâu 1
                cmd = ["git", "clone", "--depth", "1", url, str(tmp_path / "repo")]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                if res.returncode != 0:
                    print(f"  ⚠️ Lỗi clone {url}: {res.stderr.strip()}")
                    return False

                repo_path = tmp_path / "repo"
                sub_path = SUBFOLDER_MAP.get(name)
                source_dir = (repo_path / sub_path) if sub_path else repo_path

                if not (source_dir / "SKILL.md").exists():
                    # Thử tìm SKILL.md bất kỳ đâu trong repo
                    found = list(repo_path.rglob("SKILL.md"))
                    if found:
                        source_dir = found[0].parent

                if (source_dir / "SKILL.md").exists():
                    target_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)
                    print(f"  🚀 [{name}] Đã tải về và cài đặt thành công!")
                    return True
                else:
                    print(f"  ❌ [{name}] Không tìm thấy SKILL.md trong repository tải về!")
                    return False
            except Exception as e:
                print(f"  ❌ [{name}] Thất bại khi tải: {e}")
                return False

    print(f"  ⚪ [{name}] Nguồn '{url}' là cục bộ hoặc chưa hỗ trợ tự tải. Vui lòng chép thủ công.")
    return False


def main():
    parser = argparse.ArgumentParser(description="Tự động kiểm tra và tải các kỹ năng đã đăng ký")
    parser.add_argument("--status", action="store_true", help="Chỉ kiểm tra trạng thái hiện tại")
    parser.add_argument("--force", action="store_true", help="Tải lại đè lên các skill đã có")
    args = parser.parse_args()

    SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    skills = parse_registry()

    print("\n" + "=" * 80)
    print(f"📦 BỘ ĐIỀU PHỐI KỸ NĂNG AGENT-BASE (TỔNG CỘNG: {len(skills)} KỸ NĂNG ĐÃ DUYỆT)")
    print("=" * 80)

    if args.status:
        for s in skills:
            s_dir = SKILLS_DIR / s["name"]
            has_it = s_dir.exists() and (s_dir / "SKILL.md").exists()
            status_str = "🟢 ĐÃ SẴN SÀNG" if has_it else "🔴 THIẾU"
            print(f"  - {status_str}: {s['name']} (Nguồn: {s['url']})")
        print("=" * 80 + "\n")
        return

    success_count = 0
    for s in skills:
        ok = fetch_skill(s, force=args.force)
        if ok:
            success_count += 1

    print("\n" + "-" * 80)
    print(f"📊 KẾT QUẢ: {success_count}/{len(skills)} kỹ năng đã sẵn sàng trong .agents/skills/")
    print("-" * 80 + "\n")

    # Chạy kiểm tra an ninh sau khi tải
    check_script = ROOT_DIR / "scripts" / "check-skills.py"
    if check_script.exists():
        print("🔍 Đang chạy kiểm tra an ninh (check-skills)...")
        subprocess.run([sys.executable, str(check_script)], timeout=30)


if __name__ == "__main__":
    main()
