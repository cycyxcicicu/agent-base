"""Kiểm thử scripts/diagram-describe.py bằng sơ đồ draw.io giả (không dùng dữ liệu dự án)."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "diagram-describe.py"


def cell(i, value, style, x, y, w, h):
    return (f'<mxCell id="{i}" value="{value}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')


def edge(i, src, dst, value=""):
    return (f'<mxCell id="{i}" value="{value}" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="{src}" target="{dst}">'
            f'<mxGeometry relative="1" as="geometry"/></mxCell>')


def page(page_id, ends=1, name="Luong mau"):
    parts = [
        cell("lane0", "", "rounded=0;fillColor=none;strokeColor=#94a3b8;", 0, 0, 240, 600),
        cell("laneh0", "Nguoi dung", "rounded=0;fillColor=#e0f2fe;", 0, 0, 240, 40),
        cell("lane1", "", "rounded=0;fillColor=none;strokeColor=#94a3b8;", 240, 0, 240, 600),
        cell("laneh1", "He thong", "rounded=0;fillColor=#dcfce7;", 240, 0, 240, 40),
        cell("s", "", "ellipse;fillColor=#0f172a;", 100, 60, 20, 20),
        cell("a", "Bam gui", "rounded=1;arcSize=20;", 60, 100, 120, 40),
        cell("d", "Hop le?", "rhombus;fillColor=#fff7ed;", 300, 100, 120, 60),
        cell("ok", "Luu don", "rounded=1;", 300, 220, 120, 40),
        cell("e1", "", "ellipse;shape=endState;fillColor=#0f172a;", 350, 300, 20, 20),
    ]
    edges = [edge("x1", "s", "a"), edge("x2", "a", "d"), edge("x3", "d", "ok", "co"), edge("x4", "ok", "e1")]
    if ends == 2:
        parts.append(cell("e2", "", "ellipse;shape=endState;fillColor=#0f172a;", 450, 300, 20, 20))
        edges.append(edge("x5", "d", "e2", "khong"))
    else:
        edges.append(edge("x5", "d", "e1", "khong"))
    return (f'<diagram name="{name}" id="{page_id}"><mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
            + "".join(parts + edges) + "</root></mxGraphModel></diagram>")


def run(content, *args):
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "t.drawio"
        f.write_text(content, encoding="utf-8")
        return subprocess.run([sys.executable, str(SCRIPT), str(f), *args], capture_output=True, text=True, encoding="utf-8")


def mxfile(*pages):
    return '<mxfile host="app.diagrams.net">' + "".join(pages) + "</mxfile>"


class TestDiagramDescribe(unittest.TestCase):
    def test_describes_lanes_steps_and_branches(self):
        r = run(mxfile(page("p1")))
        self.assertEqual(r.returncode, 0, r.stderr)
        for expected in ("Nguoi dung", "He thong", "Bam gui", "[co] bước", "[khong] bước", "quyết định", "kết thúc", "Kiểm quy tắc: đạt"):
            self.assertIn(expected, r.stdout)

    def test_lane_headers_are_not_listed_as_steps(self):
        r = run(mxfile(page("p1")), "--json")
        data = json.loads(r.stdout)
        labels = [s["label"] for s in data["pages"][0]["steps"]]
        self.assertNotIn("Nguoi dung", labels)
        lane_of = {s["label"]: s["lane"] for s in data["pages"][0]["steps"]}
        self.assertEqual(lane_of["Bam gui"], "Nguoi dung")
        self.assertEqual(lane_of["Luu don"], "He thong")

    def test_check_passes_with_single_end(self):
        self.assertEqual(run(mxfile(page("p1")), "--check").returncode, 0)

    def test_check_fails_with_two_ends(self):
        r = run(mxfile(page("p1", ends=2)), "--check")
        self.assertEqual(r.returncode, 1)
        self.assertIn("đúng một nút kết thúc", r.stdout)

    def test_check_fails_on_duplicate_page_ids(self):
        r = run(mxfile(page("d1", name="A"), page("d1", name="B")), "--check")
        self.assertEqual(r.returncode, 1)
        self.assertIn("id trang trùng", r.stdout)

    def test_page_filter(self):
        r = run(mxfile(page("p1", name="A"), page("p2", name="B")), "--page", "B")
        self.assertIn("Trang: B", r.stdout)
        self.assertNotIn("Trang: A", r.stdout)

    def test_compressed_or_broken_file_is_reported(self):
        r = run("khong phai xml")
        self.assertEqual(r.returncode, 2)
        self.assertIn("nén", r.stderr)


if __name__ == "__main__":
    unittest.main()
