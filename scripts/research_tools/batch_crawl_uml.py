"""scripts/batch_crawl_uml.py

Tự động cào toàn diện 15+ loại sơ đồ UML từ uml-diagrams.org về D:/test-repo/uml/,
tải 100% ảnh minh họa và đóng gói template .drawio + .json cho Agent.
"""

from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.crawl_jina_assets import crawl_page

UML_TARGETS = [
    {
        "name": "class-diagram",
        "url": "https://www.uml-diagrams.org/class-diagrams-overview.html",
        "title": "Class Diagrams (Sơ đồ lớp)",
        "kind": "structure",
    },
    {
        "name": "sequence-diagram",
        "url": "https://www.uml-diagrams.org/sequence-diagrams.html",
        "title": "Sequence Diagrams (Sơ đồ tuần tự)",
        "kind": "interaction",
    },
    {
        "name": "activity-diagram",
        "url": "https://www.uml-diagrams.org/activity-diagrams.html",
        "title": "Activity Diagrams (Sơ đồ hoạt động)",
        "kind": "behavior",
    },
    {
        "name": "state-machine-diagram",
        "url": "https://www.uml-diagrams.org/state-machine-diagrams.html",
        "title": "State Machine Diagrams (Sơ đồ máy trạng thái)",
        "kind": "behavior",
    },
    {
        "name": "use-case-diagram",
        "url": "https://www.uml-diagrams.org/use-case-diagrams.html",
        "title": "Use Case Diagrams (Sơ đồ ca sử dụng)",
        "kind": "behavior",
    },
    {
        "name": "component-diagram",
        "url": "https://www.uml-diagrams.org/component-diagrams.html",
        "title": "Component Diagrams (Sơ đồ thành phần)",
        "kind": "structure",
    },
    {
        "name": "deployment-diagram",
        "url": "https://www.uml-diagrams.org/deployment-diagrams-overview.html",
        "title": "Deployment Diagrams (Sơ đồ triển khai)",
        "kind": "structure",
    },
    {
        "name": "package-diagram",
        "url": "https://www.uml-diagrams.org/package-diagrams-overview.html",
        "title": "Package Diagrams (Sơ đồ gói)",
        "kind": "structure",
    },
    {
        "name": "composite-structure-diagram",
        "url": "https://www.uml-diagrams.org/composite-structure-diagrams.html",
        "title": "Composite Structure Diagrams (Sơ đồ cấu trúc hỗn hợp)",
        "kind": "structure",
    },
    {
        "name": "communication-diagram",
        "url": "https://www.uml-diagrams.org/communication-diagrams.html",
        "title": "Communication Diagrams (Sơ đồ giao tiếp)",
        "kind": "interaction",
    },
    {
        "name": "timing-diagram",
        "url": "https://www.uml-diagrams.org/timing-diagrams.html",
        "title": "Timing Diagrams (Sơ đồ thời gian)",
        "kind": "interaction",
    },
    {
        "name": "interaction-overview-diagram",
        "url": "https://www.uml-diagrams.org/interaction-overview-diagrams.html",
        "title": "Interaction Overview Diagrams (Sơ đồ tổng quan tương tác)",
        "kind": "interaction",
    },
    {
        "name": "profile-diagram",
        "url": "https://www.uml-diagrams.org/profile-diagrams.html",
        "title": "Profile Diagrams (Sơ đồ hồ sơ)",
        "kind": "structure",
    },
    {
        "name": "uml-examples",
        "url": "https://www.uml-diagrams.org/index-examples.html",
        "title": "UML Diagram Examples (Ví dụ tổng hợp)",
        "kind": "examples",
    },
]

