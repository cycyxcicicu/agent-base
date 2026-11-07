#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/sync-mcp.py

Bộ Đồng Bộ Cấu Hình MCP Đa Nền Tảng (Universal MCP Synchronizer).
Quản lý tập trung (SSOT) danh mục MCP Servers từ agent-base và tự động xuất ra:
  1. Claude Code:          <target>/mcp.json (và ~/.claude.json nếu --global)
  2. Kilo Code:            <target>/.kilo/mcp.json
  3. Gemini / Antigravity: ~/.gemini/config/mcp_config.json
  4. Cursor:               <target>/.cursor/mcp.json

Bảo mật:
- Tự động nạp agent-base/mcp/mcp-servers.template.json (an toàn, commit được)
- Nếu có agent-base/mcp/mcp-servers.local.json (chứa secret cá nhân), nạp đè lên
- Các file mcp.json và .kilo/mcp.json trong project luôn được chặn bởi .gitignore

Usage:
  python3 scripts/sync-mcp.py --target /path/to/project
  python3 scripts/sync-mcp.py --all-projects
  python3 scripts/sync-mcp.py --global
"""

import argparse
import copy
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MCP_DIR = ROOT / "mcp"
TEMPLATE_FILE = MCP_DIR / "mcp-servers.template.json"
LOCAL_FILE = MCP_DIR / "mcp-servers.local.json"
PROJECTS_FILE = ROOT / "projects.local.json" if (ROOT / "projects.local.json").exists() else (ROOT / "projects.json")


def resolve_command_path(cmd: str) -> str:
    """Tự động phân giải đường dẫn binary theo máy hiện tại (tránh hardcode đường dẫn cá nhân)."""
    if not cmd:
        return cmd
    # Nếu là đường dẫn tương đối hoặc lệnh trần (ví dụ 'xerj', 'graphify-mcp')
    if not os.path.isabs(cmd):
        which_cmd = shutil.which(cmd)
        if which_cmd:
            return which_cmd
        local_bin = Path.home() / ".local" / "bin" / cmd
        if local_bin.is_file():
            return str(local_bin)
    else:
        # Nếu là đường dẫn tuyệt đối nhưng thuộc về máy người khác (chứa /Users/...), thử phân giải lại
        cmd_path = Path(cmd)
        if not cmd_path.is_file():
            which_cmd = shutil.which(cmd_path.name)
            if which_cmd:
                return which_cmd
            local_bin = Path.home() / ".local" / "bin" / cmd_path.name
            if local_bin.is_file():
                return str(local_bin)
    return cmd


def load_master_servers() -> dict:
    """Nạp danh mục MCP Servers master từ template + local override."""
    servers = {}

    # 1. Nạp template nếu có
    if TEMPLATE_FILE.is_file():
        try:
            with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                servers.update(data.get("mcpServers", {}))
        except Exception as e:
            print(f"⚠️ Không thể đọc {TEMPLATE_FILE}: {e}")

    # 2. Nạp local override nếu có (ưu tiên cao hơn)
    if LOCAL_FILE.is_file():
        try:
            with open(LOCAL_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                servers.update(data.get("mcpServers", {}))
        except Exception as e:
            print(f"⚠️ Không thể đọc {LOCAL_FILE}: {e}")

    return servers


def format_for_kilo(servers: dict) -> dict:
    """Định dạng cho Kilo Code (.kilo/mcp.json)."""
    kilo_servers = copy.deepcopy(servers)
    for srv in kilo_servers.values():
        if "command" in srv:
            srv["command"] = resolve_command_path(srv["command"])
    return {
        "$schema": "https://json.schemastore.org/kilo-mcp.json",
        "mcpServers": kilo_servers
    }


def format_for_claude(servers: dict) -> dict:
    """Định dạng cho Claude Code (mcp.json): chỉ lấy server enabled và bỏ metadata thừa."""
    claude_servers = {}
    for name, srv in servers.items():
        if srv.get("disabled", False):
            continue  # Bỏ qua các server bị tắt
        
        cfg = {}
        if "type" in srv:
            cfg["type"] = srv["type"]
        if "url" in srv:
            cfg["url"] = srv["url"]
        if "headers" in srv:
            cfg["headers"] = copy.deepcopy(srv["headers"])
        if "command" in srv:
            cfg["command"] = resolve_command_path(srv["command"])
        if "args" in srv:
            cfg["args"] = copy.deepcopy(srv["args"])
        if "env" in srv:
            cfg["env"] = copy.deepcopy(srv["env"])

        if cfg:
            claude_servers[name] = cfg

    return {
        "mcpServers": claude_servers
    }


def format_for_antigravity(servers: dict) -> dict:
    """Định dạng cho Antigravity / Gemini (~/.gemini/config/mcp_config.json)."""
    gemini_servers = {}
    for name, srv in servers.items():
        if srv.get("disabled", False):
            continue
        
        cfg = {}
        if "$typeName" in srv:
            cfg["$typeName"] = srv["$typeName"]
        if "type" in srv:
            cfg["type"] = srv["type"]
        if "url" in srv:
            cfg["url"] = srv["url"]
        if "command" in srv:
            cfg["command"] = resolve_command_path(srv["command"])
        if "args" in srv:
            cfg["args"] = copy.deepcopy(srv["args"])
        if "env" in srv:
            cfg["env"] = copy.deepcopy(srv["env"])
        if cfg:
            gemini_servers[name] = cfg

    return {
        "mcpServers": gemini_servers
    }


def ensure_gitignore(target_dir: Path) -> None:
    """Đảm bảo .gitignore của dự án đích chặn các file mcp cá nhân."""
    gitignore = target_dir / ".gitignore"
    rules = [
        ".kilo/mcp.json",
        ".kilo/mcp.local.json",
        ".kilo/kilo.jsonc",
        "mcp.json",
        "mcp.local.json",
        "*.mcp.local.json",
        "GEMINI.md",
        "graphify-out/",
        "project-graph.json"
    ]
    existing = gitignore.read_text(encoding="utf-8") if gitignore.is_file() else ""
    missing = [r for r in rules if r not in existing]
    if missing:
        with open(gitignore, "a", encoding="utf-8") as f:
            f.write("\n# MCP Config (Chặn tuyệt đối không commit lên Git)\n")
            for r in missing:
                f.write(f"{r}\n")
        print(f"  🔒 Cập nhật .gitignore tại: {target_dir}")


def sync_project(target_dir: Path, servers: dict) -> None:
    """Đồng bộ cấu hình MCP cho một thư mục dự án."""
    if not target_dir.is_dir():
        print(f"❌ Thư mục dự án không tồn tại: {target_dir}")
        return

    print(f"\n📂 Đồng bộ MCP cho dự án: {target_dir}")
    ensure_gitignore(target_dir)

    # 1. Kilo Code: <target>/.kilo/mcp.json
    kilo_dir = target_dir / ".kilo"
    kilo_dir.mkdir(parents=True, exist_ok=True)
    kilo_file = kilo_dir / "mcp.json"
    kilo_data = format_for_kilo(servers)
    with open(kilo_file, "w", encoding="utf-8") as f:
        json.dump(kilo_data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"  ✓ Kilo Code:        {kilo_file} ({len(kilo_data['mcpServers'])} servers)")

    # 2. Claude Code: <target>/mcp.json
    claude_file = target_dir / "mcp.json"
    claude_data = format_for_claude(servers)
    with open(claude_file, "w", encoding="utf-8") as f:
        json.dump(claude_data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"  ✓ Claude Code:      {claude_file} ({len(claude_data['mcpServers'])} active servers)")

    # 3. Cursor: <target>/.cursor/mcp.json (nếu thư mục .cursor tồn tại hoặc tạo mới)
    cursor_dir = target_dir / ".cursor"
    cursor_dir.mkdir(parents=True, exist_ok=True)
    cursor_file = cursor_dir / "mcp.json"
    with open(cursor_file, "w", encoding="utf-8") as f:
        json.dump(claude_data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"  ✓ Cursor IDE:       {cursor_file} ({len(claude_data['mcpServers'])} active servers)")


def sync_global(servers: dict) -> None:
    """Đồng bộ cấu hình toàn cục (Antigravity & Claude Global)."""
    print("\n🌐 Đang đồng bộ cấu hình MCP toàn cục trên máy...")

    # 1. Gemini / Antigravity: ~/.gemini/config/mcp_config.json
    gemini_config_dir = Path.home() / ".gemini" / "config"
    gemini_config_dir.mkdir(parents=True, exist_ok=True)
    gemini_file = gemini_config_dir / "mcp_config.json"
    gemini_data = format_for_antigravity(servers)

    # Giữ lại các thuộc tính đặc biệt của plugin Antigravity nếu có
    if gemini_file.is_file():
        try:
            with open(gemini_file, "r", encoding="utf-8") as f:
                old = json.load(f).get("mcpServers", {})
                for k, v in old.items():
                    if "$typeName" in v and k in gemini_data["mcpServers"]:
                        gemini_data["mcpServers"][k]["$typeName"] = v["$typeName"]
        except Exception:
            pass

    with open(gemini_file, "w", encoding="utf-8") as f:
        json.dump(gemini_data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"  ✓ Antigravity:      {gemini_file} ({len(gemini_data['mcpServers'])} active servers)")

    # 2. Claude Code Global: ~/.claude.json (bổ sung mcpServers nếu có)
    claude_global_file = Path.home() / ".claude.json"
    if claude_global_file.is_file():
        try:
            with open(claude_global_file, "r", encoding="utf-8") as f:
                cdata = json.load(f)
            
            if "mcpServers" not in cdata:
                cdata["mcpServers"] = {}

            claude_data = format_for_claude(servers)
            for k, v in claude_data["mcpServers"].items():
                cdata["mcpServers"][k] = v

            with open(claude_global_file, "w", encoding="utf-8") as f:
                json.dump(cdata, f, indent=2, ensure_ascii=False)
                f.write("\n")
            print(f"  ✓ Claude CLI Global:{claude_global_file} (Đã hợp nhất {len(claude_data['mcpServers'])} servers)")
        except Exception as e:
            print(f"⚠️ Không thể cập nhật {claude_global_file}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Bộ đồng bộ cấu hình MCP đa nền tảng từ agent-base")
    parser.add_argument("--target", help="Đường dẫn thư mục dự án cần đồng bộ")
    parser.add_argument("--all-projects", action="store_true", help="Đồng bộ toàn bộ các dự án trong projects.json")
    parser.add_argument("--global", dest="is_global", action="store_true", help="Đồng bộ cấu hình toàn cục (Antigravity & Claude Code)")
    args = parser.parse_args()

    servers = load_master_servers()
    if not servers:
        print("❌ Không tìm thấy MCP server nào trong mcp-servers.template.json hoặc mcp-servers.local.json!")
        sys.exit(1)

    print(f"🚀 Nạp thành công {len(servers)} MCP Servers từ agent-base/mcp/")

    # 1. Đồng bộ toàn cục nếu yêu cầu
    if args.is_global or (not args.target and not args.all_projects):
        sync_global(servers)

    # 2. Đồng bộ theo dự án cụ thể
    if args.target:
        sync_project(Path(args.target).resolve(), servers)
    elif args.all_projects:
        if PROJECTS_FILE.is_file():
            try:
                with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
                    pdata = json.load(f)
                for p in pdata.get("projects", []):
                    ppath = Path(p["path"]).expanduser().resolve()
                    if ppath.is_dir():
                        sync_project(ppath, servers)
            except Exception as e:
                print(f"❌ Lỗi đọc projects.json: {e}")
        else:
            print("⚠️ Không tìm thấy projects.json")
    else:
        # Mặc định: đồng bộ cho thư mục hiện tại nếu không truyền target
        cwd = Path.cwd().resolve()
        sync_project(cwd, servers)

    print("\n🎉 HOÀN TẤT ĐỒNG BỘ MCP ĐA NỀN TẢNG!")


if __name__ == "__main__":
    main()
