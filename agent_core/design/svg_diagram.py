"""
Editorial SVG Architecture Diagram Generator.
Học hỏi từ: diagram-design (Vector SVG, Paper Masking, Color Tiers, Arrow Hop collision avoidance).
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict, Any


@dataclass
class Box:
    box_id: str
    label: str
    subtext: str
    x: int
    y: int
    width: int = 180
    height: int = 70
    color_tier: str = "primary"  # primary, secondary, accent, neutral


@dataclass
class Connection:
    from_id: str
    to_id: str
    label: str = ""
    dashed: bool = False


class DiagramRenderer:
    """Trình tạo sơ đồ kỹ thuật và kiến trúc SVG chuẩn biên tập."""

    COLOR_MAP = {
        "primary": {"bg": "#eff6ff", "border": "#3b82f6", "text": "#1e3a8a"},
        "secondary": {"bg": "#f0fdf4", "border": "#22c55e", "text": "#14532d"},
        "accent": {"bg": "#fef3c7", "border": "#f59e0b", "text": "#78350f"},
        "neutral": {"bg": "#f8fafc", "border": "#94a3b8", "text": "#334155"}
    }

    @classmethod
    def render_svg(cls, title: str, boxes: List[Box], connections: List[Connection], width: int = 800, height: int = 500) -> str:
        box_map = {b.box_id: b for b in boxes}
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" style="font-family: system-ui, -apple-system, sans-serif; background: #ffffff;">',
            '  <defs>',
            '    <filter id="paper-mask" x="-10%" y="-10%" width="120%" height="120%">',
            '      <feFlood flood-color="#ffffff" result="bg"/>',
            '      <feMerge><feMergeNode in="bg"/><feMergeNode in="SourceGraphic"/></feMerge>',
            '    </filter>',
            '    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
            '      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#64748b"/>',
            '    </marker>',
            '  </defs>',
            f'  <text x="30" y="40" font-size="20" font-weight="700" fill="#0f172a">{title}</text>',
            '  <g id="connections">'
        ]


        # 1. Vẽ các đường nối Connections
        for conn in connections:
            from_b = box_map.get(conn.from_id)
            to_b = box_map.get(conn.to_id)
            if not from_b or not to_b:
                continue

            x1 = from_b.x + from_b.width
            y1 = from_b.y + (from_b.height // 2)
            x2 = to_b.x
            y2 = to_b.y + (to_b.height // 2)

            dash_attr = ' stroke-dasharray="5,5"' if conn.dashed else ''
            svg_parts.append(
                f'    <path d="M {x1} {y1} C {(x1+x2)//2} {y1}, {(x1+x2)//2} {y2}, {x2} {y2}" stroke="#64748b" stroke-width="2" fill="none"{dash_attr} marker-end="url(#arrow)"/>'
            )
            if conn.label:
                mid_x = (x1 + x2) // 2
                mid_y = (y1 + y2) // 2 - 8
                svg_parts.append(
                    f'    <text x="{mid_x}" y="{mid_y}" font-size="11" fill="#64748b" text-anchor="middle">{conn.label}</text>'
                )

        svg_parts.append('  </g>')
        svg_parts.append('  <g id="boxes">')

        # 2. Vẽ các Box Node
        for b in boxes:
            style = cls.COLOR_MAP.get(b.color_tier, cls.COLOR_MAP["neutral"])
            svg_parts.append(f'    <g id="{b.box_id}" transform="translate({b.x}, {b.y})">')
            svg_parts.append(
                f'      <rect width="{b.width}" height="{b.height}" rx="8" fill="{style["bg"]}" stroke="{style["border"]}" stroke-width="2"/>'
            )
            svg_parts.append(
                f'      <text x="{b.width//2}" y="{26 if b.subtext else b.height//2 + 5}" font-size="14" font-weight="600" fill="{style["text"]}" text-anchor="middle">{b.label}</text>'
            )
            if b.subtext:
                svg_parts.append(
                    f'      <text x="{b.width//2}" y="48" font-size="11" fill="{style["text"]}" opacity="0.8" text-anchor="middle">{b.subtext}</text>'
                )
            svg_parts.append('    </g>')

        svg_parts.append('  </g>')
        svg_parts.append('</svg>')

        return "\n".join(svg_parts)

    @classmethod
    def render_multi_lane_pipeline(cls, title: str, stages: List[Dict[str, str]], width: int = 900, height: int = 300) -> str:
        """Tự động bố cục các bước tuần tự theo các làn (Multi-lane) ngang với khoảng cách chuẩn hóa."""
        boxes = []
        connections = []
        n = len(stages)
        box_w = 160
        box_h = 65
        gap = max(40, (width - 60 - n * box_w) // max(1, n - 1)) if n > 1 else 0
        y = height // 2 - box_h // 2

        for idx, stage in enumerate(stages):
            x = 30 + idx * (box_w + gap)
            b = Box(
                box_id=stage.get("id", f"stage_{idx}"),
                label=stage.get("label", f"Stage {idx+1}"),
                subtext=stage.get("subtext", ""),
                x=x,
                y=y,
                width=box_w,
                height=box_h,
                color_tier=stage.get("color_tier", "primary")
            )
            boxes.append(b)
            if idx > 0:
                connections.append(Connection(
                    from_id=boxes[idx-1].box_id,
                    to_id=b.box_id,
                    label=stage.get("conn_label", "")
                ))

        return cls.render_svg(title, boxes, connections, width=width, height=height)

