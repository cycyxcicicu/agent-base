#!/usr/bin/env python3
"""scripts/diagram-describe.py

Đọc một file draw.io (`.drawio`, không nén, nhiều trang cũng được) và in ra **mô tả bằng chữ**: làn, nút, đường nối có nhãn,
và các bước đánh số theo thứ tự đi từ điểm bắt đầu. Agent không "nhìn" được ảnh, nên dùng bản chữ này để hiểu hoạt động của
sơ đồ rồi viết phần mô tả đi kèm (xem agents/knowledge/diagrams/mo-ta-hoat-dong-so-do.md).

Dùng:
  python scripts/diagram-describe.py <file.drawio>                 mô tả mọi trang
  python scripts/diagram-describe.py <file.drawio> --page "Tên"    chỉ một trang
  python scripts/diagram-describe.py <file.drawio> --json          đầu ra JSON
  python scripts/diagram-describe.py <file.drawio> --check         chỉ kiểm quy tắc, mã thoát 1 nếu có lỗi

Quy tắc kiểm (--check): id trang không trùng. Với sơ đồ hoạt động (trang có nút bắt đầu): mũi tên có đủ nguồn và đích;
đúng một nút kết thúc; quyết định có ít nhất hai nhánh và nhánh có nhãn; không có nút mồ côi. Loại khác chỉ kiểm id trang.

Chỉ dùng thư viện chuẩn. File bị nén (draw.io lưu nén) thì báo lỗi: bỏ tích File > Properties > Compressed rồi lưu lại.
"""

import argparse
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import deque

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def clean(label):
    text = html.unescape(label or "")
    text = re.sub(r"<br\s*/?>", " / ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", text).strip()


def style_map(style):
    out = {}
    for part in (style or "").split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip()
        elif part.strip():
            out[part.strip()] = True
    return out


def kind_of(style):
    s = style_map(style)
    low = (style or "").lower()
    if "umlactor" in low:
        return "tác nhân"
    if "endstate" in low:
        return "kết thúc"
    if "rhombus" in low:
        return "quyết định"
    if "ellipse" in low and str(s.get("fillColor", "")).lower() in ("#0f172a", "#000000", "#111827"):
        return "bắt đầu"
    if "ellipse" in low:
        return "use case"
    if s.get("text") or low.startswith("text"):
        return "ghi chú"
    return "việc"


def is_lane(style):
    low = (style or "").lower()
    return "swimlane" in low or "container=1" in low or "pool" in low


