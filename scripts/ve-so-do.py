#!/usr/bin/env python3
"""Vẽ sơ đồ theo MẪU CHUẨN của dự án từ một file mô tả JSON. Một công cụ cho MỌI agent và MỌI loại sơ đồ.

Agent chỉ viết JSON (nút, quan hệ, thông điệp...), KHÔNG tự tính tọa độ và KHÔNG viết XML draw.io.
Script tự bố trí, nối đường, ghi .drawio, xuất .png (cần draw.io Desktop) và kiểm lỗi bằng chữ
(cho agent không xem được ảnh).

  python3 scripts/ve-so-do.py <spec.json>                  # vẽ: ghi .drawio và .png, in kết quả kiểm
  python3 scripts/ve-so-do.py <spec.json> --check-only     # chỉ kiểm, không ghi file
  python3 scripts/ve-so-do.py --mau class|flow|swimlane|activity|usecase|statemachine|component|deployment|package|sequence|erd|bundle   # in JSON mẫu của loại đó

Trường `type` trong JSON: class (sơ đồ lớp), flow (lưu đồ một làn), swimlane (hoạt động làn theo VAI, một đầu một cuối),
usecase (use case UML, tác nhân theo vai thật), statemachine (trạng thái), component (thành phần), deployment (triển khai), package (gói), activity (hoạt động làn theo LỚP, nhiều đầu nhiều cuối, đen trắng, kiểu anhbv), sequence (tuần tự), erd (bảng dữ liệu),
bundle (gộp nhiều spec thành các tab của MỘT file .drawio; mỗi tab một loại sơ đồ).
Mã thoát: 0 đạt; 1 có LỖI. CẢNH BÁO không làm thất bại nhưng PHẢI sửa hoặc ghi lý do trong báo cáo.
Quy trình bắt buộc và chuẩn từng loại: agents/knowledge/diagrams/quy-trinh-ve-so-do-bang-json.md
Chỉ dùng thư viện chuẩn của Python.
"""
import copy
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import textwrap
import xml.etree.ElementTree as ET
from pathlib import Path

DRAWIO_CLI = "/Applications/draw.io.app/Contents/MacOS/draw.io"
INK, SEP = "#1f1f1f", "#c2c2c2"
GREEN, RED, BLUE = "#16a34a", "#dc2626", "#2563eb"
LINE_H, GAP_X, GAP_Y, MARGIN, TOP = 20, 120, 70, 40, 90

# ----------------------------------------------------------------------------------------------- JSON mẫu
MAU = {
    "class": {
        "type": "class", "title": "Mẫu sơ đồ lớp", "note": "Tam giác rỗng: Extends, implements. Thoi rỗng: chứa. Mũi tên đặc: dùng.",
        "out": "mau-lop.drawio", "png": "mau-lop.png",
        "classes": [
            {"id": "search", "col": 0, "name": "Search", "sub": "tìm kiếm", "stereo": "interface",
             "methods": ["+ searchByTitle(string title)", "+ searchByAuthor(string author)"]},
            {"id": "user", "col": 0, "name": "User", "sub": "người dùng", "stereo": "Abstract", "abstract": True,
             "attrs": ["- id : string", "- password : string"], "methods": ["+ resetPassword( ) : bool"]},
            {"id": "catalog", "col": 1, "name": "Catalog", "sub": "danh mục sách", "attrs": ["- bookTitles", "- bookAuthors"],
             "methods": ["+ searchByTitle(string query)", "+ searchByAuthor(string query)"]},
            {"id": "member", "col": 1, "name": "Member", "sub": "độc giả", "attrs": ["- dateOfMembership : date"],
             "methods": ["+ checkoutBookItem(BookItem bookItem) : bool"]}],
        "relations": [
            {"from": "catalog", "to": "search", "kind": "ext", "label": "implements"},
            {"from": "member", "to": "user", "kind": "ext", "label": "Extends"},
            {"from": "catalog", "to": "member", "kind": "dep", "label": "dùng"}]},
    "flow": {
        "type": "flow", "title": "Mẫu lưu đồ", "note": "Một điểm bắt đầu, một điểm kết thúc. Đỏ là nhánh lỗi.",
        "out": "mau-flow.drawio", "png": "mau-flow.png",
        "nodes": [
            {"id": "s", "kind": "start", "col": 0, "row": 0},
            {"id": "d1", "kind": "dec", "col": 0, "row": 1, "label": "Có điều kiện lọc nào?"},
            {"id": "p1", "kind": "proc", "col": 0, "row": 2, "label": "Kiểm tra từng điều kiện"},
            {"id": "e1", "kind": "err", "col": 1, "row": 1, "label": "Báo lỗi (INVALID)"},
            {"id": "end", "kind": "end", "col": 0, "row": 3}],
        "edges": [
            {"from": "s", "to": "d1"},
            {"from": "d1", "to": "p1", "label": "Có", "color": "green"},
            {"from": "d1", "to": "e1", "label": "Không", "color": "red"},
            {"from": "p1", "to": "end"},
            {"from": "e1", "to": "end", "color": "red", "via": 1250}]},
    "swimlane": {
        "type": "swimlane", "title": "Mẫu sơ đồ hoạt động nhiều làn bơi", "note": "Mỗi làn là một tác nhân. Một điểm bắt đầu, một điểm kết thúc. Đỏ là nhánh lỗi.",
        "out": "mau-swimlane.drawio", "png": "mau-swimlane.png",
        "lanes": [{"id": "u", "name": "Người dùng", "color": "gray"}, {"id": "fe", "name": "Giao diện", "color": "blue"},
                  {"id": "be", "name": "Backend", "color": "purple"}, {"id": "db", "name": "PostgreSQL", "color": "green"}],
        "nodes": [
            {"id": "s", "kind": "start", "lane": "u", "row": 0},
            {"id": "n1", "kind": "proc", "lane": "u", "row": 1, "label": "Bấm [Áp dụng]"},
            {"id": "d1", "kind": "dec", "lane": "fe", "row": 2, "label": "Giá trị nhập hợp lệ?"},
            {"id": "e1", "kind": "err", "lane": "fe", "row": 3, "label": "Báo lỗi tại ô nhập"},
            {"id": "n2", "kind": "proc", "lane": "be", "row": 3, "label": "Kiểm danh mục, dựng câu lọc"},
            {"id": "n3", "kind": "proc", "lane": "db", "row": 4, "label": "SELECT id ... (lấy trang mã đơn)"},
            {"id": "n4", "kind": "proc", "lane": "fe", "row": 5, "label": "Hiện bảng kết quả"},
            {"id": "end", "kind": "end", "lane": "u", "row": 6}],
        "edges": [
            {"from": "s", "to": "n1"}, {"from": "n1", "to": "d1"},
            {"from": "d1", "to": "e1", "label": "Không", "color": "red"}, {"from": "d1", "to": "n2", "label": "Có", "color": "green"},
            {"from": "n2", "to": "n3"}, {"from": "n3", "to": "n4"}, {"from": "n4", "to": "end"},
            {"from": "e1", "to": "end", "color": "red"}]},
    "sequence": {
        "type": "sequence", "title": "Mẫu sơ đồ tuần tự", "out": "mau-seq.drawio", "png": "mau-seq.png",
        "participants": [{"id": "ui", "name": "Trình duyệt", "color": "blue"}, {"id": "api", "name": "Controller\n(OrderController)"},
                         {"id": "db", "name": "PostgreSQL", "color": "green"}],
        "messages": [
            {"from": "ui", "to": "api", "label": "Gửi yêu cầu lấy danh sách"},
            {"from": "api", "to": "api", "kind": "self", "label": "Kiểm tra điều kiện lọc"},
            {"from": "api", "to": "db", "label": "SELECT id ..."},
            {"from": "db", "to": "api", "kind": "return", "label": "Danh sách mã đơn"},
            {"from": "api", "to": "ui", "kind": "return", "label": "Trang kết quả, HTTP 200"}]},
    "erd": {
        "type": "erd", "title": "Mẫu ERD", "note": "PK khóa chính, FK khóa ngoại, UQ duy nhất. Tô cam: cột nằm trong chỉ mục.",
        "out": "mau-erd.drawio", "png": "mau-erd.png",
        "tables": [
            {"id": "order", "col": 1, "name": "order", "color": "green", "hot": ["order_date"],
             "columns": [["id", "integer", "PK"], ["order_number", "varchar(50)", "UQ"], ["order_date", "timestamp", ""],
                         ["page_id", "integer", "FK"]]},
            {"id": "page", "col": 0, "name": "page", "color": "blue", "columns": [["id", "integer", "PK"], ["name", "varchar(255)", ""]]}],
        "relations": [{"from": "page", "from_col": "id", "to": "order", "to_col": "page_id", "label": "page_id"}]},
    "activity": {
        "type": "activity", "title": "Mẫu sơ đồ hoạt động theo làn lớp (kiểu anhbv)",
        "note": "Mỗi làn là một lớp hoặc thành phần. Nhiều điểm bắt đầu và kết thúc. Nét đứt là lời gọi sang làn khác. Đen trắng.",
        "out": "mau-activity.drawio", "png": "mau-activity.png",
        "lanes": [{"id": "ctl", "name": "OrderController"}, {"id": "svc", "name": "OrderService (sub 0) và OrderValidator (sub 1)"},
                  {"id": "db", "name": "PostgreSQL"}],
        "nodes": [
            {"id": "s1", "kind": "start", "lane": "ctl", "row": 0},
            {"id": "a1", "kind": "proc", "lane": "ctl", "row": 1, "label": "Nhận yêu cầu GET /orders"},
            {"id": "a2", "kind": "proc", "lane": "svc", "row": 1, "label": "Dựng bộ lọc từ tham số"},
            {"id": "d1", "kind": "dec", "lane": "svc", "row": 2, "label": "Bộ lọc hợp lệ?"},
            {"id": "x1", "kind": "err", "lane": "svc", "sub": 1, "row": 2, "label": "Ném lỗi bộ lọc (ORDER-4027)"},
            {"id": "e1", "kind": "end", "lane": "svc", "sub": 1, "row": 3, "note": "Kết thúc: trả HTTP 400"},
            {"id": "a3", "kind": "proc", "lane": "db", "row": 4, "label": "SELECT id ... một trang"},
            {"id": "a4", "kind": "proc", "lane": "ctl", "row": 5, "label": "Trả HTTP 200 và danh sách"},
            {"id": "e2", "kind": "end", "lane": "ctl", "row": 6}],
        "edges": [
            {"from": "s1", "to": "a1"}, {"from": "a1", "to": "a2", "label": "gọi service"},
            {"from": "a2", "to": "d1"}, {"from": "d1", "to": "x1", "label": "Không"},
            {"from": "d1", "to": "a3", "label": "Có", "first": "v"}, {"from": "x1", "to": "e1"},
            {"from": "a3", "to": "a4", "label": "danh sách mã đơn", "first": "v"}, {"from": "a4", "to": "e2"}]},
    "usecase": {
        "type": "usecase", "title": "Mẫu sơ đồ use case", "system": "Hệ thống đơn hàng",
        "note": "Tác nhân đặt tên theo vai thật. include: dùng chung bước; extend: mở rộng tùy điều kiện.",
        "out": "mau-usecase.drawio", "png": "mau-usecase.png",
        "usecases": [{"id": "a", "label": "Lọc đơn nâng cao"}, {"id": "b", "label": "Kiểm tra bộ lọc hợp lệ"}, {"id": "c", "label": "Xuất Excel theo bộ lọc"}],
        "actors": [{"id": "kt", "label": "Kế toán", "side": "left", "near": "a"}, {"id": "cskh", "label": "CSKH", "side": "right", "near": "c"}],
        "links": [["kt", "a"], ["cskh", "a"], ["cskh", "c"]],
        "relations": [{"from": "a", "to": "b", "type": "include"}, {"from": "c", "to": "a", "type": "extend"}]},
    "statemachine": {
        "type": "statemachine", "title": "Mẫu máy trạng thái: vòng đời một đơn (ví dụ minh họa, không phải dữ liệu thật)",
        "note": "Chuyển ghi: sự_kiện [điều_kiện] / hành_động. Trạng thái lấy từ enum thật, không tự đặt.",
        "out": "mau-statemachine.drawio", "png": "mau-statemachine.png",
        "states": [
            {"id": "i", "kind": "initial", "col": 0, "row": 0},
            {"id": "draft", "label": "Nháp", "col": 0, "row": 1.2, "actions": ["entry / tạo mã đơn"]},
            {"id": "conf", "label": "Đã xác nhận", "col": 1.3, "row": 1.2},
            {"id": "pack", "label": "Đang đóng gói", "col": 2.6, "row": 1.2},
            {"id": "ship", "label": "Đang giao", "col": 3.9, "row": 1.2},
            {"id": "done", "label": "Đã giao", "col": 3.9, "row": 3},
            {"id": "cancel", "label": "Đã hủy", "col": 1.3, "row": 3},
            {"id": "f", "kind": "final", "col": 2.6, "row": 4.3}],
        "transitions": [
            {"from": "i", "to": "draft"},
            {"from": "draft", "to": "conf", "label": "khách xác nhận [đủ tồn kho] / trừ kho"},
            {"from": "conf", "to": "pack", "label": "kho nhận đơn / in nhãn"},
            {"from": "pack", "to": "ship", "label": "bàn giao đơn vị vận chuyển"},
            {"from": "ship", "to": "done", "label": "vận chuyển báo giao xong / ghi COD"},
            {"from": "conf", "to": "cancel", "label": "khách hủy / hoàn kho"},
            {"from": "done", "to": "f", "label": "kết thúc vòng đời"},
            {"from": "cancel", "to": "f", "label": "kết thúc vòng đời"}]},
    "component": {
        "type": "component", "title": "Mẫu sơ đồ thành phần (ví dụ minh họa, không phải dữ liệu thật)",
        "note": "Chấm tròn là giao diện cung cấp; mũi tên nét đứt «use» là thành phần cần giao diện đó.",
        "out": "mau-component.drawio", "png": "mau-component.png",
        "components": [
            {"id": "web", "label": "Giao diện web", "col": 0, "row": 0},
            {"id": "ord", "label": "Dịch vụ đơn hàng", "col": 1, "row": 0, "provides": ["IOrder"]},
            {"id": "pay", "label": "Cổng thanh toán", "col": 2, "row": 0, "provides": ["IPay"]}],
        "boundaries": [{"label": "Hệ thống bán hàng", "members": ["web", "ord"]}],
        "connections": [
            {"from": "web", "to": "ord", "kind": "uses", "interface": "IOrder"},
            {"from": "ord", "to": "pay", "kind": "uses", "interface": "IPay", "label": "HTTPS"}]},
    "deployment": {
        "type": "deployment", "title": "Mẫu sơ đồ triển khai (ví dụ minh họa, không phải dữ liệu thật)",
        "note": "Nút hình hộp 3D. Artifact nằm trong nút được triển khai. Đường liền ghi giao thức.",
        "out": "mau-deployment.drawio", "png": "mau-deployment.png",
        "nodes": [
            {"id": "client", "label": "Máy người dùng", "stereo": "device", "col": 0, "row": 0, "artifacts": [{"id": "a_web", "label": "trình duyệt"}]},
            {"id": "app", "label": "Máy chủ ứng dụng", "stereo": "device", "col": 1, "row": 0, "children": ["jvm"]},
            {"id": "jvm", "label": "Java 21", "stereo": "executionEnvironment", "artifacts": [{"id": "a_jar", "label": "order-service.jar"}]},
            {"id": "dbs", "label": "Máy chủ CSDL", "stereo": "device", "col": 2, "row": 0, "artifacts": [{"id": "a_db", "label": "PostgreSQL 16"}]}],
        "paths": [{"from": "client", "to": "app", "label": "HTTPS"}, {"from": "app", "to": "dbs", "label": "JDBC"}]},
    "package": {
        "type": "package", "title": "Mẫu sơ đồ gói (ví dụ minh họa, không phải dữ liệu thật)",
        "note": "Mũi tên nét đứt: gói này phụ thuộc gói kia. «import»: nhập công khai; «access»: nhập riêng.",
        "out": "mau-package.drawio", "png": "mau-package.png",
        "packages": [
            {"id": "ui", "label": "presentation", "col": 0, "row": 0, "contains": ["OrderController", "OrderRequest"]},
            {"id": "dom", "label": "domain", "col": 1, "row": 0, "contains": ["Order", "OrderService"]},
            {"id": "db", "label": "persistence", "col": 2, "row": 0, "contains": ["OrderRepository"]}],
        "dependencies": [{"from": "ui", "to": "dom", "kind": "import"}, {"from": "db", "to": "dom", "kind": "access"}]},
    "bundle": {
        "type": "bundle", "title": "Gộp nhiều sơ đồ thành các tab của MỘT file .drawio", "out": "UC-XX.drawio",
        "pages": [{"name": "ERD Database Schema", "spec": "UC-XX-erd.spec.json"},
                  {"name": "Class Diagram", "spec": "UC-XX-class.spec.json"},
                  {"name": "Sequence Diagram", "spec": "UC-XX-sequence.spec.json"},
                  {"name": "Activity Diagram", "spec": "UC-XX-activity.spec.json"}]}
}

