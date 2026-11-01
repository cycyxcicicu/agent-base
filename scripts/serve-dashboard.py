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
import threading
import time
import urllib.parse

ROOT = Path(__file__).resolve().parent.parent
VIEWER_DIR = ROOT / "build" / "viewer"
PROJECTS_FILE = ROOT / "projects.json"

MEDIA_EXTS = {".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp", ".ico", ".drawio", ".pdf", ".md", ".txt"}

CURRENT_VERSION = int(time.time())


SWARM_MODULE = None


def get_swarm_module():
    global SWARM_MODULE
    if SWARM_MODULE is None:
        try:
            import importlib.util
            script_path = ROOT / "scripts" / "watch-swarm.py"
            if script_path.is_file():
                spec = importlib.util.spec_from_file_location("watch_swarm", str(script_path))
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                SWARM_MODULE = mod
        except Exception as e:
            print(f"⚠️ [Swarm] Không thể tải watch-swarm: {e}")
    return SWARM_MODULE


class RealtimeWatcher:
    """Theo dõi tự động các thư mục tài liệu để quét và cập nhật Dashboard Realtime."""
    def __init__(self, check_interval: float = 1.5):
        self.check_interval = check_interval
        self.last_snapshot: dict[str, float] = {}
        self.running = True

    def get_snapshot(self) -> dict[str, float]:
        snap = {}
        watch_exts = {".md", ".html", ".svg", ".json", ".png", ".jpg", ".drawio"}
        for root in get_project_roots():
            if not root.is_dir():
                continue
            for folder_name in ("doc", "docs", "tasks"):
                folder = root / folder_name
                if not folder.is_dir():
                    continue
                try:
                    for p in folder.rglob("*"):
                        if p.is_file() and p.suffix.lower() in watch_exts:
                            if any(part in p.parts for part in ("node_modules", ".git", ".venv", "build", "dist")):
                                continue
                            try:
                                snap[str(p)] = p.stat().st_mtime
                            except Exception:
                                pass
                except Exception:
                    pass
        return snap

    def start(self):
        self.last_snapshot = self.get_snapshot()
        t = threading.Thread(target=self._run, daemon=True)
        t.start()

    def _run(self):
        global CURRENT_VERSION
        while self.running:
            time.sleep(self.check_interval)
            current = self.get_snapshot()
            if current != self.last_snapshot:
                self.last_snapshot = current
                print("⚡ [Realtime] Phát hiện tài liệu thay đổi trên đĩa! Đang tự động quét & cập nhật...")
                try:
                    import subprocess
                    gen_script = ROOT / "scripts" / "generate-dashboard.py"
                    subprocess.run([sys.executable, str(gen_script)], check=True)
                    FILE_INDEX.rescan()
                    CURRENT_VERSION = int(time.time())
                    print(f"✅ [Realtime] Đã tự động cập nhật Dashboard thành công! (v={CURRENT_VERSION})")
                except Exception as e:
                    print(f"⚠️ [Realtime] Lỗi tự động cập nhật: {e}")


REALTIME_WATCHER = RealtimeWatcher()


def get_project_roots() -> list[Path]:
    roots = []
    local_p = ROOT / "projects.local.json"
    p_file = local_p if local_p.is_file() else PROJECTS_FILE
    if p_file.is_file():
        try:
            data = json.loads(p_file.read_text(encoding="utf-8"))
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


class FileIndex:
    """Chỉ mục tập trung toàn bộ file ảnh, sơ đồ và tài liệu của các dự án để tra cứu O(1)."""
    def __init__(self):
        self.filename_map: dict[str, Path] = {}
        self.subpath_map: dict[str, Path] = {}
        self.refresh()

    def refresh(self):
        self.filename_map.clear()
        self.subpath_map.clear()
        for p_root in get_project_roots():
            if not p_root.is_dir():
                continue
            for doc_folder in ("doc", "docs"):
                d_path = p_root / doc_folder
                if not d_path.is_dir():
                    continue
                for f in d_path.rglob("*"):
                    if f.is_file():
                        fname_low = f.name.lower()
                        if f.suffix.lower() in MEDIA_EXTS:
                            self.filename_map.setdefault(fname_low, f)
                        try:
                            # Lập chỉ mục mọi hậu tố đường dẫn tương đối (subpath suffixes)
                            parts = f.relative_to(p_root).parts
                            for i in range(len(parts)):
                                sub = "/".join(parts[i:]).lower()
                                self.subpath_map.setdefault(sub, f)
                        except Exception:
                            pass

    def rescan(self):
        self.refresh()