def parse_page(diagram):
    root = diagram.find(".//root")
    if root is None:
        return None
    cells = {}
    for c in root.iter("mxCell"):
        g = c.find("mxGeometry")
        geo = None
        if g is not None and g.get("width") is not None:
            geo = (float(g.get("x", 0)), float(g.get("y", 0)), float(g.get("width", 0)), float(g.get("height", 0)))
        cells[c.get("id")] = {
            "id": c.get("id"), "label": clean(c.get("value")), "style": c.get("style", ""),
            "vertex": c.get("vertex") == "1", "edge": c.get("edge") == "1", "parent": c.get("parent"),
            "source": c.get("source"), "target": c.get("target"), "geo": geo,
        }

    def absolute(cell):
        if not cell["geo"]:
            return None
        x, y, w, h = cell["geo"]
        parent = cells.get(cell["parent"])
        depth = 0
        while parent and parent["vertex"] and parent["geo"] and depth < 5:
            x += parent["geo"][0]
            y += parent["geo"][1]
            parent = cells.get(parent["parent"])
            depth += 1
        return (x, y, w, h)

    lanes = [c for c in cells.values() if c["vertex"] and is_lane(c["style"]) and c["geo"]]
    hidden = set()
    # Kiểu vẽ làn bằng hai hình chữ nhật: khung nền (fillColor=none, không nhãn) và tiêu đề tô màu nằm sát cạnh khung.
    vertices = [c for c in cells.values() if c["vertex"] and c["geo"] and c not in lanes]
    for frame in vertices:
        fa = absolute(frame)
        if frame["label"] or "fillcolor=none" not in frame["style"].lower().replace(" ", "") or max(fa[2], fa[3]) < 200:
            continue
        for head in vertices:
            ha = absolute(head)
            if head is frame or not head["label"] or head["id"] in hidden:
                continue
            inside = fa[0] - 3 <= ha[0] and fa[1] - 3 <= ha[1] and ha[0] + ha[2] <= fa[0] + fa[2] + 3 and ha[1] + ha[3] <= fa[1] + fa[3] + 3
            top = abs(ha[1] - fa[1]) <= 3 and ha[2] >= 0.8 * fa[2] and ha[3] <= 0.3 * fa[3]
            left = abs(ha[0] - fa[0]) <= 3 and ha[3] >= 0.8 * fa[3] and ha[2] <= 0.3 * fa[2]
            if inside and (top or left):
                lanes.append({**frame, "label": head["label"]})
                hidden.update([frame["id"], head["id"]])
                break
    nodes = [c for c in cells.values() if c["vertex"] and c not in lanes and c["id"] not in hidden]
    for n in nodes:
        n["kind"] = kind_of(n["style"])
        n["abs"] = absolute(n)
        n["lane"] = ""
        if n["abs"]:
            cx, cy = n["abs"][0] + n["abs"][2] / 2, n["abs"][1] + n["abs"][3] / 2
            for ln in lanes:
                lx, ly, lw, lh = absolute(ln)
                if lx <= cx <= lx + lw and ly <= cy <= ly + lh:
                    n["lane"] = ln["label"]
    edges = [c for c in cells.values() if c["edge"]]
    return {"name": diagram.get("name", ""), "id": diagram.get("id", ""), "lanes": [l["label"] for l in lanes],
            "nodes": nodes, "edges": edges, "cells": cells}


def order_steps(page):
    nodes = {n["id"]: n for n in page["nodes"] if n["kind"] != "ghi chú"}
    out_edges = {}
    indeg = {k: 0 for k in nodes}
    for e in page["edges"]:
        if e["source"] in nodes and e["target"] in nodes:
            out_edges.setdefault(e["source"], []).append(e)
            indeg[e["target"]] += 1
    starts = [k for k, n in nodes.items() if n["kind"] == "bắt đầu"] or [k for k, d in indeg.items() if d == 0]
    seen, order = set(), []
    queue = deque(sorted(starts, key=lambda k: (nodes[k]["abs"] or (0, 0))[1]))
    while queue:
        k = queue.popleft()
        if k in seen:
            continue
        seen.add(k)
        order.append(k)
        for e in sorted(out_edges.get(k, []), key=lambda e: (nodes[e["target"]]["abs"] or (0, 0))[1]):
            queue.append(e["target"])
    order += [k for k in nodes if k not in seen]
    return order, out_edges


def check_page(page):
    """Quy tắc chỉ áp cho sơ đồ hoạt động (trang có nút bắt đầu). Sequence, use case, thành phần vẽ tự do nên không kiểm."""
    problems = []
    nodes = {n["id"]: n for n in page["nodes"] if n["kind"] != "ghi chú"}
    activity = any(n["kind"] == "bắt đầu" for n in nodes.values())
    if not activity:
        return problems
    for e in page["edges"]:
        if e["source"] not in page["cells"] or e["target"] not in page["cells"]:
            problems.append(f"mũi tên {e['id']} thiếu nguồn hoặc đích")
    ends = [n for n in nodes.values() if n["kind"] == "kết thúc"]
    if len(ends) != 1:
        problems.append(f"sơ đồ hoạt động phải có đúng một nút kết thúc, đang có {len(ends)}")
    out_count = {}
    connected = set()
    for e in page["edges"]:
        out_count.setdefault(e["source"], []).append(e)
        connected.update([e["source"], e["target"]])
    for n in nodes.values():
        if n["kind"] == "quyết định":
            outs = out_count.get(n["id"], [])
            if len(outs) < 2:
                problems.append(f"quyết định '{n['label']}' có {len(outs)} nhánh (cần ít nhất 2)")
            for e in outs:
                if not e["label"]:
                    problems.append(f"nhánh ra từ '{n['label']}' chưa có nhãn")
        if n["id"] not in connected:
            problems.append(f"nút '{n['label']}' không nối vào đâu")
    return problems


