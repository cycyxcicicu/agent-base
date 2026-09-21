"""
Deterministic & Semantic Assertion Engine.
Học hỏi từ: promptfoo (Assertion Matrix: regex, contains, json-schema, length, equals).
"""

import re
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union


@dataclass
class AssertionResult:
    passed: bool
    assertion_type: str
    target: Any
    actual: Any
    reason: str


class AssertionEngine:
    """Bộ thẩm định đầu ra tự động cho AI Agent."""

    @staticmethod
    def assert_contains(text: str, substring: str, case_sensitive: bool = False) -> AssertionResult:
        """Kiểm tra văn bản có chứa chuỗi con không."""
        haystack = text if case_sensitive else text.lower()
        needle = substring if case_sensitive else substring.lower()
        passed = needle in haystack
        reason = "Khớp chuỗi con thành công" if passed else f"Không tìm thấy '{substring}' trong đầu ra"
        return AssertionResult(passed, "contains", substring, text[:80] + "...", reason)

    @staticmethod
    def assert_not_contains(text: str, substring: str, case_sensitive: bool = False) -> AssertionResult:
        """Kiểm tra văn bản tuyệt đối không chứa chuỗi cấm."""
        haystack = text if case_sensitive else text.lower()
        needle = substring if case_sensitive else substring.lower()
        passed = needle not in haystack
        reason = "Không chứa chuỗi cấm" if passed else f"Đầu ra vi phạm khi chứa '{substring}'"
        return AssertionResult(passed, "not_contains", substring, text[:80] + "...", reason)

    @staticmethod
    def assert_regex(text: str, pattern: str) -> AssertionResult:
        """Kiểm tra khớp biểu thức chính quy (Regex)."""
        match = re.search(pattern, text)
        passed = match is not None
        reason = f"Khớp regex '{pattern}'" if passed else f"Không khớp mẫu regex '{pattern}'"
        return AssertionResult(passed, "regex", pattern, text[:80] + "...", reason)

    @staticmethod
    def assert_json_valid(text: str, required_keys: Optional[List[str]] = None) -> AssertionResult:
        """Kiểm tra tính hợp lệ của JSON và các trường bắt buộc."""
        # Bóc tách JSON nếu nằm trong markdown codeblock ```json ... ```
        json_str = text.strip()
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()

        try:
            parsed = json.loads(json_str)
            if not isinstance(parsed, dict):
                return AssertionResult(False, "json_valid", "dict", type(parsed).__name__, "JSON không phải là một Object/Dict")

            if required_keys:
                missing = [k for k in required_keys if k not in parsed]
                if missing:
                    return AssertionResult(False, "json_valid", required_keys, list(parsed.keys()), f"Thiếu các trường bắt buộc: {missing}")

            return AssertionResult(True, "json_valid", required_keys or "valid_json", "valid", "JSON hợp lệ và đủ trường yêu cầu")
        except Exception as e:
            return AssertionResult(False, "json_valid", "valid_json", "syntax_error", f"Lỗi cú pháp JSON: {e}")

    @staticmethod
    def assert_length_range(text: str, min_chars: int = 0, max_chars: int = 1000000) -> AssertionResult:
        """Kiểm tra độ dài ký tự nằm trong phạm vi cho phép."""
        length = len(text)
        passed = min_chars <= length <= max_chars
        reason = f"Độ dài hợp lệ ({length} ký tự)" if passed else f"Độ dài {length} nằm ngoài ngưỡng [{min_chars}, {max_chars}]"
        return AssertionResult(passed, "length_range", (min_chars, max_chars), length, reason)