PAL = {"blue": ("#dbeafe", "#2563eb"), "green": ("#dcfce7", "#16a34a"), "purple": ("#ede9fe", "#7c3aed"),
       "amber": ("#fef3c7", "#d97706"), "red": ("#fee2e2", "#dc2626"), "gray": ("#f1f5f9", "#64748b")}
CLASS_KINDS = {
    "ext": ("endArrow=block;endFill=0;endSize=12;", False),
    "agg": ("startArrow=diamond;startFill=0;startSize=14;endArrow=none;", False),
    "comp": ("startArrow=diamond;startFill=1;startSize=14;endArrow=none;", False),
    "assoc": ("endArrow=block;endFill=1;endSize=8;", False),
    "dep": ("endArrow=open;endFill=0;endSize=10;", True),
}
COLORS = {"green": GREEN, "red": RED, "blue": BLUE, "black": INK, None: INK}


# ----------------------------------------------------------------------------------------------- XML
class Doc:
    def __init__(self, spec, width, height):
        self.n = 0
        self.mxf = ET.Element("mxfile", host="app.diagrams.net")
        d = ET.SubElement(self.mxf, "diagram", id="d1", name=spec.get("page", "Diagram"))
        gm = ET.SubElement(d, "mxGraphModel", dx="1000", dy="800", grid="1", gridSize="10", guides="1", tooltips="1",
                           connect="1", arrows="1", fold="1", page="0", pageScale="1", pageWidth=str(width),
                           pageHeight=str(height), math="0", shadow="0")
        self.root = ET.SubElement(gm, "root")
        ET.SubElement(self.root, "mxCell", id="0")
        ET.SubElement(self.root, "mxCell", id="1", parent="0")
        self.vertex(MARGIN, 10, width - 80, 30, spec.get("title", ""), "text;html=0;whiteSpace=wrap;fontSize=18;fontStyle=1;align=left;")
        if spec.get("note"):
            self.vertex(MARGIN, 42, width - 80, 24, spec["note"], "text;html=0;whiteSpace=wrap;fontSize=12;fontColor=#475569;align=left;")

    def vertex(self, x, y, w, h, value, style, vid=None):
        """vid: mã ô cố định theo mã trong JSON (để đồng bộ ngược từ bản người dùng sửa tay)."""
        self.n += 1
        cid = vid or f"v{self.n}"
        cell = ET.SubElement(self.root, "mxCell", id=cid, value=value, style=style, vertex="1", parent="1")
        ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h), **{"as": "geometry"})
        return cid

    def anchor(self, x, y):
        return self.vertex(x - 2, y - 2, 4, 4, "", "ellipse;fillColor=none;strokeColor=none;")

    def edge(self, pts, label="", color=INK, extra="", dashed=False, labelstyle="labelBackgroundColor=#ffffff;", eid=None,
             src=None, dst=None, ra=None, rb=None, lab_x=None):
        """Nối bằng điểm neo; nếu có src, dst (mã ô) và ra, rb (hình chữ nhật) thì nối thẳng vào ô, đường đi theo ô khi người dùng kéo."""
        if src and dst and ra and rb:
            ida, idb = src, dst

            def frac(pt, r):
                x1, y1, x2, y2 = r
                return (min(1, max(0, (pt[0] - x1) / max(x2 - x1, 1))), min(1, max(0, (pt[1] - y1) / max(y2 - y1, 1))))
            ex, ey = frac(pts[0], ra)
            nx, ny = frac(pts[-1], rb)
            extra += f"exitX={ex:.3f};exitY={ey:.3f};exitDx=0;exitDy=0;entryX={nx:.3f};entryY={ny:.3f};entryDx=0;entryDy=0;"
        else:
            ida, idb = self.anchor(*pts[0]), self.anchor(*pts[-1])
        mid = pts[1:-1]
        style = (f"endArrow=block;endFill=1;strokeWidth=1.5;html=0;fontSize=12;{labelstyle}strokeColor={color};"
                 + ("edgeStyle=orthogonalEdgeStyle;rounded=0;" if mid else "") + ("dashed=1;" if dashed else "") + extra)
        self.n += 1
        e = ET.SubElement(self.root, "mxCell", id=eid or f"e{self.n}", value=label, style=style, edge="1", parent="1", source=ida, target=idb)
        g = ET.SubElement(e, "mxGeometry", relative="1", **{"as": "geometry"})
        if lab_x is not None:
            g.set("x", f"{lab_x:.3f}")
        if mid:
            arr = ET.SubElement(g, "Array", **{"as": "points"})
            for px, py in mid:
                ET.SubElement(arr, "mxPoint", x=str(px), y=str(py))


# ----------------------------------------------------------------------------------------------- hình học chung
def rect(b):
    return (b["_x"], b["_y"], b["_x"] + b["_w"], b["_y"] + b["_h"])


def stack_columns(items, gap_x=GAP_X, gap_y=GAP_Y):
    """Xếp theo cột (col) trái sang phải, trong cột từ trên xuống. Phần tử có x, y thì giữ nguyên."""
    cols = {}
    for c in items:
        cols.setdefault(c.get("col", 0), []).append(c)
    x = MARGIN
    for col in sorted(cols):
        width = max(c["_w"] for c in cols[col])
        y = TOP
        for c in cols[col]:
            if "x" in c and "y" in c:
                c["_x"], c["_y"] = c["x"], c["y"]
            else:
                c["_x"], c["_y"] = x, y
            y = max(y, c["_y"]) + c["_h"] + gap_y
        x += width + gap_x


def route_boxes(a, b, via=None):
    """Nối hai hộp: kề dọc thì thẳng đứng, kề ngang thì nằm ngang, còn lại gấp khúc; via là đường vòng ngoài."""
    ax1, ay1, ax2, ay2 = rect(a)
    bx1, by1, bx2, by2 = rect(b)
    ox1, ox2, oy1, oy2 = max(ax1, bx1), min(ax2, bx2), max(ay1, by1), min(ay2, by2)
    if via is not None:
        ya, yb = ay1 + 16, by1 + 16
        return [(ax2 if via >= ax2 else ax1, ya), (via, ya), (via, yb), (bx2 if via >= bx2 else bx1, yb)]
    if ox2 - ox1 >= 40:
        x = (ox1 + ox2) // 2
        return [(x, ay2), (x, by1)] if ay2 <= by1 else [(x, ay1), (x, by2)]
    if oy2 - oy1 >= 40:
        y = (oy1 + oy2) // 2
        return [(ax2, y), (bx1, y)] if ax2 <= bx1 else [(ax1, y), (bx2, y)]
    acx, acy, bcx = (ax1 + ax2) // 2, (ay1 + ay2) // 2, (bx1 + bx2) // 2
    return [(ax2, acy) if bcx > acx else (ax1, acy), (bcx, acy), (bcx, by1 if by1 > acy else by2)]


def seg_hits(p, q, r):
    x1, y1, x2, y2 = r
    (px, py), (qx, qy) = p, q
    if px == qx:
        return x1 + 2 < px < x2 - 2 and min(py, qy) < y2 - 2 and max(py, qy) > y1 + 2
    if py == qy:
        return y1 + 2 < py < y2 - 2 and min(px, qx) < x2 - 2 and max(px, qx) > x1 + 2
    return False


def check_boxes(boxes, routes, label):
    loi, cb = [], []
    for i, a in enumerate(boxes):
        for b in boxes[i + 1:]:
            ax1, ay1, ax2, ay2 = rect(a)
            bx1, by1, bx2, by2 = rect(b)
            if ax1 < bx2 and bx1 < ax2 and ay1 < by2 and by1 < ay2:
                loi.append(f"LỖI: '{a['id']}' và '{b['id']}' chồng nhau")
    for src, dst, pts in routes:
        for p, q in zip(pts, pts[1:]):
            for c in boxes:
                if c["id"] in (src, dst):
                    continue
                if seg_hits(p, q, rect(c)):
                    cb.append(f"CẢNH BÁO: đường '{src}' -> '{dst}' cắt qua '{c['id']}' (đổi cột, thêm via, hoặc dời)")
    return loi, cb


def label_pos(pts, lab_x=None):
    """Điểm đặt nhãn của một đường nối (draw.io đặt ở giữa độ dài đường; lab_x từ -1 đến 1 dời dọc đường)."""
    segs = [(p, q, abs(q[0] - p[0]) + abs(q[1] - p[1])) for p, q in zip(pts, pts[1:])]
    total = sum(sg[2] for sg in segs) or 1
    target = total * ((lab_x or 0) + 1) / 2
    run = 0
    for p, q, ln in segs:
        if run + ln >= target and ln:
            f = (target - run) / ln
            return (p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f)
        run += ln
    return pts[-1]


def check_labels(items, boxes):
    """items: [(mô tả, nhãn, pts, lab_x)]. Cảnh báo khi nhãn chồng nhãn khác hoặc chồng lên hộp không phải đầu mút của đường."""
    rects, cb = [], []
    for desc, label, pts, lab_x, ends in items:
        if not label:
            continue
        cx, cy = label_pos(pts, lab_x)
        w = len(label) * 6.6 + 8
        r = (cx - w / 2, cy - 9, cx + w / 2, cy + 9)
        rects.append((desc, label, r))
        for b in boxes:
            if b["id"] in ends:
                continue
            bx1, by1, bx2, by2 = rect(b)
            if r[0] < bx2 and bx1 < r[2] and r[1] < by2 and by1 < r[3]:
                cb.append(f"CẢNH BÁO: nhãn \"{label[:30]}\" của {desc} đè lên hộp '{b['id']}' (đổi vị trí hộp, rút ngắn nhãn, hoặc đổi cách đi của đường)")
    for i, (d1, l1, r1) in enumerate(rects):
        for d2, l2, r2 in rects[i + 1:]:
            if r1[0] < r2[2] and r2[0] < r1[2] and r1[1] < r2[3] and r2[1] < r1[3]:
                cb.append(f"CẢNH BÁO: nhãn \"{l1[:30]}\" ({d1}) chồng lên nhãn \"{l2[:30]}\" ({d2}); dời hộp hoặc đổi cách đi")
    # nhãn đè lên ĐƯỜNG của cạnh khác (chữ bị gạch ngang hoặc dính vào đường lạ)
    for desc, label, pts, lab_x, ends in items:
        if not label:
            continue
        cx, cy = label_pos(pts, lab_x)
        w = len(label) * 6.6 + 8
        r = (cx - w / 2, cy - 9, cx + w / 2, cy + 9)
        for d2, l2, pts2, _, _ in items:
            if pts2 is pts or d2 == desc:
                continue
            if any(seg_hits(p, q, r) for p, q in zip(pts2, pts2[1:])):
                cb.append(f"CẢNH BÁO: nhãn \"{label[:30]}\" của {desc} bị đường của {d2} cắt qua (nhìn như bị gạch; đổi lab_x, đổi cột hoặc cách đi)")
    return list(dict.fromkeys(cb))


def check_edge_overlap(routes):
    """routes: [(nguồn, đích, pts)]. Cảnh báo khi hai đường KHÁC nguồn VÀ KHÁC đích có đoạn thẳng nằm chồng lên nhau (nhìn như một đường).
    Hai đường chung nguồn (tách nhánh) hoặc chung đích (gộp nhánh) được phép chạm nhau ở đầu mút."""
    cb = []
    segs = [(s, d, p, q) for s, d, pts in routes for p, q in zip(pts, pts[1:])]
    for i, (s1, d1, p1, q1) in enumerate(segs):
        for s2, d2, p2, q2 in segs[i + 1:]:
            if s1 == s2 or (s1, d1) == (s2, d2):
                continue
            # cùng đích: cho phép gộp nhánh ở đoạn cuối ngắn (tối đa 40px), không cho dùng chung cả đoạn dài
            gioi = 40 if d1 == d2 else 8
            if p1[0] == q1[0] and p2[0] == q2[0] and abs(p1[0] - p2[0]) < 4:
                lo, hi = max(min(p1[1], q1[1]), min(p2[1], q2[1])), min(max(p1[1], q1[1]), max(p2[1], q2[1]))
                if hi - lo > gioi:
                    cb.append(f"CẢNH BÁO: đường '{s1}'->'{d1}' chồng lên đường '{s2}'->'{d2}' trên một đoạn dọc ({int(hi - lo)}px); tách khe hoặc đổi cột")
            elif p1[1] == q1[1] and p2[1] == q2[1] and abs(p1[1] - p2[1]) < 4:
                lo, hi = max(min(p1[0], q1[0]), min(p2[0], q2[0])), min(max(p1[0], q1[0]), max(p2[0], q2[0]))
                if hi - lo > gioi:
                    cb.append(f"CẢNH BÁO: đường '{s1}'->'{d1}' chồng lên đường '{s2}'->'{d2}' trên một đoạn ngang ({int(hi - lo)}px); tách khe hoặc đổi hàng")
    return list(dict.fromkeys(cb))


