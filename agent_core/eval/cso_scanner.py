"""
src/eval/cso_scanner.py
CSO (Chief Security Officer) Static Security Audit Engine.
Inspired by gstack /cso: "Evidence before assurance".

Scans codebase for:
- Secrets & Credentials in code (API keys, Private keys, Hardcoded passwords)
- Command Injection (os.system, shell=True with variables)
- SQL Injection (string formatting in execute())
- Path Traversal (opening files without base path containment)
- Insecure Deserialization (unsafe pickle/yaml)
"""

import re
import ast
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class CsoFinding:
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str  # SECRET, COMMAND_INJECTION, SQLI, PATH_TRAVERSAL, INSECURE_DESERIALIZATION
    file_path: str
    line_number: int
    rule_id: str
    message: str
    snippet: str
    recommendation: str

class CsoScanner:
    """Static application security testing (SAST) scanner for agent workflows."""

    SECRET_PATTERNS = [
        ("SECRET-01", "CRITICAL", r"(?i)[\"']?(api[_-]?key|secret[_-]?key|auth[_-]?token)[\"']?\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]",
         "Hardcoded API key or secret token found."),
        ("SECRET-02", "CRITICAL", r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----",
         "Hardcoded Private Key found."),
        ("SECRET-03", "HIGH", r"(?i)[\"']?(password|passwd|pwd)[\"']?\s*[:=]\s*['\"][^'\"]{4,}['\"]",
         "Potential hardcoded password found."),
        ("SECRET-04", "CRITICAL", r"(?i)^\s*(?:export\s+)?[A-Z0-9_]*(?:api[_-]?key|secret[_-]?key|auth[_-]?token|access[_-]?token)\s*=\s*(?!['\"]?(?:your_|fake_|test_|dummy_|sk-ant-dummy|none|<)[A-Za-z0-9_\-]*)[A-Za-z0-9_\-\.]{16,}\s*$",
         "Hardcoded unquoted or dotenv-style API key / secret token found."),
    ]

    COMMAND_INJECTION_PATTERNS = [
        ("INJ-01", "CRITICAL", r"(?i)os\.system\(f?['\"].*?\{.*?\}",
         "Dynamic os.system call with format string allows command injection."),
        ("INJ-02", "CRITICAL", r"(?i)subprocess\.(Popen|run|call|check_call|check_output)\(.*shell\s*=\s*True",
         "subprocess executed with shell=True and potential external input."),
        ("INJ-03", "CRITICAL", r"(?i)\beval\s*\(",
         "Dynamic eval() call can execute arbitrary code."),
        ("INJ-04", "CRITICAL", r"(?i)\bexec\s*\(",
         "Dynamic exec() call can execute arbitrary code."),
        ("INJ-05", "CRITICAL", r"(?i)\bos\.popen\s*\(",
         "os.popen() executes commands through a shell, allowing command injection."),
    ]

    SQLI_PATTERNS = [
        ("SQLI-01", "CRITICAL", r"(?i)\.execute\(f['\"].*?(SELECT|INSERT|UPDATE|DELETE).*?\{",
         "SQL query constructed via f-string without parameterized variables."),
        ("SQLI-02", "HIGH", r"(?i)\.execute\(['\"].*?(SELECT|INSERT|UPDATE|DELETE).*?%\s*\(",
         "SQL query constructed via % formatting without DB API parameters."),
    ]

    PATH_TRAVERSAL_PATTERNS = [
        ("TRAVERSAL-01", "HIGH", r"(?i)open\(f?['\"].*?\{.*?\}",
         "Dynamic file open without visible path sanitization or within_base check."),
    ]

    DESERIALIZATION_PATTERNS = [
        ("DESER-01", "HIGH", r"(?i)pickle\.(loads|load)\(",
         "Insecure pickle deserialization allows arbitrary code execution."),
        ("DESER-02", "HIGH", r"(?i)yaml\.load\([^,)]+\)",
         "Insecure yaml.load() without SafeLoader allows arbitrary code execution."),
    ]

    INSECURE_CONFIG_PATTERNS = [
        ("INSEC-01", "HIGH", r"(?i)\bverify\s*=\s*False\b",
         "TLS certificate verification disabled (verify=False) exposes network traffic to MITM."),
    ]

    WEAK_CRYPTO_PATTERNS = [
        ("CRYPTO-01", "MEDIUM", r"(?i)\bhashlib\.md5\s*\(",
         "MD5 is cryptographically weak and prone to hash collisions."),
    ]

    # Ignore testing mocks and documentation
    EXCLUDE_PATTERNS = [
        r"[\\/]tests[\\/]",
        r"[\\/]scratch[\\/]",
        r"[\\/]docs[\\/]",
        r"[\\/]\.git([\\/]|$)",
        r"\.venv",
        r"__pycache__",
        r"\.example\.",
        r"\.sample\."
    ]

    def __init__(self, root_dir: Optional[Path] = None):
        self.root_dir = root_dir or Path.cwd()

    def should_skip(self, file_path: Path) -> bool:
        path_str = str(file_path.resolve())
        for pat in self.EXCLUDE_PATTERNS:
            if re.search(pat, path_str):
                return True
        return False

    def _ast_scan(self, content: str, file_path: str, lines: List[str]) -> Optional[List[CsoFinding]]:
        """Perform Python AST analysis to catch multi-line calls and syntactic security flaws without false positives."""
        findings: List[CsoFinding] = []
        try:
            tree = ast.parse(content)
        except Exception:
            return None

        def get_snippet(lineno: int) -> str:
            if 1 <= lineno <= len(lines):
                return lines[lineno - 1].strip()
            return ""

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                # 1. Attribute calls (subprocess.*, os.popen, hashlib.md5, etc.)
                if isinstance(func, ast.Attribute):
                    func_name = func.attr
                    mod_name = func.value.id if isinstance(func.value, ast.Name) else ""
                    if mod_name == "subprocess" and func_name in {"run", "Popen", "call", "check_call", "check_output"}:
                        for kw in node.keywords:
                            if kw.arg == "shell":
                                is_true = False
                                if isinstance(kw.value, ast.Constant) and kw.value.value is True:
                                    is_true = True
                                elif getattr(kw.value, "id", None) == "True":
                                    is_true = True
                                if is_true:
                                    findings.append(CsoFinding(
                                        severity="CRITICAL",
                                        category="COMMAND_INJECTION",
                                        file_path=file_path,
                                        line_number=node.lineno,
                                        rule_id="INJ-02",
                                        message="subprocess executed with shell=True allows command injection.",
                                        snippet=get_snippet(node.lineno),
                                        recommendation=self._get_recommendation("INJ-02")
                                    ))
                    elif mod_name == "os" and func_name == "popen":
                        findings.append(CsoFinding(
                            severity="CRITICAL",
                            category="COMMAND_INJECTION",
                            file_path=file_path,
                            line_number=node.lineno,
                            rule_id="INJ-05",
                            message="os.popen() executes commands through a shell, allowing command injection.",
                            snippet=get_snippet(node.lineno),
                            recommendation=self._get_recommendation("INJ-05")
                        ))
                    elif mod_name == "hashlib" and func_name == "md5":
                        findings.append(CsoFinding(
                            severity="MEDIUM",
                            category="WEAK_CRYPTO",
                            file_path=file_path,
                            line_number=node.lineno,
                            rule_id="CRYPTO-01",
                            message="MD5 is cryptographically weak and prone to hash collisions.",
                            snippet=get_snippet(node.lineno),
                            recommendation=self._get_recommendation("CRYPTO-01")
                        ))

                    # verify=False check
                    for kw in node.keywords:
                        if kw.arg == "verify":
                            is_false = False
                            if isinstance(kw.value, ast.Constant) and kw.value.value is False:
                                is_false = True
                            elif getattr(kw.value, "id", None) == "False":
                                is_false = True
                            if is_false:
                                findings.append(CsoFinding(
                                    severity="HIGH",
                                    category="INSECURE_CONFIG",
                                    file_path=file_path,
                                    line_number=node.lineno,
                                    rule_id="INSEC-01",
                                    message="TLS certificate verification disabled (verify=False) exposes traffic to MITM.",
                                    snippet=get_snippet(node.lineno),
                                    recommendation=self._get_recommendation("INSEC-01")
                                ))

                # 2. Direct calls (eval, exec)
                elif isinstance(func, ast.Name):
                    if func.id == "eval":
                        findings.append(CsoFinding(
                            severity="CRITICAL",
                            category="COMMAND_INJECTION",
                            file_path=file_path,
                            line_number=node.lineno,
                            rule_id="INJ-03",
                            message="Dynamic eval() call can execute arbitrary code.",
                            snippet=get_snippet(node.lineno),
                            recommendation=self._get_recommendation("INJ-03")
                        ))
                    elif func.id == "exec":
                        findings.append(CsoFinding(
                            severity="CRITICAL",
                            category="COMMAND_INJECTION",
                            file_path=file_path,
                            line_number=node.lineno,
                            rule_id="INJ-04",
                            message="Dynamic exec() call can execute arbitrary code.",
                            snippet=get_snippet(node.lineno),
                            recommendation=self._get_recommendation("INJ-04")
                        ))

        return findings

    def scan_file_content(self, content: str, file_path: str) -> List[CsoFinding]:
        findings: List[CsoFinding] = []
        lines = content.splitlines()
        seen = set()

        ast_covered_rules = {"INJ-02", "INJ-03", "INJ-04", "INJ-05", "INSEC-01", "CRYPTO-01"}
        parsed_ast_successfully = False

        # 1. AST Analysis for Python files
        if file_path.endswith(".py") or "\nimport " in content or "\ndef " in content:
            ast_res = self._ast_scan(content, file_path, lines)
            if ast_res is not None:
                parsed_ast_successfully = True
                for f in ast_res:
                    key = (f.rule_id, f.line_number)
                    if key not in seen:
                        seen.add(key)
                        findings.append(f)

        # 2. Multi-line regex scan fallback if AST wasn't used
        if not parsed_ast_successfully:
            for m in re.finditer(r"(?is)subprocess\.(Popen|run|call|check_call|check_output)\s*\([^)]*?shell\s*=\s*True", content):
                line_num = content[:m.start()].count("\n") + 1
                key = ("INJ-02", line_num)
                if key not in seen:
                    seen.add(key)
                    snippet = lines[line_num - 1].strip() if 1 <= line_num <= len(lines) else ""
                    findings.append(CsoFinding(
                        severity="CRITICAL",
                        category="COMMAND_INJECTION",
                        file_path=file_path,
                        line_number=line_num,
                        rule_id="INJ-02",
                        message="subprocess executed with shell=True allows command injection.",
                        snippet=snippet,
                        recommendation=self._get_recommendation("INJ-02")
                    ))

        # 3. Line-by-line pattern scans
        all_rules = (
            self.SECRET_PATTERNS +
            self.COMMAND_INJECTION_PATTERNS +
            self.SQLI_PATTERNS +
            self.PATH_TRAVERSAL_PATTERNS +
            self.DESERIALIZATION_PATTERNS +
            self.INSECURE_CONFIG_PATTERNS +
            self.WEAK_CRYPTO_PATTERNS
        )

        for line_idx, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("//"):
                continue

            for rule_id, severity, pattern, msg in all_rules:
                # If AST already covered code syntax for this python file, skip AST-covered rules in regex
                if parsed_ast_successfully and rule_id in ast_covered_rules:
                    continue

                key = (rule_id, line_idx)
                if key in seen:
                    continue
                if re.search(pattern, line):
                    seen.add(key)
                    rec = self._get_recommendation(rule_id)
                    findings.append(CsoFinding(
                        severity=severity,
                        category=rule_id.split("-")[0],
                        file_path=file_path,
                        line_number=line_idx,
                        rule_id=rule_id,
                        message=msg,
                        snippet=line.strip(),
                        recommendation=rec
                    ))

        return findings

    def scan_file(self, file_path: Path) -> List[CsoFinding]:
        if self.should_skip(file_path):
            return []
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            return self.scan_file_content(content, str(file_path))
        except Exception:
            return []

    def scan_directory(self, target_dir: Optional[Path] = None) -> List[CsoFinding]:
        dir_to_scan = target_dir or self.root_dir
        results: List[CsoFinding] = []
        for p in dir_to_scan.rglob("*"):
            if p.is_file() and p.suffix in {".py", ".js", ".ts", ".mjs", ".sh", ".json", ".yaml", ".yml"}:
                results.extend(self.scan_file(p))
        return results

    def _get_recommendation(self, rule_id: str) -> str:
        if rule_id.startswith("SECRET"):
            return "Use environment variables (e.g. os.environ['KEY']) or a secure vault instead of hardcoding."
        elif rule_id in {"INJ-01", "INJ-02"}:
            return "Pass command arguments as a list to subprocess.run(..., shell=False)."
        elif rule_id == "INJ-03":
            return "Avoid eval(); parse data with json.loads() or ast.literal_eval()."
        elif rule_id == "INJ-04":
            return "Avoid exec(); use modular design or safe dispatch tables."
        elif rule_id == "INJ-05":
            return "Use subprocess.run(..., shell=False) with parameterized arguments instead of os.popen()."
        elif rule_id.startswith("SQLI"):
            return "Use parameterized queries (e.g. cursor.execute('SELECT * WHERE id = ?', (id_,)))."
        elif rule_id.startswith("TRAVERSAL"):
            return "Enforce os.path.realpath containment or use a secure WithinBase check."
        elif rule_id.startswith("DESER"):
            return "Use safe JSON serialization or yaml.safe_load()."
        elif rule_id.startswith("INSEC"):
            return "Enable TLS certificate verification (omit verify=False or provide trusted CA)."
        elif rule_id.startswith("CRYPTO"):
            return "Use cryptographically secure hashing algorithms like hashlib.sha256()."
        return "Review code for secure coding best practices."

    def evaluate_gate(self, findings: List[CsoFinding]) -> Dict[str, Any]:
        critical_count = sum(1 for f in findings if f.severity == "CRITICAL")
        high_count = sum(1 for f in findings if f.severity == "HIGH")
        medium_count = sum(1 for f in findings if f.severity == "MEDIUM")
        passed = (critical_count == 0 and high_count == 0)

        return {
            "passed": passed,
            "verdict": "PASSED" if passed else "BLOCKED",
            "critical": critical_count,
            "high": high_count,
            "medium": medium_count,
            "findings": findings
        }
