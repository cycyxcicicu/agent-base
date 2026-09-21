"""
Advanced Red-Teaming Security Scanner & Deobfuscation Engine.
Học hỏi từ: promptfoo (Plugins: promptInjection, asciiSmuggling, sqlInjection, shellInjection, ssrf, dataExfil, excessiveAgency, pii).
"""

import re
import base64
import codecs
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple


@dataclass
class SecurityIssue:
    category: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    description: str
    matched_content: str


class Deobfuscator:
    """Bộ giải mã chống các kỹ thuật lách luật (Evasion & Obfuscation Attacks)."""

    LEET_MAP = str.maketrans({
        "@": "a", "4": "a", "8": "b", "3": "e", "1": "i", "!": "i",
        "0": "o", "5": "s", "$": "s", "7": "t", "+": "t"
    })

    ZERO_WIDTH_PATTERN = re.compile(r"[\u200B\u200C\u200D\uFEFF\u200E\u200F]")
    UNICODE_TAG_PATTERN = re.compile(r"[\U000E0000-\U000E007F]")
    BIDI_OVERRIDE_PATTERN = re.compile(r"[\u202A-\u202E\u2066-\u2069]")

    @classmethod
    def strip_zero_width(cls, text: str) -> str:
        return cls.ZERO_WIDTH_PATTERN.sub("", text)

    @classmethod
    def extract_ascii_smuggling(cls, text: str) -> str:
        """Giải mã chữ ẩn Unicode Tag block (ASCII smuggling E0000-E007F)."""
        tag_chars = cls.UNICODE_TAG_PATTERN.findall(text)
        if not tag_chars:
            return ""
        decoded = []
        for c in tag_chars:
            code = ord(c)
            if 0xE0020 <= code <= 0xE007E:
                decoded.append(chr(code - 0xE0000))
        return "".join(decoded)

    @classmethod
    def strip_bidi(cls, text: str) -> str:
        return cls.BIDI_OVERRIDE_PATTERN.sub("", text)

    @classmethod
    def normalize_leetspeak(cls, text: str) -> str:
        return text.translate(cls.LEET_MAP)

    @classmethod
    def decode_rot13(cls, text: str) -> str:
        try:
            return codecs.decode(text, "rot_13")
        except Exception:
            return text

    @classmethod
    def extract_and_decode_base64(cls, text: str) -> List[str]:
        """Trích xuất và giải mã các khối Base64 tiềm năng trong chuỗi."""
        decoded_strings = []
        # Bắt các chuỗi base64 có hoặc không có dấu padding '='
        b64_matches = re.findall(r"(?:^|[\s:=])([A-Za-z0-9+/]{16,}={0,2})(?:[\s\"']|$)", text)
        for candidate in b64_matches:
            try:
                decoded = base64.b64decode(candidate.strip()).decode("utf-8", errors="ignore")
                if len(decoded) > 8 and any(c.isalpha() for c in decoded):
                    decoded_strings.append(decoded)
            except Exception:
                pass
        return decoded_strings


