#!/usr/bin/env python3
"""
scripts/doc-preflight.py
Kiểm tra nhanh tài liệu trước khi thiết kế hoặc viết code (Pre-Code Doc Preflight).
Chống các bẫy thường gặp khi dự án có bản tài liệu mới thay thế bản cũ:
  - Nhiều file đặc tả / sơ đồ song song chưa dời vào archive/ hoặc chưa đánh dấu SUPERSEDED
  - File nguồn gốc (.docx/.xlsx/.pdf) mới hơn bản Markdown (.md)
  - File nằm trong index XERJ có khả năng cũ hơn file mới sửa trên đĩa
  - Task card cũ đã bị hủy (cancelled) hoặc thay thế (superseded)

Chỉ đọc, hoàn toàn an toàn, không sửa bất kỳ file nào.

Usage:
  python3 scripts/doc-preflight.py --root /path/to/workspace --uc UC-06
  python3 scripts/doc-preflight.py --root /path/to/workspace --list
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BINARY_SOURCE_EXTS = {".docx", ".xlsx", ".pdf"}
SUPERSEDED_RE = re.compile(
    r"(?:status\s*[:=]\s*superseded|superseded\s+by\b|không\s+dùng\s+để\s+code|đã\s+thay\s+thế\s+bởi)",
    re.IGNORECASE,
)
ACTIVE_SOURCE_RE = re.compile(
    r"^\s*(?:[-*>]\s*)?(?:\*\*)?(?:active\s+source|nguồn\s+chân\s+lý(?:\s+duy\s+nhất)?|tài\s+liệu\s+chính(?:\s+hiện\s+hành)?)(?:\*\*)?\s*[:\-]\s*(.+)$",
    re.IGNORECASE,
)
TASK_STATUS_RE = re.compile(
    r"(?:trạng\s+thái|status)\s*(?:\*\*|\|)*\s*[:|]\s*(.+)",
    re.IGNORECASE,
)
SUPPORTING_MD_SUFFIXES = (
    "-doi-chieu.md",
    "-happy-cases.md",
    "-hien-trang-db-va-code.md",
    "-test-plan.md",
    "-test-report.md",
    "-rtm.md",
    "-rtm-ma-tran-truy-vet.md",
    "-kich-ban-demo.md",
    "-api-design.md",
    "-cau-hoi-ke-toan.md",
    "-bien-ban-tham-dinh-gate-2.md",
)
SINGLE_TYPE_DRAWIO_RE = re.compile(
    r"(?:-(?:usecase|use-case|erd|class|sequence|activity|flow|swimlane)\.drawio$)|(?:^(?:mockup|mau)-.*\.drawio$)",
    re.IGNORECASE,
)


def _find_direct_doc(base: Path, require_features: bool = False) -> Path | None:
    for candidate in ("doc", "docs"):
        p = base / candidate
        if p.is_dir() and (not require_features or (p / "features").is_dir()):
            return p
    return None


def _within_user_scope(path: Path) -> bool:
    home = Path.home().resolve()
    res = path.resolve()
    return res != home and res != Path(res.anchor)


def resolve_doc_and_workspace_root(target_root: Path) -> tuple[Path, Path | None]:
    """Tìm cặp (workspace_root, doc_root) từ thư mục gốc workspace hoặc từ bên trong bất kỳ Git worktree / service con nào."""
    root = target_root.resolve()

    # 1. Trực tiếp tại root có doc/features hoặc docs/features (ưu tiên thư mục tài liệu chuẩn workspace)
    direct_features = _find_direct_doc(root, require_features=True)
    if direct_features:
        return root, direct_features

    # 2. Symlink doc.workspace gắn trong worktree (trỏ thẳng về <WORKSPACE_ROOT>/doc)
    doc_ws = root / "doc.workspace"
    if doc_ws.is_dir():
        resolved_doc = doc_ws.resolve()
        return resolved_doc.parent, resolved_doc

    # 3. Symlink file quy tắc workspace trong worktree (AGENTS.workspace.md / CLAUDE.workspace.md / PROJECT.workspace.md)
    for link_name in ("AGENTS.workspace.md", "CLAUDE.workspace.md", "PROJECT.workspace.md", "AGENTS.md"):
        link_path = root / link_name
        if link_path.is_symlink():
            try:
                ws_candidate = link_path.resolve().parent
                doc_p = _find_direct_doc(ws_candidate, require_features=True) or _find_direct_doc(ws_candidate, require_features=False)
                if doc_p:
                    return ws_candidate, doc_p
            except OSError:
                pass

    # 4. Đi ngược lên thư mục cha nếu đang chạy từ repo service bên trong workspace (max 4 cấp, dừng trước HOME)
    for anc in root.parents[:4]:
        if not _within_user_scope(anc):
            break
        doc_p = _find_direct_doc(anc, require_features=True)
        if doc_p:
            return anc, doc_p

    # 5. Nếu đang đứng trong Git worktree chưa sync symlink -> hỏi `git rev-parse --git-common-dir` để tìm về workspace gốc
    try:
        res = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--git-common-dir"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=3,
        )
        if res.returncode == 0 and res.stdout.strip():
            common_raw = Path(res.stdout.strip())
            common_dir = (common_raw if common_raw.is_absolute() else (root / common_raw)).resolve()
            for anc in common_dir.parents[:5]:
                if not _within_user_scope(anc):
                    break
                doc_p = _find_direct_doc(anc, require_features=True)
                if doc_p:
                    return anc, doc_p
    except Exception:
        pass

    # 6. Fallback cho workspace mới chỉ có doc/ hoặc docs/ chưa có subfolder features/
    fallback = _find_direct_doc(root, require_features=False)
    if fallback:
        return root, fallback

    return root, None


def detect_doc_root(ws_root: Path) -> Path | None:
    _, doc_root = resolve_doc_and_workspace_root(ws_root)
    return doc_root


def _norm_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def resolve_feature_dirs(doc_root: Path, uc_query: str) -> list[Path]:
    features_dir = doc_root / "features"
    if not features_dir.is_dir():
        return []
    q_norm = _norm_key(uc_query)
    exact: list[Path] = []
    partial: list[Path] = []
    for entry in sorted(features_dir.iterdir()):
        if not entry.is_dir():
            continue
        e_norm = _norm_key(entry.name)
        if e_norm == q_norm or entry.name.lower() == uc_query.lower():
            exact.append(entry)
        elif q_norm and q_norm in e_norm:
            partial.append(entry)
    return exact or partial


def _fmt_ts(mtime: float) -> str:
    return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")


def _read_head_lines(path: Path, max_lines: int = 25) -> list[str]:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            lines = []
            for _ in range(max_lines):
                line = f.readline()
                if not line:
                    break
                lines.append(line.rstrip("\r\n"))
            return lines
    except OSError:
        return []


def _extract_active_source(readme_path: Path) -> str:
    if not readme_path.is_file():
        return ""
    for line in _read_head_lines(readme_path, 40):
        m = ACTIVE_SOURCE_RE.match(line)
        if m:
            return m.group(1).strip()
    return ""


def _is_superseded_md(path: Path) -> bool:
    head = "\n".join(_read_head_lines(path, 15))
    return bool(SUPERSEDED_RE.search(head))


def _is_primary_spec_md(path: Path) -> bool:
    low = path.name.lower()
    if low == "readme.md":
        return False
    return not any(low.endswith(sfx) for sfx in SUPPORTING_MD_SUFFIXES)


def _scan_tasks(tasks_dir: Path) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    active_cards: list[tuple[str, str]] = []
    inactive_cards: list[tuple[str, str]] = []
    if not tasks_dir.is_dir():
        return active_cards, inactive_cards
    for f in sorted(tasks_dir.glob("*.md")):
        status_val = "unknown"
        for line in _read_head_lines(f, 20):
            m = TASK_STATUS_RE.search(line)
            if m:
                status_val = re.sub(r"[`*]", "", m.group(1)).strip().strip("|").strip()
                break
        low_status = status_val.lower()
        if any(k in low_status for k in ("cancelled", "canceled", "superseded")):
            inactive_cards.append((f.name, status_val))
        else:
            active_cards.append((f.name, status_val))
    return active_cards, inactive_cards


def analyze_feature(feature_dir: Path) -> dict:
    """Phân tích một thư mục UC/feature để tìm bản active, bản cũ và cảnh báo mâu thuẫn."""
    readme_path = feature_dir / "README.md"
    active_source_decl = _extract_active_source(readme_path)

    root_files = [
        p for p in feature_dir.iterdir()
        if p.is_file() and not p.name.startswith(".") and p.name != ".gitkeep"
    ]
    root_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

    active_primary_mds: list[Path] = []
    superseded_mds: list[Path] = []
    binary_sources: list[Path] = []

    for p in root_files:
        suf = p.suffix.lower()
        if suf == ".md":
            if _is_superseded_md(p):
                superseded_mds.append(p)
            elif _is_primary_spec_md(p):
                active_primary_mds.append(p)
        elif suf in BINARY_SOURCE_EXTS:
            binary_sources.append(p)

    drawio_files: list[Path] = []
    for search_dir in (feature_dir, feature_dir / "hinh"):
        if search_dir.is_dir():
            for d in search_dir.glob("*.drawio"):
                if d.is_file():
                    drawio_files.append(d)
    drawio_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

    archive_dir = feature_dir / "archive"
    archive_count = sum(1 for _ in archive_dir.rglob("*") if _.is_file()) if archive_dir.is_dir() else 0

    active_cards, inactive_cards = _scan_tasks(feature_dir / "tasks")

    traps: list[str] = []
    newest_md_mtime = max((p.stat().st_mtime for p in active_primary_mds), default=0.0)
    for b in binary_sources:
        if newest_md_mtime == 0.0:
            traps.append(
                f"[BINARY-ONLY] Có {b.name} ({_fmt_ts(b.stat().st_mtime)}) nhưng chưa có file .md đặc tả chính -> cần convert/đối chiếu trước khi code."
            )
        elif b.stat().st_mtime - newest_md_mtime > 2.0:
            newest_md_name = active_primary_mds[0].name
            traps.append(
                f"[BINARY-NEWER-THAN-MD] {b.name} ({_fmt_ts(b.stat().st_mtime)}) mới hơn {newest_md_name} ({_fmt_ts(newest_md_mtime)}) -> KHÔNG code theo .md cũ trước khi đối chiếu/cập nhật từ bản mới."
            )

    if len(active_primary_mds) > 1 and not active_source_decl:
        names = ", ".join(f"{p.name} ({_fmt_ts(p.stat().st_mtime)})" for p in active_primary_mds)
        traps.append(
            f"[MULTIPLE-ACTIVE-DOCS] Có {len(active_primary_mds)} file đặc tả chính chưa đưa vào archive/ hoặc gắn SUPERSEDED: {names}."
        )

    bundle_drawios = [d for d in drawio_files if not SINGLE_TYPE_DRAWIO_RE.search(d.name)]
    if len(bundle_drawios) > 1 and not active_source_decl:
        d_names = ", ".join(f"{p.name} ({_fmt_ts(p.stat().st_mtime)})" for p in bundle_drawios)
        traps.append(
            f"[MULTIPLE-DRAWIO] Có {len(bundle_drawios)} file .drawio chính ngoài archive/: {d_names} -> kiểm tra bản mới nhất."
        )

    return {
        "feature_dir": feature_dir,
        "has_readme": readme_path.is_file(),
        "active_source_decl": active_source_decl,
        "active_primary_mds": active_primary_mds,
        "superseded_mds": superseded_mds,
        "binary_sources": binary_sources,
        "drawio_files": drawio_files,
        "archive_count": archive_count,
        "active_cards": active_cards,
        "inactive_cards": inactive_cards,
        "traps": traps,
    }


def format_report(info: dict, ws_root: Path) -> str:
    fdir: Path = info["feature_dir"]
    try:
        rel_dir = fdir.relative_to(ws_root)
    except ValueError:
        rel_dir = fdir

    lines = [f"=== DOC PREFLIGHT: {rel_dir} ==="]
    if info["active_source_decl"]:
        lines.append(f"Active Source (theo README.md): {info['active_source_decl']}")
    elif info["has_readme"]:
        lines.append("README.md: có sẵn (chưa khai báo dòng `Active Source:` tường minh)")
    else:
        lines.append("README.md: chưa có")

    lines.append("Đặc tả Markdown đang hiệu lực (mới -> cũ):")
    if info["active_primary_mds"]:
        for idx, p in enumerate(info["active_primary_mds"]):
            tag = " [MỚI NHẤT]" if idx == 0 else ""
            lines.append(f"  - {p.name} ({_fmt_ts(p.stat().st_mtime)}){tag}")
    else:
        lines.append("  - (không có file đặc tả .md nào ở gốc UC)")

    if info["superseded_mds"]:
        lines.append("File đã đánh dấu SUPERSEDED (BỎ QUA khi code):")
        for p in info["superseded_mds"]:
            lines.append(f"  - {p.name} ({_fmt_ts(p.stat().st_mtime)}) [SUPERSEDED]")

    if info["binary_sources"]:
        lines.append("File nguồn .docx/.xlsx/.pdf (mới -> cũ):")
        for p in info["binary_sources"][:5]:
            lines.append(f"  - {p.name} ({_fmt_ts(p.stat().st_mtime)})")

    if info["active_cards"] or info["inactive_cards"]:
        lines.append("Task cards:")
        for name, st in info["active_cards"]:
            lines.append(f"  - {name}: {st}")
        for name, st in info["inactive_cards"]:
            lines.append(f"  - {name}: {st} [ĐÃ HỦY/THAY THẾ - BỎ QUA]")

    lines.append(f"Archive (`archive/`): {info['archive_count']} file cũ (đã lưu trữ)")
    if info["traps"]:
        lines.append("⚠️ CẢNH BÁO TRƯỚC KHI CODE:")
        for t in info["traps"]:
            lines.append(f"  {t}")
    else:
        lines.append("✅ TRẠNG THÁI: 0 cảnh báo xung đột phiên bản.")

    lines.append("Lưu ý XERJ: nếu tài liệu vừa tạo/sửa hoặc XERJ báo `index_stale`, đọc trực tiếp trên đĩa bằng `safe-search.py` + `read_file`.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Pre-Code Doc Preflight Checker")
    parser.add_argument("--root", default=".", help="Thư mục gốc workspace chứa doc/ hoặc docs/")
    parser.add_argument("--uc", default="", help="Mã UC hoặc tên thư mục feature cần kiểm tra (vd: UC-06, TMP-dong-bo-user)")
    parser.add_argument("--list", action="store_true", help="Liệt kê toàn bộ thư mục feature trong doc/features/")
    args = parser.parse_args()

    input_root = Path(os.path.expanduser(args.root)).resolve()
    ws_root, doc_root = resolve_doc_and_workspace_root(input_root)
    if not doc_root:
        print(f"[INFO] Không tìm thấy thư mục doc/ hoặc docs/ tại {input_root}")
        return 0
    if ws_root != input_root:
        print(f"[WORKSPACE] Nối về tài liệu dự án gốc: {ws_root} -> {doc_root}")

    features_dir = doc_root / "features"
    if args.list or not args.uc:
        if not features_dir.is_dir():
            print(f"[INFO] Chưa có {features_dir}")
            return 0
        print(f"Danh sách features tại {features_dir}:")
        for d in sorted(features_dir.iterdir()):
            if d.is_dir():
                info = analyze_feature(d)
                warn = f" ({len(info['traps'])} cảnh báo)" if info["traps"] else " (OK)"
                print(f"  - {d.name}{warn}")
        return 0

    matched = resolve_feature_dirs(doc_root, args.uc)
    if not matched:
        print(f"[WARN] Không tìm thấy thư mục feature khớp '{args.uc}' trong {features_dir}")
        return 1

    for idx, fdir in enumerate(matched):
        if idx > 0:
            print()
        print(format_report(analyze_feature(fdir), ws_root))
    return 0


if __name__ == "__main__":
    sys.exit(main())
