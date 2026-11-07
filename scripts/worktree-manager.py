#!/usr/bin/env python3
"""
Worktree Registry & Lifecycle Manager for gdt-workspace
Quản lý tập trung, chuẩn hóa vị trí và sổ bộ Git Worktrees cho toàn bộ Microservices.

Vị trí worktree chuẩn bắt buộc: ~/Documents/worktrees/<name> (hoặc biến môi trường WORKTREES_DIR)
Sổ bộ lưu trữ: doc/governance/standards/worktree-registry.json
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def resolve_workspace_root() -> Path:
    """Tự động nhận diện thư mục gốc của workspace:
    1. Biến môi trường WORKSPACE_ROOT
    2. File cấu hình cục bộ .agent-base.local.json hoặc projects.json
    3. Tìm từ thư mục hiện tại ngược lên cha nếu thấy platform-services hoặc doc/governance
    4. Thư mục sibling ../gdt-workspace nếu tồn tại
    5. Fallback: ~/Documents/gdt-workspace (hoặc ~/gdt-workspace)
    """
    if os.environ.get("WORKSPACE_ROOT"):
        return Path(os.environ["WORKSPACE_ROOT"]).expanduser().resolve()

    for cfg_candidate in [Path.cwd() / ".agent-base.local.json", Path(__file__).resolve().parent.parent / "projects.json"]:
        if cfg_candidate.exists():
            try:
                with open(cfg_candidate, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    if cfg.get("workspace_root"):
                        p = Path(cfg["workspace_root"]).expanduser()
                        if p.exists():
                            return p.resolve()
                    def_p = cfg.get("default_project")
                    for item in cfg.get("projects", []):
                        if item.get("id") == def_p:
                            p = Path(item.get("path", "")).expanduser()
                            if p.exists():
                                return p.resolve()
            except Exception:
                pass

    curr = Path.cwd().resolve()
    for parent in [curr] + list(curr.parents):
        if (parent / "platform-services").exists() or (parent / "doc/governance/standards").exists():
            return parent

    sibling = curr.parent / "gdt-workspace"
    if sibling.exists():
        return sibling.resolve()

    default_docs = Path.home() / "Documents" / "gdt-workspace"
    if (Path.home() / "Documents").exists():
        return default_docs.resolve()
    return (Path.home() / "gdt-workspace").resolve()


def resolve_worktrees_dir(ws_root: Path) -> Path:
    """Tự động nhận diện thư mục worktree tập trung:
    1. Biến môi trường WORKTREES_DIR
    2. File cấu hình cục bộ .agent-base.local.json (worktrees_dir)
    3. Thư mục sibling ngang hàng với workspace: ws_root.parent / "worktrees" nếu tồn tại
    4. Fallback: ~/Documents/worktrees (hoặc ~/worktrees nếu không có thư mục Documents)
    """
    if os.environ.get("WORKTREES_DIR"):
        return Path(os.environ["WORKTREES_DIR"]).expanduser().resolve()

    for cfg_candidate in [Path.cwd() / ".agent-base.local.json", ws_root / ".agent-base.local.json"]:
        if cfg_candidate.exists():
            try:
                with open(cfg_candidate, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    if cfg.get("worktrees_dir"):
                        p = Path(cfg["worktrees_dir"]).expanduser()
                        p.mkdir(parents=True, exist_ok=True)
                        return p.resolve()
            except Exception:
                pass

    sibling_wt = ws_root.parent / "worktrees"
    if sibling_wt.exists():
        return sibling_wt.resolve()

    if (Path.home() / "Documents").exists():
        return (Path.home() / "Documents" / "worktrees").resolve()
    return (Path.home() / "worktrees").resolve()


WORKSPACE_ROOT = resolve_workspace_root()
WORKTREES_DIR = resolve_worktrees_dir(WORKSPACE_ROOT)
REGISTRY_JSON = WORKSPACE_ROOT / "doc/governance/standards/worktree-registry.json"
REGISTRY_MD = WORKSPACE_ROOT / "doc/governance/standards/worktree-registry.md"

SERVICES_MAP = {
    "discovery-server": "platform-services/ws-discovery-server",
    "config-server": "platform-services/ws-config-server",
    "api-gateway": "platform-services/ws-api-gateway",
    "accounting-service": "business/accounting-service",
    "iam-service": "business/ws-iam",
    "ws-acct-frontend": "frontend/ws-acct-frontend",
    "frontend": "frontend/ws-acct-frontend",
    "ws-library": "platform/ws-library",
    "ws-sdk": "platform/ws-sdk",
    "ws-bom": "platform/ws-bom",
}

SERVICE_PORTS = {
    "discovery-server": 16002,
    "config-server": 16001,
    "api-gateway": 16003,
    "accounting-service": 16151,
    "iam-service": 16021,
    "ws-acct-frontend": 16091,
    "frontend": 16091,
}


def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, cwd=cwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.returncode, res.stdout.strip(), res.stderr.strip()


def load_registry():
    if REGISTRY_JSON.exists():
        try:
            with open(REGISTRY_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"version": "1.0.0", "updated_at": "", "worktrees": {}}


def save_registry(data):
    REGISTRY_JSON.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(REGISTRY_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    export_markdown(data)


def export_markdown(data):
    lines = [
        "# Sổ Bộ Đăng Ký Git Worktrees (Worktree Registry)",
        "",
        "> **Quy tắc bắt buộc 100%**:",
        "> 1. Mọi Git Worktree **PHẢI** nằm tại thư mục worktree tập trung (mặc định: `~/Documents/worktrees/<name>`). Tuyệt đối không tạo bên trong `gdt-workspace`.",
        "> 2. Khi tạo hoặc xóa worktree, Agent **BẮT BUỘC** cập nhật sổ bộ này qua `python3 scripts/worktree-manager.py`.",
        "> 3. Trước khi code, Agent tra cứu danh sách để dùng đúng worktree phục vụ task, không tạo trùng lặp.",
        "",
        f"*Cập nhật lần cuối: `{data.get('updated_at', 'N/A')}`*",
        "",
        "| Tên Worktree | Service Gốc | Nhánh Git | Task / UC | Mục đích | Port | Trạng thái |",
        "|---|---|---|---|---|---|---|",
    ]
    for name, item in sorted(data.get("worktrees", {}).items()):
        status_badge = "🟢 RUNNING" if item.get("live_status") == "RUNNING" else "⚪ STOPPED"
        port = item.get("port") or "-"
        lines.append(
            f"| `{name}` | `{item.get('service', '-')}` | `{item.get('branch', '-')}` | "
            f"**{item.get('task', '-')}** | {item.get('purpose', '-')} | `{port}` | {status_badge} |"
        )
    lines.append("")
    lines.append("## Lệnh tra cứu nhanh")
    lines.append("- Liệt kê sổ bộ: `python3 scripts/worktree-manager.py list`")
    lines.append("- Đồng bộ trạng thái: `python3 scripts/worktree-manager.py sync`")
    lines.append("- Thêm worktree mới: `python3 scripts/worktree-manager.py add --service <tên> --name <tên-wt> --branch <nhánh> --task <task> --purpose \"<mô tả>\"`")
    lines.append("- Xóa worktree an toàn: `python3 scripts/worktree-manager.py remove --name <tên-wt>`")
    lines.append("")
    with open(REGISTRY_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def resolve_service_dir(service_name):
    rel = SERVICES_MAP.get(service_name, service_name)
    target = WORKSPACE_ROOT / rel
    if target.exists():
        return target
    # Thử tìm theo tên tương đối
    for k, v in SERVICES_MAP.items():
        if service_name in k or service_name in v:
            cand = WORKSPACE_ROOT / v
            if cand.exists():
                return cand
    return None


def get_live_status(wt_path, service_name):
    pid_file = wt_path / "app.pid"
    if pid_file.exists():
        try:
            pid = int(pid_file.read_text().strip())
            rc, _, _ = run_cmd(f"ps -p {pid}")
            if rc == 0:
                return "RUNNING", pid
        except Exception:
            pass

    # Kiểm tra cổng theo service
    port = SERVICE_PORTS.get(service_name)
    if not port:
        for k, p in SERVICE_PORTS.items():
            if k in wt_path.name:
                port = p
                break
    if port:
        rc, out, _ = run_cmd(f"lsof -nP -iTCP:{port} -sTCP:LISTEN -t")
        if rc == 0 and out:
            pid = out.split()[0]
            rc2, cwd, _ = run_cmd(f"lsof -a -d cwd -p {pid} -Fn")
            if rc2 == 0 and cwd:
                clean_cwd = cwd.splitlines()[-1].replace("n", "")
                if clean_cwd == str(wt_path):
                    try:
                        pid_file.write_text(str(pid))
                    except Exception:
                        pass
                    return "RUNNING", int(pid)
    return "STOPPED", None


def sync_all():
    reg = load_registry()
    wt_dict = reg.get("worktrees", {})

    # Quét tất cả git worktree trong tất cả services
    scanned_wts = {}
    for svc_key, rel_path in SERVICES_MAP.items():
        svc_dir = WORKSPACE_ROOT / rel_path
        if not (svc_dir / ".git").exists():
            continue
        rc, out, _ = run_cmd("git worktree list", cwd=svc_dir)
        if rc == 0 and out:
            lines = out.splitlines()
            for line in lines[1:]:  # Bỏ dòng đầu là root repo
                parts = line.split()
                if not parts:
                    continue
                w_path = Path(parts[0]).resolve()
                branch = ""
                if len(parts) >= 3 and parts[2].startswith("[") and parts[2].endswith("]"):
                    branch = parts[2][1:-1]
                scanned_wts[w_path.name] = {
                    "path": str(w_path),
                    "service": svc_key,
                    "branch": branch,
                }

    # Quét thư mục WORKTREES_DIR để đối chiếu
    if WORKTREES_DIR.exists():
        for item in WORKTREES_DIR.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                name = item.name
                if (item / ".git").exists() or (item / "run.sh").exists():
                    rc, b_out, _ = run_cmd("git branch --show-current", cwd=item)
                    branch = b_out if rc == 0 and b_out else "N/A"
                    if name not in scanned_wts:
                        # Suy luận service
                        matched_svc = "unknown"
                        for s_key in SERVICES_MAP.keys():
                            if s_key in name or (s_key == "ws-acct-frontend" and "frontend" in name):
                                matched_svc = s_key
                                break
                        scanned_wts[name] = {
                            "path": str(item),
                            "service": matched_svc,
                            "branch": branch,
                        }
                    else:
                        if branch and branch != "N/A":
                            scanned_wts[name]["branch"] = branch

    # Cập nhật thông tin vào registry
    updated_dict = {}
    for name, info in scanned_wts.items():
        existing = wt_dict.get(name, {})
        wt_path = Path(info["path"])
        svc = info.get("service") or existing.get("service", "unknown")
        port = SERVICE_PORTS.get(svc)
        live_stat, pid = get_live_status(wt_path, svc)

        # Suy luận task từ tên hoặc branch
        task = existing.get("task", "")
        if not task:
            for part in name.upper().split("-") + (info.get("branch") or "").upper().split("-"):
                if part.startswith("UC") or part.startswith("MANTIS"):
                    task = part
                    break
        if not task:
            task = "N/A"

        purpose = existing.get("purpose", "")
        if not purpose:
            if "generic" in name:
                purpose = "Bộ lọc Generic Specification"
            elif "dev" in name:
                purpose = "Nhánh tính năng phát triển"
            elif "develop" in name:
                purpose = "Nhánh kiểm thử đồng bộ"
            else:
                purpose = f"Worktree cho service {svc}"

        updated_dict[name] = {
            "name": name,
            "path": str(wt_path),
            "service": svc,
            "branch": info.get("branch") or existing.get("branch", "N/A"),
            "task": task,
            "purpose": purpose,
            "port": port,
            "live_status": live_stat,
            "pid": pid,
            "created_at": existing.get("created_at", datetime.now().strftime("%Y-%m-%d")),
        }

    reg["worktrees"] = updated_dict
    save_registry(reg)
    return reg


def cmd_list(args):
    reg = sync_all()
    wts = reg.get("worktrees", {})
    print("=" * 105)
    print("                              SỔ BỘ GIT WORKTREES HỆ THỐNG")
    print(f" Thư mục chuẩn: {WORKTREES_DIR} | Cập nhật: {reg.get('updated_at')}")
    print("=" * 105)
    header = f"{'STT':<4} {'TÊN WORKTREE':<36} {'SERVICE':<20} {'TASK':<8} {'PORT':<6} {'TRẠNG THÁI':<15}"
    print(header)
    print("-" * 105)
    for idx, (name, item) in enumerate(sorted(wts.items()), start=1):
        stat = "RUNNING" if item.get("live_status") == "RUNNING" else "STOPPED"
        port_str = str(item.get("port") or "-")
        print(f"[{idx:<2}] {name:<36} {item.get('service', '-'):<20} {item.get('task', '-'):<8} {port_str:<6} {stat:<15}")
        print(f"     └─ Nhánh: {item.get('branch', '-')} | Mục đích: {item.get('purpose', '-')}")
    print("=" * 105)


def cmd_add(args):
    svc_dir = resolve_service_dir(args.service)
    if not svc_dir or not svc_dir.exists():
        print(f"[ERROR] Không tìm thấy service: {args.service}")
        sys.exit(1)

    wt_name = args.name.strip()
    target_path = WORKTREES_DIR / wt_name

    # Kiểm tra quy tắc vị trí
    if target_path.parent.resolve() != WORKTREES_DIR:
        print(f"[FATAL ERROR] Quy tắc cứng: Mọi worktree BẮT BUỘC phải nằm trong {WORKTREES_DIR}")
        print(f"Đường dẫn vi phạm: {target_path}")
        sys.exit(1)

    if target_path.exists():
        print(f"[ERROR] Worktree đã tồn tại tại: {target_path}")
        sys.exit(1)

    branch = args.branch.strip()
    create_branch_flag = "-b " if args.new_branch else ""
    git_cmd = f"git worktree add {create_branch_flag}{target_path} {branch}"
    print(f">>> Đang tạo worktree: {git_cmd} trong {svc_dir}...")
    rc, out, err = run_cmd(git_cmd, cwd=svc_dir)
    if rc != 0:
        print(f"[ERROR] Không thể tạo worktree: {err}")
        sys.exit(1)

    # Copy run.sh từ service gốc nếu target_path chưa có
    src_run = svc_dir / "run.sh"
    dst_run = target_path / "run.sh"
    if src_run.exists() and not dst_run.exists():
        shutil.copy2(src_run, dst_run)
        dst_run.chmod(0o755)

    print(f"[OK] Đã tạo thành công worktree tại: {target_path}")

    # Đăng ký vào registry
    reg = load_registry()
    wts = reg.setdefault("worktrees", {})
    wts[wt_name] = {
        "name": wt_name,
        "path": str(target_path),
        "service": args.service,
        "branch": branch,
        "task": args.task,
        "purpose": args.purpose or f"Worktree cho {args.service}",
        "port": SERVICE_PORTS.get(args.service),
        "live_status": "STOPPED",
        "pid": None,
        "created_at": datetime.now().strftime("%Y-%m-%d"),
    }
    save_registry(reg)
    sync_all()
    print(f"[OK] Đã ghi nhận worktree '{wt_name}' vào {REGISTRY_JSON}")


def cmd_remove(args):
    wt_name = args.name.strip()
    target_path = WORKTREES_DIR / wt_name

    reg = load_registry()
    wts = reg.get("worktrees", {})
    item = wts.get(wt_name)
    svc_name = item.get("service") if item else ""
    svc_dir = resolve_service_dir(svc_name) if svc_name else None

    # Dừng service nếu đang chạy
    pid_file = target_path / "app.pid"
    if pid_file.exists():
        try:
            pid = int(pid_file.read_text().strip())
            run_cmd(f"kill {pid}")
        except Exception:
            pass

    # Gọi git worktree remove
    removed = False
    if svc_dir and (svc_dir / ".git").exists():
        rc, out, err = run_cmd(f"git worktree remove --force {target_path}", cwd=svc_dir)
        if rc == 0:
            removed = True

    if not removed and target_path.exists():
        shutil.rmtree(target_path, ignore_errors=True)
        removed = True

    if wt_name in wts:
        del wts[wt_name]
        save_registry(reg)

    sync_all()
    print(f"[OK] Đã xóa worktree '{wt_name}' và cập nhật registry.")


def cmd_check(args):
    """Kiểm tra xem có worktree nào vi phạm (nằm trong workspace hoặc service con)"""
    violations = []
    for svc_key, rel_path in SERVICES_MAP.items():
        svc_dir = WORKSPACE_ROOT / rel_path
        if not (svc_dir / ".git").exists():
            continue
        rc, out, _ = run_cmd("git worktree list", cwd=svc_dir)
        if rc == 0 and out:
            lines = out.splitlines()
            for line in lines[1:]:
                parts = line.split()
                if not parts:
                    continue
                w_path = Path(parts[0]).resolve()
                if WORKSPACE_ROOT in w_path.parents or w_path == WORKSPACE_ROOT:
                    violations.append((svc_key, str(w_path)))

    if violations:
        print("[VIOLATION DETECTED] Phát hiện worktree nằm sai vị trí (bên trong workspace):")
        for svc, p in violations:
            print(f" - Service: {svc} -> Đường dẫn: {p}")
        print(f"👉 Yêu cầu: Di chuyển ra {WORKTREES_DIR} bằng 'git worktree move'")
        sys.exit(1)
    else:
        print(f"[PASS] 100% Worktrees đều nằm đúng tại {WORKTREES_DIR}. Không có worktree nào nằm trong workspace.")


def main():
    parser = argparse.ArgumentParser(description="Git Worktree Registry & Lifecycle Manager")
    subparsers = parser.add_subparsers(dest="command")

    # list
    subparsers.add_parser("list", help="Liệt kê danh sách tất cả worktrees trong registry")
    # sync
    subparsers.add_parser("sync", help="Đồng bộ lại registry từ git worktree list thật")
    # check
    subparsers.add_parser("check", help="Kiểm tra xem có worktree nào vi phạm nằm trong workspace")

    # add
    p_add = subparsers.add_parser("add", help="Tạo worktree mới đúng chuẩn và tự động ghi sổ bộ")
    p_add.add_argument("--service", required=True, help="Tên service (vd: accounting-service, ws-acct-frontend)")
    p_add.add_argument("--name", required=True, help="Tên thư mục worktree tại Documents/worktrees/")
    p_add.add_argument("--branch", required=True, help="Tên nhánh git")
    p_add.add_argument("--task", default="N/A", help="Mã Task/Use Case (vd: UC-04, UC-05)")
    p_add.add_argument("--purpose", default="", help="Mục đích của worktree")
    p_add.add_argument("--new-branch", action="store_true", help="Tạo nhánh mới với cờ -b")

    # remove
    p_rm = subparsers.add_parser("remove", help="Xóa worktree an toàn và dọn registry")
    p_rm.add_argument("--name", required=True, help="Tên thư mục worktree cần xóa")

    args = parser.parse_args()
    if not args.command or args.command == "list":
        cmd_list(args)
    elif args.command == "sync":
        sync_all()
        print("[OK] Đã đồng bộ sổ bộ worktree thành công!")
    elif args.command == "check":
        cmd_check(args)
    elif args.command == "add":
        cmd_add(args)
    elif args.command == "remove":
        cmd_remove(args)


if __name__ == "__main__":
    main()