class RedTeamScanner:
    """Bộ quét đối kháng đa tầng cho AI Prompts, Agent Outputs và Code Changes."""

    # 1. Prompt Injection & Jailbreak (English & Vietnamese)
    INJECTION_PATTERNS = [
        (r"(?i)\bignore\s+(all\s+)?(previous|prior|above|system)?\s*(instructions|rules|directives|prompts|guidelines)\b", "Prompt Injection: Yêu cầu bỏ qua chỉ thị/quy tắc"),
        (r"(?i)\bdisregard\s+(the\s+)?(above|system\s+prompt|rules|previous\s+instructions)\b", "Prompt Injection: Yêu cầu coi thường system prompt/rules"),
        (r"(?i)\bbypass\s+(all\s+)?(safety|security)?\s*(guidelines|checks|rules|filters)\b", "Jailbreak: Yêu cầu phá vỡ hàng rào an toàn/kiểm tra"),
        (r"(?i)\byou\s+are\s+now\s+(in\s+)?(developer\s+mode|unrestricted|dan\s+mode)\b", "Jailbreak: Ép chuyển sang Developer/DAN mode"),
        (r"(?i)\bsystem\s+override\s*:\s*admin\b", "Jailbreak: Giả mạo quyền quản trị viên"),
        (r"(?i)\b(bỏ\s+qua|quên|hủy)\s+(toàn\s+bộ\s+|tất\s+cả\s+|mọi\s+)?(hướng\s+dẫn|chỉ\s+dẫn|chỉ\s+thị|quy\s+tắc|câu\s+lệnh|lệnh|prompt|yêu\s+cầu)\s*(trước|cũ|hệ\s+thống|trước\s+đó)?\b", "Prompt Injection: Yêu cầu bỏ qua chỉ thị (Tiếng Việt)"),
        (r"(?i)\btừ\s+bây\s+giờ\s+bạn\s+là\b", "Jailbreak: Ép đổi nhân cách (Tiếng Việt)"),
        (r"(?i)\bquên\s+(hết|toàn\s+bộ|tất\s+cả|mọi)\s+(lệnh|quy\s+tắc|chỉ\s+thị|chỉ\s+dẫn|hướng\s+dẫn)\b", "Prompt Injection: Quên hết quy tắc (Tiếng Việt)"),
        (r"(?i)\bkhông\s+tuân\s+theo\s+(bất\s+kỳ\s+|mọi\s+|các\s+)?(chỉ\s+dẫn|quy\s+tắc|chỉ\s+thị)\b", "Prompt Injection: Không tuân theo quy tắc (Tiếng Việt)"),
    ]

    # 2. SQL Injection
    SQLI_PATTERNS = [
        (r"(?i)\bUNION\s+(ALL\s+)?SELECT\b", "SQL Injection: UNION SELECT attack"),
        (r"'\s*OR\s+'1'\s*=\s*'1", "SQL Injection: Tautology bypass ('1'='1)"),
        (r"(?i);\s*(DROP\s+TABLE|ALTER\s+TABLE|DELETE\s+FROM)\b", "SQL Injection: Phá hủy cơ sở dữ liệu"),
    ]

    # 3. Shell Injection & Excessive Agency
    SHELL_PATTERNS = [
        (r"(?i)\brm\s+-rf\s+[/~]", "Excessive Agency: Lệnh xóa toàn bộ file hệ điều hành (rm -rf /)"),
        (r"(?i)\bformat\s+[c-z]:\s+/fs", "Excessive Agency: Lệnh format ổ đĩa windows"),
        (r"(?i)(?:;\s*|\|\s*|`)\s*(?:bash|sh|cmd\.exe|powershell)\b", "Shell Injection: Kích hoạt shell con tùy ý"),
    ]

    # 4. Path Traversal & File Disclosure (open-code-review)
    TRAVERSAL_PATTERNS = [
        (r"(?:\.\./|\.\.\\){2,}", "Path Traversal: Nỗ lực đọc file ngoài thư mục dự án (../)"),
        (r"(?i)/etc/(passwd|shadow|hosts)", "File Disclosure: Cố gắng đọc file hệ thống linux"),
    ]

    # 5. SSRF (Server-Side Request Forgery - Cloud Metadata)
    SSRF_PATTERNS = [
        (r"(?i)https?://(?:169\.254\.169\.254|metadata\.google\.internal|100\.100\.100\.200)", "SSRF: Nỗ lực tấn công Cloud Metadata Endpoint"),
    ]

    # 6. PII & Secrets Leaks
    PII_PATTERNS = [
        (r"(?i)(?:api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*['\"]?([a-zA-Z0-9_\-]{20,})['\"]?", "PII/Secret: Để lộ API Key hoặc Access Token"),
        (r"ghp_[a-zA-Z0-9]{36}", "Secret: Để lộ GitHub Personal Access Token"),
        (r"ey[a-zA-Z0-9_-]{10,}\.ey[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}", "Secret: Để lộ JWT Token"),
        (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", "PII: Phát hiện địa chỉ Email người dùng"),
    ]

    # 7. Markdown Exfiltration
    EXFIL_PATTERNS = [
        (r"!\[.*?\]\(https?://[^\s)]+(?:\?|&)(?:token|pwd|pass|data|cookie|key)=.*?\)", "Data Exfiltration: Tuồn dữ liệu nhạy cảm qua thẻ ảnh Markdown"),
    ]

    @classmethod
    def scan_text(cls, text: str) -> List[SecurityIssue]:
        """Quét toàn diện chuỗi văn bản, tự động xử lý deobfuscation chống che giấu."""
        issues: List[SecurityIssue] = []

        # 1. Phát hiện ký tự tàng hình (Zero-Width)
        if len(text) != len(Deobfuscator.strip_zero_width(text)):
            issues.append(SecurityIssue(
                category="ascii_smuggling",
                severity="HIGH",
                description="Phát hiện ký tự Unicode tàng hình (Zero-Width) dùng để ẩn prompt",
                matched_content="[Zero-Width Characters Detected]"
            ))

        # 2. Phát hiện Unicode Tag block (ASCII Smuggling: E0000-E007F)
        smuggled_text = Deobfuscator.extract_ascii_smuggling(text)
        if smuggled_text:
            issues.append(SecurityIssue(
                category="ascii_smuggling",
                severity="CRITICAL",
                description=f"Phát hiện ASCII Smuggling qua Unicode Tags block (Nội dung ẩn: '{smuggled_text[:40]}...')",
                matched_content=smuggled_text[:100]
            ))

        # 3. Phát hiện BiDi Override (U+202A - U+202E)
        if len(text) != len(Deobfuscator.strip_bidi(text)):
            issues.append(SecurityIssue(
                category="bidi_override",
                severity="HIGH",
                description="Phát hiện ký tự BiDi Override (U+202E/202D) đảo ngược hướng văn bản để lừa mô hình",
                matched_content="[BiDi Override Characters Detected]"
            ))

        clean_text = Deobfuscator.strip_zero_width(Deobfuscator.strip_bidi(text))
        leet_text = Deobfuscator.normalize_leetspeak(clean_text)
        b64_decoded = Deobfuscator.extract_and_decode_base64(clean_text)

        candidates = [clean_text, leet_text] + b64_decoded
        if smuggled_text:
            candidates.append(smuggled_text)

        for cand in candidates:
            # Quét Prompt Injection
            for pattern, desc in cls.INJECTION_PATTERNS:
                m = re.search(pattern, cand)
                if m:
                    issues.append(SecurityIssue("prompt_injection", "CRITICAL", desc, m.group(0)))

            # Quét SQL Injection
            for pattern, desc in cls.SQLI_PATTERNS:
                m = re.search(pattern, cand)
                if m:
                    issues.append(SecurityIssue("sql_injection", "CRITICAL", desc, m.group(0)))

            # Quét Shell Injection / Excessive Agency
            for pattern, desc in cls.SHELL_PATTERNS:
                m = re.search(pattern, cand)
                if m:
                    issues.append(SecurityIssue("excessive_agency", "CRITICAL", desc, m.group(0)))

            # Quét Path Traversal
            for pattern, desc in cls.TRAVERSAL_PATTERNS:
                m = re.search(pattern, cand)
                if m:
                    issues.append(SecurityIssue("path_traversal", "HIGH", desc, m.group(0)))

            # Quét SSRF (phân định Metadata vs Localhost)
            for pattern, desc in cls.SSRF_PATTERNS:
                m = re.search(pattern, cand)
                if m:
                    sev = "CRITICAL" if ("169.254" in m.group(0) or "metadata" in m.group(0)) else "MEDIUM"
                    issues.append(SecurityIssue("ssrf", sev, desc, m.group(0)))

            # Quét PII (loại trừ example.com)
            for pattern, desc in cls.PII_PATTERNS:
                m = re.search(pattern, cand)
                if m:
                    matched = m.group(0)
                    if "@example.com" in matched.lower() or "@test.com" in matched.lower():
                        continue
                    issues.append(SecurityIssue("pii_leak", "HIGH", desc, matched[:30] + "..."))

            # Quét Markdown Exfil
            for pattern, desc in cls.EXFIL_PATTERNS:
                m = re.search(pattern, cand)
                if m:
                    issues.append(SecurityIssue("data_exfiltration", "CRITICAL", desc, m.group(0)))

        # Lọc trùng
        unique_issues = []
        seen = set()
        for iss in issues:
            key = (iss.category, iss.description)
            if key not in seen:
                seen.add(key)
                unique_issues.append(iss)

        return unique_issues
