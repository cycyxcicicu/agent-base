#!/usr/bin/env python3
"""
scripts/fetch-skills.py
Bộ Điều Phối & Cài Đặt Kỹ Năng Agent-Base (Skill Fetcher & Quarantine Manager)

Đọc file cấu hình trung tâm duy nhất `skills.config.json` để xác định vị trí kho
kiểm dịch (quarantine) trên máy tính hiện tại. Hỗ trợ:
  1. Khởi tạo/cập nhật đường dẫn quarantine tại 1 chỗ duy nhất (Single Source of Truth).
  2. Clone đầy đủ hoặc chọn lọc các repository quarantine về máy.
  3. Cài đặt các kỹ năng đã duyệt từ quarantine vào dự án (.agents/skills/).
  4. Chế độ tương tác hỏi người dùng (Interactive) khi khởi tạo dự án mới trên máy mới.

Sử dụng:
  python scripts/fetch-skills.py                # Chế độ tự động/tương tác thông minh
  python scripts/fetch-skills.py --status       # Chỉ kiểm tra trạng thái các skill & quarantine
  python scripts/fetch-skills.py --interactive  # Bắt buộc vào giao diện hỏi đáp người dùng
  python scripts/fetch-skills.py --clone-all    # Tải/clone toàn bộ các repo quarantine về máy
  python scripts/fetch-skills.py --sync-all     # Cài đặt tất cả skill đã duyệt vào dự án
  python scripts/fetch-skills.py --set-dir <path> # Ghi đè đường dẫn quarantine vào skills.config.json
  python scripts/fetch-skills.py --force        # Ghi đè các skill đã có trong .agents/skills/
"""

import os
import sys
import json
import shutil
import tempfile
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Cấu hình UTF-8 cho Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT_DIR / "skills.config.json"
REGISTRY_FILE = ROOT_DIR / "agents" / "knowledge" / "skills.md"
DEFAULT_QUARANTINE = "D:/skills-quarantine"

# Danh bạ các upstream repository tạo nên kho quarantine hoàn chỉnh
QUARANTINE_REPOS = {
    "archify": {
        "url": "https://github.com/tt-a1i/archify.git",
        "desc": "Archify System Map CLI & Archify-Review"
    },
    "diagram-design": {
        "url": "https://github.com/cathrynlavery/diagram-design.git",
        "desc": "Diagram Design (41 loại sơ đồ HTML/SVG)"
    },
    "pocock-skills": {
        "url": "https://github.com/mattpocock/skills.git",
        "desc": "Matt Pocock Skills (grilling, writing-for-agents, domain-modeling, codebase-design, to-spec, to-tickets)"
    },
    "ponytail": {
        "url": "https://github.com/DietrichGebert/ponytail.git",
        "desc": "Ponytail Debt Hunter (quét # ponytail: nợ kỹ thuật)"
    },
    "ECC": {
        "url": "https://github.com/affaan-m/ECC.git",
        "desc": "Architecture Decision Records (chuẩn Nygard ADR)"
    },
    "superpowers": {
        "url": "https://github.com/obra/superpowers.git",
        "desc": "Superpowers (subagent-driven-development, systematic-debugging)"
    },
    "ui-ux-pro-max-skill": {
        "url": "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git",
        "desc": "UI/UX Pro Max (192 product profiles, 79 UI styles, 22 stacks)"
    },
    "open-code-review": {
        "url": "https://github.com/alibaba/open-code-review.git",
        "desc": "Alibaba Open Code Review (chuẩn AI review theo diff)"
    },
    "i-have-adhd": {
        "url": "https://github.com/ayghri/i-have-adhd.git",
        "desc": "I Have ADHD (giao tiếp trực diện, triệt tiêu văn hoa)"
    },
    "gstack": {
        "url": "https://github.com/garrytan/gstack.git",
        "desc": "GStack Garry Tan (plan-ceo-review, plan-eng-review, cso, ship, browse, qa-web, office-hours, etc.)"
    },
    "ruflo": {
        "url": "https://github.com/ruvnet/ruflo.git",
        "desc": "Ruflo (swarm-orchestration, sparc-methodology)"
    },
    "graphify": {
        "url": "https://github.com/Graphify-Labs/graphify.git",
        "desc": "Graphify (bản đồ tri thức mã nguồn; chỉ lấy ý cho skill codebase-map, KHÔNG cài hook/công cụ nếu chưa duyệt)"
    }
}

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


