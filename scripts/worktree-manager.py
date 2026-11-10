#!/usr/bin/env python3
"""
Worktree Registry & Lifecycle Manager for gdt-workspace
Quản lý tập trung, chuẩn hóa vị trí và sổ bộ Git Worktrees cho toàn bộ Microservices.

Vị trí worktree chuẩn bắt buộc: ~/Documents/worktrees/<name> (hoặc biến môi trường WORKTREES_DIR)
Sổ bộ lưu trữ: doc/governance/standards/worktree-registry.json
"""

import argparse
import fcntl
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape


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

    for cfg_candidate in [Path.cwd() / ".agent-base.local.json", Path(__file__).resolve().parent.parent / "projects.local.json", Path(__file__).resolve().parent.parent / "projects.json"]:
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


def save_registry(data, force: bool = False) -> bool:
    REGISTRY_JSON.parent.mkdir(parents=True, exist_ok=True)
    if not force and REGISTRY_JSON.exists() and REGISTRY_MD.exists():
        prev = load_registry()
        if (
            prev.get("worktrees") == data.get("worktrees")
            and prev.get("version", "1.0.0") == data.get("version", "1.0.0")
        ):
            return False
    data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(REGISTRY_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    export_markdown(data)
    return True


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


def _wait_until_worktree_ready(wt_path: Path, timeout_sec: float = 5.0) -> None:
    """Chờ ngắn nếu `git worktree add` vừa chạy xong chưa nhả `index.lock`."""
    git_entry = wt_path / ".git"
    if not git_entry.exists():
        return
    git_dir: Path | None = None
    if git_entry.is_dir():
        git_dir = git_entry
    elif git_entry.is_file():
        try:
            first_line = git_entry.read_text(encoding="utf-8", errors="ignore").splitlines()[0].strip()
            if first_line.lower().startswith("gitdir:"):
                raw = Path(first_line.split(":", 1)[1].strip())
                git_dir = raw if raw.is_absolute() else (wt_path / raw).resolve()
        except Exception:
            return
    if not git_dir:
        return
    lock_file = git_dir / "index.lock"
    deadline = time.monotonic() + timeout_sec
    while lock_file.exists() and time.monotonic() < deadline:
        time.sleep(0.2)


def _is_git_tracked(repo_dir: Path, rel_path: str) -> bool:
    """Trả về True nếu đường dẫn đang được Git theo dõi trong repo/worktree."""
    rc, _, _ = run_cmd(f"git ls-files --error-unmatch -- {rel_path}", cwd=repo_dir)
    return rc == 0


def _restore_tracked_symlink_if_needed(repo_dir: Path, rel_path: str) -> None:
    """Phục hồi file được git track nếu từng bị thay nhầm thành symlink bởi phiên bản cũ."""
    target = repo_dir / rel_path
    if not target.is_symlink() or not _is_git_tracked(repo_dir, rel_path):
        return
    rc, status_out, _ = run_cmd(f"git status --porcelain -- {rel_path}", cwd=repo_dir)
    if rc == 0 and status_out.startswith("T"):
        run_cmd(f"git checkout -- {rel_path}", cwd=repo_dir)
    elif rc == 0 and "T " in status_out[:3]:
        run_cmd(f"git checkout -- {rel_path}", cwd=repo_dir)


def _ensure_symlink(link_path: Path, target_path: Path, allow_replace_regular: bool = True) -> None:
    """Tạo hoặc cập nhật symlink trỏ về target_path, fallback copy nếu OS không hỗ trợ."""
    if not target_path.exists():
        return
    if link_path.is_symlink():
        try:
            if link_path.resolve() == target_path.resolve():
                return
        except OSError:
            pass
        link_path.unlink()
    elif link_path.exists():
        if not allow_replace_regular:
            return
        if link_path.is_dir():
            return
        link_path.unlink()
    try:
        link_path.symlink_to(target_path, target_is_directory=target_path.is_dir())
    except Exception:
        if not target_path.is_dir():
            try:
                shutil.copy2(target_path, link_path)
            except Exception:
                pass


def _detect_doc_dir(ws_root: Path) -> str:
    if (ws_root / "doc").is_dir():
        return "doc"
    if (ws_root / "docs").is_dir():
        return "docs"
    return "doc"


def _detect_xerj_prefix(ws_root: Path) -> str:
    name = ws_root.name.lower()
    if "gdt" in name:
        return "gdt"
    if "tiktok" in name or "shoppe" in name:
        return "tiktok"
    if "agent" in name:
        return "agentbase"
    slug = re.sub(r"[^a-z0-9]+", "-", name).strip("-")
    return slug or "ax"


def _infer_task_code(wt_path: Path, branch: str = "", existing_task: str = "") -> str:
    if existing_task and existing_task != "N/A":
        return existing_task
    tokens = re.split(r"[-_/]", f"{wt_path.name}-{branch}".upper())
    for tok in tokens:
        if re.match(r"^(UC\d+|T\d+|MANTIS\d+)$", tok):
            if tok.startswith("UC") and "-" not in tok and len(tok) > 2:
                return f"UC-{tok[2:]}"
            return tok
    return "N/A"


def _infer_feature_dirs(ws_root: Path, doc_dir: str, wt_path: Path, task_code: str = "") -> list[str]:
    """Tìm thư mục hồ sơ chức năng khớp worktree hoặc mã task trong <doc>/features/."""
    features_dir = ws_root / doc_dir / "features"
    if not features_dir.is_dir():
        return []
    haystack = re.sub(r"[^a-z0-9]", "", f"{wt_path.name} {task_code}".lower())
    matches = []
    for entry in sorted(features_dir.iterdir()):
        if not entry.is_dir():
            continue
        m = re.match(r"^(uc[-_]?\d+|tmp[-_][a-z0-9-]+)", entry.name.lower())
        if not m:
            continue
        key = re.sub(r"[^a-z0-9]", "", m.group(1))
        if key and key in haystack:
            matches.append(f"{doc_dir}/features/{entry.name}/")
    return matches


def _build_worktree_claude_md(
    wt_path: Path,
    ws_root: Path,
    agentbase_root: Path,
    doc_dir: str,
    service_name: str,
    task_code: str,
    has_root_claude: bool,
    has_root_project: bool,
) -> str:
    xerj_prefix = _detect_xerj_prefix(ws_root)
    feature_dirs = _infer_feature_dirs(ws_root, doc_dir, wt_path, task_code)
    doc_links = [
        f"- **Tài liệu của task giữ nguyên tại dự án gốc** (symlink trực tiếp trong worktree): `doc.workspace/` -> `{ws_root / doc_dir}`",
    ]
    if has_root_project:
        doc_links.append("- Tổng quan workspace & lệnh build/test: `@PROJECT.workspace.md`")
    if (ws_root / doc_dir / "architecture" / "CODEMAP.md").is_file():
        doc_links.append(f"- Bản đồ kiến trúc & ranh giới service: `doc.workspace/architecture/CODEMAP.md` (`{ws_root / doc_dir / 'architecture' / 'CODEMAP.md'}`)")
    if (ws_root / doc_dir / "delivery" / "tasks" / "BOARD.md").is_file():
        doc_links.append(f"- Bảng task hiện hành: `doc.workspace/delivery/tasks/BOARD.md` (`{ws_root / doc_dir / 'delivery' / 'tasks' / 'BOARD.md'}`)")
    elif (ws_root / "tasks" / "BOARD.md").is_file():
        doc_links.append(f"- Bảng task hiện hành: `{ws_root / 'tasks' / 'BOARD.md'}`")
    if (ws_root / doc_dir / "architecture" / "engineering").is_dir():
        doc_links.append(f"- Quy ước code & DB/API/Test: `doc.workspace/architecture/engineering/`")
    if feature_dirs:
        for fdir in feature_dirs:
            rel_inside_doc = fdir.split("/", 1)[1] if "/" in fdir else fdir
            doc_links.append(f"- **Hồ sơ chức năng khớp worktree**: `doc.workspace/{rel_inside_doc}` (`{ws_root / fdir}`) — đặc tả, đối chiếu, `tasks/`, sơ đồ")
    elif (ws_root / doc_dir / "features").is_dir():
        doc_links.append(f"- Thư mục đặc tả chức năng: `doc.workspace/features/` (`{ws_root / doc_dir / 'features'}`)")

    imports = ["@AGENTS.workspace.md"]
    if has_root_claude:
        imports.append("@CLAUDE.workspace.md")
    if has_root_project:
        imports.append("@PROJECT.workspace.md")

    svc_label = service_name or wt_path.name
    has_task = bool(task_code and task_code != "N/A")
    task_label = task_code if has_task else "theo nhánh hiện tại"
    preflight_flag = f"--uc {task_code}" if has_task else "--list"
    docs_block = "\n".join(doc_links)

    return f"""# Hướng dẫn Claude Code cho Git Worktree (`{wt_path.name}`)

Thư mục này là một Git Worktree độc lập (`service`: `{svc_label}`, `task`: `{task_label}`) thuộc workspace `{ws_root}`.

## 1. Challenge Gate & Pre-Code Doc Gate (BẮT BUỘC trước khi thiết kế, hỏi ngược hay sửa code)
1. Chạy trước 1 lệnh kiểm phiên bản tài liệu (tự động nối từ worktree về `doc.workspace/` ở dự án gốc):
   `python3 {agentbase_root}/scripts/doc-preflight.py --root . {preflight_flag}`
2. Đọc đúng `Active Source` mới nhất ở workspace gốc trước khi đoán từ code hoặc hỏi lại người dùng (bỏ qua `archive/`, file gắn `SUPERSEDED`, card `cancelled`):
{docs_block}
3. **Phản biện trước khi code (Challenge Gate)**: Với task vừa/lớn hoặc đề bài mơ hồ, xuất **3 phương án + 1 khuyến nghị + rủi ro 10x scale** và đối chiếu toàn bộ yêu cầu / `- [ ] AC-xx` trong Task Card trước khi sửa source. Có thể bật khóa phạm vi pha `plan` bằng `python3 {agentbase_root}/scripts/task-gate.py set-scope --root . --mode plan`.
4. Nếu `.docx`/`.xlsx` mới hơn `.md` -> dừng code để đối chiếu/convert; nếu XERJ báo `index_stale` hoặc file vừa sửa -> đọc trực tiếp trên đĩa bằng `safe-search.py` + `read_file`.
5. Nếu file `AGENTS.md` bản stub nằm sẵn trong repo con khác với quy tắc workspace: **luôn theo `AGENTS.workspace.md` và `CLAUDE.workspace.md`** (symlink từ `{ws_root}`).

## 2. Tra cứu mã nguồn AST & phạm vi XERJ ở Worktree
- **Code nền, thư viện dùng chung (`platform/*`) & tài liệu `{doc_dir}/`**: dùng MCP `xerj_def` / `xerj_search` với `prefix="{xerj_prefix}"`.
- **File mới tạo hoặc đang sửa cục bộ trong worktree `{wt_path.name}`**: root index `{xerj_prefix}` chỉ lập chỉ mục `{ws_root}` (không lập chỉ mục `{WORKTREES_DIR}`), nên hãy dùng `python3 {agentbase_root}/scripts/safe-search.py -q "<chuỗi/tên>" -d .` kết hợp `read_file`.
- **CẤM TUYỆT ĐỐI** mọi hình thức dùng `grep`, `egrep`, `rg`, `find`, `cat` hoặc inline script để dò tìm mã nguồn.

## 3. Clean Code, Thuật ngữ & Cổng Kiểm Trước Khi Báo Xong
- Sửa file bằng `Edit`/`Write`; **cấm dùng inline Python heredoc (`python3 - <<'EOF'`, `sed`, `perl`)** để vá source.
- Không để unused imports, không viết FQN nội tuyến thay `import` (trừ trùng tên), dùng `enum`/hằng số thay magic String.
- Module Java có Spotless: chạy `./mvnw spotless:apply -DspotlessFiles='.*<TenFile>\\.java'` chỉ trên file vừa tạo/sửa và lọc `-Dtest=<TenTest>` (không `spotless:apply` toàn repo).
- **Trước khi báo hoàn thành**: chạy cổng kiểm tự động (luật cứng + thuật ngữ + kiểm đủ AC / chống skip test `RH-1` / placeholder `RH-4`):
  `python3 {agentbase_root}/scripts/verify-gate.py run --root . --changed-against develop` (và kiểm tra `doc.workspace/` khi sửa tài liệu/UI).

{chr(10).join(imports)}
"""


def inject_worktree_rules(wt_path: Path, service_name: str = "", task_code: str = ""):
    """Đảm bảo mọi worktree đều kế thừa đầy đủ luật workspace, docs dự án và hook an toàn mà không làm bẩn git."""
    if not wt_path.is_dir():
        return

    _wait_until_worktree_ready(wt_path)
    agentbase_root = Path(__file__).resolve().parent.parent
    doc_dir = _detect_doc_dir(WORKSPACE_ROOT)

    root_agents = WORKSPACE_ROOT / "AGENTS.md" if (WORKSPACE_ROOT / "AGENTS.md").exists() else agentbase_root / "AGENTS.md"
    root_claude = WORKSPACE_ROOT / "CLAUDE.md"
    root_project = WORKSPACE_ROOT / "PROJECT.md"
    root_gemini = WORKSPACE_ROOT / "GEMINI.md" if (WORKSPACE_ROOT / "GEMINI.md").exists() else agentbase_root / "GEMINI.md"
    root_doc = WORKSPACE_ROOT / doc_dir
    root_ai_rules = WORKSPACE_ROOT / ".ai-rules"
    hub_claude_dir = agentbase_root / ".claude"
    hub_mcp = WORKSPACE_ROOT / "mcp.json" if (WORKSPACE_ROOT / "mcp.json").exists() else agentbase_root / "mcp.json"

    # 1. Giữ sạch AGENTS.md nếu bị git track trong repo con; luôn tạo AGENTS.workspace.md
    _restore_tracked_symlink_if_needed(wt_path, "AGENTS.md")
    agents_tracked = _is_git_tracked(wt_path, "AGENTS.md")
    if root_agents.exists():
        _ensure_symlink(wt_path / "AGENTS.workspace.md", root_agents)
        if not agents_tracked:
            _ensure_symlink(wt_path / "AGENTS.md", root_agents)

    has_root_claude = root_claude.is_file()
    if has_root_claude:
        _ensure_symlink(wt_path / "CLAUDE.workspace.md", root_claude)

    has_root_project = root_project.is_file()
    if has_root_project:
        _ensure_symlink(wt_path / "PROJECT.workspace.md", root_project)

    if root_doc.is_dir() and not _is_git_tracked(wt_path, "doc.workspace"):
        _ensure_symlink(wt_path / "doc.workspace", root_doc, allow_replace_regular=False)

    if root_ai_rules.is_dir() and not _is_git_tracked(wt_path, ".ai-rules.workspace"):
        _ensure_symlink(wt_path / ".ai-rules.workspace", root_ai_rules, allow_replace_regular=False)

    # 2. Tạo/cập nhật CLAUDE.md (idempotent, trừ khi file bị git track trong service)
    if not _is_git_tracked(wt_path, "CLAUDE.md"):
        claude_text = _build_worktree_claude_md(
            wt_path=wt_path,
            ws_root=WORKSPACE_ROOT,
            agentbase_root=agentbase_root,
            doc_dir=doc_dir,
            service_name=service_name,
            task_code=task_code,
            has_root_claude=has_root_claude,
            has_root_project=has_root_project,
        )
        claude_file = wt_path / "CLAUDE.md"
        try:
            current_claude = claude_file.read_text(encoding="utf-8") if claude_file.exists() else None
            if current_claude != claude_text:
                claude_file.write_text(claude_text, encoding="utf-8")
        except Exception:
            pass

    # 3. Symlink GEMINI.md, .claude, mcp.json (không đụng file tracked)
    if root_gemini.exists() and not _is_git_tracked(wt_path, "GEMINI.md"):
        _ensure_symlink(wt_path / "GEMINI.md", root_gemini)

    if hub_claude_dir.is_dir() and not _is_git_tracked(wt_path, ".claude"):
        _ensure_symlink(wt_path / ".claude", hub_claude_dir, allow_replace_regular=False)

    if hub_mcp.exists() and not _is_git_tracked(wt_path, "mcp.json"):
        _ensure_symlink(wt_path / "mcp.json", hub_mcp, allow_replace_regular=False)

    # 4. Đảm bảo worktree không hiển thị các file/symlink AI này trong git status bằng git-common-dir/info/exclude
    rc, common_dir_str, _ = run_cmd("git rev-parse --git-common-dir", cwd=wt_path)
    git_common_dir = Path(common_dir_str).resolve() if (rc == 0 and common_dir_str) else None
    if not git_common_dir or not git_common_dir.exists():
        git_file = wt_path / ".git"
        if git_file.is_dir():
            git_common_dir = git_file

    if git_common_dir and git_common_dir.exists():
        exclude_file = git_common_dir / "info" / "exclude"
        try:
            exclude_file.parent.mkdir(parents=True, exist_ok=True)
            existing = exclude_file.read_text(encoding="utf-8") if exclude_file.exists() else ""
            existing_lines = {line.strip() for line in existing.splitlines()}
            needed = [
                "AGENTS.workspace.md",
                "CLAUDE.workspace.md",
                "PROJECT.workspace.md",
                "doc.workspace",
                ".ai-rules.workspace",
                ".agentbase-scope.json",
                "CLAUDE.md",
                "GEMINI.md",
                "CODEX.md",
                "mcp.json",
                "mcp.local.json",
                ".claude",
                ".claude/",
                ".kilo",
                ".kilo/",
                ".agents",
                ".agents/",
                ".qoder",
                ".qoder/",
                "project-graph.json",
                "graphify-out/",
            ]
            if not agents_tracked:
                needed.insert(0, "AGENTS.md")
            to_add = [n for n in needed if n not in existing_lines]
            if to_add:
                with open(exclude_file, "a", encoding="utf-8") as f:
                    f.write("\n# Agent-base and AI assistant rules\n" + "\n".join(to_add) + "\n")
        except Exception:
            pass


def _belongs_to_workspace(wt_path: Path, ws_root: Path) -> bool:
    """Tránh gắn nhầm rules của workspace này sang worktree thuộc một dự án khác dùng chung WORKTREES_DIR."""
    if not (wt_path / ".git").exists():
        return True
    rc, common_str, _ = run_cmd("git rev-parse --git-common-dir", cwd=wt_path)
    if rc != 0 or not common_str:
        return True
    common_raw = Path(common_str)
    common_dir = (common_raw if common_raw.is_absolute() else (wt_path / common_raw)).resolve()
    ws_res = ws_root.resolve()
    return common_dir == ws_res or ws_res in common_dir.parents


def _sync_all_impl():
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

    # Quét thư mục WORKTREES_DIR để đối chiếu (kể cả worktree tạo bằng `git worktree add` hoặc IDE)
    if WORKTREES_DIR.exists():
        for item in WORKTREES_DIR.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                name = item.name
                if (item / ".git").exists() or (item / "run.sh").exists():
                    if not _belongs_to_workspace(item, WORKSPACE_ROOT):
                        continue
                    rc, b_out, _ = run_cmd("git branch --show-current", cwd=item)
                    branch = b_out if rc == 0 and b_out else "N/A"
                    if name not in scanned_wts:
                        # Suy luận service theo SERVICES_MAP hoặc repo gốc
                        matched_svc = "unknown"
                        for s_key in SERVICES_MAP.keys():
                            if s_key in name or (s_key == "ws-acct-frontend" and "frontend" in name):
                                matched_svc = s_key
                                break
                        if matched_svc == "unknown" and (item / ".git").exists():
                            rc_c, common_s, _ = run_cmd("git rev-parse --git-common-dir", cwd=item)
                            if rc_c == 0 and common_s:
                                c_raw = Path(common_s)
                                c_dir = (c_raw if c_raw.is_absolute() else (item / c_raw)).resolve()
                                matched_svc = c_dir.parent.name
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
        branch_name = info.get("branch") or existing.get("branch", "N/A")
        task = _infer_task_code(wt_path, branch_name, existing.get("task", ""))
        inject_worktree_rules(wt_path, service_name=svc, task_code=task)

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


def sync_all(debounce_sec: float = 0.0):
    if debounce_sec > 0:
        time.sleep(debounce_sec)
    slug = re.sub(r"[^a-zA-Z0-9_-]", "_", WORKSPACE_ROOT.name or "workspace")[:80]
    lock_path = Path(tempfile.gettempdir()) / f"agentbase-wt-sync-{slug}.lock"
    try:
        with open(lock_path, "w", encoding="utf-8") as lock_file:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
            return _sync_all_impl()
    except OSError:
        return _sync_all_impl()


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


WATCHER_LABEL = "com.agentbase.worktree-sync"
DEFAULT_LAUNCH_AGENT_PLIST = Path.home() / "Library" / "LaunchAgents" / f"{WATCHER_LABEL}.plist"


def render_watcher_plist(
    python_bin: str,
    script_path: Path,
    watch_dir: Path,
    ws_root: Path,
    log_file: Path,
) -> str:
    """Sinh cấu hình LaunchAgent WatchPaths (macOS FSEvents, 0% CPU polling) để tự đồng bộ ngay khi có worktree mới."""
    args_xml = "\n".join(
        f"        <string>{xml_escape(arg)}</string>"
        for arg in [
            python_bin,
            str(script_path.resolve()),
            "sync",
            "--debounce",
            "1.5",
            "--quiet",
        ]
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{WATCHER_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
{args_xml}
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>WORKSPACE_ROOT</key>
        <string>{xml_escape(str(ws_root.resolve()))}</string>
        <key>WORKTREES_DIR</key>
        <string>{xml_escape(str(watch_dir.resolve()))}</string>
    </dict>
    <key>WatchPaths</key>
    <array>
        <string>{xml_escape(str(watch_dir.resolve()))}</string>
    </array>
    <key>ThrottleInterval</key>
    <integer>2</integer>
    <key>StandardOutPath</key>
    <string>{xml_escape(str(log_file))}</string>
    <key>StandardErrorPath</key>
    <string>{xml_escape(str(log_file))}</string>
</dict>
</plist>
"""


def install_watcher(
    plist_path: Path | None = None,
    load_launchd: bool = True,
    python_bin: str | None = None,
) -> Path:
    """Cài LaunchAgent WatchPaths theo dõi thư mục worktrees để tự động đồng bộ liên tục."""
    target_plist = plist_path or DEFAULT_LAUNCH_AGENT_PLIST
    target_plist.parent.mkdir(parents=True, exist_ok=True)
    log_file = Path.home() / ".agentbase" / "logs" / "worktree-sync.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    WORKTREES_DIR.mkdir(parents=True, exist_ok=True)

    plist_xml = render_watcher_plist(
        python_bin=python_bin or sys.executable,
        script_path=Path(__file__).resolve(),
        watch_dir=WORKTREES_DIR,
        ws_root=WORKSPACE_ROOT,
        log_file=log_file,
    )
    target_plist.write_text(plist_xml, encoding="utf-8")

    if load_launchd and sys.platform == "darwin":
        subprocess.run(["launchctl", "unload", str(target_plist)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res = subprocess.run(["launchctl", "load", "-w", str(target_plist)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Không thể nạp LaunchAgent {target_plist}: {res.stderr.strip()}")
    return target_plist


def uninstall_watcher(plist_path: Path | None = None, unload_launchd: bool = True) -> bool:
    target_plist = plist_path or DEFAULT_LAUNCH_AGENT_PLIST
    if unload_launchd and sys.platform == "darwin" and target_plist.exists():
        subprocess.run(["launchctl", "unload", str(target_plist)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if target_plist.exists():
        target_plist.unlink()
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Git Worktree Registry & Lifecycle Manager")
    subparsers = parser.add_subparsers(dest="command")

    # list
    subparsers.add_parser("list", help="Liệt kê danh sách tất cả worktrees trong registry")
    # sync
    p_sync = subparsers.add_parser("sync", help="Đồng bộ lại registry và rules từ git worktree list thật")
    p_sync.add_argument("--debounce", type=float, default=0.0, help="Chờ N giây trước khi sync (dùng cho FSEvents watcher)")
    p_sync.add_argument("--quiet", action="store_true", help="Không in log khi chạy ngầm")
    # check
    subparsers.add_parser("check", help="Kiểm tra xem có worktree nào vi phạm nằm trong workspace")
    # install-watcher / uninstall-watcher
    subparsers.add_parser("install-watcher", help="Cài macOS LaunchAgent WatchPaths tự động sync khi có worktree mới")
    subparsers.add_parser("uninstall-watcher", help="Gỡ macOS LaunchAgent tự động sync worktree")

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

    # inject (chỉ gắn rules/symlinks vào 1 worktree cụ thể, không ghi registry nếu không cần)
    p_inj = subparsers.add_parser("inject", help="Gắn rules, symlinks workspace & info/exclude vào 1 worktree cụ thể")
    p_inj.add_argument("--path", required=True, help="Đường dẫn thư mục worktree")
    p_inj.add_argument("--service", default="", help="Tên service")
    p_inj.add_argument("--task", default="", help="Mã task/UC")

    args = parser.parse_args()
    if not args.command or args.command == "list":
        cmd_list(args)
    elif args.command == "sync":
        sync_all(debounce_sec=args.debounce)
        if not args.quiet:
            print("[OK] Đã đồng bộ sổ bộ worktree thành công!")
    elif args.command == "check":
        cmd_check(args)
    elif args.command == "install-watcher":
        p = install_watcher()
        print(f"[OK] Đã bật theo dõi tự động ({WATCHER_LABEL}) tại {p} -> theo dõi {WORKTREES_DIR}")
    elif args.command == "uninstall-watcher":
        removed = uninstall_watcher()
        print("[OK] Đã gỡ LaunchAgent tự đồng bộ worktree." if removed else "[INFO] Chưa cài LaunchAgent nào.")
    elif args.command == "add":
        cmd_add(args)
    elif args.command == "remove":
        cmd_remove(args)
    elif args.command == "inject":
        inject_worktree_rules(Path(args.path).expanduser().resolve(), service_name=args.service, task_code=args.task)
        print(f"[OK] Đã cấu hình rules & doc.workspace cho worktree {args.path}")


if __name__ == "__main__":
    main()

