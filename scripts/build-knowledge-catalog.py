#!/usr/bin/env python3
"""scripts/build-knowledge-catalog.py

Biên dịch, kiểm chuẩn và phân vùng tri thức (Knowledge Graph) cho agent-base
dựa trên 2 nguồn tri thức:
1. Notebook 1: Agile SDLC & Scrum Release Management (CMMI L3, 13 Bước TDD, BACCM, RTM).
2. Notebook 2: Xây dựng niềm tin với kỹ sư AI (Lauren Tan - SpaceX / Cursor: Verification Skills, Feature Map, Eval Playbook).

Tuân thủ Python stdlib, không thêm dependency ngoài.
"""

from __future__ import annotations
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_core.knowledge.catalog import load_catalog, validate_catalog
from agent_core.knowledge.context import build_context, ContextRequest


def calculate_sha256(filepath: Path) -> str:
    """Tính hash sha256 cho tệp vật lý."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


# Danh mục các Node tri thức tinh hoa từ 2 Notebook
RAW_NODES = [
    # --- 1. ROLES (Định danh vai trò phục vụ quan hệ owned_by) ---
    {
        "id": "Role:dev",
        "kind": "Role",
        "title": "Developer / Worker Role",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/roles/dev.md",
        "owner_role": "catalog",
        "relations": [],
    },
    {
        "id": "Role:qa",
        "kind": "Role",
        "title": "Quality Assurance Role",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/roles/qa.md",
        "owner_role": "catalog",
        "relations": [],
    },
    {
        "id": "Role:reviewer",
        "kind": "Role",
        "title": "Code Reviewer Role",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/roles/reviewer.md",
        "owner_role": "catalog",
        "relations": [],
    },
    {
        "id": "Role:ba",
        "kind": "Role",
        "title": "Business Analyst Role",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/roles/ba.md",
        "owner_role": "catalog",
        "relations": [],
    },
    {
        "id": "Role:architect",
        "kind": "Role",
        "title": "System Architect Role",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/roles/architect.md",
        "owner_role": "catalog",
        "relations": [],
    },
    {
        "id": "Role:ai-eng",
        "kind": "Role",
        "title": "AI Engineer Role",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/roles/ai-eng.md",
        "owner_role": "catalog",
        "relations": [],
    },
    {
        "id": "Role:lead",
        "kind": "Role",
        "title": "Tech Lead / Head Chef Role",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/roles/lead.md",
        "owner_role": "catalog",
        "relations": [],
    },
    {
        "id": "Role:security",
        "kind": "Role",
        "title": "Security Engineer Role",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/roles/security.md",
        "owner_role": "catalog",
        "relations": [],
    },

    # --- 2. SOURCES (Nguồn tài liệu gốc) ---
    {
        "id": "Source:notebook1-agile-sdlc",
        "kind": "Source",
        "title": "Agile SDLC and Scrum Release Management Framework Source",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/quy-trinh/quy-trinh-13-buoc-tdd.md",
        "owner_role": "architect",
        "relations": [],
    },
    {
        "id": "Source:notebook2-spacex-ai-eng",
        "kind": "Source",
        "title": "High-Velocity Agent Framework Source",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/research/lauren-tan-talk.md",
        "owner_role": "ai-eng",
        "relations": [],
    },

    # --- 3. REQUIREMENTS & BUSINESS (Từ Notebook 1 & 2) ---
    {
        "id": "Requirement:baccm-and-cr",
        "kind": "Requirement",
        "title": "Mô hình BACCM, Quản lý Yêu cầu (RD) & Yêu cầu Thay đổi (CR)",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/quy-trinh/baccm-yeu-cau-va-cr.md",
        "owner_role": "ba",
        "relations": [
            {"type": "derived_from", "target": "Source:notebook1-agile-sdlc"},
            {"type": "owned_by", "target": "Role:ba"},
        ],
    },
    {
        "id": "Requirement:srs-writing-standard",
        "kind": "Requirement",
        "title": "SRS and FDD Writing Standard",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/srs/srs-fdd-writing-standard.md",
        "owner_role": "ba",
        "relations": [
            {"type": "derived_from", "target": "Source:notebook1-agile-sdlc"},
            {"type": "owned_by", "target": "Role:ba"},
        ],
    },

    # --- 4. RULES (Quy chuẩn thực thi, CMMI, TDD) ---
    {
        "id": "Design:tdd-13-steps",
        "kind": "Design",
        "title": "Quy trình 13 Bước TDD/ATDD & Tiêu chuẩn DoD",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/quy-trinh/quy-trinh-13-buoc-tdd.md",
        "owner_role": "dev",
        "relations": [
            {"type": "derived_from", "target": "Source:notebook1-agile-sdlc"},
            {"type": "owned_by", "target": "Role:dev"},
        ],
    },
    {
        "id": "Design:cmmi-l3-70-checks",
        "kind": "Design",
        "title": "Bộ 70 Mục kiểm CMMI Level 3 & PMBOK cho QA/Reviewer",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/quy-trinh/cmmi-l3-70-muc-kiem.md",
        "owner_role": "qa",
        "relations": [
            {"type": "derived_from", "target": "Source:notebook1-agile-sdlc"},
            {"type": "owned_by", "target": "Role:qa"},
        ],
    },
    {
        "id": "Design:cso-security",
        "kind": "Design",
        "title": "CSO Security Assessment Framework",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/cso-security-framework.md",
        "owner_role": "security",
        "relations": [
            {"type": "owned_by", "target": "Role:security"},
        ],
    },
    {
        "id": "Design:bug-handling-pipeline",
        "kind": "Design",
        "title": "Quy trình Xử lý Bug Hàng loạt",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/quy-trinh/xu-ly-bug-hang-loat.md",
        "owner_role": "qa",
        "relations": [
            {"type": "derived_from", "target": "Source:notebook1-agile-sdlc"},
            {"type": "owned_by", "target": "Role:qa"},
        ],
    },
    {
        "id": "Design:tech-radar-policy",
        "kind": "Design",
        "title": "Tech Radar Adoption Policy",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/tech-radar.md",
        "owner_role": "architect",
        "relations": [
            {"type": "owned_by", "target": "Role:architect"},
        ],
    },

    # --- 5. SKILLS (Kỹ năng thực chiến từ Notebook 2) ---
    {
        "id": "Skill:verification-skills-cdp",
        "kind": "Skill",
        "title": "Kỹ năng Tự Xác minh (Verification Skills), Feature Map & PR Nguyên tử",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/verification-skills-cdp.md",
        "owner_role": "dev",
        "relations": [
            {"type": "derived_from", "target": "Source:notebook2-spacex-ai-eng"},
            {"type": "owned_by", "target": "Role:dev"},
        ],
    },
    {
        "id": "Skill:skills-registry",
        "kind": "Skill",
        "title": "Agent Skills Registry & Taxonomy",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/skills.md",
        "owner_role": "architect",
        "relations": [
            {"type": "owned_by", "target": "Role:architect"},
        ],
    },

    # --- 6. EVAL SUITES & HARNESS ---
    {
        "id": "EvalSuite:eval-playbook-and-constraints",
        "kind": "EvalSuite",
        "title": "Eval Playbook, Agent Tái hiện Bug & 5 Tầng Ràng buộc Cứng",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/eval-playbook-va-hard-constraints.md",
        "owner_role": "ai-eng",
        "relations": [
            {"type": "derived_from", "target": "Source:notebook2-spacex-ai-eng"},
            {"type": "owned_by", "target": "Role:ai-eng"},
        ],
    },

    # --- 7. DESIGNS (Kiến trúc & Tiêu chuẩn) ---
    {
        "id": "Design:prompt-as-code-registry",
        "kind": "Design",
        "title": "Quản trị Prompt as Code, Thư viện Golden Prompts & Chỉ số Shift-Left",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/prompt-as-code-registry.md",
        "owner_role": "architect",
        "relations": [
            {"type": "derived_from", "target": "Source:notebook1-agile-sdlc"},
            {"type": "implements", "target": "Requirement:baccm-and-cr"},
            {"type": "owned_by", "target": "Role:architect"},
        ],
    },
    {
        "id": "Design:frontend-patterns",
        "kind": "Design",
        "title": "Frontend Component Contract and Design Patterns",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/frontend-patterns.md",
        "owner_role": "architect",
        "relations": [
            {"type": "owned_by", "target": "Role:architect"},
        ],
    },
    {
        "id": "Design:chuan-ve-so-do",
        "kind": "Design",
        "title": "Chuẩn Vẽ Sơ đồ Kỹ thuật và Kiến trúc",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/srs/chuan-ve-so-do.md",
        "owner_role": "architect",
        "relations": [
            {"type": "owned_by", "target": "Role:architect"},
        ],
    },

    # --- 8. PROTOCOL CHUẨN (nguồn quyết định, xem agents/protocols/source-precedence.md) ---
    # Chỉ Rule mới bị nạp bắt buộc cho MỌI vai khi đã approved; để tiết kiệm ngữ cảnh chỉ giữ hai Rule cốt lõi (task-loop, definition-of-done),
    # còn lại là Requirement/Design chỉ nạp cho vai sở hữu.
    {
        "id": "Source:company-process",
        "kind": "Source",
        "title": "Quy trình công ty (ghi chú từ tài liệu hướng dẫn)",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/quy-trinh/quy-trinh-cong-ty.md",
        "owner_role": "lead",
        "relations": [
            {"type": "owned_by", "target": "Role:lead"},
        ],
    },
    {
        "id": "Rule:task-loop",
        "kind": "Rule",
        "title": "Vòng 13 bước và 8 cổng kiểm soát một task (DoR 7 tiêu chí)",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/protocols/task-loop.md",
        "owner_role": "lead",
        "relations": [
            {"type": "owned_by", "target": "Role:lead"},
        ],
    },
    {
        "id": "Rule:definition-of-done",
        "kind": "Rule",
        "title": "Định nghĩa hoàn thành theo cỡ việc",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/protocols/definition-of-done.md",
        "owner_role": "lead",
        "relations": [
            {"type": "owned_by", "target": "Role:lead"},
        ],
    },
    {
        "id": "Design:git-rules",
        "kind": "Design",
        "title": "Quy tắc Git (GitFlow, commit, MR, hook)",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/protocols/git-rules.md",
        "owner_role": "lead",
        "relations": [
            {"type": "owned_by", "target": "Role:lead"},
        ],
    },
    {
        "id": "Requirement:change-request",
        "kind": "Requirement",
        "title": "Quản lý thay đổi yêu cầu (CR, CCB)",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/protocols/change-request.md",
        "owner_role": "ba",
        "relations": [
            {"type": "derived_from", "target": "Source:company-process"},
            {"type": "owned_by", "target": "Role:ba"},
        ],
    },
    {
        "id": "Requirement:ai-provenance",
        "kind": "Requirement",
        "title": "Đánh dấu nguồn gốc AI, sổ prompt, .aiignore",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/protocols/ai-provenance.md",
        "owner_role": "ai-eng",
        "relations": [
            {"type": "derived_from", "target": "Source:company-process"},
            {"type": "owned_by", "target": "Role:ai-eng"},
        ],
    },
    {
        "id": "Requirement:plan-critique",
        "kind": "Requirement",
        "title": "Lập kế hoạch và phản biện trước khi sinh code",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/protocols/plan-critique.md",
        "owner_role": "dev",
        "relations": [
            {"type": "derived_from", "target": "Source:company-process"},
            {"type": "owned_by", "target": "Role:dev"},
        ],
    },
    {
        "id": "Requirement:pair-review",
        "kind": "Requirement",
        "title": "Review theo cặp (Solution-Pair, Code-Review-Pair)",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/protocols/pair-review.md",
        "owner_role": "reviewer",
        "relations": [
            {"type": "derived_from", "target": "Source:company-process"},
            {"type": "owned_by", "target": "Role:reviewer"},
        ],
    },
    {
        "id": "Requirement:release-note",
        "kind": "Requirement",
        "title": "Release note",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/protocols/release-note.md",
        "owner_role": "lead",
        "relations": [
            {"type": "derived_from", "target": "Source:company-process"},
            {"type": "owned_by", "target": "Role:lead"},
        ],
    },
    {
        "id": "Requirement:lesson-learned",
        "kind": "Requirement",
        "title": "Bài học sau mỗi lần làm",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/protocols/lesson-learned.md",
        "owner_role": "lead",
        "relations": [
            {"type": "derived_from", "target": "Source:company-process"},
            {"type": "owned_by", "target": "Role:lead"},
        ],
    },
    {
        "id": "Requirement:ticket-status",
        "kind": "Requirement",
        "title": "Ánh xạ trạng thái ticket công ty sang task card",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/protocols/ticket-status.md",
        "owner_role": "lead",
        "relations": [
            {"type": "derived_from", "target": "Source:company-process"},
            {"type": "owned_by", "target": "Role:lead"},
        ],
    },

    # --- 9. TRI THỨC BỔ SUNG TỪ gdt-workspace ---
    {
        "id": "Design:chuan-code-va-review",
        "kind": "Design",
        "title": "Chuẩn code, cấu trúc và checklist review",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/chuan-code-va-review.md",
        "owner_role": "reviewer",
        "relations": [
            {"type": "owned_by", "target": "Role:reviewer"},
        ],
    },
    {
        "id": "Design:chuan-sql-va-loi",
        "kind": "Design",
        "title": "Chuẩn SQL và xử lý lỗi cơ sở dữ liệu",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/chuan-sql-va-loi.md",
        "owner_role": "architect",
        "relations": [
            {"type": "owned_by", "target": "Role:architect"},
        ],
    },
    {
        "id": "Design:zero-downtime-migrations",
        "kind": "Design",
        "title": "Di chuyển cơ sở dữ liệu không gián đoạn",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/zero-downtime-migrations.md",
        "owner_role": "architect",
        "relations": [
            {"type": "owned_by", "target": "Role:architect"},
        ],
    },
    {
        "id": "Design:cloud-recipes",
        "kind": "Design",
        "title": "Công thức kiến trúc đám mây",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/cloud-recipes.md",
        "owner_role": "architect",
        "relations": [
            {"type": "owned_by", "target": "Role:architect"},
        ],
    },
    {
        "id": "EvalSuite:llm-redteam-taxonomy",
        "kind": "EvalSuite",
        "title": "Phân loại lỗ hổng và kiểm thử ứng dụng AI/LLM",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/llm-redteam-taxonomy.md",
        "owner_role": "security",
        "relations": [
            {"type": "owned_by", "target": "Role:security"},
        ],
    },
    {
        "id": "Requirement:document-templates",
        "kind": "Requirement",
        "title": "Chỉ mục mẫu tài liệu (đặc tả, thiết kế, test report, TestLink)",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/templates/README.md",
        "owner_role": "ba",
        "relations": [
            {"type": "owned_by", "target": "Role:ba"},
        ],
    },
    {
        "id": "Source:harness2-recursive-harnessing",
        "kind": "Source",
        "title": "Harness2: Recursive Agent Harnessing (ghi chú nghiên cứu)",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/research/harness2.md",
        "owner_role": "ai-eng",
        "relations": [
            {"type": "owned_by", "target": "Role:ai-eng"},
        ],
    },
]


def build_catalog_manifest(root_dir: Path) -> dict:
    """Tự động tính toán hash sha256 cho toàn bộ nodes và tạo manifest json chuẩn."""
    nodes = []
    print(f"📦 Bắt đầu quét và tính toán sha256 cho {len(RAW_NODES)} nodes...")

    for raw in RAW_NODES:
        rel_path = raw["content_ref"]
        abs_path = root_dir / rel_path

        if not abs_path.is_file():
            print(f"❌ Cảnh báo: Tệp không tồn tại: {rel_path}")
            continue

        sha256 = calculate_sha256(abs_path)
        node_copy = dict(raw)
        node_copy["content_sha256"] = sha256
        node_copy["provenance"] = [r["target"] for r in raw["relations"] if r["type"] == "derived_from"]
        nodes.append(node_copy)

    apply_human_approvals(root_dir, nodes)
    manifest_data = {
        "schema_version": 1,
        "nodes": nodes,
    }
    return manifest_data


def apply_human_approvals(root_dir: Path, nodes: list, rel_path: str = "agents/knowledge/approvals.json") -> int:
    """Đổi state sang approved CHỈ khi con người đã ghi duyệt trong agents/knowledge/approvals.json.

    Theo agents/protocols/approval.md: AI không tự đóng dấu Approved; lời "ok" trong chat không có hiệu lực.
    File cần `approved_by` và `approved_at` khác rỗng, và `approved_ids` (danh sách id, hoặc ["*"] cho tất cả).
    """
    path = root_dir / rel_path
    if not path.is_file():
        return 0
    data = json.loads(path.read_text(encoding="utf-8"))
    if not str(data.get("approved_by", "")).strip() or not str(data.get("approved_at", "")).strip():
        print(f"ℹ️  {rel_path} chưa có người duyệt: mọi nút giữ state draft.")
        return 0
    ids = data.get("approved_ids", [])
    count = 0
    for node in nodes:
        if "*" in ids or node["id"] in ids:
            node["state"] = "approved"
            count += 1
    print(f"✅ Áp dụng duyệt của {data['approved_by']} ({data['approved_at']}) từ {rel_path}: {count} nút -> approved.")
    return count


def generate_role_contexts(root_dir: Path, manifest_path: Path):
    """Trích xuất và xuất các file ngữ cảnh riêng cho từng role."""
    catalog = load_catalog(str(root_dir), filename=str(manifest_path.relative_to(root_dir)))
    context_dir = root_dir / ".local" / "context"
    context_dir.mkdir(parents=True, exist_ok=True)

    target_roles = ["dev", "qa", "reviewer", "ba", "architect", "ai-eng", "lead", "security"]
    print(f"\n🎯 Đang phân vùng Scoped Context cho các vai trò vào: {context_dir.relative_to(root_dir)}/")

    for role in target_roles:
        req = ContextRequest(role=role, budget=30000, include_draft=True)
        bundle = build_context(catalog, req)
        out = bundle.to_dict()
        # Phụ lục dự thảo chỉ giữ mục lục (đường dẫn, tiêu đề, ước lượng token), không chép nội dung:
        # agent mở đúng file khi cần, tránh nạp lại toàn bộ tri thức vào ngữ cảnh.
        out["appendix"] = [
            {k: n.get(k) for k in ("id", "kind", "title", "state", "owner_role", "content_ref", "estimated_tokens")}
            for n in out.get("appendix", [])
        ]
        role_file = context_dir / f"{role}.json"
        with open(role_file, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        total_nodes = len(bundle.nodes) + len(bundle.appendix)
        print(f"  ✅ [{role.upper()}]: {total_nodes} nodes ({bundle.estimated_tokens:,} tokens) -> {role_file.name}")


def main():
    root_dir = ROOT
    manifest_path = root_dir / "agents" / "knowledge" / "knowledge-manifest.json"

    print("==================================================================")
    print("🚀 BIÊN DỊCH KNOWLEDGE GRAPH CHO AGENT-BASE (2 NOTEBOOKS)")
    print("==================================================================")

    # 1. Tính toán hash và lưu manifest
    manifest_data = build_catalog_manifest(root_dir)
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)
    print(f"💾 Đã lưu catalog manifest: {manifest_path.relative_to(root_dir)}")

    # 1b. Bản duyệt CỤC BỘ cho chính agent-base: manifest mẫu phải giữ toàn draft (tests/test_knowledge_seed.py),
    # nên dấu duyệt riêng của người dùng nằm ở .local/ (đã .gitignore, không nằm trong agents/manifest.txt
    # nên không mang sang dự án khác).
    import copy
    local_nodes = copy.deepcopy(manifest_data["nodes"])
    for n in local_nodes:
        n["state"] = "draft"
    local_rel = ".local/knowledge-approvals.json"
    if apply_human_approvals(root_dir, local_nodes, local_rel):
        local_manifest = root_dir / ".local" / "knowledge-manifest.json"
        local_manifest.parent.mkdir(parents=True, exist_ok=True)
        local_manifest.write_text(json.dumps({"schema_version": 1, "nodes": local_nodes}, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"💾 Đã lưu manifest cục bộ (đã duyệt): {local_manifest.relative_to(root_dir)}")
        context_manifest = local_manifest
    else:
        context_manifest = manifest_path

    # 2. Chạy 11 Validators tĩnh (V00 - V10)
    print("\n🔍 Đang kích hoạt 11 Bộ kiểm tra CMMI L3 (Validators V00 - V10)...")
    catalog = load_catalog(str(root_dir), filename="agents/knowledge/knowledge-manifest.json")
    diagnostics = validate_catalog(catalog)

    if diagnostics:
        print(f"❌ Phát hiện {len(diagnostics)} lỗi trong catalog:")
        for d in diagnostics:
            print(f"  - [{d.code}] {d.message} ({d.node_id})")
        sys.exit(1)
    else:
        print(f"✅ Tuyệt đối hợp lệ! 0 lỗi ({len(catalog.nodes)} nodes đã kiểm định thành công).")

    # 3. Phân vùng Scoped Context cho các Roles
    catalog = load_catalog(str(root_dir), filename=str(context_manifest.relative_to(root_dir)))
    generate_role_contexts(root_dir, context_manifest)

    print("\n==================================================================")
    print("🎉 HOÀN THÀNH TÍCH HỢP KNOWLEDGE GRAPH THÀNH CÔNG!")
    print("==================================================================")


if __name__ == "__main__":
    main()