def get_os_type() -> str:
    """Xác định loại hệ điều hành: 'windows', 'macos', hoặc 'linux'."""
    if sys.platform == "win32":
        return "windows"
    elif sys.platform == "darwin":
        return "macos"
    return "linux"


def get_example_path() -> str:
    """Trả về ví dụ đường dẫn phù hợp với hệ điều hành đang chạy."""
    os_t = get_os_type()
    if os_t == "windows":
        return "D:/skills-quarantine hoặc E:/skills-quarantine"
    elif os_t == "macos":
        return "~/skills-quarantine hoặc /Volumes/Data/skills-quarantine"
    else:
        return "~/skills-quarantine hoặc /data/skills-quarantine"


def check_forbidden_system_path(path: Path) -> Tuple[bool, str]:
    """
    Kiểm tra xem đường dẫn có vi phạm quy định cấm lưu vào ổ hệ thống OS hay không.
    - Windows: Cấm ổ C:
    - macOS & Linux: Cấm thư mục gốc root / hoặc thư mục hệ điều hành (/System, /usr, /bin, /etc, /Library...)
    """
    try:
        expanded = path.expanduser().resolve()
    except Exception:
        expanded = path

    # 1. Windows: Cấm ổ C:
    if sys.platform == "win32" or getattr(expanded, "drive", ""):
        if getattr(expanded, "drive", "").upper() == "C:":
            return True, "NGHIÊM CẤM CẤU HÌNH VÀO Ổ C: (ổ hệ điều hành Windows)! Vui lòng chọn ổ dữ liệu khác (D:, E:, F:...)."

    # 2. macOS & Linux: Cấm root và thư mục hệ thống
    if sys.platform != "win32":
        str_p = str(expanded)
        if str_p == "/":
            return True, "NGHIÊM CẤM lưu trực tiếp vào thư mục gốc hệ thống (/)! Vui lòng lưu vào thư mục người dùng (~/skills-quarantine) hoặc ổ đĩa riêng (/Volumes/...)."
        forbidden_system_dirs = ["/System", "/Library", "/bin", "/sbin", "/usr", "/etc", "/var", "/private", "/dev"]
        for f_dir in forbidden_system_dirs:
            if str_p == f_dir or str_p.startswith(f_dir + "/"):
                return True, f"NGHIÊM CẤM lưu vào thư mục hệ thống ({f_dir})! Vui lòng lưu vào thư mục người dùng (~/skills-quarantine) hoặc /Volumes/..."

    return False, ""


def get_available_data_drives() -> List[str]:
    """Liệt kê các vị trí lưu trữ dữ liệu an toàn khả dụng theo từng hệ điều hành."""
    drives = []
    if sys.platform == "win32":
        import string
        for letter in string.ascii_uppercase:
            if letter == 'C':
                continue
            drive_path = f"{letter}:\\"
            if os.path.exists(drive_path):
                try:
                    usage = shutil.disk_usage(drive_path)
                    free_gb = usage.free // (1024 ** 3)
                    drives.append(f"{letter}:/ (Trống {free_gb} GB)")
                except Exception:
                    drives.append(f"{letter}:/")
    elif sys.platform == "darwin":  # macOS
        try:
            home = Path.home()
            usage = shutil.disk_usage(home)
            free_gb = usage.free // (1024 ** 3)
            drives.append(f"~ (Thư mục người dùng: {home}, Trống {free_gb} GB)")
        except Exception:
            drives.append(f"~ ({Path.home()})")
        vol_dir = Path("/Volumes")
        if vol_dir.exists():
            for v in vol_dir.iterdir():
                if v.is_dir() and v.name != "Macintosh HD":
                    try:
                        usage = shutil.disk_usage(v)
                        free_gb = usage.free // (1024 ** 3)
                        drives.append(f"{v} (Ổ đĩa ngoài/phân vùng riêng, Trống {free_gb} GB)")
                    except Exception:
                        drives.append(str(v))
    else:  # Linux
        try:
            home = Path.home()
            usage = shutil.disk_usage(home)
            free_gb = usage.free // (1024 ** 3)
            drives.append(f"~ (Thư mục người dùng: {home}, Trống {free_gb} GB)")
        except Exception:
            drives.append(f"~ ({Path.home()})")
        for p in ["/data", "/mnt", "/media"]:
            cand = Path(p)
            if cand.exists():
                drives.append(str(cand))
    return drives