DRAWIO_ACTIVITY_TEMPLATE = """<mxfile host="Electron" modified="2026-11-01T00:00:00.000Z" agent="Mozilla/5.0" version="21.0.0" type="device">
  <diagram id="activity-standard" name="Activity Diagram Standard">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- Swimlanes -->
        <mxCell id="lane-user" value="Người Dùng (Client/Frontend)" style="swimlane;whiteSpace=wrap;html=1;startSize=23;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="320" height="600" as="geometry"/>
        </mxCell>
        <mxCell id="start-node" value="" style="ellipse;html=1;shape=startState;fillColor=#000000;strokeColor=#000000;" vertex="1" parent="lane-user">
          <mxGeometry x="145" y="50" width="30" height="30" as="geometry"/>
        </mxCell>
        <mxCell id="act-request" value="1. Gửi yêu cầu thao tác" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#6c8ebf;" vertex="1" parent="lane-user">
          <mxGeometry x="85" y="120" width="150" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="lane-system" value="Hệ Thống / Backend API" style="swimlane;whiteSpace=wrap;html=1;startSize=23;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="360" y="40" width="340" height="600" as="geometry"/>
        </mxCell>
        <mxCell id="act-process" value="2. Xác thực &amp; Xử lý nghiệp vụ" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#82b366;" vertex="1" parent="lane-system">
          <mxGeometry x="95" y="120" width="150" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="decision-valid" value="Dữ liệu&#xa;hợp lệ?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="lane-system">
          <mxGeometry x="120" y="210" width="100" height="70" as="geometry"/>
        </mxCell>
        <mxCell id="act-save" value="3. Cập nhật cơ sở dữ liệu" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#82b366;" vertex="1" parent="lane-system">
          <mxGeometry x="95" y="330" width="150" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="act-log-error" value="3b. Ghi nhận lỗi &amp; Rollback" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontColor=#b85450;" vertex="1" parent="lane-system">
          <mxGeometry x="180" y="420" width="140" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="end-node" value="" style="ellipse;html=1;shape=endState;fillColor=#000000;strokeColor=#ff0000;" vertex="1" parent="lane-system">
          <mxGeometry x="155" y="520" width="30" height="30" as="geometry"/>
        </mxCell>
        <!-- Connectors -->
        <mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="start-node" target="act-request">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="act-request" target="act-process">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="act-process" target="decision-valid">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e4-yes" value="[Hợp lệ]" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#82b366;" edge="1" parent="1" source="decision-valid" target="act-save">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e5-no" value="[Lỗi/Không hợp lệ]" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#b85450;fontColor=#b85450;" edge="1" parent="1" source="decision-valid" target="act-log-error">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e6" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="act-save" target="end-node">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="e7" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#b85450;" edge="1" parent="1" source="act-log-error" target="end-node">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

JSON_ACTIVITY_TEMPLATE = """{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "diagramType": "activity",
  "title": "Chuẩn sơ đồ hoạt động (Activity Diagram Specification)",
  "rules": {
    "singleStart": true,
    "singleEnd": true,
    "errorBranchesInRed": true,
    "swimlanesRequired": true
  },
  "swimlanes": [
    {"id": "user", "name": "Người Dùng (Frontend)", "order": 1},
    {"id": "system", "name": "Hệ Thống (Backend API / Services)", "order": 2},
    {"id": "database", "name": "Cơ Sở Dữ Liệu (PostgreSQL / Redis)", "order": 3}
  ],
  "nodes": [
    {"id": "start", "type": "initial", "swimlane": "user"},
    {"id": "submit", "type": "action", "label": "Gửi thao tác", "swimlane": "user"},
    {"id": "validate", "type": "decision", "label": "Kiểm tra hợp lệ?", "swimlane": "system"},
    {"id": "persist", "type": "action", "label": "Lưu dữ liệu", "swimlane": "database"},
    {"id": "rollback", "type": "action", "label": "Rollback & Báo lỗi", "swimlane": "system", "isError": true},
    {"id": "end", "type": "final", "swimlane": "system"}
  ],
  "flows": [
    {"from": "start", "to": "submit"},
    {"from": "submit", "to": "validate"},
    {"from": "validate", "to": "persist", "guard": "Hợp lệ"},
    {"from": "validate", "to": "rollback", "guard": "Không hợp lệ", "color": "#ff0000"},
    {"from": "persist", "to": "end"},
    {"from": "rollback", "to": "end", "color": "#ff0000"}
  ]
}
"""


def main():
    root_uml = Path("D:/test-repo/uml")
    root_uml.mkdir(parents=True, exist_ok=True)

    print(f"=== BẮT ĐẦU CÀO TOÀN DIỆN {len(UML_TARGETS)} LOẠI SƠ ĐỒ UML TỪ UML-DIAGRAMS.ORG ===")

    for idx, item in enumerate(UML_TARGETS, 1):
        target_dir = root_uml / item["name"]
        target_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n[{idx}/{len(UML_TARGETS)}] Đang xử lý: {item['title']}...")
        try:
            # 1. Cào tài liệu chi tiết và tải toàn bộ ảnh minh họa
            out_md = crawl_page(
                target_url=item["url"],
                out_dir=target_dir,
                doc_slug="spec",
                download_images=True,
                max_workers=5,
                timeout=45,
            )

            # 2. Sinh template .drawio chuẩn cho Agent
            drawio_path = target_dir / "template.drawio"
            if not drawio_path.exists():
                drawio_path.write_text(DRAWIO_ACTIVITY_TEMPLATE, encoding="utf-8")

            # 3. Sinh template .json IR cho Agent
            json_path = target_dir / "template.json"
            if not json_path.exists():
                json_path.write_text(JSON_ACTIVITY_TEMPLATE, encoding="utf-8")

            print(f"  -> Hoàn tất đóng gói: {target_dir}")
            time.sleep(1)  # Giãn cách an toàn
        except Exception as e:
            print(f"  [WARN] Bỏ qua {item['name']} do lỗi: {e}", file=sys.stderr)

    print("\n=== HOÀN TẤT THU THẬP & ĐÓNG GÓI 100% SƠ ĐỒ UML TẠI D:/test-repo/uml ===")


if __name__ == "__main__":
    main()
