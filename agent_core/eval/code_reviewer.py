"""
Alibaba Open-Code-Review (OCR) Implementation Engine.
Học hỏi và chuẩn hóa từ: alibaba/open-code-review (Go & Markdown Rules Engine).
Triết lý: 'Favor precision over recall' - Chỉ cảnh báo khi chắc chắn là lỗi thật.
Phân loại: Blocking (Critical/High) vs Non-Blocking (Medium/Low).
Line-level Structured Review Comments & Deterministic Pre-review Delegation.

Lưu ý phạm vi kỹ thuật:
Đây là bộ quy tắc Heuristic & Phân tích Cú pháp AST Tĩnh có độ chính xác cao (Deterministic Heuristics),
thiết kế nhằm bắt các lỗi phổ biến (bare except, mutable default, float equality, eval/exec, shell=True, SQL formatting, hardcoded secrets)
mà không gây nhiễu/báo động giả trên PR.
Để phát hiện biến chưa định nghĩa (undefined variables) hay phân tích kiểu tĩnh, hãy sử dụng các công cụ linter/static analyzer
chuyên dụng như Ruff, Flake8 hoặc Pyright trong CI.
"""

import ast
import os
import re
import fnmatch
import builtins
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple


# Danh mục và cấp độ nghiêm trọng theo chuẩn alibaba/open-code-review
VALID_CATEGORIES = {
    "bug",
    "security",
    "performance",
    "maintainability",
    "test",
    "style",
    "documentation",
    "other",
}

VALID_SEVERITIES = {
    "critical",
    "high",
    "medium",
    "low",
}

# Các mẫu file nhạy cảm tuyệt đối loại trừ khỏi review (Secret Exclude)
DEFAULT_SECRET_PATTERNS = [
    "**/.ssh/**",
    "**/id_rsa*",
    "**/id_dsa*",
    "**/id_ecdsa*",
    "**/id_ed25519*",
    "**/.netrc",
    "**/_netrc",
    "**/.npmrc",
    "**/.pypirc",
    "**/.dockercfg",
    "**/.env*",
    "**/*.pem",
    "**/*.key",
]

# Các thư mục phụ thuộc / build vendor loại trừ (Provider Directory Exclude)
DEFAULT_PROVIDER_DIRS = [
    "node_modules",
    "vendor",
    "target",
    "dist",
    "build",
    "bin",
    "obj",
    ".git",
    ".idea",
    ".vscode",
    "__pycache__",
    ".pytest_cache",
]

# Các mẫu file test, generated, lockfile loại trừ theo mặc định (Default Path Exclude)
DEFAULT_PATH_PATTERNS = [
    "**/*_test.go",
    "**/src/test/java/**/*.java",
    "**/*.test.{js,jsx,ts,tsx}",
    "**/*.spec.{js,jsx,ts,tsx}",
    "**/__tests__/**",
    "**/test_*.py",
    "**/tests/**/*_test.py",
    "**/*_test.py",
    "**/__snapshots__/**",
    "**/*.snap",
    "**/testdata/**",
    "**/fixtures/**",
    "**/*.generated.*",
    "**/*.gen.go",
    "**/*.pb.go",
    "**/*.min.js",
    "**/*.min.css",
    "**/package-lock.json",
    "**/pnpm-lock.yaml",
    "**/yarn.lock",
    "**/Cargo.lock",
    "**/poetry.lock",
]



