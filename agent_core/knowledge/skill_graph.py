"""agent_core.knowledge.skill_graph

Đồ thị Kỹ năng (Skill Knowledge Graph) cho kho kỹ năng (quarantine & installed skills).
Đảm bảo 100% PORTABLE:
- Không lưu đường dẫn tuyệt đối của bất kỳ máy tính nào vào file graph JSON.
- Phân giải động (dynamic resolution) qua file cấu hình cục bộ skills.config.local.json hoặc biến môi trường.
- Hỗ trợ quét nhanh 1.600+ skills trong < 1 giây, phát hiện độ lệch (drift) khi có skill mới hoặc thay đổi.
- Tuân thủ Python stdlib, không phụ thuộc thư viện ngoài.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

ROOT_DEFAULT = Path(__file__).resolve().parent.parent.parent

# 8 Taxonomy domains chuẩn
TAXONOMY_DOMAINS = {
    "architecture": ["uml", "architecture", "adr", "pattern", "clean", "hexagonal", "ddd", "system", "structure", "microservice", "archify"],
    "development": ["spring", "jpa", "hibernate", "react", "typescript", "javascript", "python", "backend", "frontend", "api", "code", "crud", "postgres", "sql", "refactor"],
    "testing": ["test", "tdd", "bdd", "mock", "assert", "qa", "testlink", "testcontainers", "boundary", "cypress", "playwright", "jest"],
    "devops": ["docker", "k8s", "kubernetes", "ci", "cd", "pipeline", "deploy", "ship", "release", "container", "git", "linux", "cloud", "aws", "gcp"],
    "security": ["security", "cso", "owasp", "auth", "oauth", "jwt", "crypto", "vulnerability", "agentshield", "secret", "permission", "scan"],
    "design": ["ui", "ux", "design", "css", "tailwind", "component", "wireframe", "style", "font", "color", "icon", "phosphor", "screen", "mockup"],
    "business": ["ba", "babok", "business", "srs", "fdd", "glossary", "user story", "tickets", "spec", "domain", "interview", "mba"],
    "management": ["agile", "scrum", "sprint", "cmmi", "lead", "project", "governance", "retro", "retrospective", "wayfinder", "task", "roadmap"]
}

# Độ ưu tiên repo khi chọn nguồn chính (primary_source)
REPO_PRIORITY = [
    "ECC",
    "superpowers",
    "gstack",
    "pocock-skills",
    "skills",
    "archify",
    "diagram-design",
    "ui-ux-pro-max-skill",
    "open-code-review",
    "i-have-adhd",
    "ponytail",
    "ruflo",
]


def check_forbidden_system_path(path: Path) -> Tuple[bool, str]:
    """Kiểm tra đường dẫn có vi phạm quy định cấm lưu vào ổ hệ thống OS hay không."""
    try:
        expanded = path.expanduser().resolve()
    except Exception:
        expanded = path

    # Windows: Cấm ổ C:
    if sys.platform == "win32" or getattr(expanded, "drive", ""):
        if getattr(expanded, "drive", "").upper() == "C:":
            return True, "CẤM CẤU HÌNH VÀO Ổ C: (ổ hệ điều hành Windows)!"

    # macOS & Linux: Cấm root và thư mục hệ thống
    if sys.platform != "win32":
        str_p = str(expanded)
        if str_p == "/":
            return True, "CẤM cấu hình vào thư mục gốc hệ thống (/)!"
        # Cho phép các thư mục tạm (tempfile) phục vụ kiểm thử
        if str_p.startswith("/var/folders") or str_p.startswith("/private/var/folders") or str_p.startswith("/tmp") or str_p.startswith("/private/tmp"):
            return False, ""
        forbidden_system_dirs = ["/System", "/Library", "/bin", "/sbin", "/usr", "/etc", "/var", "/private", "/dev"]
        for f_dir in forbidden_system_dirs:
            if str_p == f_dir or str_p.startswith(f_dir + "/"):
                return True, f"CẤM cấu hình vào thư mục hệ thống ({f_dir})!"

    return False, ""


def load_skills_config(root_dir: Optional[Path] = None) -> Tuple[Optional[Path], Path, Path]:
    """
    Đọc cấu hình kho kỹ năng theo thứ tự ưu tiên:
    1. Biến môi trường SKILLS_QUARANTINE_DIR
    2. skills.config.local.json (file riêng của từng máy, nằm trong .gitignore)
    3. skills.config.json (file mẫu dự phòng của repo)
    
    Trả về: (quarantine_dir, skills_dir, config_source_path)
    """
    root = (root_dir or ROOT_DEFAULT).resolve()
    skills_path = root / ".agents" / "skills"
    quarantine_path: Optional[Path] = None

    local_cfg = root / "skills.config.local.json"
    fallback_cfg = root / "skills.config.json"
    chosen_cfg = local_cfg if local_cfg.exists() else fallback_cfg

    if chosen_cfg.exists():
        try:
            data = json.loads(chosen_cfg.read_text(encoding="utf-8"))
            if data.get("quarantine_dir"):
                cand = Path(data["quarantine_dir"]).expanduser()
                is_bad, _ = check_forbidden_system_path(cand)
                if not is_bad and cand.exists():
                    quarantine_path = cand
            if data.get("skills_dir"):
                p = Path(data["skills_dir"]).expanduser()
                skills_path = p if p.is_absolute() else (root / p)
        except Exception:
            pass

    # Biến môi trường ghi đè tường minh nếu có
    if os.environ.get("SKILLS_QUARANTINE_DIR"):
        env_cand = Path(os.environ["SKILLS_QUARANTINE_DIR"]).expanduser()
        is_bad, _ = check_forbidden_system_path(env_cand)
        if not is_bad and env_cand.exists():
            quarantine_path = env_cand

    return quarantine_path, skills_path, chosen_cfg


def save_skills_local_config(quarantine_dir: Path, root_dir: Optional[Path] = None, skills_dir: Optional[Path] = None) -> Path:
    """
    Lưu cấu hình đường dẫn máy cục bộ vào skills.config.local.json (file này nằm trong .gitignore).
    TUYỆT ĐỐI KHÔNG GHI ĐÈ đường dẫn máy riêng vào skills.config.json.
    """
    root = (root_dir or ROOT_DEFAULT).resolve()
    expanded = quarantine_dir.expanduser().resolve()
    is_bad, reason = check_forbidden_system_path(expanded)
    if is_bad:
        raise ValueError(f"NGHIÊM CẤM lưu cấu hình kho kỹ năng: {reason}")

    local_cfg = root / "skills.config.local.json"
    data = {
        "$schema": "./schemas/skills-config.schema.json",
        "description": "Cấu hình đường dẫn máy cục bộ của người dùng (nằm trong .gitignore, không commit lên git).",
        "quarantine_dir": str(expanded).replace("\\", "/"),
        "skills_dir": str(skills_dir) if skills_dir else ".agents/skills"
    }
    local_cfg.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return local_cfg



def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Tách YAML frontmatter và phần thân markdown của SKILL.md (không cần PyYAML)."""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    fm_text = parts[1]
    body = parts[2].strip()
    meta: Dict[str, Any] = {}
    current_key: Optional[str] = None

    for line in fm_text.splitlines():
        line_s = line.strip()
        if not line_s or line_s.startswith("#"):
            continue

        if ":" in line_s and not line_s.startswith("-"):
            k, v = line_s.split(":", 1)
            k = k.strip()
            v = v.strip().strip("\"'")
            meta[k] = v
            current_key = k
        elif line_s.startswith("-") and current_key:
            val = line_s.lstrip("- ").strip("\"'")
            if not isinstance(meta.get(current_key), list):
                meta[current_key] = []
            meta[current_key].append(val)

    if "allowed-tools" in meta and "allowed_tools" not in meta:
        meta["allowed_tools"] = meta["allowed-tools"]
    elif "allowed_tools" in meta and "allowed-tools" not in meta:
        meta["allowed-tools"] = meta["allowed_tools"]

    return meta, body