FILE_INDEX = FileIndex()


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
        global CURRENT_VERSION
        parsed = urllib.parse.urlparse(self.path)
        raw_path = urllib.parse.unquote(parsed.path).lstrip("/")

        # API kiểm tra phiên bản realtime
        if raw_path == "api/version":
            body = json.dumps({"version": CURRENT_VERSION}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # API trạng thái Kilo Swarm thời gian thực cho monitor.html
        if raw_path == "api/state":
            swarm = get_swarm_module()
            if swarm and hasattr(swarm, "get_current_swarm_state"):
                state = swarm.get_current_swarm_state(force_refresh=True)
                body = json.dumps(state, ensure_ascii=False).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            else:
                self.send_response(503)
                self.end_headers()
            return

        # API thông tin vai trò agent
        if raw_path == "api/role":
            query = urllib.parse.parse_qs(parsed.query)
            role_id = query.get('id', [''])[0]
            roles_dir = ROOT / 'agents' / 'roles'
            role_file = roles_dir / f"{role_id}.md"
            content = "Không tìm thấy vai trò này."
            if role_file.exists() and role_file.is_file():
                content = role_file.read_text(encoding='utf-8')
            body = json.dumps({'id': role_id, 'content': content}, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # SSE Stream cho monitor.html đẩy sự kiện trực tiếp
        if raw_path == "events":
            swarm = get_swarm_module()
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            try:
                if swarm and hasattr(swarm, "get_current_swarm_state"):
                    initial_state = swarm.get_current_swarm_state()
                    self.wfile.write(f"data: {json.dumps(initial_state, ensure_ascii=False)}\n\n".encode('utf-8'))
                    self.wfile.flush()
                while True:
                    time.sleep(1.5)
                    if swarm and hasattr(swarm, "get_current_swarm_state"):
                        cur_state = swarm.get_current_swarm_state()
                        self.wfile.write(f"data: {json.dumps(cur_state, ensure_ascii=False)}\n\n".encode('utf-8'))
                        self.wfile.flush()
            except Exception:
                pass
            return

        # API quét và làm mới toàn bộ dữ liệu dự án tự động
        if raw_path == "api/refresh":
            try:
                import subprocess
                gen_script = ROOT / "scripts" / "generate-dashboard.py"
                subprocess.run([sys.executable, str(gen_script)], check=True)
                FILE_INDEX.rescan()
                CURRENT_VERSION = int(time.time())
                body = b'{"status":"ok","message":"Du lieu da duoc lam moi thanh cong"}'
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except Exception as e:
                body = f'{{"status":"error","message":"{str(e)}"}}'.encode('utf-8')
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            return

        # 1. Trang chủ
        if not raw_path or parsed.path == "/":
            local_file = VIEWER_DIR / "index.html"
            if local_file.is_file():
                return self._serve_real_file(local_file)

        # 2. Phục vụ tài nguyên tĩnh trực tiếp từ VIEWER_DIR nếu có (html, js, css...)
        viewer_candidate = (VIEWER_DIR / raw_path).resolve()
        try:
            if viewer_candidate.is_file() and VIEWER_DIR in viewer_candidate.parents:
                return self._serve_real_file(viewer_candidate)
        except Exception:
            pass

        # 3. Chuẩn hóa đường dẫn: loại bỏ dấu ../ nếu có ở đầu
        norm_path = raw_path
        while norm_path.startswith("../"):
            norm_path = norm_path[3:]
        norm_path_low = norm_path.lower()

        # 4. Tìm kiếm theo đường dẫn tương đối trong các thư mục dự án
        for p_root in get_project_roots():
            candidate = (p_root / norm_path).resolve()
            if candidate.is_file():
                return self._serve_real_file(candidate)
            # Thử thêm tiền tố doc/ hoặc docs/ hoặc doc/srs/
            for prefix in ("doc", "docs", "doc/srs", "doc/srs/hinh"):
                sub_candidate = (p_root / prefix / norm_path).resolve()
                if sub_candidate.is_file():
                    return self._serve_real_file(sub_candidate)

        # 5. Tra cứu qua FILE_INDEX theo subpath tương đối (ưu tiên cao hơn tra cứu thuần tên file)
        if norm_path_low in FILE_INDEX.subpath_map:
            return self._serve_real_file(FILE_INDEX.subpath_map[norm_path_low])

        # 6. Tra cứu theo tên file (filename) nếu là ảnh hoặc sơ đồ
        filename_low = Path(norm_path).name.lower()
        if filename_low in FILE_INDEX.filename_map:
            return self._serve_real_file(FILE_INDEX.filename_map[filename_low])

        # 7. Quét lại dự án một lần nếu file mới được thêm vào
        FILE_INDEX.refresh()
        if norm_path_low in FILE_INDEX.subpath_map:
            return self._serve_real_file(FILE_INDEX.subpath_map[norm_path_low])
        if filename_low in FILE_INDEX.filename_map:
            return self._serve_real_file(FILE_INDEX.filename_map[filename_low])

        # Không tìm thấy
        self.send_error(404, f"File not found: {raw_path}")

    def _serve_real_file(self, file_path: Path):
        try:
            ctype, _ = mimetypes.guess_type(str(file_path))
            if not ctype:
                if file_path.suffix.lower() == ".drawio":
                    ctype = "application/xml"
                elif file_path.suffix.lower() == ".md":
                    ctype = "text/plain; charset=utf-8"
                elif file_path.suffix.lower() == ".svg":
                    ctype = "image/svg+xml"
                else:
                    ctype = "application/octet-stream"

            # Tự động gắn Nút Quay lại Dashboard & Hiệu ứng chuỗi gói tin di chuyển chậm
            if file_path.suffix.lower() == ".html" and file_path != (VIEWER_DIR / "index.html") and file_path != (VIEWER_DIR / "monitor.html"):
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                injected = """
<script>
  if (window.self !== window.top) {
    document.documentElement.classList.add('archify-in-iframe');
  }
</script>
<style id="archify-clean-view">
  html, body {
    margin: 0 !important;
    padding-top: 0.5rem !important;
    padding-bottom: 0.5rem !important;
    box-sizing: border-box !important;
  }
  /* Khi nhúng trong iframe (Drawer / Tab SRS / Viewer modal): ẨN nút quay lại, bỏ margin né nút */
  html.archify-in-iframe #archify-back-to-dashboard {
    display: none !important;
  }
  html.archify-in-iframe .header {
    margin-left: 0 !important;
    padding-right: 15rem !important;
    margin-bottom: 0.4rem !important;
  }
  html.archify-in-iframe .header-row {
    min-width: 0 !important;
  }
  html.archify-in-iframe .header-row h1 {
    font-size: 1.1rem !important;
    line-height: 1.35 !important;
    white-space: normal !important;
    word-break: normal !important;
    overflow-wrap: break-word !important;
  }

  /* Khi mở trực tiếp toàn màn hình ngoài tab mới */
  html:not(.archify-in-iframe) #archify-back-to-dashboard {
    position: fixed;
    top: 12px;
    left: 16px;
    z-index: 99999;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 7px 16px;
    background: rgba(15, 23, 42, 0.92);
    color: #38bdf8;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 13px;
    font-weight: 700;
    text-decoration: none;
    border: 1px solid rgba(56, 189, 248, 0.5);
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.45);
    backdrop-filter: blur(10px);
    transition: all 0.2s ease;
  }
  html:not(.archify-in-iframe) #archify-back-to-dashboard:hover {
    background: #0284c7;
    color: #ffffff;
    border-color: #38bdf8;
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(56, 189, 248, 0.4);
  }
  @media (min-width: 1024px) {
    html:not(.archify-in-iframe) .header {
      margin-left: 190px !important;
      margin-bottom: 0.4rem !important;
    }
  }
  @media (max-width: 1023px) {
    html:not(.archify-in-iframe) .header {
      margin-top: 48px !important;
      margin-left: 0 !important;
      padding-right: 0 !important;
    }
  }

  /* Cố định tiêu đề h1 không bao giờ bị bóp nát thành cột dọc */
  .header-row h1 {
    white-space: normal !important;
    word-break: normal !important;
    overflow-wrap: break-word !important;
    min-width: 0 !important;
  }

  /* Khi cột ở bên phải hoặc thu gọn: giữ fit màn hình không trượt trang */
  html:is([data-reader-rail="true"], [data-reader-rail="collapsed"], [data-reader-rail="overlay"]) {
    height: 100vh !important;
    max-height: 100vh !important;
    overflow: hidden !important;
  }
  html:is([data-reader-rail="true"], [data-reader-rail="collapsed"], [data-reader-rail="overlay"]) body {
    height: 100vh !important;
    max-height: 100vh !important;
    overflow: hidden !important;
  }
  /* Khi cột ở bên dưới: cho phép cuộn tự do */
  html[data-reader-rail="bottom"] {
    height: auto !important;
    max-height: none !important;
    overflow-y: auto !important;
  }
  html[data-reader-rail="bottom"] body {
    height: auto !important;
    max-height: none !important;
    overflow-y: auto !important;
  }
  .diagram-container {
    height: calc(100vh - 4.5rem) !important;
    max-height: calc(100vh - 4.5rem) !important;
  }
  html[data-reader-rail="true"] .reader-rail {
    max-height: calc(100vh - 4.5rem) !important;
    overflow-y: auto !important;
  }

  /* Hiệu ứng chuỗi hạt gói tin di chuyển chậm rãi, mượt mà */
  @keyframes slowPacketStream {
    from { stroke-dashoffset: 240; }
    to { stroke-dashoffset: 0; }
  }
  .archify-packet-bead {
    pointer-events: none !important;
    fill: none !important;
    stroke: #38bdf8 !important;
    stroke-width: 4.5px !important;
    stroke-linecap: round !important;
    stroke-dasharray: 6px 44px !important;
    filter: drop-shadow(0 0 3px #38bdf8) drop-shadow(0 0 7px #0284c7) !important;
    animation: slowPacketStream 9s linear infinite !important;
    opacity: 0.92 !important;
  }
</style>
<a href="/index.html" id="archify-back-to-dashboard" onclick="if(window.history.length > 1 && document.referrer && document.referrer.includes(window.location.host)){window.history.back();return false;}else{const t=sessionStorage.getItem('dash_active_tab')||'diagrams';window.location.href='/index.html#'+t;return false;}" title="Quay lại Bảng điều khiển chính">
  <span style="font-size: 16px; font-weight: bold;">←</span> Quay lại Dashboard
</a>
<script>
  // Tắt presentation stage để giữ cột thông tin linh hoạt
  if (document.documentElement.getAttribute('data-present') === 'true') {
    document.documentElement.removeAttribute('data-present');
  }

  // Tự động gắn các viên gói tin di chuyển chậm dọc theo mọi đường nối
  function setupSlowPacketMotion() {
    const paths = document.querySelectorAll('svg path[data-animate="edge"]');
    if (!paths || paths.length === 0) return;
    paths.forEach(path => {
      if (path.dataset.packetAdded) return;
      const d = path.getAttribute('d');
      if (!d) return;
      const overlay = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      overlay.setAttribute('d', d);
      overlay.setAttribute('class', 'archify-packet-bead');
      if (path.hasAttribute('transform')) {
        overlay.setAttribute('transform', path.getAttribute('transform'));
      }
      path.parentNode.insertBefore(overlay, path.nextSibling);
      path.dataset.packetAdded = '1';
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupSlowPacketMotion);
  } else {
    setupSlowPacketMotion();
  }
  setTimeout(setupSlowPacketMotion, 500);
  setTimeout(setupSlowPacketMotion, 1500);
</script>
"""
                if "</head>" in content:
                    content = content.replace("</head>", injected + "</head>")
                elif "<body" in content:
                    content = content.replace("<body", injected + "<body")
                data = content.encode("utf-8")
            else:
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

    # Kích hoạt bộ theo dõi tài liệu Realtime
    REALTIME_WATCHER.start()
    print("📡 [Realtime Watcher] Đã kích hoạt theo dõi tự động: Mọi thay đổi tài liệu sẽ được live-update tức thì!")

    server_address = ("", args.port)
    httpd = ThreadingHTTPServer(server_address, DashboardHandler)
    print(f"🚀 Dashboard Server đang chạy tại: http://localhost:{args.port}/index.html")
    print(f"📁 Phục vụ giao diện: {VIEWER_DIR}")
    print(f"🔗 Tự động liên kết ảnh/sơ đồ ({len(FILE_INDEX.filename_map)} file media) từ: {[str(r) for r in get_project_roots()]}")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
