"""
Technical Debt Ledger.
Học hỏi từ: ponytail (Sổ cái nợ kỹ thuật, kiểm tra trần chịu đựng và xuất báo cáo).
"""

from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from .parser import DebtParser, DebtItem


class DebtLedger:
    """Quản lý và kết xuất sổ cái nợ kỹ thuật tập trung."""

    def __init__(self, root_dir: Path):
        self.root_dir = Path(root_dir)
        self.items: List[DebtItem] = []

    def harvest(self) -> List[DebtItem]:
        """Thu hoạch toàn bộ các khoản nợ kỹ thuật từ codebase."""
        self.items = DebtParser.scan_directory(self.root_dir)
        return self.items

    def render_markdown(self) -> str:
        """Xuất bảng tổng hợp Markdown cho docs/DEBT.md."""
        lines = [
            "# Sổ Cái Nợ Kỹ Thuật (Technical Debt Ledger)",
            "",
            "> Tự động thu hoạch bởi `agent_core/debt/ledger.py` theo triết lý Ponytail.",
            f"> Tổng số khoản nợ được ghi nhận: **{len(self.items)}**",
            "",
            "| Vị trí (File:Dòng) | Đi Tắt (Shortcut) | Trần Chịu Đựng (Ceiling) | Lộ Trình Nâng Cấp (Upgrade) |",
            "| :--- | :--- | :--- | :--- |"
        ]

        if not self.items:
            lines.append("| *(Không có nợ)* | Hệ thống sạch bóng | N/A | N/A |")
        else:
            for item in self.items:
                # Rút gọn path tương đối
                try:
                    rel_path = Path(item.file_path).relative_to(self.root_dir)
                except Exception:
                    rel_path = Path(item.file_path).name
                loc = f"`{rel_path}:{item.line_number}`"
                lines.append(f"| {loc} | {item.shortcut} | **{item.ceiling}** | {item.upgrade_path} |")

        lines.append("")
        return "\n".join(lines)

    def audit_ceilings(self, current_metrics: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Kiểm toán toàn bộ trần chịu đựng (Ceiling):
        - Phát hiện trần thời gian hết hạn (Ngày hết hạn < Hôm nay)
        - Phát hiện trần số lượng vượt ngưỡng (Ví dụ: metrics['requests_per_sec'] > ceiling)
        """
        import datetime
        import re

        if not self.items:
            self.harvest()

        metrics = current_metrics or {}
        today = datetime.date.today()
        breaches = []

        for item in self.items:
            ceiling_str = item.ceiling.strip()

            # 1. Kiểm tra trần ngày tháng (YYYY-MM-DD)
            date_match = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", ceiling_str)
            if date_match:
                try:
                    exp_date = datetime.date.fromisoformat(date_match.group(1))
                    if exp_date < today:
                        breaches.append({
                            "item": item,
                            "type": "DATE_EXPIRED",
                            "message": f"Nợ kỹ thuật tại {Path(item.file_path).name}:{item.line_number} đã hết hạn vào ngày {exp_date}!"
                        })
                except Exception:
                    pass

            # 2. Kiểm tra trần tải lượng (Số lượng: vd 50 req/s, 100 users)
            num_match = re.search(r"(\d+)\s*([a-zA-Z_/]+)?", ceiling_str)
            if num_match:
                limit = int(num_match.group(1))
                unit = (num_match.group(2) or "").lower()
                for metric_key, val in metrics.items():
                    if isinstance(val, (int, float)) and val > limit:
                        # Kiểm tra khớp đơn vị hoặc tên chỉ số
                        if not unit or unit in metric_key.lower():
                            breaches.append({
                                "item": item,
                                "type": "THRESHOLD_EXCEEDED",
                                "message": f"Chỉ số {metric_key}={val} đã vượt quá trần chịu đựng {limit} ({item.shortcut})"
                            })

        return breaches

    def verify_pre_commit_gate(self, current_metrics: Optional[Dict[str, Any]] = None, force_harvest: bool = False) -> Tuple[bool, str]:
        """
        Cổng chặn Pre-Commit: Trả về False và thông báo lỗi nếu có khoản nợ nào vượt trần.
        """
        if force_harvest or not self.items:
            self.harvest()
        breaches = self.audit_ceilings(current_metrics)
        if not breaches:
            return True, f"Hợp lệ: Toàn bộ {len(self.items)} khoản nợ đều nằm trong trần chịu đựng."

        details = "\n".join([f"  ❌ [{b['type']}] {b['message']}" for b in breaches])
        return False, f"CẢNH BÁO PRE-COMMIT: Phát hiện {len(breaches)} khoản nợ vi phạm trần chịu đựng:\n{details}"

    def write_to_file(self, target_file: Optional[Path] = None):
        """Ghi kết quả ra file markdown (mặc định docs/DEBT.md)."""
        out_path = target_file or (self.root_dir / "docs" / "DEBT.md")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(self.render_markdown(), encoding="utf-8")