def estimate_tokens(text: str) -> int:
    """Ước tính tokens tương tự chuẩn OpenAI/Claude (~4 ký tự/token)."""
    if not text:
        return 0
    return max(1, len(text) // 4)


def parse_approved_skills(registry_file: Path) -> Dict[str, Dict[str, Any]]:
    """Đọc sổ đăng ký agents/knowledge/skills.md để lấy thông tin các skill đã được duyệt."""
    if not registry_file.exists():
        return {}

    approved = {}
    content = registry_file.read_text(encoding="utf-8", errors="ignore")
    lines = content.splitlines()

    for line in lines:
        if not line.startswith("|") or line.startswith("|---") or "Ngày duyệt" in line:
            continue
        cols = [c.strip() for c in line.split("|")[1:-1]]
        if len(cols) >= 6:
            skill_name = cols[0]
            url = cols[1]
            version = cols[2]
            approved_date = cols[3]
            approved_by = cols[4]
            roles_str = cols[5]
            roles = [r.strip() for r in roles_str.split(",") if r.strip()]
            approved[skill_name] = {
                "name": skill_name,
                "url": url,
                "version": version,
                "approved_date": approved_date,
                "approved_by": approved_by,
                "roles": roles,
                "has_script": cols[6] if len(cols) > 6 else "Không",
                "notes": cols[7] if len(cols) > 7 else ""
            }

    return approved


def classify_taxonomy_and_roles(name: str, desc: str, triggers: List[str], approved_roles: Optional[List[str]] = None) -> Tuple[str, List[str]]:
    """Phân loại domain và vai trò phù hợp cho skill."""
    corpus = f"{name} {desc} {' '.join(triggers)}".lower()

    # 1. Domain classification
    scores = {}
    for domain, kws in TAXONOMY_DOMAINS.items():
        score = 0
        for kw in kws:
            if kw in corpus:
                score += 2 if kw in name.lower() else 1
        if score > 0:
            scores[domain] = score

    domain = max(scores.items(), key=lambda x: x[1])[0] if scores else "development"

    # 2. Roles classification
    if approved_roles:
        return domain, approved_roles

    # Mapping heuristics theo domain nếu chưa được duyệt
    domain_to_roles = {
        "architecture": ["architect", "reviewer"],
        "development": ["dev", "reviewer"],
        "testing": ["qa", "dev"],
        "devops": ["devops", "sre"],
        "security": ["security", "reviewer"],
        "design": ["designer", "dev"],
        "business": ["ba", "product", "analyst"],
        "management": ["lead", "writer"]
    }
    roles = domain_to_roles.get(domain, ["dev"])
    return domain, roles


def select_primary_source(variants: List[Dict[str, Any]], skill_name: str) -> Dict[str, Any]:
    """Chọn nguồn tốt nhất trong các biến thể của cùng một skill."""
    if len(variants) == 1:
        return variants[0]

    # Ưu tiên các file không nằm trong thư mục dịch tài liệu ngôn ngữ khác (ja-JP, zh-CN...)
    clean_variants = [v for v in variants if not any(lang in v["rel_path"] for lang in ["/ja-JP/", "/zh-CN/", "/es-ES/", "/ko-KR/"])]
    candidates = clean_variants if clean_variants else variants

    # Ưu tiên theo thứ tự bảng ưu tiên REPO_PRIORITY
    def score_variant(v: Dict[str, Any]) -> int:
        repo = v["repo"]
        priority_idx = REPO_PRIORITY.index(repo) if repo in REPO_PRIORITY else 999
        # Ưu tiên đường dẫn chuẩn skills/<name>/SKILL.md
        path_bonus = 0 if f"skills/{skill_name}/" in v["rel_path"] or v["rel_path"].startswith(f"{repo}/{skill_name}/") else 100
        return priority_idx + path_bonus

    candidates.sort(key=score_variant)
    return candidates[0]


def scan_quarantine_skills(quarantine_dir: Path, root_dir: Optional[Path] = None) -> Dict[str, Any]:
    """
    Quét toàn bộ kho quarantine, phân tích tất cả SKILL.md và xây dựng Đồ thị Kỹ năng.
    TẤT CẢ ĐƯỜNG DẪN ĐỀU LÀ RELATIVE PATH TÍNH TỪ quarantine_dir (HOÀN TOÀN PORTABLE).
    """
    root = (root_dir or ROOT_DEFAULT).resolve()
    skills_dir = root / ".agents" / "skills"
    registry_file = root / "agents" / "knowledge" / "skills.md"
    approved_skills = parse_approved_skills(registry_file)

    installed_names = set()
    if skills_dir.exists():
        for d in skills_dir.iterdir():
            if d.is_dir() and (d / "SKILL.md").exists():
                installed_names.add(d.name)

    # 1. Tìm tất cả các file SKILL.md
    raw_skills_by_name: Dict[str, List[Dict[str, Any]]] = {}
    repos_scanned = set()
    total_files = 0

    for path in quarantine_dir.glob("**/SKILL.md"):
        # Tránh các file trong .git hoặc node_modules
        parts = path.parts
        if ".git" in parts or "node_modules" in parts:
            continue

        try:
            rel_from_quarantine = path.relative_to(quarantine_dir)
            repo_name = rel_from_quarantine.parts[0]
            repos_scanned.add(repo_name)

            content = path.read_text(encoding="utf-8", errors="ignore")
            # Chuẩn hóa LF để tính SHA256 độc lập hệ điều hành
            normalized_content = content.replace("\r\n", "\n")
            sha256_hash = hashlib.sha256(normalized_content.encode("utf-8")).hexdigest()

            fm, body = parse_frontmatter(content)
            name = fm.get("name") or path.parent.name
            name = name.strip()

            line_cnt = len(content.splitlines())
            tokens = estimate_tokens(content)

            triggers = fm.get("triggers", [])
            if isinstance(triggers, str):
                triggers = [triggers]

            allowed_tools = fm.get("allowed-tools", [])
            if isinstance(allowed_tools, str):
                allowed_tools = [allowed_tools]

            variant_info = {
                "repo": repo_name,
                "rel_path": str(rel_from_quarantine).replace("\\", "/"),
                "sha256": sha256_hash,
                "line_count": line_cnt,
                "tokens": tokens,
                "description": fm.get("description", "").strip(),
                "triggers": triggers,
                "allowed_tools": allowed_tools,
                "version": fm.get("version", "1.0.0"),
            }

            raw_skills_by_name.setdefault(name, []).append(variant_info)
            total_files += 1
        except Exception:
            continue

    # 2. Xây dựng các Node của Đồ thị
    nodes: Dict[str, Dict[str, Any]] = {}
    taxonomy_counts: Dict[str, int] = {k: 0 for k in TAXONOMY_DOMAINS}
    taxonomy_counts["general"] = 0

    for name, variants in raw_skills_by_name.items():
        primary = select_primary_source(variants, name)
        approved_info = approved_skills.get(name)
        approved_roles = approved_info["roles"] if approved_info else None

        desc = primary["description"]
        if not desc:
            for v in variants:
                if v["description"]:
                    desc = v["description"]
                    break

        domain, roles = classify_taxonomy_and_roles(name, desc, primary["triggers"], approved_roles)
        if domain in taxonomy_counts:
            taxonomy_counts[domain] += 1
        else:
            taxonomy_counts["general"] += 1

        is_approved = name in approved_skills
        is_installed = name in installed_names

        # Xây dựng node ID theo chuẩn T-11: Skill:<name>
        node_id = f"Skill:{name}"

        node_data = {
            "id": node_id,
            "kind": "Skill",
            "name": name,
            "title": name.replace("-", " ").title(),
            "domain": domain,
            "roles": roles,
            "description": desc or f"Kỹ năng {name}",
            "triggers": primary["triggers"],
            "allowed_tools": primary["allowed_tools"],
            "estimated_tokens": primary["tokens"],
            "line_count": primary["line_count"],
            "approved": is_approved,
            "installed": is_installed,
            "primary_source": {
                "repo": primary["repo"],
                "rel_path": primary["rel_path"],
                "sha256": primary["sha256"],
                "line_count": primary["line_count"],
            },
            "variant_count": len(variants),
            "variants": [
                {
                    "repo": v["repo"],
                    "rel_path": v["rel_path"],
                    "sha256": v["sha256"],
                    "line_count": v["line_count"],
                }
                for v in variants
            ],
            "relations": [
                {"type": "owned_by", "target": f"Role:{r}"} for r in roles
            ]
        }
        nodes[node_id] = node_data

    # 3. Tạo các quan hệ related_to giữa các skill liên quan
    skill_names = set(raw_skills_by_name.keys())
    for nid, node in nodes.items():
        desc_lower = node["description"].lower()
        for other_name in skill_names:
            if other_name != node["name"] and len(other_name) > 3 and other_name in desc_lower:
                node["relations"].append({"type": "related_to", "target": f"Skill:{other_name}"})

    now_utc = datetime.now(timezone.utc).isoformat()
    return {
        "schema_version": 2,
        "generated_at": now_utc,
        "taxonomy_domains": taxonomy_counts,
        "stats": {
            "total_skills": len(nodes),
            "total_variants": total_files,
            "total_approved": len(approved_skills),
            "total_installed": len(installed_names),
            "repos_scanned": sorted(list(repos_scanned)),
        },
        "nodes": list(nodes.values())
    }


def save_skill_graph(graph_data: Dict[str, Any], output_path: Path) -> None:
    """Ghi đồ thị kỹ năng ra file JSON với định dạng UTF-8 đẹp và chuẩn."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)


def load_skill_graph(graph_path: Path) -> Optional[Dict[str, Any]]:
    """Đọc file đồ thị skill-graph.json."""
    if not graph_path.exists():
        return None
    try:
        with open(graph_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def resolve_skill_path(node_or_source: Any, quarantine_dir: Optional[Path] = None, root_dir: Optional[Path] = None) -> Optional[Path]:
    """
    Phân giải đường dẫn động (Dynamic Path Resolution) cho máy hiện tại:
    Lấy relative path trong đồ thị và ghép với quarantine_dir cục bộ.
    Tuyệt đối không lưu vết đường dẫn tuyệt đối vào đồ thị.
    Hỗ trợ đầu vào: Node dict, Primary source dict, Variant dict, chuỗi str hoặc Path.
    """
    if quarantine_dir is None:
        quarantine_dir, _, _ = load_skills_config(root_dir)

    if not quarantine_dir or not quarantine_dir.exists():
        return None

    rel_path = None
    if isinstance(node_or_source, (str, Path)):
        rel_path = str(node_or_source)
    elif isinstance(node_or_source, dict):
        if "primary_source" in node_or_source and isinstance(node_or_source["primary_source"], dict):
            rel_path = node_or_source["primary_source"].get("rel_path")
        elif "rel_path" in node_or_source:
            rel_path = node_or_source.get("rel_path")

    if not rel_path:
        return None

    clean_rel = rel_path.lstrip("/\\")
    full_path = (quarantine_dir / clean_rel).resolve()
    return full_path if full_path.exists() else None


def check_skill_graph_drift(graph_data: Dict[str, Any], quarantine_dir: Path) -> Tuple[bool, Dict[str, Any]]:
    """
    Kiểm tra độ lệch giữa kho quarantine thực tế trên máy và file đồ thị.
    Phát hiện:
    - new_skills: file SKILL.md mới chưa có trong đồ thị
    - deleted_skills: file SKILL.md có trong đồ thị nhưng đã bị xóa
    - modified_skills: file SKILL.md có hash nội dung thay đổi
    """
    current_files: Dict[str, str] = {}
    for path in quarantine_dir.glob("**/SKILL.md"):
        parts = path.parts
        if ".git" in parts or "node_modules" in parts:
            continue
        try:
            rel = str(path.relative_to(quarantine_dir)).replace("\\", "/")
            content = path.read_text(encoding="utf-8", errors="ignore").replace("\r\n", "\n")
            h = hashlib.sha256(content.encode("utf-8")).hexdigest()
            current_files[rel] = h
        except Exception:
            continue

    graph_files: Dict[str, str] = {}
    for node in graph_data.get("nodes", []):
        if "variants" in node and isinstance(node["variants"], list):
            for v in node["variants"]:
                if isinstance(v, dict) and "rel_path" in v and "sha256" in v:
                    graph_files[v["rel_path"]] = v["sha256"]
        elif "primary_source" in node and isinstance(node["primary_source"], dict):
            ps = node["primary_source"]
            if "rel_path" in ps and "sha256" in ps:
                graph_files[ps["rel_path"]] = ps["sha256"]

    added = [p for p in current_files if p not in graph_files]
    deleted = [p for p in graph_files if p not in current_files]
    modified = [p for p in current_files if p in graph_files and current_files[p] != graph_files[p]]

    is_in_sync = len(added) == 0 and len(deleted) == 0 and len(modified) == 0
    return is_in_sync, {
        "added": added,
        "deleted": deleted,
        "modified": modified,
        "total_current": len(current_files),
        "total_in_graph": len(graph_files)
    }


# Từ điển Ánh xạ Ý định Song ngữ (Vietnamese-to-English Skill Intent Taxonomy)
VIETNAMESE_SKILL_SYNONYMS: Dict[str, List[str]] = {
    "vẽ": ["diagram", "drawio", "archify", "visualize"],
    "sơ đồ": ["diagram", "architecture", "flowchart", "sequence", "erd"],
    "kiến trúc": ["architecture", "adr", "system", "design", "archify"],
    "kiểm thử": ["test", "tdd", "testing", "qa", "verification", "junit"],
    "đơn vị": ["unit", "junit", "mockito"],
    "bảo mật": ["security", "cso", "vulnerability", "auth", "audit", "scan"],
    "nợ": ["debt", "ponytail"],
    "nợ kỹ thuật": ["debt", "ponytail"],
    "giao diện": ["ui", "ux", "frontend", "design", "component", "tailwind", "css"],
    "truy vấn": ["query", "sql", "jpa", "database", "postgres", "mysql"],
    "cơ sở dữ liệu": ["database", "postgres", "mysql", "liquibase", "migration", "jpa"],
    "tối ưu": ["optimize", "performance", "tuning", "lcp"],
    "lỗi": ["bug", "debug", "debugging", "investigate", "fix"],
    "sửa lỗi": ["debugging", "investigate", "troubleshoot", "systematic-debugging"],
    "nghiệp vụ": ["business", "domain", "spec", "ba", "requirements"],
    "phân tích": ["analyst", "analysis", "spec", "domain-modeling", "to-spec"],
    "đặc tả": ["spec", "specification", "to-spec", "requirements"],
    "chia việc": ["tickets", "to-tickets", "breakdown", "task"],
    "hàng đợi": ["queue", "kafka", "rabbitmq"],
    "bộ nhớ": ["memory", "leak", "cache", "redis"],
    "đăng nhập": ["auth", "authentication", "jwt", "session", "cookie"],
    "phân quyền": ["authorization", "permission", "rbac"],
    "đối soát": ["reconciliation", "accounting"],
    "đơn hàng": ["order", "orders"],
    "kho": ["warehouse", "inventory"],
    "công nợ": ["debt", "accounting"],
    "đánh giá": ["review", "critique", "eval", "audit"],
    "soi code": ["code-review", "open-code-review", "review"],
    "review code": ["open-code-review", "review", "code-review"],
    "khóa bảng": ["lock", "deadlock", "postgres", "migration"],
    "di chuyển dữ liệu": ["migration", "database-migrations"],
}


def _remove_vietnamese_accents(text: str) -> str:
    """Loại bỏ dấu tiếng Việt để hỗ trợ tìm kiếm không dấu."""
    s1 = "àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ"
    s0 = "aaaaaaaaaaaaaaaaaeeeeeeeeeeeiiiiiooooooooooooooooouuuuuuuuuuuyyyyydAAAAAAAAAAAAAAAAAEEEEEEEEEEEIIIIIOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYYD"
    res = []
    for c in text:
        idx = s1.find(c)
        res.append(s0[idx] if idx >= 0 else c)
    return "".join(res)


def search_skills(
    graph_data: Dict[str, Any],
    query: str,
    role: Optional[str] = None,
    budget: int = 1200,
    limit: int = 5,
    quarantine_dir: Optional[Path] = None,
    root_dir: Optional[Path] = None
) -> List[Dict[str, Any]]:
    """
    Tra cứu kỹ năng JIT (On-Demand Skill Retrieval) theo từ khóa và vai trò.
    Hỗ trợ xử lý Tiếng Việt (có dấu & không dấu) và ánh xạ từ đồng nghĩa song ngữ.
    Tự động phân giải đường dẫn cục bộ động cho máy hiện tại.
    """
    q_raw = (query or "").strip()
    q_lower = q_raw.lower()
    q_no_accents = _remove_vietnamese_accents(q_lower)

    # 1. Trích xuất token Unicode (hỗ trợ cả tiếng Việt và ký tự đặc biệt)
    raw_tokens = [kw for kw in re.findall(r'[\w\-]+', q_lower, re.UNICODE) if len(kw) > 1]
    no_accent_tokens = [kw for kw in re.findall(r'[\w\-]+', q_no_accents) if len(kw) > 1]

    # 2. Mở rộng từ khóa song ngữ qua bảng VIETNAMESE_SKILL_SYNONYMS
    expanded_english_terms: Set[str] = set()
    for phrase, en_terms in VIETNAMESE_SKILL_SYNONYMS.items():
        phrase_no_acc = _remove_vietnamese_accents(phrase)
        if phrase in q_lower or phrase_no_acc in q_no_accents:
            expanded_english_terms.update(en_terms)
        else:
            for token in raw_tokens + no_accent_tokens:
                if token == phrase or token == phrase_no_acc:
                    expanded_english_terms.update(en_terms)

    keywords = set(raw_tokens + no_accent_tokens)
    matched = []

    for node in graph_data.get("nodes", []):
        # Lọc RBAC theo vai trò nếu được chỉ định
        if role and role not in node.get("roles", []):
            continue

        name = node.get("name", "")
        name_lower = name.lower()
        desc = node.get("description", "")
        domain = node.get("domain", "")
        triggers = " ".join(node.get("triggers", []))
        corpus = f"{name} {desc} {domain} {triggers}".lower()
        corpus_words = set(re.findall(r'[\w\-]+', corpus, re.UNICODE))
        name_words = set(re.findall(r'[\w\-]+', name_lower, re.UNICODE))

        score = 0
        # 1. Khớp chính xác tên skill
        if q_lower == name_lower or q_no_accents == name_lower:
            score += 100
        elif q_lower in name_lower or q_no_accents in name_lower:
            score += 35

        # 2. Khớp cụm từ trong mô tả / corpus
        if q_lower in corpus or q_no_accents in corpus:
            score += 20

        # 3. Khớp từ khóa tiếng Anh mở rộng từ ý định tiếng Việt (High Priority Boost)
        for en_term in expanded_english_terms:
            if en_term == name_lower:
                score += 80
            elif en_term in name_words:
                score += 45
            elif en_term in name_lower:
                score += 25
            elif en_term in corpus_words:
                score += 15
            elif en_term in corpus:
                score += 8

        # 4. Khớp từng từ khóa gốc (token)
        for kw in keywords:
            if len(kw) <= 3:
                if kw in name_words:
                    score += 20
                elif kw in corpus_words:
                    score += 5
            else:
                if kw in name_words:
                    score += 15
                elif kw in name_lower:
                    score += 8
                elif kw in corpus_words:
                    score += 6
                elif kw in corpus:
                    score += 3

        if score > 0:
            # Gắn đường dẫn động phân giải cục bộ
            resolved_p = resolve_skill_path(node, quarantine_dir=quarantine_dir, root_dir=root_dir)
            item = dict(node)
            item["score"] = score
            item["local_path"] = str(resolved_p) if resolved_p else None
            item["file_uri"] = resolved_p.as_uri() if resolved_p else None
            matched.append((score, item))

    matched.sort(key=lambda x: x[0], reverse=True)
    results = []
    current_tokens = 0

    for score, item in matched[:limit]:
        item_tokens = item.get("estimated_tokens", 100)
        results.append(item)
        current_tokens += item_tokens
        if current_tokens >= budget and len(results) >= 2:
            break

    return results

