#!/usr/bin/env python3
"""scripts/srs-check.py

Kiểm một bản đặc tả (SRS) dạng md theo quy trình ở agents/protocols/srs-workflow.md.

  python scripts/srs-check.py <file.md> [<file.md> ...]
  python scripts/srs-check.py --all            kiểm mọi UC-*.md trong "Thư mục SRS" của PROJECT.md (mặc định docs/spec)
  python scripts/srs-check.py <file.md> --strict   cảnh báo cũng làm thất bại
  python scripts/srs-check.py <file.md> --json
  python scripts/srs-check.py <file.md> --full     hồ sơ hoàn chỉnh (trước khi bàn giao): bắt thêm Nhật ký thay đổi, Hạng mục
                                                   thiết kế, WBS, RTM, rủi ro, câu hỏi chờ xác nhận, use-case đủ 4 phần

LỖI (mã thoát 1): thiếu mục bắt buộc; ảnh sơ đồ không tồn tại; một AC-xx không có ca kiểm thử nào nhắc tới;
file .drawio được dẫn tới vi phạm quy tắc (scripts/diagram-describe.py).
CẢNH BÁO: từ cảm tính ("nhanh", "mượt"...); ảnh chưa có mô tả bước; nhắc cơ sở dữ liệu mà không có ERD hoặc "không thêm bảng";
nhắc chuyển trạng thái mà không có sơ đồ trạng thái; câu hỏi mở không nằm cuối.

Chỉ dùng thư viện chuẩn. Không sửa file.
"""

import argparse
import importlib.util
import json
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agent_core.knowledge.search import normalize  # noqa: E402

REQUIRED_SECTIONS = {
    "tác nhân": r"\b(tac nhan|actor)\b",
    "use case hoặc user story": r"(use case|user story|ca su dung)",
    "sơ đồ": r"\b(so do|diagram)\b",
    "yêu cầu phi chức năng": r"(phi chuc nang|\bnfr\b|non functional)",
    "kiểm thử": r"(kiem thu|\btest\b)",
    "câu hỏi mở": r"cau hoi",
}
# Chế độ --full: hồ sơ hoàn chỉnh của một chức năng (khung template 16 mục + use-case chi tiết).
# Mục tiêu: không để hồ sơ lên bàn giao khi thiếu Nhật ký, Hạng mục thiết kế, use-case đủ 4 phần, câu hỏi chờ xác nhận.
FULL_SECTIONS = {
    "nhật ký thay đổi": r"nhat ky (thay doi|sua doi)",
    "hạng mục thiết kế": r"(hang muc thiet ke|dau muc thiet ke|design checklist)",
    "kế hoạch phân rã (WBS)": r"(\bwbs\b|phan ra cong viec|ke hoach)",
    "truy vết yêu cầu (RTM)": r"(\brtm\b|truy vet)",
    "rủi ro": r"(rui ro|\brisk\b)",
    "câu hỏi chờ xác nhận": r"cau hoi.*cho xac nhan",
}
FULL_USECASE_PARTS = {
    "tiền điều kiện": r"tien dieu kien|precondition",
    "luồng chính": r"luong chinh|main flow|happy path",
    "luồng thay thế": r"luong thay the|alternative",
    "luồng ngoại lệ hoặc lỗi": r"ngoai le|luong loi|exception|nhanh loi",
}
VAGUE = ["nhanh", "mượt", "trực quan", "dễ dùng", "dễ sử dụng", "thân thiện", "bảo mật cao", "hợp lý", "đẹp", "v.v",
         "vân vân", "tbd", "tương tự như trên"]
STEP_LINE = re.compile(r"^\s*(?:\|\s*)?(?:[-*]\s*)?(?:\*\*)?(?:Bước\s*)?\d+(?:\.\d+)*[.)|\s*:]", re.I)
IMG = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")
DRAWIO = re.compile(r"\[[^\]]*\]\(([^)\s]+\.drawio)\)")
AC_ID = re.compile(r"\bAC-\d+\b")


FLOW_IMAGE = re.compile(r"(hoat-dong|activity|sequence|trang-thai|vong-doi|state|flow|luong)", re.I)


def resolve(base: Path, target: str, warnings, line):
    """Đường dẫn trong liên kết md -> Path. Liên kết file:// theo máy vẫn mở được nhưng bị cảnh báo vì hỏng trên máy khác."""
    if target.startswith("file://"):
        warnings.append((line, f"liên kết tuyệt đối theo máy ({target[:40]}...): dùng đường dẫn tương đối"))
        return Path(target[len("file://"):])
    return base.parent / target