def detect_existing_quarantine() -> Optional[Path]:
    """Tìm xem trên các vị trí lưu trữ an toàn đã có sẵn thư mục quarantine chưa."""
    if os.environ.get("SKILLS_QUARANTINE_DIR"):
        p = Path(os.environ["SKILLS_QUARANTINE_DIR"]).expanduser()
        is_bad, _ = check_forbidden_system_path(p)
        if p.exists() and not is_bad:
            return p

    if sys.platform == "win32":
        for drive in ["D", "E", "F", "G", "H"]:
            candidate = Path(f"{drive}:/skills-quarantine")
            if candidate.exists():
                return candidate
    elif sys.platform == "darwin":  # macOS
        home_cand = Path.home() / "skills-quarantine"
        if home_cand.exists():
            return home_cand
        vol_dir = Path("/Volumes")
        if vol_dir.exists():
            for v in vol_dir.iterdir():
                cand = v / "skills-quarantine"
                if cand.exists():
                    return cand
    else:  # Linux
        home_cand = Path.home() / "skills-quarantine"
        if home_cand.exists():
            return home_cand
        for p in ["/data/skills-quarantine", "/mnt/skills-quarantine"]:
            cand = Path(p)
            if cand.exists():
                return cand
    return None


def load_skills_config() -> Tuple[Optional[Path], Path]:
    """
    Đọc cấu hình từ file trung tâm skills.config.json.
    Trả về: (quarantine_dir, skills_dir).
    Hỗ trợ cả Windows (cấm C:) và macOS/Linux (cấm root/system, hỗ trợ ~).
    Nếu đường dẫn chưa tồn tại trên máy hiện tại, trả về None để bắt buộc hỏi người dùng trước khi làm.
    """
    quarantine_path: Optional[Path] = None
    skills_path = ROOT_DIR / ".agents" / "skills"

    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            if "quarantine_dir" in data and data["quarantine_dir"]:
                cand = Path(data["quarantine_dir"]).expanduser()
                is_bad, reason = check_forbidden_system_path(cand)
                if is_bad:
                    print(f"⛔ CẢNH BÁO AN TOÀN: File skills.config.json trỏ vào vùng cấm: {reason}")
                    quarantine_path = None
                elif cand.exists():
                    quarantine_path = cand
                else:
                    # Đường dẫn trong file cấu hình chưa tồn tại trên máy tính này
                    # (ví dụ khi mới clone dự án về máy mới). Bắt buộc hỏi người dùng trước!
                    quarantine_path = None
            if "skills_dir" in data and data["skills_dir"]:
                p = Path(data["skills_dir"]).expanduser()
                skills_path = p if p.is_absolute() else (ROOT_DIR / p)
        except Exception as e:
            print(f"⚠️ Cảnh báo khi đọc {CONFIG_FILE}: {e}")

    # Cho phép biến môi trường SKILLS_QUARANTINE_DIR ghi đè tường minh nếu hợp lệ
    if os.environ.get("SKILLS_QUARANTINE_DIR"):
        env_cand = Path(os.environ["SKILLS_QUARANTINE_DIR"]).expanduser()
        is_bad, _ = check_forbidden_system_path(env_cand)
        if not is_bad and env_cand.exists():
            quarantine_path = env_cand

    return quarantine_path, skills_path


def save_skills_config(quarantine_dir: Path, skills_dir: Optional[Path] = None) -> None:
    """Ghi đường dẫn quarantine_dir vào file cấu hình duy nhất skills.config.json."""
    expanded = quarantine_dir.expanduser()
    is_bad, reason = check_forbidden_system_path(expanded)
    if is_bad:
        raise ValueError(f"NGHIÊM CẤM lưu cấu hình kho kỹ năng: {reason}")

    data = {}
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}

    data["$schema"] = "./schemas/skills-config.schema.json"
    data["description"] = "Cấu hình trung tâm duy nhất cho thư mục kỹ năng và quarantine của dự án. Thay đổi ở đây sẽ tự động áp dụng cho tất cả các script, wrapper và agent."
    data["quarantine_dir"] = str(quarantine_dir).replace("\\", "/")
    if skills_dir:
        try:
            rel = skills_dir.relative_to(ROOT_DIR)
            data["skills_dir"] = str(rel).replace("\\", "/")
        except ValueError:
            data["skills_dir"] = str(skills_dir).replace("\\", "/")
    elif "skills_dir" not in data:
        data["skills_dir"] = ".agents/skills"

    CONFIG_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"💾 Đã lưu cấu hình vào: {CONFIG_FILE.relative_to(ROOT_DIR)}")