def check_shared_segments(routes):
    """routes: [(nhóm, mô tả, pts)]. Cảnh báo khi đoạn dọc hoặc ngang của hai quan hệ KHÁC nhóm nằm trùng nhau (nhìn như một đường)."""
    cb = []
    segs = []
    for grp, desc, pts in routes:
        for p, q in zip(pts, pts[1:]):
            segs.append((grp, desc, p, q))
    for i, (g1, d1, p1, q1) in enumerate(segs):
        for g2, d2, p2, q2 in segs[i + 1:]:
            if g1 == g2:
                continue
            if p1[0] == q1[0] and p2[0] == q2[0] and abs(p1[0] - p2[0]) < 3:
                lo, hi = max(min(p1[1], q1[1]), min(p2[1], q2[1])), min(max(p1[1], q1[1]), max(p2[1], q2[1]))
                if hi - lo > 12:
                    cb.append(f"CẢNH BÁO: {d1} và {d2} dùng chung một đoạn dọc, người xem tưởng cùng một quan hệ (đặt hai bảng khác cột hoặc tách khe)")
            elif p1[1] == q1[1] and p2[1] == q2[1] and abs(p1[1] - p2[1]) < 3:
                lo, hi = max(min(p1[0], q1[0]), min(p2[0], q2[0])), min(max(p1[0], q1[0]), max(p2[0], q2[0]))
                if hi - lo > 12:
                    cb.append(f"CẢNH BÁO: {d1} và {d2} dùng chung một đoạn ngang, người xem tưởng cùng một quan hệ")
    return list(dict.fromkeys(cb))


# ----------------------------------------------------------------------------------------------- CLASS
def class_sizes(c):
    hh = 26 + (18 if c.get("sub") else 0) + (18 if c.get("stereo") else 0)
    attrs, methods = c.get("attrs", []), c.get("methods", [])
    ah = LINE_H * len(attrs) + 10 if attrs else 14
    mh = LINE_H * len(methods) + 10 if methods else 0
    lines = [c["name"], c.get("sub", "")] + attrs + methods
    c["_hh"], c["_ah"], c["_mh"] = hh, ah, mh
    c["_w"] = c.get("w") or max(220, int(max(len(s) for s in lines) * 7 + 28))
    c["_h"] = hh + ah + mh


def run_class(spec):
    cs = spec["classes"]
    ids = [c["id"] for c in cs]
    loi = [f"LỖI: quan hệ trỏ tới lớp không có: '{r[k]}'" for r in spec.get("relations", []) for k in ("from", "to") if r[k] not in ids]
    loi += [f"LỖI: kind '{r.get('kind')}' không hợp lệ (dùng: {', '.join(CLASS_KINDS)})" for r in spec.get("relations", []) if r.get("kind", "assoc") not in CLASS_KINDS]
    if loi:
        return None, loi, []
    for c in cs:
        class_sizes(c)
    stack_columns(cs)
    by = {c["id"]: c for c in cs}
    routes = [(r["from"], r["to"], route_boxes(by[r["from"]], by[r["to"]], r.get("via"))) for r in spec.get("relations", [])]
    loi, cb = check_boxes(cs, routes, "lớp")
    cb += check_labels([(f"quan hệ {r['from']}->{r['to']}", r.get("label", ""), pts, None, (r["from"], r["to"]))
                        for r, (_, _, pts) in zip(spec.get("relations", []), routes)], cs)
    for c in cs:
        for s in c.get("attrs", []) + c.get("methods", []):
            if len(s) * 6.6 + 16 > c["_w"]:
                cb.append(f"CẢNH BÁO: dòng quá dài so với hộp '{c['id']}': \"{s[:50]}\" (tăng w hoặc rút gọn)")
    w = max(rect(c)[2] for c in cs) + 200
    h = max(rect(c)[3] for c in cs) + 120
    doc = Doc(spec, w, h)
    body = "rounded=0;html=0;whiteSpace=nowrap;fontSize=12;fillColor=none;strokeColor=none;align=left;verticalAlign=top;spacingLeft=8;spacingTop=5;"
    for c in cs:
        x, y, wd, hh, ah, mh = c["_x"], c["_y"], c["_w"], c["_hh"], c["_ah"], c["_mh"]
        doc.vertex(x, y, wd, c["_h"], "", f"rounded=0;html=0;fillColor=#ffffff;strokeColor={INK};strokeWidth=1.2;", f"cls_{c['id']}")
        safe = c["name"].replace("<", "&lt;").replace(">", "&gt;")
        nm = f"<i>{safe}</i>" if c.get("abstract") else safe
        label = (f"<b>&lt;&lt;{c['stereo']}&gt;&gt;</b><br>" if c.get("stereo") else "") + f"<b>{nm}</b>"
        if c.get("sub"):
            label += f"<br><font color='#475569' style='font-size:11px'>{c['sub']}</font>"
        doc.vertex(x, y, wd, hh, label, "rounded=0;html=1;whiteSpace=wrap;fontSize=13;fillColor=none;strokeColor=none;align=center;verticalAlign=middle;", f"cls_{c['id']}_h")
        doc.vertex(x, y + hh, wd, ah, "\n".join(c.get("attrs", [])), body, f"cls_{c['id']}_a")
        doc.vertex(x, y + hh, wd, 1, "", f"rounded=0;html=0;fillColor={SEP};strokeColor=none;")
        if c.get("methods"):
            doc.vertex(x, y + hh + ah, wd, 1, "", f"rounded=0;html=0;fillColor={SEP};strokeColor=none;")
            doc.vertex(x, y + hh + ah, wd, mh, "\n".join(c["methods"]), body, f"cls_{c['id']}_m")
    for k, (r, (_, _, pts)) in enumerate(zip(spec.get("relations", []), routes), 1):
        extra, dashed = CLASS_KINDS[r.get("kind", "assoc")]
        doc.edge(pts, r.get("label", ""), INK, extra, dashed, eid=f"rel_{k}",
                 src=f"cls_{r['from']}", dst=f"cls_{r['to']}", ra=rect(by[r["from"]]), rb=rect(by[r["to"]]))
    return doc, loi, cb


