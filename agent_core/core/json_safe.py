"""
Safe JSON Serializer & Deserializer.
Học hỏi từ: gemini_webapi & open-code-review
"""

import json as std_json
from typing import Any, Union, Optional

try:
    import orjson
    HAS_ORJSON = True
except ImportError:
    HAS_ORJSON = False


class SafeJsonWrapper:
    """Lớp bọc JSON an toàn: ưu tiên orjson (siêu tốc), tự động fallback sang stdlib json khi gặp UTF-8 dị thường."""

    @staticmethod
    def loads(s: Union[str, bytes], *args, **kwargs) -> Any:
        if HAS_ORJSON:
            try:
                return orjson.loads(s)
            except Exception:
                pass
        
        if isinstance(s, bytes):
            s = s.decode("utf-8", errors="replace")
        return std_json.loads(s, *args, **kwargs)

    @staticmethod
    def dumps(obj: Any, indent: Optional[int] = None, **kwargs) -> str:
        if HAS_ORJSON and indent is None:
            try:
                return orjson.dumps(obj).decode("utf-8")
            except Exception:
                pass
        return std_json.dumps(obj, indent=indent, ensure_ascii=False, **kwargs)


safe_json = SafeJsonWrapper