def get_quarantine_map(quarantine_dir: Path) -> Dict[str, Path]:
    """Xây dựng bản đồ ánh xạ các skill từ thư mục quarantine."""
    return {
        "diagram-design": quarantine_dir / "diagram-design",
        "grilling": quarantine_dir / "pocock-skills/skills/engineering/grilling",
        "writing-for-agents": quarantine_dir / "pocock-skills/skills/productivity/writing-for-agents",
        "domain-modeling": quarantine_dir / "pocock-skills/skills/engineering/domain-modeling",
        "codebase-design": quarantine_dir / "pocock-skills/skills/engineering/codebase-design",
        "to-spec": quarantine_dir / "pocock-skills/skills/engineering/to-spec",
        "to-tickets": quarantine_dir / "pocock-skills/skills/engineering/to-tickets",
        "ponytail-debt": quarantine_dir / "ponytail/skills/ponytail-debt",
        "architecture-decision-records": quarantine_dir / "ECC/skills/architecture-decision-records",
        "subagent-driven-development": quarantine_dir / "superpowers/skills/subagent-driven-development",
        "systematic-debugging": quarantine_dir / "superpowers/skills/systematic-debugging",
        "ui-ux-pro-max": quarantine_dir / "ui-ux-pro-max-skill",
        "open-code-review": quarantine_dir / "open-code-review/skills/open-code-review",
        "i-have-adhd": quarantine_dir / "i-have-adhd/skills/i-have-adhd",
        "plan-ceo-review": quarantine_dir / "gstack/plan-ceo-review",
        "plan-eng-review": quarantine_dir / "gstack/plan-eng-review",
        "cso": quarantine_dir / "gstack/cso",
        "ship": quarantine_dir / "gstack/ship",
        "archify": quarantine_dir / "archify/archify",
        "archify-review": quarantine_dir / "archify/.agents/skills/archify-review",
        "swarm-orchestration": quarantine_dir / "ruflo/.agents/skills/swarm-orchestration",
        "sparc-methodology": quarantine_dir / "ruflo/.agents/skills/sparc-methodology",
        "careful": quarantine_dir / "gstack/careful",
        "browse": quarantine_dir / "gstack/browse",
        "qa-web": quarantine_dir / "gstack/qa",
        "office-hours": quarantine_dir / "gstack/office-hours",
        "investigate": quarantine_dir / "gstack/investigate",
        "devex-review": quarantine_dir / "gstack/devex-review",
    }


def parse_registry() -> List[Dict[str, str]]:
    """Đọc và bóc tách bảng kỹ năng đã duyệt từ agents/knowledge/skills.md."""
    if not REGISTRY_FILE.exists():
        print(f"❌ Không tìm thấy sổ đăng ký: {REGISTRY_FILE}")
        return []

    lines = REGISTRY_FILE.read_text(encoding="utf-8", errors="replace").splitlines()
    skills = []

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


def clone_repo(name: str, url: str, target_dir: Path) -> bool:
    """Clone một repository shallow (độ sâu 1) vào thư mục chỉ định."""
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    if target_dir.exists():
        print(f"  ✅ [Repo: {name}] Đã có sẵn tại {target_dir}")
        return True

    print(f"  📥 [Repo: {name}] Đang clone từ {url}...")
    try:
        cmd = ["git", "clone", "--depth", "1", url, str(target_dir)]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if res.returncode == 0:
            print(f"  ✨ [Repo: {name}] Clone thành công!")
            return True
        else:
            print(f"  ❌ [Repo: {name}] Lỗi: {res.stderr.strip()}")
            return False
    except Exception as e:
        print(f"  ❌ [Repo: {name}] Thất bại: {e}")
        return False