def srs_dir():
    pj = ROOT / "PROJECT.md"
    if pj.is_file():
        for line in pj.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\|\s*Thư mục SRS\s*\|\s*`?([^|`]+?)`?\s*\|", line)
            if m and "(điền" not in m.group(1):
                return ROOT / m.group(1).strip()
    return ROOT / "docs" / "spec"


def load_diagram_tool():
    spec = importlib.util.spec_from_file_location("diagram_describe", ROOT / "scripts" / "diagram-describe.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def clean_lines(text):
    """Trả về [(số dòng, nội dung, trong_khối_mã)] sau khi bỏ chú thích HTML."""
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    out, fence = [], False
    for n, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            fence = not fence
            out.append((n, line, True))
            continue
        out.append((n, line, fence))
    return out


def check_file(path: Path, full: bool = False):
    errors, warnings = [], []
    text = path.read_text(encoding="utf-8")
    lines = clean_lines(text)
    body = "\n".join(l for _, l, f in lines if not f)
    norm = normalize(body)

    headings = [(n, re.sub(r"^#+\s*", "", l).strip(), len(l) - len(l.lstrip("#"))) for n, l, f in lines
                if not f and re.match(r"^#{2,4}\s", l)]
    norm_heads = [normalize(h) for _, h, _ in headings]

    # --- mục bắt buộc
    for name, pat in REQUIRED_SECTIONS.items():
        if not any(re.search(pat, h) for h in norm_heads):
            errors.append((0, f"thiếu mục bắt buộc: {name}"))
    if not re.search(r"a/c|tiêu chí chấp nhận|tiêu chí nghiệm thu", body.lower()):
        errors.append((0, "thiếu tiêu chí nghiệm thu (A/C)"))
    if full:
        for name, pat in FULL_SECTIONS.items():
            if not any(re.search(pat, h) for h in norm_heads):
                errors.append((0, f"[--full] thiếu mục bắt buộc của hồ sơ hoàn chỉnh: {name}"))
        for name, pat in FULL_USECASE_PARTS.items():
            if not re.search(pat, norm):
                errors.append((0, f"[--full] use-case chi tiết thiếu phần: {name}"))

    # --- A/C và ca kiểm thử
    test_start = next((n for (n, h, _), nh in zip(headings, norm_heads) if re.search(r"(kiem thu|\btest\b)", nh)), None)
    defs, refs = {}, set()
    for n, l, f in lines:
        if f:
            continue
        cells = [c.strip() for c in l.strip().strip("|").split("|")] if l.strip().startswith("|") else []
        if cells and re.fullmatch(r"AC-\d+", cells[0]) and (test_start is None or n < test_start):
            defs.setdefault(cells[0], n)
        elif test_start is not None and n >= test_start:
            refs.update(AC_ID.findall(l))
    for ac, n in sorted(defs.items()):
        if ac not in refs:
            errors.append((n, f"{ac} chưa có ca kiểm thử nào nhắc tới (mỗi A/C cần ít nhất một ca)"))

    # --- sơ đồ: ảnh, mô tả, nguồn .drawio
    diagrams = 0
    for idx, (n, l, f) in enumerate(lines):
        if f:
            continue
        for m in IMG.finditer(l):
            diagrams += 1
            target = urllib.parse.unquote(m.group(1))
            if target.startswith(("http://", "https://")):
                continue
            local = resolve(path, target, warnings, n)
            if not local.is_file():
                errors.append((n, f"ảnh sơ đồ không tồn tại: {target}"))
            window = []
            for _, nl, nf in lines[idx + 1: idx + 61]:
                if re.match(r"^#{1,3}\s", nl) or IMG.search(nl):
                    break
                window.append(nl)
            steps = sum(1 for w in window if STEP_LINE.match(w))
            filled = sum(1 for w in window if w.strip())
            if FLOW_IMAGE.search(target):
                if steps < 2:
                    warnings.append((n, f"ảnh {target} chưa có mô tả hoạt động (cần ít nhất 2 bước đánh số ngay dưới ảnh)"))
            elif filled < 4:
                warnings.append((n, f"ảnh {target} chưa có phần mô tả đi kèm (bảng hoặc đoạn giải thích)"))
        for m in DRAWIO.finditer(l):
            diagrams += 1
            src = resolve(path, urllib.parse.unquote(m.group(1)), warnings, n)
            if not src.is_file():
                errors.append((n, f"file nguồn sơ đồ không tồn tại: {m.group(1)}"))
                continue
            errors.extend(check_drawio(src, n))
    diagrams += len(re.findall(r"^```mermaid", body, flags=re.M))
    if diagrams == 0:
        errors.append((0, "chưa có sơ đồ nào (ảnh, khối mermaid hoặc nguồn .drawio)"))

    # --- gợi ý sơ đồ tối thiểu
    if re.search(r"(co so du lieu|database|\bdb\b|entity)", norm) and not re.search(r"(\berd\b|khong them bang|quan he thuc the)", norm):
        warnings.append((0, "nhắc cơ sở dữ liệu nhưng chưa có ERD hoặc dòng \"không thêm bảng\""))
    if re.search(r"(chuyen trang thai|doi trang thai)", norm) and not re.search(r"(state|vong doi|so do trang thai)", norm):
        warnings.append((0, "có chuyển trạng thái nhưng chưa có sơ đồ trạng thái (vòng đời)"))

    # --- từ cảm tính (bỏ qua mục câu hỏi mở và dòng đã có số liệu)
    question_from = next((n for (n, h, _), nh in zip(headings, norm_heads) if "cau hoi" in nh), 10 ** 9)
    pat = re.compile(r"(?<!\w)(" + "|".join(re.escape(w) for w in VAGUE) + r")(?!\w)", re.I)
    for n, l, f in lines:
        if f or n >= question_from or re.search(r"\d", l):
            continue
        m = pat.search(l)
        if m:
            warnings.append((n, f"từ cảm tính \"{m.group(1)}\": hãy lượng hóa"))

    # --- câu hỏi mở nằm cuối
    h2 = [(n, normalize(h)) for n, h, lvl in headings if lvl == 2]
    for i, (n, h) in enumerate(h2):
        if "cau hoi" in h and any(not re.search(r"(phu luc|tham khao|nhat ky)", later) for _, later in h2[i + 1:]):
            warnings.append((n, "mục câu hỏi mở nên là mục cuối của tài liệu"))
    return errors, warnings