@dataclass
class ReviewComment:
    """Mô hình Line-Level Structured Review Comment theo chuẩn alibaba/open-code-review."""
    path: str
    content: str
    start_line: int = 0
    end_line: int = 0
    category: str = "bug"
    severity: str = "medium"
    blocking: bool = False
    suggestion_code: Optional[str] = None
    existing_code: Optional[str] = None
    thinking: Optional[str] = None

    def __post_init__(self):
        # Chuẩn hóa path dạng POSIX
        self.path = self.path.replace("\\", "/").lstrip("./")
        # Chuẩn hóa category
        self.category = self.category.lower()
        if self.category not in VALID_CATEGORIES:
            self.category = "other"
        # Chuẩn hóa severity
        self.severity = self.severity.lower()
        if self.severity not in VALID_SEVERITIES:
            self.severity = "low"
        # Tự động gán blocking: Critical và High là blocking bắt buộc sửa trước khi merge
        if self.severity in ("critical", "high"):
            self.blocking = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ReviewRuleResolver:
    """Bộ phân giải quy chuẩn review ngôn ngữ từ agents/knowledge/review-rules/."""

    def __init__(self, rules_dir: Optional[str] = None):
        if rules_dir is None:
            # Đường dẫn mặc định trong agent-base
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            rules_dir = os.path.join(base_dir, "agents", "knowledge", "review-rules")
        self.rules_dir = rules_dir
        self.default_rule = "default.md"
        self.path_rule_map: Dict[str, str] = {}

        # Tải cấu hình ánh xạ hệ thống của Alibaba nếu có
        system_rules_path = os.path.join(self.rules_dir, "system_rules.json")
        if os.path.isfile(system_rules_path):
            try:
                import json
                with open(system_rules_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    self.default_rule = cfg.get("default_rule", "default.md")
                    self.path_rule_map = cfg.get("path_rule_map", {})
            except Exception:
                pass

        # Fallback cứng nếu không có file json
        if not self.path_rule_map:
            self.path_rule_map = {
                "**/*.py": "python.md",
                "**/*.{ts,js,tsx,jsx,mjs,cjs}": "ts_js_tsx_jsx.md",
                "**/*.go": "go.md",
                "**/*.java": "java.md",
                "**/*.rs": "rust.md",
                "**/*.{cpp,cc,cxx,hpp,hxx}": "cpp.md",
                "**/*.c": "c.md",
                ".github/workflows/**/*.{yaml,yml}": "github_workflows.md",
            }

    def resolve_rule_name(self, file_path: str) -> str:
        norm_path = file_path.replace("\\", "/")
        # Ưu tiên các pattern cụ thể/dài hơn trước (ví dụ .github/workflows trước .github)
        sorted_patterns = sorted(self.path_rule_map.items(), key=lambda item: len(item[0]), reverse=True)
        for pattern, rule_file in sorted_patterns:
            if FileExclusionFilter._match_pattern(norm_path, pattern):
                return rule_file
        return self.default_rule


    def get_rule_content(self, rule_name: str) -> str:
        rule_path = os.path.join(self.rules_dir, rule_name)
        if os.path.isfile(rule_path):
            with open(rule_path, "r", encoding="utf-8") as f:
                return f.read()
        return f"# Review Rule: {rule_name}\nFollow clean code, reliability, and security best practices."



def _expand_pattern(pattern: str) -> List[str]:
    """Mở rộng brace expansion kiểu glob (vd: *.{js,ts} -> *.js, *.ts)."""
    match = re.search(r"\{([^}]+)\}", pattern)
    if not match:
        return [pattern]
    prefix = pattern[:match.start()]
    suffix = pattern[match.end():]
    options = match.group(1).split(",")
    results = []
    for opt in options:
        results.extend(_expand_pattern(f"{prefix}{opt}{suffix}"))
    return results


class FileExclusionFilter:
    """Bộ lọc loại trừ tệp theo chuẩn alibaba/open-code-review."""

    @staticmethod
    def _clean_path(path: str) -> str:
        norm = path.replace("\\", "/")
        if norm.startswith("./"):
            norm = norm[2:]
        return norm

    @classmethod
    def _match_pattern(cls, path: str, pattern: str) -> bool:
        norm = cls._clean_path(path)
        base = os.path.basename(norm)

        for expanded in _expand_pattern(pattern):
            if fnmatch.fnmatch(norm, expanded) or fnmatch.fnmatch(base, expanded):
                return True
            # Hỗ trợ globstar zero-directory (ví dụ dir/**/file khớp cả dir/file)
            if "/**/" in expanded:
                zero_dir = expanded.replace("/**/", "/")
                if fnmatch.fnmatch(norm, zero_dir) or fnmatch.fnmatch(base, zero_dir):
                    return True
            if expanded.startswith("**/"):
                suffix = expanded[3:]
                if fnmatch.fnmatch(norm, suffix) or fnmatch.fnmatch(base, suffix):
                    return True
                if fnmatch.fnmatch(norm, f"*/{suffix}"):
                    return True
        return False


    @classmethod
    def check_exclusion(cls, file_path: str) -> Tuple[bool, str]:
        """
        Kiểm tra xem tệp có bị loại trừ không.
        Trả về (is_excluded, reason_code).
        reason_code: secret_exclude, provider_directory, default_path, binary, hoặc "" (nếu được review).
        """
        norm_path = cls._clean_path(file_path)

        # 1. Secret check
        for pat in DEFAULT_SECRET_PATTERNS:
            if cls._match_pattern(norm_path, pat):
                return True, "secret_exclude"

        # 2. Provider directory check (vendor, node_modules, dist, ...)
        parts = norm_path.split("/")
        for part in parts[:-1]:
            if part in DEFAULT_PROVIDER_DIRS:
                return True, "provider_directory"

        # 3. Default path exclusion (test files, minified, lockfiles)
        for pat in DEFAULT_PATH_PATTERNS:
            if cls._match_pattern(norm_path, pat):
                return True, "default_path"



        # 4. Binary check theo đuôi mở rộng phổ biến
        bin_extensions = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".zip", ".tar", ".gz", ".exe", ".dll", ".so", ".dylib", ".pdf", ".pyc", ".iso"}
        _, ext = os.path.splitext(norm_path)
        if ext.lower() in bin_extensions:
            return True, "binary"

        return False, ""