def fetch_skill(skill_info: Dict[str, str], skills_dir: Path, quarantine_map: Dict[str, Path], force: bool = False) -> bool:
    """Sao chép hoặc kéo một skill vào thư mục .agents/skills/ của dự án."""
    name = skill_info["name"]
    url = skill_info["url"]
    target_dir = skills_dir / name

    # Nếu là bản chắt lọc tự viết nội bộ
    if "Tự viết" in url or not url.startswith("http"):
        if (target_dir / "SKILL.md").exists():
            print(f"  ✨ [{name}] Bản chuẩn nội bộ đã sẵn sàng tại {target_dir.name}/")
            return True
        print(f"  ⚠️ [{name}] Bản tự viết nội bộ chưa có tại {target_dir.name}/. Vui lòng kiểm tra.")
        return False

    if target_dir.exists() and (target_dir / "SKILL.md").exists() and not force:
        print(f"  ✅ [{name}] Đã có sẵn tại {skills_dir.name}/{name}")
        return True

    print(f"  📥 [{name}] Đang nạp từ kho...")

    # 1. Kiểm tra nguồn kiểm dịch cục bộ (Ưu tiên số 1 - Nhanh & Không tốn mạng)
    local_src = quarantine_map.get(name)
    if local_src and local_src.exists() and (local_src / "SKILL.md").exists():
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(local_src, target_dir, dirs_exist_ok=True)
        print(f"  ✨ [{name}] Đã sao chép từ kho kiểm dịch: {local_src}")
        return True

    # 2. Tải qua Git Clone nếu là remote URL
    if url.startswith("http"):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            try:
                cmd = ["git", "clone", "--depth", "1", url, str(tmp_path / "repo")]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                if res.returncode != 0:
                    print(f"  ⚠️ Lỗi clone {url}: {res.stderr.strip()}")
                    return False

                repo_path = tmp_path / "repo"
                sub_path = SUBFOLDER_MAP.get(name)
                source_dir = (repo_path / sub_path) if sub_path else repo_path

                if not (source_dir / "SKILL.md").exists():
                    found = list(repo_path.rglob("SKILL.md"))
                    if found:
                        source_dir = found[0].parent

                if (source_dir / "SKILL.md").exists():
                    target_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)
                    print(f"  🚀 [{name}] Đã tải về và cài đặt thành công!")
                    return True
                else:
                    print(f"  ❌ [{name}] Không tìm thấy SKILL.md trong repo {url}")
                    return False
            except Exception as e:
                print(f"  ❌ [{name}] Thất bại khi tải: {e}")
                return False

    print(f"  ⚪ [{name}] Nguồn '{url}' là cục bộ hoặc chưa hỗ trợ tự tải. Vui lòng chép thủ công.")
    return False