def check_drawio(src: Path, ref_line: int):
    """Chạy quy tắc của diagram-describe.py cho từng trang của file .drawio được dẫn tới."""
    tool = load_diagram_tool()
    problems = []
    try:
        tree = ET.parse(src)
    except ET.ParseError:
        return [(ref_line, f"{src.name}: không đọc được XML (file có thể bị nén)")]
    diagrams = tree.getroot().findall("diagram")
    ids = [d.get("id") for d in diagrams]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        problems.append((ref_line, f"{src.name}: id trang trùng {dup}"))
    for d in diagrams:
        page = tool.parse_page(d)
        if page is None:
            problems.append((ref_line, f"{src.name}: trang {d.get('name')} bị nén hoặc rỗng"))
            continue
        for p in tool.check_page(page):
            problems.append((ref_line, f"{src.name} [{page['name']}]: {p}"))
    return problems


def main():
    ap = argparse.ArgumentParser(description="Kiểm một đặc tả SRS dạng md.")
    ap.add_argument("files", nargs="*")
    ap.add_argument("--all", action="store_true", help="Kiểm mọi UC-*.md trong Thư mục SRS của PROJECT.md")
    ap.add_argument("--strict", action="store_true", help="Cảnh báo cũng làm thất bại")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--full", action="store_true",
                    help="Hồ sơ hoàn chỉnh: bắt thêm Nhật ký, Hạng mục thiết kế, WBS, RTM, rủi ro, câu hỏi chờ xác nhận, "
                         "use-case đủ tiền điều kiện/luồng chính/luồng thay thế/lỗi")
    args = ap.parse_args()

    targets = [Path(f) for f in args.files]
    if args.all:
        base = srs_dir()
        targets += sorted(p for p in base.rglob("UC-*.md")
                          if not re.search(r"(thiet-ke|doi-chieu)", p.name))
    if not targets:
        print("Không có file nào để kiểm (truyền đường dẫn hoặc dùng --all).", file=sys.stderr)
        sys.exit(2)

    failed, report = False, []
    for t in targets:
        if not t.is_file():
            print(f"LỖI  không thấy file {t}", file=sys.stderr)
            sys.exit(2)
        errors, warnings = check_file(t, full=args.full)
        failed = failed or bool(errors) or (args.strict and bool(warnings))
        report.append({"file": str(t), "errors": errors, "warnings": warnings})

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for r in report:
            for n, m in r["errors"]:
                print(f"LỖI       {r['file']}{':' + str(n) if n else ''}  {m}")
            for n, m in r["warnings"]:
                print(f"CẢNH BÁO  {r['file']}{':' + str(n) if n else ''}  {m}")
            if not r["errors"] and not r["warnings"]:
                print(f"ĐẠT       {r['file']}")
        total_e = sum(len(r["errors"]) for r in report)
        total_w = sum(len(r["warnings"]) for r in report)
        print(f"{len(report)} file: {total_e} lỗi, {total_w} cảnh báo")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
