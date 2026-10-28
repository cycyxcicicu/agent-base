#!/usr/bin/env python3
"""
scripts/serve-dashboard.py
Máy chủ HTTP thông minh phục vụ Dashboard và tự động điều hướng (proxy) tới ảnh, sơ đồ,
tài liệu thật của các dự án (không bao giờ bị 404).

Dùng:
  python3 scripts/serve-dashboard.py [--port 8899]
"""

from __future__ import annotations
import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
import os
from pathlib import Path
import sys
import urllib.parse

ROOT = Path(__file__).resolve().parent.parent
VIEWER_DIR = ROOT / "build" / "viewer"
PROJECTS_FILE = ROOT / "projects.json"


def get_project_roots() -> list[Path]:
    roots = []
    if PROJECTS_FILE.is_file():
        try:
            data = json.loads(PROJECTS_FILE.read_text(encoding="utf-8"))
            for p in data.get("projects", []):
                pth = Path(p.get("path", "")).resolve()
                if pth.is_dir() and pth not in roots:
                    roots.append(pth)
        except Exception:
            pass
    # Thêm gdt-workspace mặc định nếu chưa có
    ws = ROOT.parent / "gdt-workspace" if ROOT.name == "agent-base" else ROOT.parent
    if ws.is_dir() and ws not in roots:
        roots.append(ws)
    return roots


class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(VIEWER_DIR), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        req_path = urllib.parse.unquote(parsed.path).lstrip("/")

        # 1. Nếu yêu cầu file trong doc/ hoặc docs/ hoặc file ảnh/sơ đồ của dự án
        if req_path.startswith("doc/") or req_path.startswith("docs/") or req_path.startswith("hinh/"):
            for p_root in get_project_roots():
                candidate = (p_root / req_path).resolve()
                if candidate.is_file():
                    return self._serve_real_file(candidate)
                # Thử fallback: nếu req_path là hinh/... -> thử p_root / doc / srs / hinh / ...
                if req_path.startswith("hinh/"):
                    sub_cand = (p_root / "doc" / "srs" / req_path).resolve()
                    if sub_cand.is_file():
                        return self._serve_real_file(sub_cand)

        # 2. Phục vụ bình thường từ VIEWER_DIR
        local_file = (VIEWER_DIR / req_path).resolve()
        if not req_path or parsed.path == "/":
            local_file = VIEWER_DIR / "index.html"

        if local_file.is_file():
            return self._serve_real_file(local_file)

        # 3. Thử tìm lần cuối trong các dự án
        for p_root in get_project_roots():
            candidate = (p_root / req_path).resolve()
            if candidate.is_file():
                return self._serve_real_file(candidate)

        # Không tìm thấy
        self.send_error(404, f"Không tìm thấy file: {req_path}")

    def _serve_real_file(self, file_path: Path):
        try:
            ctype, _ = mimetypes.guess_type(str(file_path))
            if not ctype:
                if file_path.suffix.lower() == ".drawio":
                    ctype = "application/xml"
                elif file_path.suffix.lower() == ".md":
                    ctype = "text/plain; charset=utf-8"
                else:
                    ctype = "application/octet-stream"

            data = file_path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_error(500, f"Lỗi đọc file: {e}")


def main():
    parser = argparse.ArgumentParser(description="Chạy Dashboard Server")
    parser.add_argument("--port", type=int, default=8899, help="Cổng chạy máy chủ (mặc định 8899)")
    args = parser.parse_args()

    # Tự động build lại nếu chưa có thư mục
    if not (VIEWER_DIR / "index.html").is_file():
        print("🔨 Đang tự động dựng Dashboard...")
        import subprocess
        subprocess.run([sys.executable, str(ROOT / "scripts" / "generate-dashboard.py")], check=True)

    server_address = ("", args.port)
    httpd = ThreadingHTTPServer(server_address, DashboardHandler)
    print(f"🚀 Dashboard Server đang chạy tại: http://localhost:{args.port}/index.html")
    print(f"📁 Phục vụ giao diện: {VIEWER_DIR}")
    print(f"🔗 Tự động liên kết ảnh/sơ đồ từ: {[str(r) for r in get_project_roots()]}")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