def render_text(page, problems):
    order, out_edges = order_steps(page)
    nodes = {n["id"]: n for n in page["nodes"]}
    num = {k: i + 1 for i, k in enumerate(order)}
    lines = [f"## Trang: {page['name']} (id {page['id']})", ""]
    if page["lanes"]:
        lines += ["Làn: " + ", ".join(page["lanes"]), ""]
    lines += ["| Bước | Loại | Làn | Nội dung | Đi tới |", "|---|---|---|---|---|"]
    for k in order:
        n = nodes[k]
        targets = []
        for e in out_edges.get(k, []):
            t = nodes[e["target"]]
            label = f"[{e['label']}] " if e["label"] else ""
            targets.append(f"{label}bước {num[e['target']]}")
        lines.append(f"| {num[k]} | {n['kind']} | {n['lane']} | {n['label']} | {'; '.join(targets) or '-'} |")
    notes = [n["label"] for n in page["nodes"] if n["kind"] == "ghi chú" and n["label"]]
    if notes:
        lines += ["", "Ghi chú trên sơ đồ: " + " | ".join(notes)]
    lines += ["", "Kiểm quy tắc: " + ("đạt" if not problems else "")]
    lines += [f"- {p}" for p in problems]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Mô tả bằng chữ nội dung một file draw.io.")
    ap.add_argument("file")
    ap.add_argument("--page", help="Chỉ một trang theo tên")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true", help="Chỉ kiểm quy tắc")
    args = ap.parse_args()

    try:
        tree = ET.parse(args.file)
    except ET.ParseError as e:
        print(f"LỖI: không đọc được XML ({e}). File có thể bị nén: bỏ tích File > Properties > Compressed rồi lưu lại.", file=sys.stderr)
        sys.exit(2)
    diagrams = tree.getroot().findall("diagram")
    if not diagrams:
        print("LỖI: không có trang nào.", file=sys.stderr)
        sys.exit(2)

    ids = [d.get("id") for d in diagrams]
    global_problems = [f"id trang trùng: {i}" for i in sorted({i for i in ids if ids.count(i) > 1})]
    results, failed = [], bool(global_problems)
    for d in diagrams:
        if args.page and d.get("name") != args.page:
            continue
        page = parse_page(d)
        if page is None:
            print(f"LỖI: trang '{d.get('name')}' bị nén hoặc rỗng.", file=sys.stderr)
            failed = True
            continue
        problems = check_page(page)
        failed = failed or bool(problems)
        results.append((page, problems))

    if args.check:
        for p in global_problems:
            print(f"[file] {p}")
        for page, problems in results:
            for p in problems:
                print(f"[{page['name']}] {p}")
        print("Đạt." if not failed else "Có lỗi.")
        sys.exit(1 if failed else 0)

    if args.json:
        out = []
        for page, problems in results:
            order, out_edges = order_steps(page)
            nodes = {n["id"]: n for n in page["nodes"]}
            out.append({
                "page": page["name"], "lanes": page["lanes"], "problems": problems,
                "steps": [{"step": i + 1, "id": k, "kind": nodes[k]["kind"], "lane": nodes[k]["lane"], "label": nodes[k]["label"],
                           "to": [{"label": e["label"], "id": e["target"]} for e in out_edges.get(k, [])]}
                          for i, k in enumerate(order)],
            })
        print(json.dumps({"file_problems": global_problems, "pages": out}, ensure_ascii=False, indent=2))
    else:
        for p in global_problems:
            print(f"CẢNH BÁO: {p}")
        for page, problems in results:
            print(render_text(page, problems))
    sys.exit(0)


if __name__ == "__main__":
    main()