def run_interactive(quarantine_dir: Optional[Path], skills_dir: Path) -> None:
    """Giao diện hỏi đáp tương tác trực tiếp với người dùng (hỗ trợ Windows, macOS, Linux)."""
    os_t = get_os_type()
    os_name = "macOS" if os_t == "macos" else ("Windows" if os_t == "windows" else "Linux")

    print("\n" + "=" * 80)
    print("🛠️  BỘ ĐIỀU PHỐI KỸ NĂNG & KHO KIỂM DỊCH AGENT-BASE (QUARANTINE SETUP)")
    print("=" * 80)
    print(f"🖥️  Hệ điều hành đang chạy: {os_name}")
    print("⚠️  QUY ĐỊNH AN TOÀN BẮT BUỘC:")
    if os_t == "windows":
        print("   1. NGHIÊM CẤM TUYỆT ĐỐI cấu hình hoặc tải về ổ C: (ổ hệ điều hành Windows).")
    else:
        print("   1. NGHIÊM CẤM TUYỆT ĐỐI cấu hình vào thư mục gốc hệ thống (/, /System). Khuyến nghị dùng ~/skills-quarantine.")
    print("   2. BẮT BUỘC HỎI NGƯỜI DÙNG TRƯỚC: Người dùng tự chọn thư mục lưu trữ trên máy.")
    print("   3. Khai báo tại 1 NƠI DUY NHẤT (skills.config.json), mọi công cụ tự động nhận diện.\n")

    detected = detect_existing_quarantine()
    suggested = str(quarantine_dir).replace("\\", "/") if (quarantine_dir and quarantine_dir.exists()) else (str(detected).replace("\\", "/") if detected else "")

    print("📁 [BƯỚC 1/3] HỎI NGƯỜI DÙNG NƠI LƯU TRỮ KHO KỸ NĂNG (QUARANTINE DIRECTORY)")
    available_drives = get_available_data_drives()
    if available_drives:
        print(f"   Vị trí lưu trữ dữ liệu an toàn phát hiện trên máy: {', '.join(available_drives)}")
    if suggested:
        print(f"   Phát hiện thư mục dữ liệu đã có sẵn: {suggested}")
    else:
        print("   Chưa có thư mục cấu hình sẵn trên máy này.")

    ex_str = get_example_path()
    while True:
        prompt_msg = f"👉 Nhập đường dẫn thư mục bạn muốn lưu kho skills {'[Enter để dùng ' + suggested + ']: ' if suggested else ': '}"
        user_input = input(prompt_msg).strip()

        target_str = user_input if user_input else suggested
        if not target_str:
            print(f"❌ Đường dẫn không được để trống! Vui lòng nhập đường dẫn an toàn (ví dụ: {ex_str}):")
            continue

        chosen_path = Path(target_str).expanduser()

        is_bad, reason = check_forbidden_system_path(chosen_path)
        if is_bad:
            print(f"\n⛔ LỖI: {reason}")
            print(f"   Ví dụ hợp lệ trên hệ điều hành {os_name}: {ex_str}\n")
            continue

        try:
            save_skills_config(chosen_path, skills_dir)
        except Exception as e:
            print(f"❌ Lỗi khi lưu cấu hình: {e}")
            continue

        quarantine_dir = chosen_path.resolve()
        print(f"✅ Đã xác nhận thư mục lưu trữ: {quarantine_dir}\n")
        break

    quarantine_dir.mkdir(parents=True, exist_ok=True)
    quarantine_map = get_quarantine_map(quarantine_dir)

    # Bước 2: Kiểm tra các repository quarantine trên máy
    print("\n" + "-" * 80)
    print("🔍 [BƯỚC 1/2] KIỂM TRA CÁC KHO NGUỒN TRONG QUARANTINE")
    print("-" * 80)
    missing_repos = []
    for r_name, r_info in QUARANTINE_REPOS.items():
        r_path = quarantine_dir / r_name
        has_it = r_path.exists()
        status_label = "🟢 ĐÃ CÓ" if has_it else "🔴 CHƯA CÓ"
        print(f"  {status_label}  {r_name:22} : {r_info['desc']}")
        if not has_it:
            missing_repos.append(r_name)

    if missing_repos:
        print(f"\n⚠️ Máy tính hiện đang thiếu {len(missing_repos)} kho nguồn kiểm dịch.")
        print("Bạn muốn xử lý như thế nào?")
        print("  [1] Tải/Clone TẤT CẢ các repo còn thiếu về thư mục này (Khuyến nghị)")
        print("  [2] Chọn từng repo cụ thể để tải")
        print("  [3] Bỏ qua bước này (đã có nguồn khác hoặc tự tải sau)")
        choice = input("👉 Lựa chọn của bạn [1/2/3] (Mặc định: 1): ").strip() or "1"

        if choice == "1":
            print("\n🚀 Đang clone tất cả các repo còn thiếu...")
            for r_name in missing_repos:
                clone_repo(r_name, QUARANTINE_REPOS[r_name]["url"], quarantine_dir / r_name)
        elif choice == "2":
            print("\nChọn các repo cần tải (phân cách bằng dấu phẩy, ví dụ: 1,3,4):")
            for idx, r_name in enumerate(missing_repos, 1):
                print(f"  [{idx}] {r_name} ({QUARANTINE_REPOS[r_name]['url']})")
            selected_idx = input("👉 Nhập số thứ tự: ").strip()
            if selected_idx:
                for part in selected_idx.split(","):
                    p = part.strip()
                    if p.isdigit() and 1 <= int(p) <= len(missing_repos):
                        picked = missing_repos[int(p) - 1]
                        clone_repo(picked, QUARANTINE_REPOS[picked]["url"], quarantine_dir / picked)
        else:
            print("  ⚪ Đã bỏ qua tải kho quarantine.")
    else:
        print("\n✨ Tất cả 11 kho nguồn quarantine đã sẵn sàng trên máy tính!")

    # Bước 3: Kiểm tra các skill của dự án trong .agents/skills/
    print("\n" + "-" * 80)
    print("📦 [BƯỚC 2/2] KIỂM TRA KỸ NĂNG ĐÃ CÀI ĐẶT TRONG DỰ ÁN (.agents/skills/)")
    print("-" * 80)
    skills = parse_registry()
    missing_skills = []
    for s in skills:
        s_dir = skills_dir / s["name"]
        has_it = s_dir.exists() and (s_dir / "SKILL.md").exists()
        status_label = "🟢 ĐÃ CÓ" if has_it else "🔴 THIẾU"
        print(f"  {status_label}  {s['name']:30} (Phiên bản: {s['version']})")
        if not has_it:
            missing_skills.append(s)

    if missing_skills:
        print(f"\n⚠️ Dự án đang thiếu {len(missing_skills)}/{len(skills)} kỹ năng.")
        print("Bạn muốn cài đặt kỹ năng vào dự án:")
        print("  [1] Cài đặt TẤT CẢ kỹ năng còn thiếu từ quarantine (Khuyến nghị)")
        print("  [2] Chọn từng kỹ năng cụ thể để cài đặt")
        print("  [3] Bỏ qua (không thay đổi .agents/skills/)")
        choice = input("👉 Lựa chọn của bạn [1/2/3] (Mặc định: 1): ").strip() or "1"

        if choice == "1":
            print("\n🚀 Đang cài đặt tất cả kỹ năng còn thiếu...")
            for s in missing_skills:
                fetch_skill(s, skills_dir, quarantine_map, force=False)
        elif choice == "2":
            print("\nChọn các kỹ năng cần cài đặt (phân cách bằng dấu phẩy):")
            for idx, s in enumerate(missing_skills, 1):
                print(f"  [{idx}] {s['name']}")
            selected_idx = input("👉 Nhập số thứ tự: ").strip()
            if selected_idx:
                for part in selected_idx.split(","):
                    p = part.strip()
                    if p.isdigit() and 1 <= int(p) <= len(missing_skills):
                        picked = missing_skills[int(p) - 1]
                        fetch_skill(picked, skills_dir, quarantine_map, force=False)
        else:
            print("  ⚪ Đã bỏ qua cài đặt kỹ năng.")
    else:
        print("\n✨ Tất cả kỹ năng trong sổ đăng ký đã sẵn sàng trong .agents/skills/!")

    print("\n" + "=" * 80)
    print("🎉 HOÀN TẤT THIẾT LẬP KỸ NĂNG!")
    print(f"  - Cấu hình duy nhất: {CONFIG_FILE.relative_to(ROOT_DIR)}")
    print(f"  - Kho quarantine:    {quarantine_dir}")
    print(f"  - Kỹ năng dự án:    {skills_dir.relative_to(ROOT_DIR)}")
    print("=" * 80 + "\n")


