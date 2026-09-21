"""
3-Tier Design Token Resolution & Compiler.
Học hỏi từ: ui-ux-pro-max-skill (Primitive ➔ Semantic ➔ Component ➔ CSS / Tailwind).
"""

import re
import json
from typing import Dict, Any, Optional


class DesignTokens:
    def __init__(self, raw_tokens: Dict[str, Any]):
        self.raw = raw_tokens
        self.resolved: Dict[str, str] = {}
        self.resolve_all()

    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = "") -> Dict[str, Any]:
        items: Dict[str, Any] = {}
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(self._flatten_dict(v, new_key))
            else:
                items[new_key] = v
        return items

    def resolve_all(self):
        """Giải quyết toàn bộ các biến lồng nhau {primitive.color.blue.600}."""
        flat = self._flatten_dict(self.raw)
        
        # Vòng lặp giải quyết tham chiếu đệ quy
        resolved = {}
        ref_pattern = re.compile(r"\{([^}]+)\}")

        for key, val in flat.items():
            curr_val = str(val)
            for _ in range(10):  # Tối đa 10 cấp dereference
                match = ref_pattern.search(curr_val)
                if not match:
                    break
                ref_key = match.group(1).strip()
                target_val = flat.get(ref_key, flat.get(ref_key.lower()))
                if target_val is not None:
                    curr_val = curr_val.replace(match.group(0), str(target_val))
                else:
                    break
            resolved[key] = curr_val

        self.resolved = resolved


class TokenCompiler:
    """Biên dịch Design Tokens thành CSS Variables hoặc Tailwind config."""

    @staticmethod
    def to_css_variables(tokens: DesignTokens, selector: str = ":root") -> str:
        lines = [f"{selector} {{"]
        for k, v in sorted(tokens.resolved.items()):
            # Chuyển đổi key dạng semantic.color.primary thành --semantic-color-primary
            var_name = "--" + k.replace(".", "-").lower()
            lines.append(f"  {var_name}: {v};")
        lines.append("}")
        return "\n".join(lines)

    @staticmethod
    def to_tailwind_colors(tokens: DesignTokens) -> Dict[str, Any]:
        """Trích xuất màu sắc cấu hình Tailwind."""
        colors = {}
        for k, v in tokens.resolved.items():
            if "color" in k.lower():
                clean_name = k.replace("primitive.color.", "").replace("semantic.color.", "").replace(".", "-")
                colors[clean_name] = v
        return colors