# ----------------------------------------------------------------------------------------------- ERD
def run_erd(spec):
    """Quan hệ khai báo THEO CỘT: from/from_col là cột khóa chính (phía một), to/to_col là cột khóa ngoại (phía nhiều).
    to_col có thể là danh sách: mỗi cột khóa ngoại một đường về cùng một cột khóa chính."""
    ts = spec["tables"]
    ids = [t["id"] for t in ts]
    by = {t["id"]: t for t in ts}
    loi = [f"LỖI: quan hệ trỏ tới bảng không có: '{r[k]}'" for r in spec.get("relations", []) for k in ("from", "to") if r[k] not in ids]
    if not loi:
        def cols(tid):
            return [c[0] for c in by[tid]["columns"]]
        for r in spec.get("relations", []):
            if "from_col" not in r or "to_col" not in r:
                loi.append(f"LỖI: quan hệ '{r['from']}' -> '{r['to']}' thiếu from_col hoặc to_col (ERD phải nối đúng cột khóa chính với cột khóa ngoại)")
                continue
            if r["from_col"] not in cols(r["from"]):
                loi.append(f"LỖI: bảng '{r['from']}' không có cột '{r['from_col']}'")
            for c in (r["to_col"] if isinstance(r["to_col"], list) else [r["to_col"]]):
                if c not in cols(r["to"]):
                    loi.append(f"LỖI: bảng '{r['to']}' không có cột '{c}'")
    if loi:
        return None, loi, []
    row, head = 26, 36
    for t in ts:
        t["_w"] = t.get("w") or max(300, int(max(len(c[0]) + len(c[1]) for c in t["columns"]) * 8 + 90))
        t["_h"] = head + row * len(t["columns"])
    stack_columns(ts, gap_x=200, gap_y=60)

    def cell_rect(tid, col_name, side):
        """Hình chữ nhật của ô ở đầu trái (side 'l') hoặc đầu phải (side 'r') của hàng chứa cột col_name."""
        t = by[tid]
        i = [c[0] for c in t["columns"]].index(col_name)
        cw0, cw1 = int(t["_w"] * .5), int(t["_w"] * .3)
        y1 = t["_y"] + head + i * row
        if side == "l":
            return (t["_x"], y1, t["_x"] + cw0, y1 + row), f"tbl_{tid}_{i}_0"
        return (t["_x"] + cw0 + cw1, y1, t["_x"] + t["_w"], y1 + row), f"tbl_{tid}_{i}_2"

    edges, routes = [], []
    # Mỗi quan hệ một đường dọc RIÊNG: mọi quan hệ đi qua cùng một khe giữa hai cột bảng (bất kể chiều) được dàn cách nhau 40 điểm,
    # để hai quan hệ khác nhau không bao giờ dùng chung một đoạn dọc (người xem sẽ tưởng cùng một quan hệ).
    nhom = {}
    for r in spec.get("relations", []):
        ra_, rb_ = rect(by[r["from"]]), rect(by[r["to"]])
        trai_ = ra_[2] <= rb_[0]
        khe = (ra_[2], rb_[0]) if trai_ else (rb_[2], ra_[0])
        nhom.setdefault(khe, []).append(r)
    # quan hệ có bảng khóa chính ở BÊN TRÁI lấy đường dọc bên trái, bên phải lấy bên phải: hai đoạn ngang cùng hàng không chạm nhau
    lech = {}
    for rs in nhom.values():
        rs.sort(key=lambda r: 0 if rect(by[r["from"]])[2] <= rect(by[r["to"]])[0] else 1)
        for i, r in enumerate(rs):
            lech[id(r)] = (i - (len(rs) - 1) / 2) * 40
    for r in spec.get("relations", []):
        a, b = by[r["from"]], by[r["to"]]
        a_left_of_b = rect(a)[2] <= rect(b)[0]
        b_left_of_a = rect(b)[2] <= rect(a)[0]
        if not (a_left_of_b or b_left_of_a):
            loi.append(f"LỖI: bảng '{r['from']}' và '{r['to']}' chồng nhau theo chiều ngang; đặt ở hai cột khác nhau")
            continue
        fk_cols = r["to_col"] if isinstance(r["to_col"], list) else [r["to_col"]]
        for n, fk in enumerate(fk_cols):
            sa, sb = ("r", "l") if a_left_of_b else ("l", "r")
            ra, ida = cell_rect(r["from"], r["from_col"], sa)
            rb, idb = cell_rect(r["to"], fk, sb)
            xa = ra[2] if sa == "r" else ra[0]
            xb = rb[0] if sb == "l" else rb[2]
            ya, yb = (ra[1] + ra[3]) // 2, (rb[1] + rb[3]) // 2
            xm = int((xa + xb) // 2 + lech[id(r)])
            pts = [(xa, ya), (xb, yb)] if ya == yb else [(xa, ya), (xm, ya), (xm, yb), (xb, yb)]
            label = r.get("label", "") if n == len(fk_cols) // 2 else ""
            edges.append((pts, label, ida, idb, ra, rb))
            routes.append((r["from"], r["to"], pts))
    if loi:
        return None, loi, []
    l2, cb = check_boxes(ts, routes, "bảng")
    loi += l2
    cb += check_shared_segments([(f"{a}>{b}", f"quan hệ {a}->{b}", pts) for a, b, pts in routes])
    cb += check_labels([(f"quan hệ {a}->{b}", lab, pts, None, (a, b)) for (a, b, pts), (_, lab, _, _, _, _) in zip(routes, edges)], ts)
    doc = Doc(spec, max(rect(t)[2] for t in ts) + 200, max(rect(t)[3] for t in ts) + 120)
    plain = spec.get("plain", True)  # mặc định đen trắng; "plain": false để tô màu theo bảng
    cell = "rounded=0;html=0;fontSize=12;strokeColor=#cbd5e1;align=left;spacingLeft=6;whiteSpace=nowrap;"
    for t in ts:
        fill, stroke = ("#f2f2f2", INK) if plain else PAL.get(t.get("color", "blue"), PAL["blue"])
        doc.vertex(t["_x"], t["_y"], t["_w"], head, t["name"],
                   f"rounded=0;html=0;fontStyle=1;fontSize=14;fillColor={fill};strokeColor={stroke};", f"tbl_{t['id']}")
        cw = [int(t["_w"] * .5), int(t["_w"] * .3)]
        cw.append(t["_w"] - cw[0] - cw[1])
        yy = t["_y"] + head
        for ri, (name, typ, key) in enumerate(t["columns"]):
            hot = name in t.get("hot", [])
            for i, txt in enumerate((name, typ, key)):
                st = cell + f"fillColor={('#e5e5e5' if plain else '#ffe4cc') if hot else '#ffffff'};"
                if key == "PK" or hot:
                    st += "fontStyle=1;"
                if hot and not plain:
                    st += "fontColor=#b45309;"
                elif i == 2 and not plain:
                    st += "fontColor=#6b21a8;"
                doc.vertex(t["_x"] + sum(cw[:i]), yy, cw[i], row, txt, st, f"tbl_{t['id']}_{ri}_{i}")
            yy += row
    # đường có nhãn vẽ SAU CÙNG để các đường chung trục không đè lên chữ
    for k, (pts, label, ida, idb, ra, rb) in sorted(enumerate(edges, 1), key=lambda t: bool(t[1][1])):
        doc.edge(pts, label, "#1f2937", "startArrow=ERmandOne;startFill=0;endArrow=ERmany;endFill=0;", eid=f"rel_{k}",
                 src=ida, dst=idb, ra=ra, rb=rb)
    return doc, loi, cb




# ----------------------------------------------------------------------------------------------- FLOW
def flow_route(a, b, e):
    """Đường đi của một cạnh giữa hai nút (dùng chung cho flow, swimlane, activity).
    via: đường vòng thẳng đứng tại x đó; first='v': đi dọc trước rồi rẽ ngang; còn lại thẳng hoặc gấp một khúc."""
    ax1, ay1, ax2, ay2 = rect(a)
    bx1, by1, bx2, by2 = rect(b)
    acx, acy, bcx, bcy = (ax1 + ax2) // 2, (ay1 + ay2) // 2, (bx1 + bx2) // 2, (by1 + by2) // 2
    if "via" in e:
        v = e["via"]
        yin = bcy + e.get("yin", 0)  # yin: dời điểm vào dọc cạnh bên của đích để nhiều đường cùng đích không chồng lên nhau
        return [(ax2 if v >= acx else ax1, acy), (v, acy), (v, yin), (bx2 if v >= bcx else bx1, yin)]
    if e.get("first") == "v" and abs(acx - bcx) >= 5:
        # đi dọc trước rồi mới rẽ ngang vào cạnh bên của đích (nút nhánh phụ gộp vào luồng chính)
        return [(acx, ay2 if bcy > acy else ay1), (acx, bcy), (bx2 if acx > bcx else bx1, bcy)]
    if abs(acx - bcx) < 5:
        return [(acx, ay2), (bcx, by1)] if bcy > acy else [(acx, ay1), (bcx, by2)]
    if abs(acy - bcy) < 5:
        return [(ax2, acy), (bx1, bcy)] if bcx > acx else [(ax1, acy), (bx2, bcy)]
    return [(ax2 if bcx > acx else ax1, acy), (bcx, acy), (bcx, by1 if bcy > acy else by2)]


def run_flow(spec):
    ns, es = spec["nodes"], spec.get("edges", [])
    ids = [n["id"] for n in ns]
    lanes = spec.get("lanes") or []
    lane_idx = {ln["id"]: i for i, ln in enumerate(lanes)}
    loi = [f"LỖI: cạnh trỏ tới nút không có: '{e[k]}'" for e in es for k in ("from", "to") if e[k] not in ids]
    if spec.get("type") == "swimlane" and not lanes:
        loi.append("LỖI: type swimlane cần trường `lanes` (danh sách làn: id, name, color)")
    if lanes:
        for n in ns:
            if n.get("lane") not in lane_idx:
                loi.append(f"LỖI: nút '{n['id']}' thiếu `lane` hoặc lane không có trong `lanes`: '{n.get('lane')}'")
            else:
                n["col"] = lane_idx[n["lane"]]
    kinds = {"start", "end", "proc", "dec", "ok", "err", "ex", "junc"}
    loi += [f"LỖI: nút '{n['id']}' có kind không hợp lệ '{n.get('kind')}' (dùng: {', '.join(sorted(kinds))})" for n in ns if n.get("kind") not in kinds]
    if loi:
        return None, loi, []
    starts = [n for n in ns if n["kind"] == "start"]
    ends = [n for n in ns if n["kind"] == "end"]
    if len(starts) != 1:
        loi.append(f"LỖI: cần ĐÚNG 1 điểm bắt đầu, đang có {len(starts)}")
    if len(ends) != 1:
        loi.append(f"LỖI: cần ĐÚNG 1 điểm kết thúc, đang có {len(ends)}")
    cb = []
    lane_w = 520
    colx = tuple(MARGIN + i * lane_w + lane_w // 2 for i in range(len(lanes))) if lanes else (380, 860, 1340, 1820)
    y0 = 210 if lanes else 130  # có làn bơi thì chừa chỗ cho dòng tiêu đề làn
    for n in ns:
        k = n["kind"]
        n["_w"], n["_h"] = {"start": (30, 30), "end": (30, 30), "junc": (22, 22), "dec": (380, 110)}.get(k, (360, 90))
        cx = n.get("x") if "x" in n else colx[min(n.get("col", 0), len(colx) - 1)]
        cy = n.get("y") if "y" in n else y0 + int(n.get("row", 0) * 125)
        n["_x"], n["_y"] = cx - n["_w"] // 2, cy - n["_h"] // 2
        if k in ("proc", "ok", "err", "ex", "dec") and not n.get("label"):
            loi.append(f"LỖI: nút '{n['id']}' thiếu label")
    by = {n["id"]: n for n in ns}
    out = {}
    for e in es:
        out.setdefault(e["from"], []).append(e)
    for n in ns:
        if n["kind"] == "dec":
            outs = out.get(n["id"], [])
            if len(outs) < 2:
                loi.append(f"LỖI: nút quyết định '{n['id']}' chỉ có {len(outs)} nhánh ra (cần ít nhất 2)")
            for e in outs:
                if not e.get("label"):
                    loi.append(f"LỖI: nhánh ra từ '{n['id']}' sang '{e['to']}' chưa có nhãn (Có, Không...)")
        if n["kind"] != "end" and not out.get(n["id"]):
            loi.append(f"LỖI: nút '{n['id']}' không có cạnh đi ra (mọi nhánh phải về điểm kết thúc)")
    if starts:
        seen, stack = set(), [starts[0]["id"]]
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            stack += [e["to"] for e in out.get(cur, [])]
        for n in ns:
            if n["id"] not in seen:
                loi.append(f"LỖI: nút '{n['id']}' không với tới được từ điểm bắt đầu")
        if ends and ends[0]["id"] not in seen:
            loi.append("LỖI: điểm kết thúc không với tới được từ điểm bắt đầu")
    routes = [(e["from"], e["to"], flow_route(by[e["from"]], by[e["to"]], e)) for e in es]
    l2, c2 = check_boxes(ns, routes, "nút")
    loi += l2
    cb += c2
    doc = Doc(spec, max(max(rect(n)[2] for n in ns) + 340, MARGIN + len(lanes) * lane_w + 100),
              max(rect(n)[3] for n in ns) + 120)
    bottom = max(rect(n)[3] for n in ns) + 60
    for i, ln in enumerate(lanes):
        fill, stroke = PAL.get(ln.get("color", "gray"), PAL["gray"])
        lx = MARGIN + i * lane_w
        doc.vertex(lx, 130, lane_w, bottom - 130, "", f"rounded=0;fillColor=none;strokeColor={stroke};strokeWidth=1.5;")
        doc.vertex(lx, 130, lane_w, 44, ln.get("name", ln["id"]),
                   f"rounded=0;fillColor={fill};strokeColor={stroke};fontStyle=1;fontSize=13;whiteSpace=wrap;html=0;")
    styles = {"proc": "rounded=1;arcSize=12;fillColor=#ede9fe;strokeColor=#7c3aed;", "ok": "rounded=1;arcSize=12;fillColor=#dcfce7;strokeColor=#16a34a;",
              "err": "rounded=1;arcSize=12;fillColor=#fee2e2;strokeColor=#dc2626;fontColor=#991b1b;",
              "ex": "rounded=1;arcSize=12;fillColor=#fee2e2;strokeColor=#dc2626;fontColor=#991b1b;",
              "dec": "rhombus;fillColor=#fff7ed;strokeColor=#ea580c;"}
    for n in ns:
        k = n["kind"]
        nid = f"node_{n['id']}"
        if k == "start":
            doc.vertex(n["_x"], n["_y"], 30, 30, "", "ellipse;fillColor=#0f172a;strokeColor=#0f172a;", nid)
        elif k == "end":
            doc.vertex(n["_x"], n["_y"], 30, 30, "", "ellipse;shape=endState;fillColor=#0f172a;strokeColor=#0f172a;", nid)
        elif k == "junc":
            doc.vertex(n["_x"], n["_y"], 22, 22, "", "ellipse;fillColor=#ffffff;strokeColor=#475569;", nid)
        else:
            doc.vertex(n["_x"], n["_y"], n["_w"], n["_h"], n["label"],
                       styles[k] + ("whiteSpace=wrap;html=0;fontSize=12;fontColor=#0f172a;" if k not in ("err", "ex") else "whiteSpace=wrap;html=0;fontSize=12;"), nid)
    for k, (e, (_, _, pts)) in enumerate(zip(es, routes), 1):
        doc.edge(pts, e.get("label", ""), COLORS.get(e.get("color"), INK), "", e.get("dashed", False), eid=f"edge_{k}",
                 src=f"node_{e['from']}", dst=f"node_{e['to']}", ra=rect(by[e["from"]]), rb=rect(by[e["to"]]))
    return doc, loi, cb


# ----------------------------------------------------------------------------------------------- ACTIVITY
ACT_COL_W, ACT_NODE_W, ACT_ROW_H, ACT_PAD = 330, 250, 115, 25


def run_activity(spec):
    """Sơ đồ hoạt động theo MẪU anhbv (UML Activity, đen trắng): mỗi làn là MỘT LỚP hoặc THÀNH PHẦN (không phải vai người dùng).
    Cho phép nhiều điểm bắt đầu và nhiều điểm kết thúc (mỗi làn có điểm vào riêng khi nó chạy độc lập). Mũi tên liền trong làn,
    nét đứt khi sang làn khác (lời gọi, message). Nhánh quyết định ghi điều kiện trong ngoặc vuông [Có], [Không]."""
    lanes, ns, es = spec.get("lanes", []), spec["nodes"], spec.get("edges", [])
    ids = [n["id"] for n in ns]
    lane_idx = {ln["id"]: i for i, ln in enumerate(lanes)}
    loi = [f"LỖI: cạnh trỏ tới nút không có: '{e[k]}'" for e in es for k in ("from", "to") if e[k] not in ids]
    if not lanes:
        loi.append("LỖI: type activity cần trường `lanes` (mỗi làn một lớp hoặc thành phần: id, name)")
    kinds = {"start", "end", "proc", "dec", "junc", "err"}
    for n in ns:
        if n.get("lane") not in lane_idx:
            loi.append(f"LỖI: nút '{n['id']}' thiếu `lane` hoặc lane không có trong `lanes`: '{n.get('lane')}'")
        if n.get("kind") not in kinds:
            loi.append(f"LỖI: nút '{n['id']}' có kind không hợp lệ '{n.get('kind')}' (dùng: {', '.join(sorted(kinds))})")
        elif n["kind"] in ("proc", "dec", "err") and not n.get("label"):
            loi.append(f"LỖI: nút '{n['id']}' thiếu label")
    if loi:
        return None, loi, []
    by = {n["id"]: n for n in ns}
    out, inc = {}, {}
    for e in es:
        out.setdefault(e["from"], []).append(e)
        inc.setdefault(e["to"], []).append(e)
    starts = [n for n in ns if n["kind"] == "start"]
    ends = [n for n in ns if n["kind"] == "end"]
    if not starts:
        loi.append("LỖI: cần ít nhất 1 điểm bắt đầu")
    if not ends:
        loi.append("LỖI: cần ít nhất 1 điểm kết thúc")
    for n in starts:
        if inc.get(n["id"]):
            loi.append(f"LỖI: điểm bắt đầu '{n['id']}' không được có cạnh đi vào")
    for n in ns:
        if n["kind"] == "end" and out.get(n["id"]):
            loi.append(f"LỖI: điểm kết thúc '{n['id']}' không được có cạnh đi ra")
        if n["kind"] != "end" and not out.get(n["id"]):
            loi.append(f"LỖI: nút '{n['id']}' không có cạnh đi ra (mọi nhánh phải tới một điểm kết thúc)")
        if n["kind"] == "dec":
            outs = out.get(n["id"], [])
            if len(outs) < 2:
                loi.append(f"LỖI: nút quyết định '{n['id']}' chỉ có {len(outs)} nhánh ra (cần ít nhất 2)")
            loi += [f"LỖI: nhánh ra từ '{n['id']}' sang '{e['to']}' chưa có điều kiện (ví dụ [Có], [Không])" for e in outs if not e.get("label")]
    reach = set()
    stack = [n["id"] for n in starts]
    while stack:
        cur = stack.pop()
        if cur in reach:
            continue
        reach.add(cur)
        stack += [e["to"] for e in out.get(cur, [])]
    loi += [f"LỖI: nút '{n['id']}' không với tới được từ điểm bắt đầu nào" for n in ns if n["id"] not in reach]
    # mỗi điểm bắt đầu phải tới được ít nhất một điểm kết thúc
    for s in starts:
        seen, st = set(), [s["id"]]
        while st:
            cur = st.pop()
            if cur in seen:
                continue
            seen.add(cur)
            st += [e["to"] for e in out.get(cur, [])]
        if not any(n["id"] in seen for n in ends):
            loi.append(f"LỖI: điểm bắt đầu '{s['id']}' không tới được điểm kết thúc nào")
    # bố cục: mỗi làn có nhiều cột con (sub); độ rộng làn theo số cột con
    nsub = [1 + max([n.get("sub", 0) for n in ns if n["lane"] == ln["id"]] or [0]) for ln in lanes]
    lane_x, x = [], MARGIN
    for k in nsub:
        lane_x.append(x)
        x += k * ACT_COL_W + 2 * ACT_PAD - 20
    total_w = x - MARGIN
    y0 = 190
    cb = []
    for n in ns:
        k = n["kind"]
        li = lane_idx[n["lane"]]
        if k in ("start", "end"):
            n["_w"], n["_h"] = 30, 30
        elif k == "junc":
            n["_w"], n["_h"] = 22, 22
        elif k == "dec":
            n["_w"], n["_h"] = ACT_NODE_W + 20, 90
        else:
            n["_w"] = ACT_NODE_W
            n["_h"] = max(64, 24 + 18 * -(-len(n["label"]) // 32))
        cx = n["x"] if "x" in n else lane_x[li] + ACT_PAD + n.get("sub", 0) * ACT_COL_W + ACT_COL_W // 2 - 10
        cy = n["y"] if "y" in n else y0 + int(n.get("row", 0) * ACT_ROW_H)
        n["_x"], n["_y"] = cx - n["_w"] // 2, cy - n["_h"] // 2
        if k == "dec" and len(n["label"]) > 60:
            cb.append(f"CẢNH BÁO: nhãn nút quyết định '{n['id']}' dài ({len(n['label'])} ký tự), chữ có thể tràn hình thoi; rút gọn")
        if k in ("proc", "err") and len(n["label"]) > 120:
            cb.append(f"CẢNH BÁO: nhãn nút '{n['id']}' quá dài ({len(n['label'])} ký tự); tách thành hai bước")
    routes = []
    for e in es:
        a, b = by[e["from"]], by[e["to"]]
        e["_cross"] = a["lane"] != b["lane"]
        routes.append((e["from"], e["to"], flow_route(a, b, e)))
        if e["_cross"] and not e.get("label"):
            cb.append(f"CẢNH BÁO: cạnh liên làn '{e['from']}' -> '{e['to']}' chưa có nhãn (ghi: gọi, publish, trả về...)")
    notes = [{"id": f"ghichu_{n['id']}", "_x": n["_x"] - 100, "_y": n["_y"] + 34, "_w": 230, "_h": 36} for n in ns if n["kind"] == "end" and n.get("note")]
    l2, c2 = check_boxes(ns + notes, routes, "nút")
    loi += l2
    cb += c2
    cb += check_edge_overlap(routes)
    act_labels = []
    for e, (_, _, pts) in zip(es, routes):
        lab = e.get("label", "")
        if lab and by[e["from"]]["kind"] == "dec" and not lab.startswith("["):
            lab = f"[{lab}]"
        seg = [abs(q[0] - p[0]) + abs(q[1] - p[1]) for p, q in zip(pts, pts[1:])]
        tong = max(sum(seg), 1)
        lab_x = 2 * min(seg[0] / 2, 90 + len(lab) * 3) / tong - 1 if lab and len(pts) > 2 else None  # nhãn nằm sát nút nguồn
        act_labels.append((lab, lab_x))
    cb += check_labels([(f"cạnh {e['from']}->{e['to']}", lab, pts, lx, (e["from"], e["to"]))
                        for e, (_, _, pts), (lab, lx) in zip(es, routes, act_labels)], ns + notes)
    bottom = max(rect(n)[3] for n in ns) + 70
    legend_h = 250 if spec.get("legend", True) else 0
    doc = Doc(spec, total_w + 2 * MARGIN, bottom + legend_h + 60)
    top = 100
    for i, ln in enumerate(lanes):
        w = nsub[i] * ACT_COL_W + 2 * ACT_PAD - 20
        doc.vertex(lane_x[i], top, w, bottom - top, "", f"rounded=0;fillColor=none;strokeColor={INK};strokeWidth=1.2;")
        doc.vertex(lane_x[i], top, w, 50, ln.get("name", ln["id"]), f"rounded=0;fillColor=#f2f2f2;strokeColor={INK};fontStyle=1;fontSize=13;whiteSpace=wrap;html=0;")
    styles = {"proc": "rounded=1;arcSize=25;fillColor=#ffffff;strokeColor=#1f1f1f;", "err": "rounded=1;arcSize=25;fillColor=#ffffff;strokeColor=#1f1f1f;strokeWidth=2.5;",
              "dec": "rhombus;fillColor=#ffffff;strokeColor=#1f1f1f;"}
    for n in ns:
        k, nid = n["kind"], f"node_{n['id']}"
        if k == "start":
            doc.vertex(n["_x"], n["_y"], 30, 30, "", "ellipse;fillColor=#000000;strokeColor=#000000;", nid)
        elif k == "end":
            doc.vertex(n["_x"], n["_y"], 30, 30, "", "ellipse;shape=endState;fillColor=#000000;strokeColor=#000000;", nid)
            if n.get("note"):
                doc.vertex(n["_x"] - 100, n["_y"] + 34, 230, 36, n["note"], "text;html=0;whiteSpace=wrap;fontSize=11;fontStyle=2;align=center;verticalAlign=top;")
        elif k == "junc":
            doc.vertex(n["_x"], n["_y"], 22, 22, "", "ellipse;fillColor=#ffffff;strokeColor=#1f1f1f;", nid)
        else:
            doc.vertex(n["_x"], n["_y"], n["_w"], n["_h"], n["label"], styles[k] + "whiteSpace=wrap;html=0;fontSize=12;fontColor=#000000;", nid)
    for k, (e, (_, _, pts), (lab, lab_x)) in enumerate(zip(es, routes, act_labels), 1):
        doc.edge(pts, lab, INK, "", e["_cross"] or e.get("dashed", False), eid=f"edge_{k}",
                 src=f"node_{e['from']}", dst=f"node_{e['to']}", ra=rect(by[e["from"]]), rb=rect(by[e["to"]]), lab_x=lab_x)
    if spec.get("legend", True):
        ly = bottom + 30
        doc.vertex(MARGIN, ly, 520, legend_h - 20, "", f"rounded=0;fillColor=none;strokeColor={SEP};")
        doc.vertex(MARGIN + 12, ly + 6, 300, 22, "Chú giải (UML Activity)", "text;html=0;fontStyle=1;fontSize=12;align=left;")
        rows = [("Nút bắt đầu (initial node)", "start"), ("Nút kết thúc (activity final node)", "end"), ("Hành động (action)", "proc"),
                ("Rẽ nhánh (decision), điều kiện dạng [guard] trên cạnh ra", "dec"), ("Luồng điều khiển trong một làn", "line"),
                ("Lời gọi hoặc message sang làn khác", "dash")]
        for i, (txt, sym) in enumerate(rows):
            yy = ly + 36 + i * 32
            if sym == "start":
                doc.vertex(MARGIN + 24, yy + 2, 20, 20, "", "ellipse;fillColor=#000000;strokeColor=#000000;")
            elif sym == "end":
                doc.vertex(MARGIN + 24, yy + 2, 20, 20, "", "ellipse;shape=endState;fillColor=#000000;strokeColor=#000000;")
            elif sym == "proc":
                doc.vertex(MARGIN + 16, yy + 2, 44, 20, "", "rounded=1;arcSize=25;fillColor=#ffffff;strokeColor=#1f1f1f;")
            elif sym == "dec":
                doc.vertex(MARGIN + 22, yy, 28, 24, "", "rhombus;fillColor=#ffffff;strokeColor=#1f1f1f;")
            else:
                doc.edge([(MARGIN + 14, yy + 12), (MARGIN + 62, yy + 12)], "", INK, "", sym == "dash")
            doc.vertex(MARGIN + 80, yy, 430, 24, txt, "text;html=0;fontSize=11;align=left;verticalAlign=middle;")
    return doc, loi, cb


# ----------------------------------------------------------------------------------------------- USE CASE
def run_usecase(spec):
    """Sơ đồ use case UML (đen trắng). Tác nhân ĐẶT TÊN THEO VAI THẬT (Kế toán, CSKH...), không đặt "User".
    JSON giống file `.usecase.json` cũ của workspace: usecases [{id,label}], actors [{id,label,side,near}], links [[actor,usecase]],
    relations [{from,to,type: include|extend}]. include: from gọi to (mũi tên từ from sang to); extend: from mở rộng to."""
    ucs, acts = spec["usecases"], spec["actors"]
    uid, aid = {u["id"] for u in ucs}, {a["id"] for a in acts}
    links, rels = spec.get("links", []), spec.get("relations", [])
    loi = [f"LỖI: liên kết trỏ tới tác nhân hoặc use case không có: {l}" for l in links if l[0] not in aid or l[1] not in uid]
    loi += [f"LỖI: quan hệ trỏ tới use case không có: '{r['from']}' -> '{r['to']}'" for r in rels if r["from"] not in uid or r["to"] not in uid]
    loi += [f"LỖI: quan hệ '{r['from']}' -> '{r['to']}' có type '{r.get('type')}' không hợp lệ (include hoặc extend)" for r in rels if r.get("type") not in ("include", "extend")]
    if loi:
        return None, loi, []
    cb = []
    gens = spec.get("generalizations", [])
    loi += [f"LỖI: kế thừa tác nhân trỏ tới tác nhân không có: {g}" for g in gens if g[0] not in aid or g[1] not in aid]
    in_gen = {x for g in gens for x in g}
    for a in acts:
        if not any(l[0] == a["id"] for l in links) and a["id"] not in in_gen:
            loi.append(f"LỖI: tác nhân '{a['id']}' không nối với use case nào")
        if a["label"].strip().lower() in ("user", "người dùng", "nguoi dung", "actor"):
            cb.append(f"CẢNH BÁO: tác nhân '{a['id']}' đặt tên chung chung '{a['label']}'; dùng tên vai thật (Kế toán, CSKH, Telesale, Nhân viên kho, Quản trị viên...) hoặc 'Người dùng hệ thống' làm tác nhân tổng quát có chủ đích")
    touched = {l[1] for l in links} | {r["from"] for r in rels} | {r["to"] for r in rels}
    cb += [f"CẢNH BÁO: use case '{u['id']}' không nối với tác nhân hay use case nào" for u in ucs if u["id"] not in touched]
    # include và extend không được tạo vòng
    graph = {}
    for r in rels:
        graph.setdefault(r["from"], []).append(r["to"])
    def co_vong(n, path):
        return n in path or any(co_vong(m, path | {n}) for m in graph.get(n, []))
    if any(co_vong(u["id"], set()) for u in ucs):
        loi.append("LỖI: quan hệ include/extend tạo vòng")
    COL, ROW0, RH, LEFT, RIGHT = 470, 150, 74, 120, 900
    if gens:                                   # tác nhân con kế thừa tác nhân cha: chừa một cột bên trái cho các tác nhân con
        COL, LEFT, RIGHT = COL + 190, LEFT + 190, RIGHT + 190
    pos = {u["id"]: ROW0 + i * RH for i, u in enumerate(ucs)}
    linked = {}
    for a_, u in links:
        linked.setdefault(a_, []).append(pos[u])
    children, child_set = {}, {g[0] for g in gens}
    for c, par in gens:
        children.setdefault(par, []).append(c)
    ay = {}
    for a in acts:
        if a["id"] in child_set:
            continue
        ys = linked.get(a["id"]) or [pos.get(a.get("near"), ROW0)]
        ay[a["id"]] = a.get("y") or sum(ys) / len(ys)
    for sd in ("left", "right"):          # giãn các tác nhân cùng bên, tối thiểu 130
        ids = sorted([a["id"] for a in acts if a["id"] not in child_set and (a.get("side") == "left") == (sd == "left")], key=lambda i: ay[i])
        for i in range(1, len(ids)):
            ay[ids[i]] = max(ay[ids[i]], ay[ids[i - 1]] + 130)
    for par, kids in children.items():    # các tác nhân con xếp dọc quanh tác nhân cha
        for i, c in enumerate(kids):
            ay[c] = ay[par] + (i - (len(kids) - 1) / 2) * 130
    side = {a["id"]: a.get("side") for a in acts}
    doc = Doc(spec, RIGHT + 260, int(max(ROW0 + len(ucs) * RH + 100, max(ay.values(), default=0) + 170)))
    E = 140                                     # nửa chiều rộng hình elip use case (chữ có chỗ, không chạm viền)
    sys_w = 2 * E + 120 + 44 * max(len(rels) - 1, 0) + 40
    doc.vertex(COL - E - 50, ROW0 - 50, sys_w, len(ucs) * RH + 20, "", f"rounded=0;fillColor=none;strokeColor={INK};strokeWidth=1.5;", "system")
    doc.vertex(COL - E - 50, ROW0 - 78, sys_w, 24, spec.get("system", "Hệ thống"), "text;html=0;fontStyle=1;fontSize=13;align=center;")
    for u in ucs:
        doc.vertex(COL - E, pos[u["id"]] - 31, 2 * E, 62, u["label"], f"ellipse;whiteSpace=wrap;html=0;fontSize=12;fillColor=#ffffff;strokeColor={INK};strokeWidth=1.2;", f"uc_{u['id']}")
    actor_x = {}
    for a in acts:
        actor_x[a["id"]] = LEFT - 220 if a["id"] in child_set else (LEFT if a.get("side") == "left" else RIGHT)
        doc.vertex(actor_x[a["id"]] - 20, ay[a["id"]] - 40, 40, 70, a["label"],
                   f"shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=0;fontStyle=1;fontSize=12;strokeColor={INK};strokeWidth=1.5;whiteSpace=wrap;", f"actor_{a['id']}")
    for k, (c, par) in enumerate(gens, 1):   # kế thừa tác nhân: nét liền, tam giác rỗng ở phía tác nhân cha
        doc.edge([(actor_x[c] + 20, ay[c] - 5), (actor_x[par] - 20, ay[par] - 5)], "", INK, "endArrow=block;endFill=0;endSize=12;", False, eid=f"gen_{k}")
    for k, (a_, u) in enumerate(links, 1):
        left = side[a_] == "left"
        ax = LEFT + 20 if left else RIGHT - 20
        doc.edge([(ax, ay[a_] - 5), (COL - E if left else COL + E, pos[u])], "", INK, "endArrow=none;", False, eid=f"link_{k}")
    boxes = [{"id": u["id"], "_x": COL - E, "_y": pos[u["id"]] - 31, "_w": 2 * E, "_h": 62} for u in ucs]
    rroutes = []
    rank = {k: i for i, k in enumerate(sorted(range(len(rels)), key=lambda k: abs(pos[rels[k]["to"]] - pos[rels[k]["from"]])))}  # đường ngắn dùng rãnh gần, đường dài rãnh xa
    ends = {}                                    # mỗi đầu mút một độ cao riêng trên viền elip, để các mũi tên không chồng nhau
    for r in rels:
        for u in (r["from"], r["to"]):
            ends[u] = ends.get(u, 0) + 1
    used = {}

    def attach(u):
        i = used.get(u, 0)
        used[u] = i + 1
        dy = (i - (ends[u] - 1) / 2) * 14
        return int(COL + E * (1 - (dy / 31) ** 2) ** 0.5), pos[u] + int(dy)
    for k, r in enumerate(rels):
        xv = COL + E + 40 + 44 * rank[k]     # mỗi quan hệ một đường dọc riêng, không dùng chung
        (xa, ya), (xb, yb) = attach(r["from"]), attach(r["to"])
        rroutes.append((r["from"], r["to"], [(xa, ya), (xv, ya), (xv, yb), (xb, yb)]))
    cb += check_edge_overlap(rroutes)
    # đặt nhãn «include»/«extend» ở chỗ không đè đường khác (thử vài vị trí dọc đường)
    labs = []
    for k, (r, (_, _, pts)) in enumerate(zip(rels, rroutes)):
        txt = "\u00abinclude\u00bb" if r["type"] == "include" else "\u00abextend\u00bb"
        best, bw = None, 10 ** 9
        for lx in (0, -0.3, 0.3, -0.5, 0.5, -0.15, 0.15):
            cx, cy = label_pos(pts, lx)
            w = len(txt) * 6.6 + 8
            rc = (cx - w / 2, cy - 9, cx + w / 2, cy + 9)
            hit = sum(1 for j, (_, _, p2) in enumerate(rroutes) if j != k and any(seg_hits(p, q, rc) for p, q in zip(p2, p2[1:])))
            hit += sum(1 for p, q in zip(pts, pts[1:]) if p[1] == q[1] and abs(p[1] - cy) < 14 and min(p[0], q[0]) < rc[2] and max(p[0], q[0]) > rc[0])
            hit += sum(1 for o in labs if abs(o[0] - cx) < 80 and abs(o[1] - cy) < 18)
            if hit < bw:
                best, bw = (lx, cx, cy), hit
        labs.append((best[1], best[2], best[0]))
        doc.edge(pts, txt, INK, "endArrow=open;endFill=0;", True, eid=f"rel_{k + 1}", lab_x=best[0])
    cb += check_labels([(f"quan hệ {r['from']}->{r['to']}", "\u00abinclude\u00bb" if r["type"] == "include" else "\u00abextend\u00bb", pts, lb[2], ())
                        for r, (_, _, pts), lb in zip(rels, rroutes, labs)], [])
    return doc, loi, cb


# ----------------------------------------------------------------------------------------------- BỐN LOẠI MỚI: trạng thái, thành phần, triển khai, gói
def grid_center(n, colw=300, rowh=130, x0=150, y0=140):
    """Đặt nút theo lưới: col (cột) và row (hàng) là số thực; x, y (nếu có) là tâm tuyệt đối."""
    cx = n["x"] if "x" in n else MARGIN + x0 + int(round(n.get("col", 0) * colw))
    cy = n["y"] if "y" in n else y0 + int(round(n.get("row", 0) * rowh))
    n["_x"], n["_y"] = int(cx - n["_w"] // 2), int(cy - n["_h"] // 2)


def bbox(items, pad_x=40, pad_top=48, pad_bottom=36):
    x1 = min(i["_x"] for i in items) - pad_x
    y1 = min(i["_y"] for i in items) - pad_top
    x2 = max(i["_x"] + i["_w"] for i in items) + pad_x
    y2 = max(i["_y"] + i["_h"] for i in items) + pad_bottom
    return x1, y1, x2, y2


def near_source_labelx(pts, lab):
    seg = [abs(q[0] - p[0]) + abs(q[1] - p[1]) for p, q in zip(pts, pts[1:])]
    tong = max(sum(seg), 1)
    return 2 * min(seg[0] / 2, 90 + len(lab) * 3) / tong - 1 if lab and len(pts) > 2 else None


# ------------------------------------------------------------------ STATE MACHINE
def run_statemachine(spec):
    """Máy trạng thái UML (đen trắng). Trạng thái: hộp bo góc có tên và (tùy chọn) các hoạt động trong (entry/do/exit).
    Chuyển: mũi tên nhãn `sự_kiện [điều_kiện] / hành_động`. initial: chấm đen; final: chấm đôi; choice: hình thoi.
    Trạng thái ghép (composite): đặt `parent` cho các trạng thái con; khung bao tự dựng quanh các con."""
    sts, trs = spec["states"], spec.get("transitions", [])
    byid = {}
    loi = []
    for s in sts:
        if s["id"] in byid:
            loi.append(f"LỖI: id trạng thái trùng: '{s['id']}'")
        byid[s["id"]] = s
        s.setdefault("kind", "state")
        if s["kind"] not in ("state", "initial", "final", "choice"):
            loi.append(f"LỖI: trạng thái '{s['id']}' có kind không hợp lệ '{s['kind']}' (state, initial, final, choice)")
        if s["kind"] == "state" and not s.get("label"):
            loi.append(f"LỖI: trạng thái '{s['id']}' thiếu label")
    for s in sts:
        if s.get("parent") and s["parent"] not in byid:
            loi.append(f"LỖI: trạng thái '{s['id']}' có parent không có: '{s['parent']}'")
    loi += [f"LỖI: chuyển trỏ tới trạng thái không có: '{t[k]}'" for t in trs for k in ("from", "to") if t[k] not in byid]
    if loi:
        return None, loi, []
    kids = {}
    for s in sts:
        if s.get("parent"):
            kids.setdefault(s["parent"], []).append(s)
    for p in kids:
        byid[p]["composite"] = True
    out, inc = {}, {}
    for t in trs:
        out.setdefault(t["from"], []).append(t)
        inc.setdefault(t["to"], []).append(t)
    cb = []
    regions = {}
    for s in sts:
        regions.setdefault(s.get("parent"), []).append(s)
    for reg, lst in regions.items():
        ini = [s for s in lst if s["kind"] == "initial"]
        if len(ini) > 1:
            loi.append(f"LỖI: mỗi vùng chỉ có tối đa một trạng thái đầu (initial); vùng '{reg or 'chính'}' có {len(ini)}")
        if not ini and reg is None:
            loi.append("LỖI: máy trạng thái thiếu trạng thái đầu (initial)")
    for s in sts:
        k, i = s["kind"], s["id"]
        if k == "initial":
            if inc.get(i):
                loi.append(f"LỖI: trạng thái đầu '{i}' không được có chuyển đi vào")
            if len(out.get(i, [])) != 1:
                loi.append(f"LỖI: trạng thái đầu '{i}' phải có đúng một chuyển đi ra")
        elif k == "final":
            if out.get(i):
                loi.append(f"LỖI: trạng thái cuối '{i}' không được có chuyển đi ra")
        elif k == "choice":
            outs = out.get(i, [])
            if len(outs) < 2:
                loi.append(f"LỖI: nút chọn (choice) '{i}' cần ít nhất 2 chuyển đi ra")
            cb += [f"CẢNH BÁO: chuyển ra từ nút chọn '{i}' sang '{t['to']}' chưa có điều kiện [..]" for t in outs if "[" not in t.get("label", "")]
        elif not s.get("composite") and not out.get(i):
            cb.append(f"CẢNH BÁO: trạng thái '{i}' không có chuyển đi ra mà chưa phải final; thêm chuyển hoặc đổi thành kind final")
    # tới được từ trạng thái đầu
    seen, stack = set(), [s["id"] for s in sts if s["kind"] == "initial"]
    while stack:
        cur = stack.pop()
        if cur in seen:
            continue
        seen.add(cur)
        stack += [t["to"] for t in out.get(cur, [])]
        if byid[cur].get("composite"):
            stack += [c["id"] for c in kids[cur] if c["kind"] == "initial"]
    for s in sts:
        if s["id"] not in seen and not (s.get("parent") and s["parent"] in seen and s["kind"] == "initial"):
            loi.append(f"LỖI: trạng thái '{s['id']}' không với tới được từ trạng thái đầu")
    seen_lab = {}
    for t in trs:
        src = byid[t["from"]]
        if src["kind"] != "initial" and not t.get("label"):
            cb.append(f"CẢNH BÁO: chuyển '{t['from']}' -> '{t['to']}' chưa có nhãn (sự kiện [điều kiện] / hành động)")
        key = (t["from"], t.get("label", ""))
        if t.get("label") and key in seen_lab:
            cb.append(f"CẢNH BÁO: trạng thái '{t['from']}' có hai chuyển cùng nhãn '{t['label']}' (không xác định); thêm điều kiện [..]")
        seen_lab[key] = 1
    for p, lst in kids.items():
        if len(lst) < 2:
            cb.append(f"CẢNH BÁO: trạng thái ghép '{p}' chỉ có {len(lst)} trạng thái con")
    # kích thước và vị trí
    leaf = [s for s in sts if not s.get("composite")]
    for s in leaf:
        k = s["kind"]
        acts = s.get("actions", [])
        if k == "initial":
            s["_w"] = s["_h"] = 26
        elif k == "final":
            s["_w"] = s["_h"] = 30
        elif k == "choice":
            s["_w"] = s["_h"] = 44
        else:
            s["_w"] = max(170, int(len(s["label"]) * 8.5) + 40, int(max([len(a) for a in acts] or [0]) * 6.6) + 30)
            s["_h"] = 46 + (20 * len(acts) + 8 if acts else 0)
        grid_center(s)
    for p, lst in kids.items():
        byid[p]["_x"], byid[p]["_y"], x2, y2 = bbox(lst)
        byid[p]["_w"], byid[p]["_h"] = x2 - byid[p]["_x"], y2 - byid[p]["_y"]
    for p in kids:                                    # khung ghép chỉ được chứa con của nó
        r = rect(byid[p])
        for s in leaf:
            if s.get("parent") != p and not any(c is s for c in kids[p]):
                a = rect(s)
                if a[0] < r[2] and r[0] < a[2] and a[1] < r[3] and r[1] < a[3]:
                    # trạng thái thuộc khung cha của p thì hợp lệ
                    q, ok = byid[p].get("parent"), False
                    while q:
                        if s.get("parent") == q and False:
                            ok = True
                        q = byid[q].get("parent")
                    loi.append(f"LỖI: '{s['id']}' nằm trong khung trạng thái ghép '{p}' nhưng không phải con của nó (đổi vị trí hoặc đặt parent)")
    routes = []
    for t in trs:
        a, b = byid[t["from"]], byid[t["to"]]
        if a is b:
            x2, cy = a["_x"] + a["_w"], a["_y"] + a["_h"] // 2
            pts = [(x2, cy - 12), (x2 + 45, cy - 12), (x2 + 45, cy + 12), (x2, cy + 12)]
        else:
            pts = flow_route(a, b, t)
        routes.append((t["from"], t["to"], pts))
    l2, c2 = check_boxes(leaf, [r for r in routes if not byid[r[0]].get("composite") and not byid[r[1]].get("composite")], "trạng thái")
    loi += l2
    cb += c2
    cb += check_labels([(f"chuyển {t['from']}->{t['to']}", t.get("label", ""), pts, near_source_labelx(pts, t.get("label", "")), (t["from"], t["to"]))
                        for t, (_, _, pts) in zip(trs, routes)], leaf)
    allb = list(byid.values())
    doc = Doc(spec, max(rect(b)[2] for b in allb) + 260, max(rect(b)[3] for b in allb) + 120)
    for p in kids:                                    # khung ghép vẽ trước
        b = byid[p]
        doc.vertex(b["_x"], b["_y"], b["_w"], b["_h"], b["label"], f"rounded=1;arcSize=6;fillColor=none;strokeColor={INK};strokeWidth=1.3;verticalAlign=top;fontStyle=1;fontSize=12;html=0;spacingTop=6;", f"st_{p}")
    for s in leaf:
        k, sid = s["kind"], f"st_{s['id']}"
        if k == "initial":
            doc.vertex(s["_x"], s["_y"], 26, 26, "", "ellipse;fillColor=#000000;strokeColor=#000000;", sid)
        elif k == "final":
            doc.vertex(s["_x"], s["_y"], 30, 30, "", "ellipse;shape=endState;fillColor=#000000;strokeColor=#000000;", sid)
        elif k == "choice":
            doc.vertex(s["_x"], s["_y"], 44, 44, "", f"rhombus;fillColor=#ffffff;strokeColor={INK};", sid)
        else:
            acts = s.get("actions", [])
            doc.vertex(s["_x"], s["_y"], s["_w"], s["_h"], s["label"], f"rounded=1;arcSize=22;fillColor=#ffffff;strokeColor={INK};strokeWidth=1.2;verticalAlign=top;fontStyle=1;fontSize=12;html=0;spacingTop=6;whiteSpace=wrap;", sid)
            if acts:
                doc.vertex(s["_x"], s["_y"] + 30, s["_w"], 1, "", f"rounded=0;fillColor={INK};strokeColor=none;")
                doc.vertex(s["_x"] + 4, s["_y"] + 34, s["_w"] - 8, 20 * len(acts) + 6, "\n".join(acts), "text;html=0;fontSize=11;align=left;verticalAlign=top;whiteSpace=nowrap;")
    for k, (t, (_, _, pts)) in enumerate(zip(trs, routes), 1):
        lab = t.get("label", "")
        doc.edge(pts, lab, INK, "", False, eid=f"tr_{k}", src=f"st_{t['from']}", dst=f"st_{t['to']}",
                 ra=rect(byid[t["from"]]), rb=rect(byid[t["to"]]), lab_x=near_source_labelx(pts, lab))
    return doc, loi, cb


# ------------------------------------------------------------------ COMPONENT
def run_component(spec):
    """Sơ đồ thành phần UML (đen trắng). Thành phần: hộp «component». Giao diện cung cấp (provided): chấm tròn "kẹo mút" cạnh thành phần.
    Giao diện yêu cầu (required): mũi tên phụ thuộc nét đứt (kind 'uses') từ thành phần cần tới chấm tròn của nơi cung cấp (cách UML cho phép:
    required interface chỉ định bằng usage dependency). boundaries: khung bao nhóm thành phần (ví dụ một hệ thống)."""
    comps = spec["components"]
    conns = spec.get("connections", [])
    byid, loi, cb = {}, [], []
    for c in comps:
        if c["id"] in byid:
            loi.append(f"LỖI: id thành phần trùng: '{c['id']}'")
        byid[c["id"]] = c
        if not c.get("label"):
            loi.append(f"LỖI: thành phần '{c['id']}' thiếu label")
    for c in conns:
        for k in ("from", "to"):
            if c[k] not in byid:
                loi.append(f"LỖI: kết nối trỏ tới thành phần không có: '{c[k]}'")
        if c.get("kind", "uses") not in ("uses", "dependency"):
            loi.append(f"LỖI: kết nối '{c['from']}' -> '{c['to']}' có kind '{c.get('kind')}' không hợp lệ (uses, dependency)")
    for b in spec.get("boundaries", []):
        loi += [f"LỖI: khung '{b.get('label')}' chứa thành phần không có: '{m}'" for m in b.get("members", []) if m not in byid]
    if loi:
        return None, loi, []
    used = set()
    for c in conns:
        if c.get("kind", "uses") == "uses":
            if not c.get("interface"):
                loi.append(f"LỖI: kết nối uses '{c['from']}' -> '{c['to']}' thiếu `interface` (tên giao diện được dùng)")
            elif c["interface"] not in byid[c["to"]].get("provides", []):
                loi.append(f"LỖI: '{c['to']}' không cung cấp giao diện '{c['interface']}' (thêm vào provides)")
            else:
                used.add((c["to"], c["interface"]))
    for c in comps:
        cb += [f"CẢNH BÁO: giao diện '{i}' của '{c['id']}' không có thành phần nào dùng" for i in c.get("provides", []) if (c["id"], i) not in used]
        if not any(x["from"] == c["id"] or x["to"] == c["id"] for x in conns):
            cb.append(f"CẢNH BÁO: thành phần '{c['id']}' không nối với thành phần nào")
    # kích thước, vị trí, chấm tròn
    balls = []
    for c in comps:
        c["_w"] = max(200, int(len(c["label"]) * 8.5) + 70)
        c["_h"] = max(80, 36 + 30 * max(len(c.get("provides", [])), 1))
        grid_center(c, colw=380, rowh=170, x0=170, y0=200)
    for c in comps:
        for i, name in enumerate(c.get("provides", [])):
            side = c.get("pside")
            if not side:                       # chấm tròn đặt phía có thành phần dùng nó, để mũi tên không xuyên qua hộp
                req = [byid[x["from"]] for x in conns if x["to"] == c["id"] and x.get("kind", "uses") == "uses" and x.get("interface") == name]
                side = "left" if req and sum(r["_x"] + r["_w"] / 2 for r in req) / len(req) < c["_x"] + c["_w"] / 2 else "right"
            by_ = c["_y"] + 24 + i * 30
            bx = c["_x"] + c["_w"] + 38 if side == "right" else c["_x"] - 38 - 18
            balls.append({"id": f"ball_{c['id']}_{name}", "_x": bx, "_y": by_, "_w": 18, "_h": 18, "comp": c["id"], "name": name, "side": side})
    ballmap = {(b["comp"], b["name"]): b for b in balls}
    routes, items = [], []
    for k, c in enumerate(conns):
        a = byid[c["from"]]
        if c.get("kind", "uses") == "uses" and (c["to"], c.get("interface")) in ballmap:
            b = ballmap[(c["to"], c["interface"])]
        else:
            b = byid[c["to"]]
        pts = flow_route(a, b, c)
        routes.append((c["from"], b["id"], pts))
        items.append((c, a, b, pts))
    boxes = comps + balls
    l2, c2 = check_boxes(boxes, [(r[0], r[1], r[2]) for r in routes], "thành phần")
    loi += [x for x in l2 if "ball_" not in x]
    cb += [x for x in c2 if True]
    cb += check_labels([(f"kết nối {c['from']}->{c['to']}", c.get("label", ""), pts, near_source_labelx(pts, c.get("label", "")), (c["from"], c["to"], b["id"]))
                        for c, a, b, pts in items], boxes)
    bounds = []
    for bd in spec.get("boundaries", []):
        mem = [byid[m] for m in bd["members"]]
        mem += [bl for bl in balls if bl["comp"] in bd["members"]]
        x1, y1, x2, y2 = bbox(mem, 36, 52, 34)
        bounds.append((bd.get("label", ""), x1, y1, x2, y2))
    xs = [rect(b)[2] for b in boxes] + [bd[3] for bd in bounds]
    ys = [rect(b)[3] for b in boxes] + [bd[4] for bd in bounds]
    doc = Doc(spec, max(xs) + 260, max(ys) + 120)
    for label, x1, y1, x2, y2 in bounds:
        doc.vertex(x1, y1, x2 - x1, y2 - y1, label, f"rounded=0;fillColor=none;strokeColor={INK};strokeWidth=1.5;verticalAlign=top;fontStyle=1;fontSize=13;html=0;spacingTop=6;")
    for c in comps:
        doc.vertex(c["_x"], c["_y"], c["_w"], c["_h"], f"«{c.get('stereo', 'component')}»\n{c['label']}",
                   f"rounded=0;fillColor=#ffffff;strokeColor={INK};strokeWidth=1.3;html=0;fontSize=12;fontStyle=1;whiteSpace=wrap;", f"cmp_{c['id']}")
    for b in balls:
        cx = b["_x"] + 9
        edge_x = (b["_x"] - 20) if b["side"] == "right" else (b["_x"] + 18 + 20)
        doc.edge([(edge_x, b["_y"] + 9), (b["_x"] if b["side"] == "right" else b["_x"] + 18, b["_y"] + 9)], "", INK, "endArrow=none;", False, eid=f"stick_{b['comp']}_{b['name']}")
        doc.vertex(b["_x"], b["_y"], 18, 18, "", f"ellipse;fillColor=#ffffff;strokeColor={INK};strokeWidth=1.3;", b["id"])
        doc.vertex(b["_x"] - 26, b["_y"] - 20, 70, 18, b["name"], "text;html=0;fontSize=11;align=center;whiteSpace=nowrap;")
    for k, (c, a, b, pts) in enumerate(items, 1):
        lab = c.get("label", "")
        if c.get("kind", "uses") == "uses" and not lab:
            lab = "«use»"
        doc.edge(pts, lab, INK, "endArrow=open;endFill=0;", True, eid=f"con_{k}", lab_x=near_source_labelx(pts, lab))
    return doc, loi, cb


# ------------------------------------------------------------------ DEPLOYMENT
def run_deployment(spec):
    """Sơ đồ triển khai UML (đen trắng). Nút (node) vẽ hình hộp 3D; kind: device (thiết bị vật lý), executionEnvironment (môi trường chạy),
    node. Artifact (tệp, ảnh, jar...) nằm TRONG nút nó được triển khai tới (artifacts). children: nút lồng trong nút.
    Đường liền giữa hai nút là communication path, nhãn ghi giao thức."""
    nodes, paths = spec["nodes"], spec.get("paths", [])
    byid, loi, cb = {}, [], []
    for n in nodes:
        if n["id"] in byid:
            loi.append(f"LỖI: id nút trùng: '{n['id']}'")
        byid[n["id"]] = n
        n.setdefault("stereo", "node")
        if n["stereo"] not in ("node", "device", "executionEnvironment"):
            loi.append(f"LỖI: nút '{n['id']}' có stereo '{n['stereo']}' không hợp lệ (node, device, executionEnvironment)")
        if not n.get("label"):
            loi.append(f"LỖI: nút '{n['id']}' thiếu label")
    parent = {}
    for n in nodes:
        for ch in n.get("children", []):
            if ch not in byid:
                loi.append(f"LỖI: nút '{n['id']}' có con không có: '{ch}'")
            elif ch in parent:
                loi.append(f"LỖI: nút '{ch}' nằm trong hai nút cha")
            else:
                parent[ch] = n["id"]
    loi += [f"LỖI: đường nối trỏ tới nút không có: '{p[k]}'" for p in paths for k in ("from", "to") if p[k] not in byid]
    art_ids = [a["id"] for n in nodes for a in n.get("artifacts", [])]
    loi += [f"LỖI: artifact trùng id: '{a}'" for a in set(art_ids) if art_ids.count(a) > 1]
    if loi:
        return None, loi, []

    def size(n):
        chs = [byid[c] for c in n.get("children", [])]
        for c in chs:
            size(c)
        arts = len(n.get("artifacts", []))
        if chs:
            n["_w"] = sum(c["_w"] for c in chs) + 30 * (len(chs) - 1) + 50
            n["_h"] = max(c["_h"] for c in chs) + 80 + 46 * arts
        else:
            n["_w"] = max(250, int(len(n["label"]) * 9) + 60)
            n["_h"] = 78 + 46 * arts

    top = [n for n in nodes if n["id"] not in parent]
    for n in top:
        size(n)
    stack_columns(top, gap_x=170, gap_y=80)

    def place(n):
        chs = [byid[c] for c in n.get("children", [])]
        x = n["_x"] + 25
        for c in chs:
            c["_x"], c["_y"] = x, n["_y"] + 62
            place(c)
            x += c["_w"] + 30
    for n in top:
        place(n)
    boxes = top
    routes = []
    for p in paths:
        a, b = byid[p["from"]], byid[p["to"]]
        pts = route_boxes(a, b, p.get("via"))
        routes.append((p["from"], p["to"], pts))
    l2, c2 = check_boxes(top, [r for r in routes if r[0] in {t['id'] for t in top} and r[1] in {t['id'] for t in top}], "nút")
    loi += l2
    cb += c2
    cb += check_labels([(f"đường {p['from']}-{p['to']}", p.get("label", ""), pts, near_source_labelx(pts, p.get("label", "")), (p["from"], p["to"]))
                        for p, (_, _, pts) in zip(paths, routes)], top)
    touched = {p["from"] for p in paths} | {p["to"] for p in paths}
    for n in top:
        if n["id"] not in touched and not any(c in touched for c in n.get("children", [])):
            cb.append(f"CẢNH BÁO: nút '{n['id']}' không có đường nối nào")
    doc = Doc(spec, max(rect(b)[2] for b in nodes) + 260, max(rect(b)[3] for b in nodes) + 120)
    kw = {"device": "«device»\n", "executionEnvironment": "«execution environment»\n", "node": ""}

    def draw(n):
        doc.vertex(n["_x"], n["_y"], n["_w"], n["_h"], kw[n["stereo"]] + n["label"],
                   f"shape=cube;size=14;whiteSpace=wrap;html=0;fillColor=#ffffff;strokeColor={INK};strokeWidth=1.3;verticalAlign=top;fontStyle=1;fontSize=12;spacingTop=14;", f"node_{n['id']}")
        base = n["_y"] + n["_h"] - 46 * len(n.get("artifacts", [])) - 8
        for i, a in enumerate(n.get("artifacts", [])):
            doc.vertex(n["_x"] + 24, base + i * 46, n["_w"] - 52, 38, f"«artifact»\n{a['label']}", f"rounded=0;fillColor=#ffffff;strokeColor={INK};html=0;fontSize=11;whiteSpace=wrap;", f"art_{a['id']}")
        for c in n.get("children", []):
            draw(byid[c])
    for n in top:
        draw(n)
    for k, (p, (_, _, pts)) in enumerate(zip(paths, routes), 1):
        doc.edge(pts, p.get("label", ""), INK, "endArrow=none;", False, eid=f"path_{k}", lab_x=near_source_labelx(pts, p.get("label", "")))
    return doc, loi, cb


# ------------------------------------------------------------------ PACKAGE
def run_package(spec):
    """Sơ đồ gói UML (đen trắng). Gói: hình thư mục có tên và danh sách thành phần chứa (contains). Phụ thuộc giữa các gói: mũi tên nét đứt
    đầu hở, kind: use (dùng, không nhãn), import («import», nhập công khai), access («access», nhập riêng), merge («merge», trộn)."""
    pk, deps = spec["packages"], spec.get("dependencies", [])
    byid, loi, cb = {}, [], []
    for p in pk:
        if p["id"] in byid:
            loi.append(f"LỖI: id gói trùng: '{p['id']}'")
        byid[p["id"]] = p
        if not p.get("label"):
            loi.append(f"LỖI: gói '{p['id']}' thiếu label")
    kinds = {"use": "", "import": "«import»", "access": "«access»", "merge": "«merge»"}
    for d in deps:
        for k in ("from", "to"):
            if d[k] not in byid:
                loi.append(f"LỖI: phụ thuộc trỏ tới gói không có: '{d[k]}'")
        if d.get("kind", "use") not in kinds:
            loi.append(f"LỖI: phụ thuộc '{d['from']}' -> '{d['to']}' có kind '{d.get('kind')}' không hợp lệ ({', '.join(kinds)})")
    if loi:
        return None, loi, []
    graph = {}
    for d in deps:
        graph.setdefault(d["from"], []).append(d["to"])
    def cyc(n, path):
        if n in path:
            return path[path.index(n):] + [n]
        for m in graph.get(n, []):
            r = cyc(m, path + [n])
            if r:
                return r
        return None
    found = set()
    for p in pk:
        r = cyc(p["id"], [])
        if r and frozenset(r) not in found:
            found.add(frozenset(r))
            cb.append("CẢNH BÁO: phụ thuộc VÒNG giữa các gói: " + " -> ".join(r) + " (nên bẻ vòng)")
    for p in pk:
        if not any(d["from"] == p["id"] or d["to"] == p["id"] for d in deps):
            cb.append(f"CẢNH BÁO: gói '{p['id']}' không có phụ thuộc nào")
        cont = p.get("contains", [])
        p["_w"] = max(230, int(len(p["label"]) * 9) + 50, int(max([len(c) for c in cont] or [0]) * 7) + 40)
        p["_h"] = 66 + 20 * len(cont) if cont else 84
        grid_center(p, colw=360, rowh=190, x0=170)
    routes = []
    for d in deps:
        pts = flow_route(byid[d["from"]], byid[d["to"]], d)
        routes.append((d["from"], d["to"], pts))
    l2, c2 = check_boxes(pk, routes, "gói")
    loi += l2
    cb += c2
    cb += check_labels([(f"phụ thuộc {d['from']}->{d['to']}", d.get("label") or kinds[d.get("kind", "use")], pts, near_source_labelx(pts, d.get("label") or kinds[d.get("kind", "use")]), (d["from"], d["to"]))
                        for d, (_, _, pts) in zip(deps, routes)], pk)
    doc = Doc(spec, max(rect(b)[2] for b in pk) + 260, max(rect(b)[3] for b in pk) + 120)
    for p in pk:
        doc.vertex(p["_x"], p["_y"], p["_w"], p["_h"], p["label"],
                   f"shape=folder;tabWidth=80;tabHeight=18;tabPosition=left;whiteSpace=wrap;html=0;fillColor=#ffffff;strokeColor={INK};strokeWidth=1.3;verticalAlign=top;fontStyle=1;fontSize=12;spacingTop=24;", f"pkg_{p['id']}")
        if p.get("contains"):
            doc.vertex(p["_x"] + 8, p["_y"] + 46, p["_w"] - 16, 20 * len(p["contains"]), "\n".join(p["contains"]), "text;html=0;fontSize=11;align=left;verticalAlign=top;whiteSpace=nowrap;")
    for k, (d, (_, _, pts)) in enumerate(zip(deps, routes), 1):
        lab = d.get("label") or kinds[d.get("kind", "use")]
        doc.edge(pts, lab, INK, "endArrow=open;endFill=0;", True, eid=f"dep_{k}", src=f"pkg_{d['from']}", dst=f"pkg_{d['to']}",
                 ra=rect(byid[d["from"]]), rb=rect(byid[d["to"]]), lab_x=near_source_labelx(pts, lab))
    return doc, loi, cb


# ----------------------------------------------------------------------------------------------- SEQUENCE
def run_sequence(spec):
    ps, ms = spec["participants"], spec.get("messages", [])
    ids = [p["id"] for p in ps]
    loi = [f"LỖI: thông điệp trỏ tới đối tượng không có: '{m[k]}'" for m in ms for k in ("from", "to") if m[k] not in ids]
    loi += [f"LỖI: thông điệp từ '{m['from']}' tới chính nó phải có kind 'self'" for m in ms if m["from"] == m["to"] and m.get("kind") != "self"]
    if loi:
        return None, loi, []
    step = max(225, max(len(l) for p in ps for l in p["name"].split("\n")) * 8 + 40)
    xs = {p["id"]: 125 + i * step for i, p in enumerate(ps)}
    y = 210
    ys = []
    wraps = {}  # nhãn dài hơn khoảng cách giữa hai đường đời thì xuống dòng, để chữ không tràn ra ngoài và đè đường đời khác
    k0 = 0
    for mi, m in enumerate(ms):
        kind0 = m.get("kind", "call")
        if kind0 != "return":
            k0 += 1
        txt0 = m.get("label", "") if kind0 == "return" else f"{k0}. {m.get('label', '')}"
        lines = [txt0]
        if kind0 != "self":
            maxc = max(12, int((abs(xs[m["from"]] - xs[m["to"]]) - 24) / 6.6))
            if len(txt0) > maxc:
                lines = textwrap.wrap(txt0, maxc) or [txt0]
        wraps[mi] = "\n".join(lines)
        ys.append(y + max(0, len(lines) - 1) * 16)
        y += (90 if kind0 == "self" else 50) + max(0, len(lines) - 1) * 16
    bottom = y + 30
    doc = Doc(spec, max(xs.values()) + 300, bottom + 60)
    cb = []
    for i, p in enumerate(ps):
        fill, stroke = ("#f2f2f2", INK) if spec.get("plain", True) else PAL.get(p.get("color", "purple"), PAL["purple"])
        doc.vertex(xs[p["id"]] - 100, 90, 200, 76, p["name"], f"rounded=1;arcSize=12;whiteSpace=wrap;html=0;fontSize=12;fontStyle=1;fillColor={fill};strokeColor={stroke};", f"par_{p['id']}")
        doc.edge([(xs[p["id"]], 166), (xs[p["id"]], bottom)], "", "#94a3b8", "endArrow=none;", True)
    k = 0
    for mi, (m, yy) in enumerate(zip(ms, ys), 1):
        kind = m.get("kind", "call")
        if kind != "return":
            k += 1
        txt = m.get("label", "") if kind == "return" else f"{k}. {m.get('label', '')}"
        if kind == "self":
            x0 = xs[m["from"]]
            doc.edge([(x0, yy), (x0 + 60, yy), (x0 + 60, yy + 40), (x0, yy + 40)], txt, INK, "", False, "labelBackgroundColor=#ffffff;align=left;", eid=f"msg_{mi}")
        else:
            # nhãn xuống dòng cho vừa khoảng cách hai đường đời; nền trắng để đường đời của đối tượng ở giữa không gạch qua chữ
            # call: đồng bộ, mũi tên đặc; async: bất đồng bộ, đầu hở nét liền; return: trả về, đầu hở nét đứt (UML 2.5, interaction-message.md)
            doc.edge([(xs[m["from"]], yy), (xs[m["to"]], yy)], wraps[mi - 1], INK, "endArrow=open;endFill=0;" if kind in ("return", "async") else "",
                     kind == "return", "labelBackgroundColor=#ffffff;verticalAlign=bottom;spacingBottom=4;", eid=f"msg_{mi}")
    loi += [f"LỖI: thông điệp {i} có kind '{m.get('kind')}' không hợp lệ (call, async, return, self)" for i, m in enumerate(ms, 1) if m.get("kind", "call") not in ("call", "async", "return", "self")]
    calls = sum(1 for m in ms if m.get("kind", "call") != "return")
    returns = sum(1 for m in ms if m.get("kind") == "return")
    if returns > calls:
        cb.append(f"CẢNH BÁO: số dòng trả về ({returns}) nhiều hơn số lời gọi ({calls})")
    return doc, loi, cb


RUNNERS = {"class": run_class, "flow": run_flow, "swimlane": run_flow, "sequence": run_sequence, "erd": run_erd, "activity": run_activity, "usecase": run_usecase,
           "statemachine": run_statemachine, "component": run_component, "deployment": run_deployment, "package": run_package}


# ----------------------------------------------------------------------------------------------- bảo vệ bản sửa tay và đồng bộ ngược
def sha_of(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sidecar(out):
    return Path(str(out) + ".sha")


def read_cells(drawio):
    """Đọc các ô của file .drawio (dạng văn bản, không nén). Trả None nếu file bị nén."""
    d = ET.parse(drawio).getroot().find("diagram")
    gm = d.find("mxGraphModel") if d is not None else None
    if gm is None:
        return None
    return {c.get("id"): c for c in gm.iter("mxCell")}


def geom(cell):
    g = cell.find("mxGeometry")
    if g is None:
        return None
    return tuple(round(float(g.get(k, 0))) for k in ("x", "y", "width", "height"))


def plain(html_text):
    s = re.sub(r"<br\s*/?>", "\n", html_text or "")
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def lay_tu_drawio(spec, spec_path, out):
    """So bản .drawio người dùng đã sửa với bản vừa sinh mới từ JSON, ghi phần khác biệt (vị trí, chữ) ngược vào JSON."""
    kind = spec.get("type", "class")
    edited = read_cells(out)
    if edited is None:
        print("LỖI: file .drawio đang ở dạng nén (draw.io Desktop: Tệp > Thuộc tính > bỏ chọn Nén), không đọc được.")
        return 1
    fresh_spec = copy.deepcopy(spec)
    fresh_doc, loi, _ = RUNNERS[kind](fresh_spec)
    if fresh_doc is None:
        print("\n".join(loi))
        return 1
    fresh = {c.get("id"): c for c in fresh_doc.root.iter("mxCell")}
    changes = []
    cls = {c["id"]: c for c in spec.get("classes", [])}
    nodes = {n["id"]: n for n in spec.get("nodes", [])}
    tbls = {t["id"]: t for t in spec.get("tables", [])}
    pars = {p["id"]: p for p in spec.get("participants", [])}
    for cid, cell in edited.items():
        if cid not in fresh or cid in ("0", "1"):
            continue
        g_new, g_old = geom(cell), geom(fresh[cid])
        v_new, v_old = cell.get("value") or "", fresh[cid].get("value") or ""
        moved = g_new and g_old and (abs(g_new[0] - g_old[0]) > 3 or abs(g_new[1] - g_old[1]) > 3)
        resized = g_new and g_old and abs(g_new[2] - g_old[2]) > 3
        m = re.fullmatch(r"cls_(.+?)(_h|_a|_m)?", cid)
        if cid.startswith("cls_") and m and m.group(1) in cls:
            c, part = cls[m.group(1)], m.group(2)
            if part is None and (moved or resized):
                c["x"], c["y"], c["w"] = g_new[0], g_new[1], g_new[2]
                changes.append(f"lớp '{c['id']}': vị trí và độ rộng -> x={g_new[0]}, y={g_new[1]}, w={g_new[2]}")
            elif part == "_h" and v_new != v_old:
                segs = [s for s in plain(re.sub(r"<br\s*/?>", "<br>", v_new).replace("<br>", "<br>")).split("\n") if s.strip()]
                stereo = ""
                if segs and segs[0].startswith("<<") and segs[0].endswith(">>"):
                    stereo, segs = segs[0][2:-2], segs[1:]
                if segs:
                    c["name"] = segs[0].strip()
                    c["abstract"] = "<i>" in v_new
                    if len(segs) > 1:
                        c["sub"] = segs[1].strip()
                if stereo:
                    c["stereo"] = stereo
                changes.append(f"lớp '{c['id']}': tên, nghĩa, stereotype")
            elif part in ("_a", "_m") and v_new != v_old:
                c["attrs" if part == "_a" else "methods"] = [s for s in v_new.split("\n") if s.strip()]
                changes.append(f"lớp '{c['id']}': {'thuộc tính' if part == '_a' else 'hàm'}")
        elif cid.startswith("node_") and cid[5:] in nodes:
            n = nodes[cid[5:]]
            if moved and g_new:
                n["x"], n["y"] = g_new[0] + g_new[2] // 2, g_new[1] + g_new[3] // 2
                changes.append(f"nút '{n['id']}': vị trí -> x={n['x']}, y={n['y']} (tâm)")
            if v_new != v_old and v_new:
                n["label"] = v_new
                changes.append(f"nút '{n['id']}': nhãn")
        elif cid.startswith("tbl_") and cid[4:] in tbls:
            t = tbls[cid[4:]]
            if moved and g_new:
                t["x"], t["y"] = g_new[0], g_new[1]
                changes.append(f"bảng '{t['id']}': vị trí -> x={g_new[0]}, y={g_new[1]}")
            if v_new != v_old:
                t["name"] = v_new
                changes.append(f"bảng '{t['id']}': tên")
        elif cid.startswith("par_") and cid[4:] in pars and v_new != v_old:
            pars[cid[4:]]["name"] = v_new
            changes.append(f"đối tượng '{cid[4:]}': tên")
        elif cid.startswith("msg_") and v_new != v_old:
            idx = int(cid[4:]) - 1
            if 0 <= idx < len(spec.get("messages", [])):
                spec["messages"][idx]["label"] = re.sub(r"^\d+\.\s*", "", v_new)
                changes.append(f"thông điệp {idx + 1}: nhãn")
    # Phần KHÔNG đồng bộ ngược được: đường nối, ô mới thêm, màu sắc
    def edge_count(cells):
        return sum(1 for c in cells.values() if c.get("edge") == "1")
    canh_bao = []
    if edge_count(edited) != edge_count(fresh):
        canh_bao.append("CẢNH BÁO: số đường nối trong file .drawio khác JSON (đã thêm hoặc xóa đường). Quan hệ KHÔNG đồng bộ ngược: sửa `relations`/`edges`/`messages` trong JSON bằng tay.")
    moi = [i for i in edited if i not in fresh and i not in ("0", "1") and edited[i].get("vertex") == "1"
           and not (geom(edited[i]) and geom(edited[i])[2] == 4)]
    if moi:
        canh_bao.append(f"CẢNH BÁO: có {len(moi)} ô mới thêm tay trong .drawio (không có trong JSON); thêm vào JSON nếu muốn giữ.")
    spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sidecar(out).write_text(sha_of(out), encoding="utf-8")
    for line in changes:
        print("ĐỒNG BỘ:", line)
    for line in canh_bao:
        print(line)
    print(f"Đã cập nhật {spec_path} ({len(changes)} thay đổi). Chạy lại ve-so-do.py với --ghi-de để dựng lại .drawio từ JSON "
          "(màu sắc và chỉnh sửa hình thức do bạn làm sẽ mất).")
    return 0


def run_bundle(spec_path, spec, args):
    """Gộp nhiều spec JSON thành MỘT file .drawio nhiều tab. Mỗi spec con vẫn là nguồn sự thật của tab đó;
    file .drawio riêng của spec con KHÔNG được ghi (chỉ ghi file gộp). Ảnh .png của từng tab lấy theo trường `png` của spec con."""
    base = spec_path.parent
    out = base / spec.get("out", spec_path.stem + ".drawio")
    root = ET.Element("mxfile", host="app.diagrams.net")
    pages, tong_loi = [], 0
    for i, pg in enumerate(spec.get("pages", []), 1):
        sp = base / pg["spec"]
        sub = json.loads(sp.read_text(encoding="utf-8"))
        kind = sub.get("type", "class")
        if kind not in RUNNERS:
            print(f"LỖI: tab '{pg.get('name')}': type '{kind}' không hợp lệ")
            tong_loi += 1
            continue
        doc, loi, cb = RUNNERS[kind](sub)
        print(f"--- Tab {i}: {pg.get('name')} ({pg['spec']})")
        for line in loi + cb:
            print("  " + line)
        tong_loi += len(loi)
        if doc is None:
            continue
        d = doc.mxf.find("diagram")
        d.set("name", pg.get("name", sub.get("title", f"Tab {i}")))
        d.set("id", f"p{i}")
        root.append(d)
        pages.append((i, base / sub["png"] if sub.get("png") else None, d))
        print(f"  ({len(loi)} lỗi, {len(cb)} cảnh báo)")
    print("KIỂM: " + ("có lỗi" if tong_loi else "đạt") + f" ({len(root.findall('diagram'))}/{len(spec.get('pages', []))} tab)")
    if tong_loi or "--check-only" in args:
        return 1 if tong_loi else 0
    side = sidecar(out)
    if out.exists() and "--ghi-de" not in args:
        da_sinh = side.read_text(encoding="utf-8").strip() if side.exists() else None
        if da_sinh is None or da_sinh != sha_of(out):
            print(f"DỪNG: {out.name} đã bị sửa tay (hoặc không do công cụ sinh). KHÔNG ghi đè. Bỏ chỉnh sửa tay: thêm --ghi-de")
            return 2
    ET.indent(root, space="  ")
    ET.ElementTree(root).write(out, encoding="utf-8", xml_declaration=False)
    side.write_text(sha_of(out), encoding="utf-8")
    print(f"Đã ghi {out} ({len(pages)} tab)")
    cli = os.environ.get("DRAWIO_CLI", DRAWIO_CLI)
    if not Path(cli).exists():
        print("CHƯA XUẤT ẢNH: không thấy draw.io Desktop. Báo rõ 'chưa xem ảnh' khi nộp.")
        return 0
    for i, png, d in pages:
        if not png:
            continue
        gm = d.find("mxGraphModel")
        big = max(int(gm.get("pageWidth")), int(gm.get("pageHeight")))
        scale = str(round(min(2.0, 4000 / big), 2))
        r = subprocess.run([cli, "-x", "-f", "png", "-p", str(i), "-s", scale, "-b", "10", "-o", str(png), str(out)], capture_output=True, text=True)
        print(f"Đã xuất {png}" if png.exists() else f"Xuất ảnh lỗi ({png.name}): {r.stderr[:200]}")
    return 0


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if args[0] == "--mau":
        kind = args[1] if len(args) > 1 else "class"
        if kind not in MAU:
            print(f"Loại không có: {kind}. Dùng: {', '.join(MAU)}")
            return 1
        print(json.dumps(MAU[kind], ensure_ascii=False, indent=2))
        return 0
    spec_path = Path(args[0])
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    kind = spec.get("type", "class")
    if kind == "bundle":
        return run_bundle(spec_path, spec, args)
    if kind not in RUNNERS:
        print(f"LỖI: type '{kind}' không hợp lệ (dùng: {', '.join(RUNNERS)}, bundle)")
        return 1
    base = spec_path.parent
    out = base / spec.get("out", spec_path.stem + ".drawio")
    if "--lay-tu-drawio" in args:
        if not out.exists():
            print(f"LỖI: chưa có {out} để lấy.")
            return 1
        return lay_tu_drawio(spec, spec_path, out)
    doc, loi, cb = RUNNERS[kind](spec)
    for line in loi + cb:
        print(line)
    if doc is None or "--check-only" in args:
        print("KIỂM: " + ("có lỗi" if loi else "đạt") + f" ({len(cb)} cảnh báo)")
        return 1 if loi else 0
    # Chặn ghi đè bản người dùng đã sửa tay trong draw.io
    side = sidecar(out)
    if out.exists() and "--ghi-de" not in args:
        da_sinh = side.read_text(encoding="utf-8").strip() if side.exists() else None
        if da_sinh is None or da_sinh != sha_of(out):
            print(f"DỪNG: {out.name} đã bị sửa tay (hoặc không do công cụ sinh). KHÔNG ghi đè.\n"
                  f"  - Giữ chỉnh sửa của bạn và cập nhật JSON: python3 scripts/ve-so-do.py {spec_path.name} --lay-tu-drawio\n"
                  "  - Bỏ chỉnh sửa tay, dựng lại từ JSON: thêm --ghi-de")
            return 2
    tree = ET.ElementTree(doc.mxf)
    ET.indent(tree, space="  ")
    tree.write(out, encoding="utf-8", xml_declaration=False)
    side.write_text(sha_of(out), encoding="utf-8")
    print(f"Đã ghi {out}")
    if spec.get("png"):
        png = base / spec["png"]
        cli = os.environ.get("DRAWIO_CLI", DRAWIO_CLI)
        if Path(cli).exists():
            gm = doc.mxf.find("diagram").find("mxGraphModel")
            big = max(int(gm.get("pageWidth")), int(gm.get("pageHeight")))
            scale = str(round(min(2.0, 4000 / big), 2))  # ảnh quá lớn (trên khoảng 4000 điểm) bị cắt cụt khi xuất, nên tự giảm tỉ lệ
            r = subprocess.run([cli, "-x", "-f", "png", "-s", scale, "-b", "10", "-o", str(png), str(out)], capture_output=True, text=True)
            print(f"Đã xuất {png}" if png.exists() else f"Xuất ảnh lỗi: {r.stderr[:200]}")
        else:
            print("CHƯA XUẤT ẢNH: không thấy draw.io Desktop (brew install --cask drawio, hoặc đặt DRAWIO_CLI). Báo rõ 'chưa xem ảnh' khi nộp.")
    print("KIỂM: " + ("có lỗi" if loi else "đạt") + f" ({len(cb)} cảnh báo). Nếu xem được ảnh: mở ảnh xem từng hộp và đường, sửa JSON, vẽ lại.")
    return 1 if loi else 0


if __name__ == "__main__":
    sys.exit(main())