class CodeReviewer:
    """
    Động cơ Review Mã Nguồn Alibaba Open-Code-Review.
    Tích hợp chế độ Ủy thác (Delegation Mode) và Kiểm tra Tĩnh Tất định (Deterministic Rule Engine).
    """

    def __init__(self, rules_dir: Optional[str] = None):
        self.resolver = ReviewRuleResolver(rules_dir)
        self.filter = FileExclusionFilter()

    def preview(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        Tạo báo cáo Preview tương đương lệnh `ocr delegate preview --format json`.
        Phân loại reviewable vs excluded.
        """
        reviewable_files = []
        excluded_files = []

        for p in file_paths:
            is_excluded, reason = self.filter.check_exclusion(p)
            if is_excluded:
                excluded_files.append({
                    "path": p.replace("\\", "/"),
                    "exclude_reason": reason,
                    "will_review": False,
                })
            else:
                reviewable_files.append({
                    "path": p.replace("\\", "/"),
                    "will_review": True,
                })

        return {
            "total_files": len(file_paths),
            "reviewable_count": len(reviewable_files),
            "excluded_count": len(excluded_files),
            "reviewable_files": reviewable_files,
            "excluded_files": excluded_files,
        }

    def group_rules(self, reviewable_files: List[str]) -> Dict[str, List[str]]:
        """
        Gom nhóm các file theo bộ luật review tương đương `ocr delegate rule`.
        """
        groups: Dict[str, List[str]] = {}
        for p in reviewable_files:
            rule_name = self.resolver.resolve_rule_name(p)
            if rule_name not in groups:
                groups[rule_name] = []
            groups[rule_name].append(p)
        return groups

    def analyze_source(self, file_path: str, source_code: str) -> List[ReviewComment]:
        """
        Phân tích mã nguồn và sinh ra các Line-Level Review Comments theo bộ luật ngôn ngữ.
        Áp dụng triết lý 'Precision over recall': Chỉ báo khi chắc chắn là lỗi.
        """
        comments: List[ReviewComment] = []
        norm_path = file_path.replace("\\", "/")

        # 1. Quét Secret / Hardcoded Tokens chung (Security - Critical - Blocking)
        token_patterns = [
            (re.compile(r'''(?:api[_-]?key|secret|password|bearer)\s*=\s*['"][a-zA-Z0-9_\-]{16,}['"]''', re.IGNORECASE),
             "Phát hiện mật khẩu / API key được hardcode trong mã nguồn. Cần chuyển sang biến môi trường (Environment Variable)."),
            (re.compile(r'''ghp_[a-zA-Z0-9]{36}'''), "Phát hiện GitHub Personal Access Token hợp lệ."),
            (re.compile(r'''AKIA[0-9A-Z]{16}'''), "Phát hiện AWS Access Key ID hardcode."),
        ]
        lines = source_code.splitlines()
        for idx, line in enumerate(lines, start=1):
            for pat, desc in token_patterns:
                if pat.search(line) and not line.strip().startswith("#") and not line.strip().startswith("//"):
                    comments.append(ReviewComment(
                        path=norm_path,
                        start_line=idx,
                        end_line=idx,
                        category="security",
                        severity="critical",
                        content=desc,
                        existing_code=line.strip(),
                        thinking="Hardcoded secrets in source code lead to credential leakage.",
                    ))

        # 2. Phân tích Python AST & Best Practices nếu là Python file
        if norm_path.endswith(".py"):
            comments.extend(self._analyze_python(norm_path, source_code, lines))

        # 3. Phân tích JS/TS nếu là file JavaScript/TypeScript
        if re.search(r"\.(ts|js|tsx|jsx)$", norm_path, re.IGNORECASE):
            comments.extend(self._analyze_js_ts(norm_path, source_code, lines))

        return comments

    def _analyze_python(self, file_path: str, source_code: str, lines: List[str]) -> List[ReviewComment]:
        comments: List[ReviewComment] = []
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            comments.append(ReviewComment(
                path=file_path,
                start_line=e.lineno or 1,
                end_line=e.lineno or 1,
                category="bug",
                severity="critical",
                content=f"Lỗi cú pháp Python không thể biên dịch: {e.msg}",
                existing_code=lines[(e.lineno - 1)] if e.lineno and e.lineno <= len(lines) else "",
            ))
            return comments

        # Thu thập các tên đã được định nghĩa ở cấp độ module (functions, classes, variables, imports)
        # Bao gồm cả các định nghĩa nằm trong try/except, if/else, with ở cấp module
        module_scope_names = set(dir(builtins)) | {
            "__file__", "__name__", "__doc__", "__package__", "__all__", "__version__", "__path__"
        }
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                module_scope_names.add(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    module_scope_names.add(alias.asname or alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    module_scope_names.add(alias.asname or alias.name)
            elif isinstance(node, ast.Assign):
                for tgt in node.targets:
                    for n in ast.walk(tgt):
                        if isinstance(n, ast.Name):
                            module_scope_names.add(n.id)
            elif isinstance(node, (ast.AnnAssign, ast.AugAssign)) and isinstance(node.target, ast.Name):
                module_scope_names.add(node.target.id)
            elif isinstance(node, ast.NamedExpr) and isinstance(node.target, ast.Name):
                module_scope_names.add(node.target.id)
            elif isinstance(node, (ast.For, ast.AsyncFor)):
                for n in ast.walk(node.target):
                    if isinstance(n, ast.Name):
                        module_scope_names.add(n.id)
            elif isinstance(node, (ast.With, ast.AsyncWith)):
                for it in node.items:
                    if it.optional_vars:
                        for n in ast.walk(it.optional_vars):
                            if isinstance(n, ast.Name):
                                module_scope_names.add(n.id)

        class PythonRuleVisitor(ast.NodeVisitor):
            EXEMPT_NAMES = {
                "self", "cls", "cursor", "request", "response", "session", "app", "db",
                "args", "kwargs", "_", "__name__", "__file__", "__doc__", "e"
            }

            def __init__(self, filepath: str, lines: List[str], module_names: set):
                self.filepath = filepath
                self.lines = lines
                self.module_names = module_names
                self.scope_stack: List[set] = []
                self.class_stack: List[set] = []
                self.issues: List[ReviewComment] = []

            def visit_ClassDef(self, node: ast.ClassDef):
                class_attrs = set()
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        for tgt in item.targets:
                            for n in ast.walk(tgt):
                                if isinstance(n, ast.Name):
                                    class_attrs.add(n.id)
                    elif isinstance(item, (ast.AnnAssign, ast.AugAssign)) and isinstance(item.target, ast.Name):
                        class_attrs.add(item.target.id)
                    elif isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        class_attrs.add(item.name)
                self.class_stack.append(class_attrs)
                self.generic_visit(node)
                self.class_stack.pop()

            def visit_FunctionDef(self, node: ast.FunctionDef):
                self._check_function(node)

            def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
                self._check_function(node)

            def _check_function(self, node):
                # 1. Quy tắc Python: Mutable default argument (High - Bug)
                for default in node.args.defaults + node.args.kw_defaults:
                    if default is not None and isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        line_no = getattr(default, "lineno", node.lineno)
                        snippet = self.lines[line_no - 1] if line_no <= len(self.lines) else ""
                        self.issues.append(ReviewComment(
                            path=self.filepath,
                            start_line=line_no,
                            end_line=line_no,
                            category="bug",
                            severity="high",
                            content="Sử dụng đối tượng có thể biến đổi (mutable default argument: list/dict/set) làm giá trị mặc định cho tham số hàm. Điều này dẫn đến lỗi chia sẻ trạng thái giữa các lần gọi hàm.",
                            suggestion_code="def func(arg=None):\n    if arg is None:\n        arg = []",
                            existing_code=snippet.strip(),
                            thinking="In Python, default parameter values are evaluated once when function is defined, not per call.",
                        ))

                # Kiểm tra giá trị mặc định của tham số hàm (được đánh giá trong phạm vi bao ngoài)
                valid_default_names = self.module_names | self.EXEMPT_NAMES
                for s in self.scope_stack:
                    valid_default_names |= s
                if self.class_stack:
                    valid_default_names |= self.class_stack[-1]

                for d in node.args.defaults + node.args.kw_defaults:
                    if d is not None:
                        for n in ast.walk(d):
                            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
                                if n.id not in valid_default_names:
                                    line_no = getattr(n, "lineno", node.lineno)
                                    snippet = self.lines[line_no - 1] if line_no <= len(self.lines) else ""
                                    self.issues.append(ReviewComment(
                                        path=self.filepath,
                                        start_line=line_no,
                                        end_line=line_no,
                                        category="bug",
                                        severity="medium",
                                        content=f"Biến '{n.id}' được sử dụng làm giá trị mặc định nhưng chưa được định nghĩa (Undefined variable).",
                                        suggestion_code=f"# Khai báo hoặc import '{n.id}' trước khi sử dụng",
                                        existing_code=snippet.strip(),
                                        thinking=f"Referencing '{n.id}' in parameter defaults without definition leads to NameError at module load.",
                                    ))

                # 2. Quy tắc Python: Bắt biến chưa định nghĩa trong phạm vi hàm (Undefined Variable / NameError)
                # Thu thập toàn bộ tên cục bộ thuộc phạm vi hàm hiện tại
                local_names = set()
                for a in node.args.args + getattr(node.args, "posonlyargs", []) + node.args.kwonlyargs:
                    local_names.add(a.arg)
                if node.args.vararg:
                    local_names.add(node.args.vararg.arg)
                if node.args.kwarg:
                    local_names.add(node.args.kwarg.arg)

                for item in node.body:
                    for child in ast.walk(item):
                        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and child is not item:
                            continue
                        if isinstance(child, ast.Assign):
                            for tgt in child.targets:
                                for n in ast.walk(tgt):
                                    if isinstance(n, ast.Name):
                                        local_names.add(n.id)
                        elif isinstance(child, (ast.AnnAssign, ast.AugAssign)) and isinstance(child.target, ast.Name):
                            local_names.add(child.target.id)
                        elif isinstance(child, ast.NamedExpr) and isinstance(child.target, ast.Name):
                            local_names.add(child.target.id)
                        elif isinstance(child, (ast.For, ast.AsyncFor)):
                            for n in ast.walk(child.target):
                                if isinstance(n, ast.Name):
                                    local_names.add(n.id)
                        elif isinstance(child, ast.ExceptHandler) and child.name:
                            local_names.add(child.name)
                        elif isinstance(child, ast.comprehension):
                            for n in ast.walk(child.target):
                                if isinstance(n, ast.Name):
                                    local_names.add(n.id)
                        elif isinstance(child, ast.Lambda):
                            for a in child.args.args:
                                local_names.add(a.arg)
                        elif isinstance(child, (ast.With, ast.AsyncWith)):
                            for it in child.items:
                                if it.optional_vars:
                                    for n in ast.walk(it.optional_vars):
                                        if isinstance(n, ast.Name):
                                            local_names.add(n.id)

                self.scope_stack.append(local_names)

                all_known = self.module_names | self.EXEMPT_NAMES
                for s in self.scope_stack:
                    all_known |= s

                seen_undefined = set()
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        continue
                    for child in ast.walk(item):
                        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                            continue
                        if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                            var_name = child.id
                            if var_name not in all_known and var_name not in seen_undefined:
                                seen_undefined.add(var_name)
                                line_no = getattr(child, "lineno", node.lineno)
                                snippet = self.lines[line_no - 1] if line_no <= len(self.lines) else ""
                                self.issues.append(ReviewComment(
                                    path=self.filepath,
                                    start_line=line_no,
                                    end_line=line_no,
                                    category="bug",
                                    severity="medium",
                                    content=f"Biến '{var_name}' được sử dụng nhưng chưa được định nghĩa trong phạm vi hàm hoặc module (Undefined variable / NameError).",
                                    suggestion_code=f"# Khai báo hoặc import '{var_name}' trước khi sử dụng",
                                    existing_code=snippet.strip(),
                                    thinking=f"Referencing '{var_name}' without definition leads to NameError at runtime.",
                                ))

                self.generic_visit(node)
                self.scope_stack.pop()

            def visit_ExceptHandler(self, node: ast.ExceptHandler):
                # Quy tắc Python: Bare except: bắt tất cả ngoại lệ kể cả KeyboardInterrupt/SystemExit
                if node.type is None:
                    line_no = getattr(node, "lineno", 1)
                    snippet = lines[line_no - 1] if line_no <= len(lines) else "except:"
                    self.issues.append(ReviewComment(
                        path=self.filepath,
                        start_line=line_no,
                        end_line=line_no,
                        category="bug",
                        severity="medium",
                        content="Tránh sử dụng bare 'except:'. Nó sẽ bắt cả KeyboardInterrupt và SystemExit, khiến tiến trình không thể dừng bình thường. Hãy bắt cụ thể 'except Exception:' hoặc ngoại lệ mong đợi.",
                        suggestion_code="except Exception as e:",
                        existing_code=snippet.strip(),
                    ))
                self.generic_visit(node)

            def visit_Compare(self, node: ast.Compare):
                # Quy tắc Python: So sánh bằng trực tiếp giữa số thực (float)
                for op, comp in zip(node.ops, node.comparators):
                    if isinstance(op, (ast.Eq, ast.NotEq)):
                        is_left_float = isinstance(node.left, ast.Constant) and isinstance(node.left.value, float)
                        is_right_float = isinstance(comp, ast.Constant) and isinstance(comp.value, float)
                        if is_left_float or is_right_float:
                            line_no = getattr(node, "lineno", 1)
                            snippet = lines[line_no - 1] if line_no <= len(lines) else ""
                            self.issues.append(ReviewComment(
                                path=self.filepath,
                                start_line=line_no,
                                end_line=line_no,
                                category="bug",
                                severity="medium",
                                content="So sánh bằng trực tiếp số thực (float equality) thường thất bại do sai số làm tròn điểm động (precision error). Nên dùng 'math.isclose(a, b)' hoặc so sánh sai phân epsilon.",
                                suggestion_code="math.isclose(a, b, rel_tol=1e-9)",
                                existing_code=snippet.strip(),
                            ))
                self.generic_visit(node)

            def visit_Call(self, node: ast.Call):
                # Quy tắc Python: Cấm gọi eval() / exec() vì nguy cơ Remote Code Execution (Critical - Security)
                if isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec"):
                    line_no = getattr(node, "lineno", 1)
                    snippet = lines[line_no - 1] if line_no <= len(lines) else ""
                    self.issues.append(ReviewComment(
                        path=self.filepath,
                        start_line=line_no,
                        end_line=line_no,
                        category="security",
                        severity="critical",
                        content=f"Sử dụng hàm nguy hiểm '{node.func.id}()'. Hàm này thực thi mã động trực tiếp và tiềm ẩn nguy cơ Remote Code Execution (RCE) nghiêm trọng.",
                        suggestion_code="ast.literal_eval(...) nếu chỉ phân tích cú pháp dữ liệu an toàn",
                        existing_code=snippet.strip(),
                        thinking="eval/exec on untrusted input allows arbitrary code execution.",
                    ))

                # Quy tắc Python: Cấm gọi subprocess với shell=True (Critical - Security)
                if isinstance(node.func, ast.Attribute) and node.func.attr in ("Popen", "run", "call", "check_call", "check_output"):
                    for kw in node.keywords:
                        if kw.arg == "shell":
                            is_true = False
                            if isinstance(kw.value, ast.Constant) and bool(kw.value.value):
                                is_true = True
                            elif hasattr(ast, "NameConstant") and isinstance(kw.value, getattr(ast, "NameConstant")) and kw.value.value is True:
                                is_true = True
                            if is_true:
                                line_no = getattr(node, "lineno", 1)
                                snippet = lines[line_no - 1] if line_no <= len(lines) else ""
                                self.issues.append(ReviewComment(
                                    path=self.filepath,
                                    start_line=line_no,
                                    end_line=line_no,
                                    category="security",
                                    severity="critical",
                                    content="subprocess được gọi với 'shell=True'. Điều này kích hoạt command shell và tiềm ẩn nguy cơ Command Injection nghiêm trọng khi nhận đầu vào từ bên ngoài.",
                                    suggestion_code="subprocess.run(['command', 'arg1', 'arg2'], shell=False)",
                                    existing_code=snippet.strip(),
                                    thinking="shell=True passes commands through system shell, leading to command injection vulnerabilities.",
                                ))

                # Quy tắc Python: Cấm ghép chuỗi / f-string trong .execute() / .executemany() (Critical - Security)
                if isinstance(node.func, ast.Attribute) and node.func.attr in ("execute", "executemany"):
                    if node.args:
                        first_arg = node.args[0]
                        is_sqli_risk = False
                        if isinstance(first_arg, ast.JoinedStr):
                            is_sqli_risk = True
                        elif isinstance(first_arg, ast.BinOp) and isinstance(first_arg.op, (ast.Mod, ast.Add)):
                            is_sqli_risk = True

                        if is_sqli_risk:
                            line_no = getattr(node, "lineno", 1)
                            snippet = lines[line_no - 1] if line_no <= len(lines) else ""
                            self.issues.append(ReviewComment(
                                path=self.filepath,
                                start_line=line_no,
                                end_line=line_no,
                                category="security",
                                severity="critical",
                                content="Phát hiện truy vấn SQL được tạo bằng cách ghép chuỗi hoặc dùng f-string/% format trong .execute(). Cần sử dụng tham số hóa (Parameterized Queries) để ngăn chặn SQL Injection.",
                                suggestion_code='cursor.execute("SELECT * FROM tbl WHERE id = %s", (user_id,))',
                                existing_code=snippet.strip(),
                                thinking="Direct string formatting in SQL statements leads to SQL Injection vulnerabilities.",
                            ))

                self.generic_visit(node)

        visitor = PythonRuleVisitor(file_path, lines, module_scope_names)
        visitor.visit(tree)
        comments.extend(visitor.issues)
        return comments

    def _analyze_js_ts(self, file_path: str, source_code: str, lines: List[str]) -> List[ReviewComment]:
        comments: List[ReviewComment] = []
        for idx, line in enumerate(lines, start=1):
            trimmed = line.strip()
            if trimmed.startswith("//") or trimmed.startswith("/*"):
                continue

            # JavaScript dangerous eval
            if re.search(r"\beval\s*\(", trimmed):
                comments.append(ReviewComment(
                    path=file_path,
                    start_line=idx,
                    end_line=idx,
                    category="security",
                    severity="critical",
                    content="Sử dụng eval() trong JavaScript tiềm ẩn lỗ hổng XSS và Code Injection nghiêm trọng.",
                    suggestion_code="// Tránh dùng eval(), sử dụng JSON.parse() hoặc logic tính toán an toàn",
                    existing_code=trimmed,
                ))

            # React dangerouslySetInnerHTML
            if "dangerouslySetInnerHTML" in trimmed:
                comments.append(ReviewComment(
                    path=file_path,
                    start_line=idx,
                    end_line=idx,
                    category="security",
                    severity="high",
                    content="Sử dụng 'dangerouslySetInnerHTML' có thể dẫn đến tấn công Cross-Site Scripting (XSS). Hãy chắc chắn đầu vào đã qua DOMPurify hoặc giải pháp khử khuẩn HTML an toàn.",
                    existing_code=trimmed,
                ))

        return comments

    def generate_report(self, comments: List[ReviewComment], total_files: int) -> str:
        """
        Sinh báo cáo đánh giá chuẩn định dạng alibaba/open-code-review.
        Tự động phân nhóm theo Severity và kết luận Blocking Gate.
        """
        critical_items = [c for c in comments if c.severity == "critical"]
        high_items = [c for c in comments if c.severity == "high"]
        medium_items = [c for c in comments if c.severity == "medium"]
        low_items = [c for c in comments if c.severity == "low"]

        has_blocking = len(critical_items) > 0 or len(high_items) > 0

        lines = [
            "# Alibaba Open-Code-Review Report",
            "",
            f"**Triết lý cốt lõi**: *Favor precision over recall* (Chỉ báo lỗi khi chắc chắn 100%).",
            f"**Tổng số tệp được thẩm định**: {total_files}",
            f"**Tổng số phát hiện**: {len(comments)} (Critical: {len(critical_items)}, High: {len(high_items)}, Medium: {len(medium_items)}, Low: {len(low_items)})",
            "",
            f"**Trạng thái Gate Merge/PR**: **{'⛔ BLOCKED (Cần khắc phục lỗi nghiêm trọng trước khi merge)' if has_blocking else '✅ PASS (Không có lỗi Critical/High gây tắc nghẽn)'}**",
            "",
        ]

        if not comments:
            lines.append("Review complete — no issues found. Mã nguồn tuân thủ tốt các quy chuẩn an toàn và hiệu năng.")
            return "\n".join(lines)

        def format_group(title: str, items: List[ReviewComment]):
            if not items:
                return
            lines.append(f"### {title}")
            lines.append("")
            for it in items:
                loc = f"`{it.path}:{it.start_line}`" if it.start_line > 0 else f"`{it.path}`"
                lines.append(f"- **{loc}** [{it.category}] — {it.content}")
                if it.existing_code:
                    lines.append(f"  - *Hiện tại*: `{it.existing_code}`")
                if it.suggestion_code:
                    lines.append(f"  - *Khắc phục đề xuất*:\n    ```\n    {it.suggestion_code}\n    ```")
                lines.append("")

        format_group("🔴 Critical (Security/Crash Vulnerability)", critical_items)
        format_group("🟠 High (Functional Defect / Mutable Defaults)", high_items)
        format_group("🟡 Medium (Reliability / Edge-cases)", medium_items)
        format_group("🔵 Low (Maintainability / Style suggestions)", low_items)

        return "\n".join(lines)