def print_status(quarantine_dir: Optional[Path], skills_dir: Path) -> None:
    """In bảng trạng thái chi tiết của quarantine và skills."""
    print("\n" + "=" * 80)
    print("📊 TRẠNG THÁI HỆ THỐNG KỸ NĂNG AGENT-BASE")
    print("=" * 80)
    print(f"📍 File cấu hình duy nhất: {CONFIG_FILE.relative_to(ROOT_DIR) if CONFIG_FILE.exists() else 'Chưa tạo'}")
    if quarantine_dir:
        print(f"📁 Thư mục quarantine:     {quarantine_dir} ({'Tồn tại' if quarantine_dir.exists() else 'KHÔNG TỒN TẠI'})")
    else:
        print(f"📁 Thư mục quarantine:     CHƯA CẤU HÌNH (Chạy 'python scripts/setup-skills.py' để chọn)")
    print(f"📦 Thư mục kỹ năng:       {skills_dir.relative_to(ROOT_DIR)}\n")

    print("-" * 80)
    print("1. KHO NGUỒN QUARANTINE TRÊN MÁY TÍNH:")
    print("-" * 80)
    for r_name, r_info in QUARANTINE_REPOS.items():
        has_it = (quarantine_dir / r_name).exists() if quarantine_dir else False
        status_label = "🟢 ĐÃ CÓ" if has_it else "🔴 THIẾU"
        print(f"  {status_label}  {r_name:22} : {r_info['desc']}")

    print("\n" + "-" * 80)
    print("2. KỸ NĂNG TRONG DỰ ÁN (.agents/skills/):")
    print("-" * 80)
    skills = parse_registry()
    ready_count = 0
    for s in skills:
        s_dir = skills_dir / s["name"]
        has_it = s_dir.exists() and (s_dir / "SKILL.md").exists()
        if has_it:
            ready_count += 1
        status_label = "🟢 SẴN SÀNG" if has_it else "🔴 THIẾU"
        print(f"  {status_label}  {s['name']:30} (Nguồn: {s['url']})")

    print("\n" + "=" * 80)
    print(f"📈 TỔNG KẾT: {ready_count}/{len(skills)} kỹ năng đã sẵn sàng trong dự án.")
    print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Bộ điều phối kỹ năng & kho kiểm dịch Agent-Base")
    parser.add_argument("--status", action="store_true", help="Chỉ kiểm tra và in trạng thái hiện tại")
    parser.add_argument("--force", action="store_true", help="Tải/sao chép lại đè lên các skill đã có")
    parser.add_argument("--interactive", "-i", action="store_true", help="Chạy chế độ tương tác hỏi người dùng")
    parser.add_argument("--clone-all", action="store_true", help="Clone toàn bộ các repo quarantine về máy")
    parser.add_argument("--sync-all", action="store_true", help="Đồng bộ toàn bộ skill đã duyệt vào dự án")
    parser.add_argument("--set-dir", type=str, help="Cập nhật đường dẫn quarantine vào skills.config.json")
    args = parser.parse_args()

    quarantine_dir, skills_dir = load_skills_config()

    if args.set_dir:
        cand = Path(args.set_dir).expanduser()
        is_bad, reason = check_forbidden_system_path(cand)
        if is_bad:
            sys.exit(f"❌ LỖI NGHIÊM CẤM: {reason}\n")
        save_skills_config(cand, skills_dir)
        print(f"✅ Đã cập nhật quarantine_dir: {cand.resolve()}")
        return

    is_interactive_terminal = hasattr(sys.stdin, "isatty") and sys.stdin.isatty()

    if args.clone_all:
        if not quarantine_dir or not quarantine_dir.exists():
            if is_interactive_terminal:
                run_interactive(quarantine_dir, skills_dir)
                return
            sys.exit("❌ LỖI: Chưa chọn thư mục quarantine hoặc thư mục chưa tồn tại trên máy.\n"
                     "BẮT BUỘC PHẢI HỎI NGƯỜI DÙNG MUỐN LƯU Ở ĐÂU TRƯỚC KHI TẢI.\n"
                     "Vui lòng chạy 'python scripts/setup-skills.py' để chọn thư mục trước!")
        quarantine_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n🚀 Đang clone toàn bộ {len(QUARANTINE_REPOS)} repo quarantine về {quarantine_dir} (repo đã có thì bỏ qua)...")
        for r_name, r_info in QUARANTINE_REPOS.items():
            clone_repo(r_name, r_info["url"], quarantine_dir / r_name)
        save_skills_config(quarantine_dir, skills_dir)
        print("✨ Hoàn tất clone kho quarantine!\n")
        return

    if args.status:
        print_status(quarantine_dir, skills_dir)
        return

    # Nếu chạy interactive hoặc dòng lệnh có cờ --interactive
    if args.interactive:
        run_interactive(quarantine_dir, skills_dir)
        return

    # Nếu người dùng chạy `python scripts/fetch-skills.py` mà môi trường tương tác (TTY) và thiếu skill hoặc config chưa có hoặc thư mục quarantine chưa tồn tại
    skills = parse_registry()
    has_missing = any(not (skills_dir / s["name"] / "SKILL.md").exists() for s in skills)

    if is_interactive_terminal and not args.sync_all and (not CONFIG_FILE.exists() or not quarantine_dir or not quarantine_dir.exists() or has_missing):
        run_interactive(quarantine_dir, skills_dir)
        return

    if not quarantine_dir or not quarantine_dir.exists():
        sys.exit("❌ LỖI: Chưa cấu hình hoặc thư mục quarantine chưa tồn tại trên máy tính này.\n"
                 "BẮT BUỘC PHẢI HỎI NGƯỜI DÙNG MUỐN LƯU Ở ĐÂU TRƯỚC KHI LÀM.\n"
                 "Vui lòng chạy 'python scripts/setup-skills.py' để chọn thư mục lưu trữ trên máy tính của bạn!")

    # Chế độ headless / automation (mặc định nếu không phải TTY hoặc có --sync-all)
    quarantine_map = get_quarantine_map(quarantine_dir)
    skills_dir.mkdir(parents=True, exist_ok=True)
    save_skills_config(quarantine_dir, skills_dir)

    print("\n" + "=" * 80)
    print(f"📦 BỘ ĐIỀU PHỐI KỸ NĂNG AGENT-BASE (TỔNG CỘNG: {len(skills)} KỸ NĂNG ĐÃ DUYỆT)")
    print(f"📁 Kho kiểm dịch: {quarantine_dir}")
    print("=" * 80)

    success_count = 0
    for s in skills:
        ok = fetch_skill(s, skills_dir, quarantine_map, force=args.force)
        if ok:
            success_count += 1

    print("\n" + "-" * 80)
    print(f"📊 KẾT QUẢ: {success_count}/{len(skills)} kỹ năng đã sẵn sàng trong {skills_dir.relative_to(ROOT_DIR)}/")
    print("-" * 80 + "\n")

    # Kiểm tra an ninh sau khi đồng bộ
    check_script = ROOT_DIR / "scripts" / "check-skills.py"
    if check_script.exists():
        print("🔍 Đang chạy kiểm tra an ninh (check-skills)...")
        subprocess.run([sys.executable, str(check_script)], timeout=30)


if __name__ == "__main__":
    main()
