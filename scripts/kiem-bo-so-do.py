#!/usr/bin/env python3
"""Kiểm BỘ sơ đồ của một UC: bước 2 của vòng "agent vẽ -> kiểm -> sửa". Chạy SAU khi agent (Gemini, Claude...) vẽ xong.

  python3 ~/Documents/agent-base/scripts/kiem-bo-so-do.py <thư mục hinh> [--xerj] [--doc <md của UC>] [--ghi <file.md>]

`ve-so-do.py --check-only` chỉ kiểm HÌNH THỨC từng sơ đồ. Script này kiểm thêm những thứ agent hay sai mà công cụ không bắt:
  - bộ đủ chưa (bundle bốn tab ERD, Class, Sequence, Activity; có use case riêng), ảnh có cũ hơn spec không, file .drawio có bị sửa tay không;
  - activity: làn đặt tên kiểu "Nhánh lỗi", "Kết thúc"; làn gộp Người dùng với Giao diện; điểm kết thúc không ghi kết quả;
  - use case: tác nhân là thành phần nội bộ, tác nhân nằm trong tên hệ thống, gộp hai vai ("CSKH hoặc kho");
  - nhất quán chéo: tên lớp ở sequence và activity phải có trong sơ đồ lớp;
  - con số trên hình (phải có nguồn); với --xerj: tên lớp chưa thấy trong chỉ mục XERJ (có thể nằm ở worktree, người kiểm tra tay).
Mức: LỖI (phải sửa), CẢNH BÁO (sửa hoặc giải thích), XEM TAY (người hoặc agent kiểm chứng với nguồn thật). Mã thoát 1 nếu có LỖI.
Chỉ dùng thư viện chuẩn.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

VE = Path(__file__).with_name("ve-so-do.py")
FORBID_LANE = re.compile(r"nhánh lỗi|kết thúc|^chung$|^lỗi$|error|failure", re.I)
INTERNAL = re.compile(r"frontend|backend|giao diện|gateway|\bapi\b|ws-|-service|database|postgres|controller|\bdao\b", re.I)
MERGED_ROLE = re.compile(r"\bhoặc\b|/|&|\bvà\b", re.I)
INFRA = {"PostgreSQL", "RabbitMQ", "MySQL", "Redis", "Kafka", "Eureka", "OpenAPI", "JavaScript", "TypeScript", "GitLab", "GitHub", "WebSocket", "PostgresSQL"}
CAMEL = re.compile(r"\b[A-Z][a-z0-9]+(?:[A-Z][A-Za-z0-9]*)+\b")
NUM = re.compile(r"(?<![\w.\-#])\d+(?![\w.\-])")


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def kiem(folder, use_xerj=False, doc=None):
    base = Path(folder)
    out = []  # (mức, mã, mô tả)

    def add(level, code, msg):
        out.append((level, code, msg))

    specs = {}
    for p in sorted(base.glob("*.spec.json")):
        try:
            specs[p.name] = load(p)
        except Exception as e:
            add("LỖI", "S0", f"{p.name}: JSON hỏng ({e})")
    if not specs:
        add("LỖI", "S0", f"không có file *.spec.json trong {base}")
        return out, specs
    by_type = {}
    for n, s in specs.items():
        by_type.setdefault(s.get("type"), []).append((n, s))

    # S1: công cụ hình thức
    for n in specs:
        if specs[n].get("type") == "bundle":
            continue   # bốn tab của bundle đã được kiểm riêng từng spec con
        r = subprocess.run([sys.executable, "-I", str(VE), str(base / n), "--check-only"], capture_output=True, text=True)
        lines = [l for l in r.stdout.splitlines() if l.startswith(("LỖI", "CẢNH BÁO", "  CẢNH BÁO", "  LỖI"))]
        for l in lines:
            lv = "LỖI" if l.strip().startswith("LỖI") else "CẢNH BÁO"
            add(lv, "S1", f"{n}: {l.strip()}")
        if r.returncode not in (0, 1):
            add("LỖI", "S1", f"{n}: công cụ lỗi mã {r.returncode}")

    # S2: bộ đủ chưa
    bundles = by_type.get("bundle", [])
    if not bundles:
        add("CẢNH BÁO", "S2", "chưa có spec loại bundle (một UC một file .drawio bốn tab)")
    for n, b in bundles:
        kinds = []
        for pg in b.get("pages", []):
            sp = specs.get(pg["spec"])
            kinds.append(sp.get("type") if sp else None)
            if sp is None:
                add("LỖI", "S2", f"{n}: tab '{pg.get('name')}' trỏ tới spec không có: {pg['spec']}")
        if sorted(k for k in kinds if k) != sorted(["erd", "class", "sequence", "activity"]):
            add("CẢNH BÁO", "S2", f"{n}: bundle phải đúng bốn tab erd, class, sequence, activity; đang có {kinds}")
    if "usecase" not in by_type:
        add("CẢNH BÁO", "S2", "chưa có spec use case (file riêng, không nằm trong bundle)")

    # S3: ảnh và drawio còn mới, không bị sửa tay
    for n, s in specs.items():
        if s.get("type") == "bundle":
            out_p = base / s.get("out", "")
            if out_p.exists():
                side = Path(str(out_p) + ".sha")
                if side.exists() and side.read_text(encoding="utf-8").strip() != sha(out_p):
                    add("CẢNH BÁO", "S3", f"{out_p.name} đã bị sửa tay hoặc không do công cụ sinh (sha khác); đừng sinh lại đè")
            else:
                add("CẢNH BÁO", "S3", f"{s.get('out')} chưa được sinh")
            continue
        png = s.get("png")
        if png:
            pp = base / png
            if not pp.exists():
                add("CẢNH BÁO", "S3", f"{n}: chưa có ảnh {png}")
            elif pp.stat().st_mtime + 1 < (base / n).stat().st_mtime:
                add("CẢNH BÁO", "S3", f"{n}: ảnh {png} CŨ hơn spec; sinh lại rồi xem lại ảnh")

    # A: activity
    class_names = set()
    for n, s in by_type.get("class", []):
        for c in s.get("classes", []):
            class_names.add(re.sub(r"<.*?>", "", c["name"]).strip())
    for n, s in by_type.get("activity", []):
        for ln in s.get("lanes", []):
            name = ln.get("name", "")
            first = name.split("\n")[0]
            if FORBID_LANE.search(first):
                add("LỖI", "A1", f"{n}: làn '{first}' không phải một lớp hoặc thành phần (không đặt làn Nhánh lỗi, Kết thúc, Chung)")
            if re.search(r"người dùng", name, re.I) and re.search(r"trình duyệt|giao diện|frontend|browser", name, re.I):
                add("CẢNH BÁO", "A2", f"{n}: làn '{first}' gộp Người dùng với Giao diện; tách thành hai làn")
            ids = CAMEL.findall(name.replace("\n", ""))
            for i in ids:
                if re.search(r"frontend|giao diện", name, re.I):
                    continue   # thành phần giao diện (React) không nằm trong sơ đồ lớp Java
                if class_names and i not in class_names and i not in INFRA:
                    add("CẢNH BÁO", "X2", f"{n}: lớp '{i}' ở làn '{first}' không có trong sơ đồ lớp (thêm hộp hoặc sửa tên)")
        for nd in s.get("nodes", []):
            if nd.get("kind") == "end" and not nd.get("note"):
                add("CẢNH BÁO", "A3", f"{n}: điểm kết thúc '{nd['id']}' chưa ghi kết quả (note)")

    # U: use case
    for n, s in by_type.get("usecase", []):
        sysname = s.get("system", "")
        for a in s.get("actors", []):
            lab = a["label"].replace("\n", " ")
            if INTERNAL.search(lab):
                add("CẢNH BÁO", "U1", f"{n}: tác nhân '{lab}' trông như thành phần NỘI BỘ; chỉ hợp lệ nếu là hệ thống bên ngoài, nằm ngoài khung hệ thống")
            for tok in re.findall(r"[\w\-]{4,}", lab):
                if INTERNAL.search(tok) and tok.lower() in sysname.lower():
                    add("LỖI", "U2", f"{n}: tác nhân '{lab}' nằm trong tên hệ thống '{sysname}' (vừa trong vừa ngoài khung)")
            if MERGED_ROLE.search(lab):
                add("CẢNH BÁO", "U3", f"{n}: tác nhân '{lab}' có vẻ gộp nhiều vai; tách thành các tác nhân riêng")

    # X1: sequence participants có trong class
    for n, s in by_type.get("sequence", []):
        for p in s.get("participants", []):
            for i in CAMEL.findall(p["name"].replace("\n", "")):
                if class_names and i not in class_names and i not in INFRA:
                    add("CẢNH BÁO", "X1", f"{n}: đối tượng '{i}' không có trong sơ đồ lớp")

    # N: con số cần nguồn
    nums = {}
    for n, s in specs.items():
        texts = []
        for nd in s.get("nodes", []):
            texts += [nd.get("label", ""), nd.get("note", "")]
        for m in s.get("messages", []):
            texts.append(m.get("label", ""))
        for c in s.get("classes", []):
            texts += c.get("attrs", []) + c.get("methods", [])
        for t in texts:
            t2 = re.sub(r"(HTTP|ORDER-|MAN-|UC-|BR-)\s*\d[\d.\-]*", "", t)
            for x in NUM.findall(t2):
                nums.setdefault(x, set()).add(n)
    if nums:
        add("XEM TAY", "N1", "con số trên hình, mỗi số phải có nguồn (cấu hình, tài liệu, mã): " +
            "; ".join(f"{k} ({', '.join(sorted(v))})" for k, v in sorted(nums.items())))

    # N2: tên lớp trong chỉ mục XERJ
    if use_xerj and class_names:
        thieu = []
        for c in sorted(class_names):
            try:
                r = subprocess.run(["xerj", "def", c, "--prefix", "gdt"], capture_output=True, text=True, timeout=25)
                if "no definition" in (r.stdout + r.stderr):
                    thieu.append(c)
            except Exception:
                add("XEM TAY", "N2", "không chạy được xerj; kiểm tên lớp thủ công")
                thieu = []
                break
        if thieu:
            add("XEM TAY", "N2", "chưa thấy trong chỉ mục XERJ (có thể ở worktree hoặc bịa tên): " + ", ".join(thieu))

    # D: tài liệu nhúng ảnh
    if doc:
        text = Path(doc).read_text(encoding="utf-8")
        for n, s in specs.items():
            png = s.get("png")
            if png and png not in text:
                add("CẢNH BÁO", "D1", f"tài liệu chưa nhúng ảnh {png}")
    return out, specs


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    folder = a[0]
    doc = a[a.index("--doc") + 1] if "--doc" in a else None
    out, specs = kiem(folder, "--xerj" in a, doc)
    out = list(dict.fromkeys(out))
    lines = [f"# Báo cáo kiểm bộ sơ đồ: {folder}", ""]
    for lv in ("LỖI", "CẢNH BÁO", "XEM TAY"):
        items = [x for x in out if x[0] == lv]
        lines.append(f"## {lv} ({len(items)})")
        lines += [f"- [{c}] {m}" for _, c, m in items] or ["- (không có)"]
        lines.append("")
    pngs = [s["png"] for s in specs.values() if s.get("png")]
    lines.append("## Việc người hoặc agent PHẢI làm tiếp (công cụ không thay được)")
    lines.append("- Mở và xem từng ảnh: " + ", ".join(pngs))
    lines.append("- Đối chiếu mỗi tên, con số trên hình với nguồn thật (mã nguồn qua XERJ, CSDL, tài liệu UC); phiếu phân tích phải có cột Nguồn.")
    lines.append("- Mỗi nhánh `if`, `throw` trong các hàm đã đi qua có mặt trong activity chưa.")
    rep = "\n".join(lines)
    print(rep)
    if "--ghi" in a:
        Path(a[a.index("--ghi") + 1]).write_text(rep + "\n", encoding="utf-8")
    return 1 if any(x[0] == "LỖI" for x in out) else 0


if __name__ == "__main__":
    sys.exit(main())
