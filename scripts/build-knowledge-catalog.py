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

    # --- 10. SƠ ĐỒ (agents/knowledge/diagrams) ---
    {
        "id": "Role:designer",
        "kind": "Role",
        "title": "Designer Role",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/roles/designer.md",
        "owner_role": "catalog",
        "relations": [],
    },
    {
        "id": "Design:diagram-aws-architecture-icons-guide",
        "kind": "Design",
        "title": "Icon và bố cục hạ tầng AWS",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/diagrams/aws-architecture-icons-guide.md",
        "owner_role": "designer",
        "relations": [
            {"type": "owned_by", "target": "Role:designer"},
        ],
    },
    {
        "id": "Design:diagram-bpmn-20-camunda-guide",
        "kind": "Design",
        "title": "BPMN 2.0 Camunda",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/diagrams/bpmn-20-camunda-guide.md",
        "owner_role": "designer",
        "relations": [
            {"type": "owned_by", "target": "Role:designer"},
        ],
    },
    {
        "id": "Design:diagram-c4-plantuml-guide",
        "kind": "Design",
        "title": "C4-PlantUML",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/diagrams/c4-plantuml-guide.md",
        "owner_role": "designer",
        "relations": [
            {"type": "owned_by", "target": "Role:designer"},
        ],
    },
    {
        "id": "Design:diagram-dbml-and-d2-guide",
        "kind": "Design",
        "title": "DBML và D2",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/diagrams/dbml-and-d2-guide.md",
        "owner_role": "designer",
        "relations": [
            {"type": "owned_by", "target": "Role:designer"},
        ],
    },
    {
        "id": "Design:diagram-diagrams-cheatsheet-and-decision-matrix",
        "kind": "Design",
        "title": "Ma trận chọn công cụ vẽ sơ đồ",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/diagrams/diagrams-cheatsheet-and-decision-matrix.md",
        "owner_role": "designer",
        "relations": [
            {"type": "owned_by", "target": "Role:designer"},
        ],
    },
    {
        "id": "Design:diagram-drawio-csv-autolayout",
        "kind": "Design",
        "title": "Draw.io CSV Auto-Layout",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/diagrams/drawio-csv-autolayout.md",
        "owner_role": "designer",
        "relations": [
            {"type": "owned_by", "target": "Role:designer"},
        ],
    },
    {
        "id": "Design:diagram-drawio-icons-index",
        "kind": "Design",
        "title": "Danh mục icon Draw.io",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/diagrams/drawio-icons-index.md",
        "owner_role": "designer",
        "relations": [
            {"type": "owned_by", "target": "Role:designer"},
        ],
    },
    {
        "id": "Design:diagram-mermaid-syntax-guide",
        "kind": "Design",
        "title": "Cú pháp Mermaid",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/diagrams/mermaid-syntax-guide.md",
        "owner_role": "designer",
        "relations": [
            {"type": "owned_by", "target": "Role:designer"},
        ],
    },
    {
        "id": "Design:diagram-mo-ta-hoat-dong-so-do",
        "kind": "Design",
        "title": "Mô tả hoạt động đi kèm sơ đồ",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/diagrams/mo-ta-hoat-dong-so-do.md",
        "owner_role": "ba",
        "relations": [
            {"type": "owned_by", "target": "Role:ba"},
        ],
    },
    {
        "id": "Design:diagram-python-diagrams-and-drawpyo",
        "kind": "Design",
        "title": "Vẽ sơ đồ bằng Python diagrams và drawpyo",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/diagrams/python-diagrams-and-drawpyo.md",
        "owner_role": "designer",
        "relations": [
            {"type": "owned_by", "target": "Role:designer"},
        ],
    },
    {
        "id": "Design:diagram-quy-uoc-draw-io-va-archify",
        "kind": "Design",
        "title": "Quy ước vẽ và sửa sơ đồ bằng draw.io và archify",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/diagrams/quy-uoc-draw-io-va-archify.md",
        "owner_role": "designer",
        "relations": [
            {"type": "owned_by", "target": "Role:designer"},
        ],
    },
    {
        "id": "Design:diagram-structurizr-dsl-guide",
        "kind": "Design",
        "title": "Structurizr DSL",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/diagrams/structurizr-dsl-guide.md",
        "owner_role": "designer",
        "relations": [
            {"type": "owned_by", "target": "Role:designer"},
        ],
    },
    {
        "id": "Design:diagram-uml-25-guide",
        "kind": "Design",
        "title": "Tra cứu UML 2.5.1",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/diagrams/uml-25-guide.md",
        "owner_role": "designer",
        "relations": [
            {"type": "owned_by", "target": "Role:designer"},
        ],
    },
    {
        "id": "Design:playwright-and-k6-testing",
        "kind": "Design",
        "title": "Playwright E2E & Grafana K6 Load Testing Standards",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/playwright-and-k6-testing.md",
        "owner_role": "qa",
        "relations": [
            {"type": "owned_by", "target": "Role:qa"},
            {"type": "owned_by", "target": "Role:dev"},
        ],
    },
    {
        "id": "Design:openapi-commits-and-backstage",
        "kind": "Design",
        "title": "Conventional Commits, OpenAPI 3.0 & Backstage Software Catalog",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/openapi-commits-and-backstage.md",
        "owner_role": "architect",
        "relations": [
            {"type": "owned_by", "target": "Role:architect"},
            {"type": "owned_by", "target": "Role:dev"},
            {"type": "owned_by", "target": "Role:lead"},
        ],
    },


    # --- 11. KỸ THUẬT BỔ SUNG ---
    {
        "id": "Design:clean-architecture-and-ddd",
        "kind": "Design",
        "title": "Clean Architecture, DDD và mẫu thiết kế",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/clean-architecture-and-ddd.md",
        "owner_role": "architect",
        "relations": [
            {"type": "owned_by", "target": "Role:architect"},
        ],
    },
    {
        "id": "Design:kubernetes-architecture-and-manifests",
        "kind": "Design",
        "title": "Kiến trúc Kubernetes và manifest production",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/kubernetes-architecture-and-manifests.md",
        "owner_role": "architect",
        "relations": [
            {"type": "owned_by", "target": "Role:architect"},
        ],
    },
    {
        "id": "Design:sql-postgresql-and-jpa-hibernate",
        "kind": "Design",
        "title": "Tối ưu PostgreSQL và JPA/Hibernate",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/sql-postgresql-and-jpa-hibernate.md",
        "owner_role": "architect",
        "relations": [
            {"type": "owned_by", "target": "Role:architect"},
        ],
    },
    {
        "id": "Design:technical-writing-and-doc-standards",
        "kind": "Design",
        "title": "Technical Documentation Standards (Google, Microsoft & The Good Docs Project)",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/srs/technical-writing-and-doc-standards.md",
        "owner_role": "ba",
        "relations": [
            {"type": "owned_by", "target": "Role:ba"},
            {"type": "owned_by", "target": "Role:architect"},
        ],
    },
    {
        "id": "Design:postgresql-partitioning-and-performance",
        "kind": "Design",
        "title": "PostgreSQL Declarative Partitioning & Keyset Pagination (Use The Index Luke)",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/postgresql-partitioning-and-performance.md",
        "owner_role": "dev",
        "relations": [
            {"type": "owned_by", "target": "Role:dev"},
            {"type": "owned_by", "target": "Role:architect"},
        ],
    },
    {
        "id": "Design:redis-patterns-and-enterprise-architecture",
        "kind": "Design",
        "title": "Redis Architecture Patterns & Enterprise Application Patterns (Martin Fowler)",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/redis-patterns-and-enterprise-architecture.md",
        "owner_role": "architect",
        "relations": [
            {"type": "owned_by", "target": "Role:architect"},
            {"type": "owned_by", "target": "Role:dev"},
            {"type": "owned_by", "target": "Role:lead"},
        ],
    },
    {
        "id": "Design:clean-code-and-refactoring-guide",
        "kind": "Design",
        "title": "Clean Code, Martin Fowler Refactoring Catalog & Google Engineering Practices",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/clean-code-and-refactoring-guide.md",
        "owner_role": "dev",
        "relations": [
            {"type": "owned_by", "target": "Role:dev"},
            {"type": "owned_by", "target": "Role:reviewer"},
        ],
    },
    {
        "id": "Design:gof-design-patterns-and-solid",
        "kind": "Design",
        "title": "Detailed 23 GoF Design Patterns, SOLID & GRASP Principles",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/gof-design-patterns-and-solid.md",
        "owner_role": "architect",
        "relations": [
            {"type": "owned_by", "target": "Role:architect"},
            {"type": "owned_by", "target": "Role:dev"},
        ],
    },
    {
        "id": "Design:big-o-and-jvm-performance-tuning",
        "kind": "Design",
        "title": "Big-O Algorithmic Complexity & JVM Performance Tuning (Java 21 LTS)",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/big-o-and-jvm-performance-tuning.md",
        "owner_role": "dev",
        "relations": [
            {"type": "owned_by", "target": "Role:dev"},
            {"type": "owned_by", "target": "Role:architect"},
        ],
    },
    {
        "id": "Design:enterprise-integration-and-microservices-patterns",
        "kind": "Design",
        "title": "Enterprise Integration Patterns (EIP) & Microservices Patterns (Saga, Outbox)",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/enterprise-integration-and-microservices-patterns.md",
        "owner_role": "architect",
        "relations": [
            {"type": "owned_by", "target": "Role:architect"},
            {"type": "owned_by", "target": "Role:dev"},
            {"type": "owned_by", "target": "Role:lead"},
        ],
    },
    {
        "id": "Design:sonarqube-vault-and-terraform",
        "kind": "Design",
        "title": "SonarQube Quality Gates, HashiCorp Vault & Terraform (IaC)",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/sonarqube-vault-and-terraform.md",
        "owner_role": "security",
        "relations": [
            {"type": "owned_by", "target": "Role:security"},
            {"type": "owned_by", "target": "Role:architect"},
            {"type": "owned_by", "target": "Role:reviewer"},
        ],
    },
    {
        "id": "Design:distributed-systems-and-ddia",
        "kind": "Design",
        "title": "Designing Data-Intensive Applications (DDIA - Martin Kleppmann)",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/distributed-systems-and-ddia.md",
        "owner_role": "architect",
        "relations": [
            {"type": "owned_by", "target": "Role:architect"},
            {"type": "owned_by", "target": "Role:dev"},
            {"type": "owned_by", "target": "Role:lead"},
        ],
    },
    {
        "id": "Design:kafka-spark-and-iceberg-lakehouse",
        "kind": "Design",
        "title": "Apache Kafka, Apache Spark & Apache Iceberg Data Lakehouse Standards",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/kafka-spark-and-iceberg-lakehouse.md",
        "owner_role": "architect",
        "relations": [
            {"type": "owned_by", "target": "Role:architect"},
            {"type": "owned_by", "target": "Role:dev"},
            {"type": "owned_by", "target": "Role:ai-eng"},
        ],
    },
    {
        "id": "Design:mcp-and-bdd-testing",
        "kind": "Design",
        "title": "Model Context Protocol (MCP) & Cucumber BDD Testing Standards",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/mcp-and-bdd-testing.md",
        "owner_role": "ai-eng",
        "relations": [
            {"type": "owned_by", "target": "Role:ai-eng"},
            {"type": "owned_by", "target": "Role:qa"},
            {"type": "owned_by", "target": "Role:ba"},
        ],
    },
    {
        "id": "Design:junit5-mockito-testcontainers-and-jest",
        "kind": "Design",
        "title": "JUnit 5, Mockito, Testcontainers Real Database & Jest Frontend TDD",
        "state": "draft",
        "version": 1,
        "content_ref": "agents/knowledge/ky-thuat/junit5-mockito-testcontainers-and-jest.md",
        "owner_role": "dev",
        "relations": [
            {"type": "owned_by", "target": "Role:dev"},
            {"type": "owned_by", "target": "Role:qa"},
            {"type": "owned_by", "target": "Role:reviewer"},
        ],
    },
]


# ---------------------------------------------------------------------------
# Tự đăng ký nút cho file chưa có trong RAW_NODES (protocol, tri thức, skill) và nối cạnh liên quan.
# Thêm file mới vào agents/protocols, agents/knowledge hoặc .agents/skills thì chạy lại là có nút, không cần sửa tay.
# ---------------------------------------------------------------------------
import re

ROLE_NODES = {"dev", "qa", "reviewer", "ba", "architect", "ai-eng", "lead", "security", "designer"}
ROLE_ALIAS = {
    "analyst": "ba", "writer": "ba", "product": "ba", "researcher": "architect", "sre": "dev", "dba": "architect",
    "devops": "architect", "data-eng": "architect", "mobile": "dev", "debt-hunter": "reviewer", "runner": "qa",
    "model-tester": "qa",
}
PROTOCOL_OWNER = {
    "bug-repro": "qa", "challenger": "architect", "test-cases": "qa", "spec-writing": "ba", "intake": "ba",
    "hard-rules": "reviewer", "commit-plan": "dev", "task-branch": "dev", "worktree-lifecycle": "dev", "deploy": "dev",
    "mcp-policy": "security", "skill-eval": "ai-eng", "research-brief": "architect", "feature-map": "qa",
    "ui-fidelity": "designer", "atomic-changes": "reviewer", "harness-recursion": "lead",
}
KNOWLEDGE_OWNER = {
    "verification-cli-runbook": "qa", "glossary": "lead", "lauren-tan-primary-sources": "ai-eng", "graphify": "architect",
}

# Từ khóa và từ đồng nghĩa (tiếng Việt, tiếng Anh) để tra cứu theo từ khóa trúng hơn.
KEYWORDS = {
    "Design:sql-postgresql-and-jpa-hibernate": "sql chậm slow query chỉ mục index explain n+1 jpa hibernate postgres tối ưu truy vấn",
    "Design:chuan-sql-va-loi": "sql lỗi cơ sở dữ liệu database deadlock unique violation giao dịch transaction liquibase",
    "Design:zero-downtime-migrations": "migration đổi schema không dừng hệ thống expand contract đổi cột đổi tên bảng",
    "Design:diagram-mo-ta-hoat-dong-so-do": "mô tả sơ đồ hoạt động bước nhánh activity diagram description đọc sơ đồ",
    "Design:chuan-ve-so-do": "vẽ sơ đồ erd sequence activity use case state checklist diagram",
    "Design:tdd-13-steps": "tdd test trước 13 bước dod definition of done rtm",
    "Design:bug-handling-pipeline": "bug lỗi hàng loạt gom nhóm mantis tái hiện reproduce",
    "Design:git-rules": "git commit nhánh branch merge request tag release gitflow message",
    "Requirement:change-request": "thay đổi yêu cầu cr ccb change request",
    "Requirement:ai-provenance": "ai sinh code prompt registry aiignore nguồn gốc ai-generated",
    "Design:cso-security": "bảo mật audit lỗ hổng security vulnerability",
    "Design:kubernetes-architecture-and-manifests": "k8s kubernetes triển khai pod deployment manifest",
    "Design:redis-patterns-and-enterprise-architecture": "redis cache khóa phân tán distributed lock",
    "Requirement:srs-writing-standard": "srs đặc tả viết tài liệu fdd yêu cầu specification",
    "Design:clean-architecture-and-ddd": "kiến trúc sạch clean architecture ddd tầng domain hexagonal",
    "Requirement:plan-critique": "kế hoạch phản biện pseudo-code trước khi code probe",
    "Requirement:pair-review": "review cặp solution pair soát chéo",
    "Requirement:release-note": "phát hành release note changelog",
    "Requirement:lesson-learned": "bài học retro retrospective kinh nghiệm",
    "Requirement:ticket-status": "trạng thái ticket status board",
    "Design:chuan-code-va-review": "review code checklist soát code reviewer",
}

# Cụm kiến thức liên quan: "clique" nối mọi cặp, "star" nối phần tử đầu (hub) với các phần tử còn lại.
# Phần tử là id nút hoặc đường dẫn file (nút tự đăng ký có id suy ra từ đường dẫn).
RELATED_CLUSTERS = [
    ("clique", ["Design:diagram-mo-ta-hoat-dong-so-do", "Design:diagram-quy-uoc-draw-io-va-archify", "Design:chuan-ve-so-do",
                "Design:diagram-diagrams-cheatsheet-and-decision-matrix", "Skill:diagram-design", "Skill:archify"]),
    ("star", ["Design:diagram-diagrams-cheatsheet-and-decision-matrix", "Design:diagram-drawio-csv-autolayout",
              "Design:diagram-drawio-icons-index", "Design:diagram-python-diagrams-and-drawpyo", "Design:diagram-mermaid-syntax-guide",
              "Design:diagram-c4-plantuml-guide", "Design:diagram-structurizr-dsl-guide", "Design:diagram-dbml-and-d2-guide",
              "Design:diagram-uml-25-guide", "Design:diagram-bpmn-20-camunda-guide", "Design:diagram-aws-architecture-icons-guide"]),
    ("clique", ["Design:chuan-sql-va-loi", "Design:sql-postgresql-and-jpa-hibernate", "Design:postgresql-partitioning-and-performance",
                "Design:zero-downtime-migrations", "Skill:postgres-patterns", "Skill:jpa-patterns"]),
    ("clique", ["Design:junit5-mockito-testcontainers-and-jest", "Skill:springboot-tdd", "Skill:springboot-patterns",
                "Design:tdd-13-steps", "Skill:test-value", "Skill:subagent-driven-development", "Skill:systematic-debugging"]),
    ("clique", ["Rule:task-loop", "Rule:definition-of-done", "Design:tdd-13-steps", "Requirement:plan-critique",
                "Requirement:pair-review", "Requirement:ticket-status", "Requirement:lesson-learned", "Requirement:release-note"]),
    ("clique", ["Requirement:change-request", "Requirement:baccm-and-cr", "Requirement:srs-writing-standard",
                "Requirement:document-templates", "Design:technical-writing-and-doc-standards", "agents/protocols/spec-writing.md"]),
    ("clique", ["Design:git-rules", "Design:openapi-commits-and-backstage", "agents/protocols/commit-plan.md",
                "agents/protocols/task-branch.md", "agents/protocols/worktree-lifecycle.md"]),
    ("clique", ["Requirement:ai-provenance", "Design:prompt-as-code-registry", "EvalSuite:eval-playbook-and-constraints",
                "Skill:verification-skills-cdp", "Source:harness2-recursive-harnessing", "agents/protocols/hard-rules.md"]),
    ("clique", ["Design:cso-security", "EvalSuite:llm-redteam-taxonomy", "Skill:security-scan", "Skill:careful", "Skill:cso",
                "agents/protocols/mcp-policy.md"]),
    ("star", ["Design:clean-architecture-and-ddd", "Design:gof-design-patterns-and-solid", "Design:enterprise-integration-and-microservices-patterns",
              "Design:distributed-systems-and-ddia", "Design:redis-patterns-and-enterprise-architecture", "Skill:codebase-design",
              "Skill:domain-modeling", "Skill:architecture-decision-records", "Design:kafka-spark-and-iceberg-lakehouse",
              "Design:kubernetes-architecture-and-manifests", "Design:cloud-recipes"]),
    ("clique", ["Design:bug-handling-pipeline", "agents/protocols/bug-repro.md", "Skill:investigate", "Skill:systematic-debugging"]),
    ("clique", ["agents/protocols/approval.md", "agents/protocols/risk-gate.md", "agents/protocols/source-precedence.md",
                "Requirement:change-request"]),
    ("clique", ["Design:chuan-code-va-review", "agents/protocols/atomic-changes.md", "Skill:open-code-review", "Requirement:pair-review"]),
    ("clique", ["agents/protocols/test-cases.md", "Design:cmmi-l3-70-checks", "Skill:qa-web", "Design:junit5-mockito-testcontainers-and-jest"]),
    ("clique", ["Skill:plan-ceo-review", "Skill:plan-eng-review", "Skill:grilling", "Skill:to-spec", "Skill:to-tickets",
                "Skill:wayfinder", "agents/protocols/challenger.md"]),
]
RELATED_CLUSTERS += [
    ("clique", ["Design:clean-code-and-refactoring-guide", "Design:big-o-and-jvm-performance-tuning", "Design:chuan-code-va-review",
                "Design:gof-design-patterns-and-solid"]),
    ("clique", ["Design:playwright-and-k6-testing", "Design:mcp-and-bdd-testing", "Design:junit5-mockito-testcontainers-and-jest",
                "agents/protocols/test-cases.md"]),
    ("clique", ["Design:sonarqube-vault-and-terraform", "Design:cso-security", "Design:kubernetes-architecture-and-manifests",
                "Design:cloud-recipes"]),
    ("clique", ["Design:frontend-patterns", "Skill:ui-ux-pro-max", "Design:playwright-and-k6-testing"]),
    ("clique", ["Design:tech-radar-policy", "agents/protocols/research-brief.md", "Source:graphify",
                "Source:lauren-tan-primary-sources", "Source:harness2-recursive-harnessing"]),
    ("clique", ["Source:notebook1-agile-sdlc", "Design:tdd-13-steps", "Requirement:baccm-and-cr", "Design:cmmi-l3-70-checks"]),
    ("clique", ["Source:notebook2-spacex-ai-eng", "Design:prompt-as-code-registry", "EvalSuite:eval-playbook-and-constraints",
                "Skill:verification-skills-cdp"]),
    ("clique", ["Source:company-process", "Requirement:change-request", "Rule:task-loop", "Design:git-rules"]),
    ("star", ["Design:glossary", "Rule:task-loop", "Rule:definition-of-done"]),
    ("clique", ["Design:verification-cli-runbook", "Skill:verification-skills-cdp", "Design:tdd-13-steps"]),
]
FALLBACK_HUB = {"Requirement": "Rule:task-loop", "Skill": "Skill:skills-registry"}


def _h1(text, fallback):
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def _slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _registry_roles(root_dir):
    """Đọc cột 'Vai được dùng' trong sổ agents/knowledge/skills.md."""
    path = root_dir / "agents" / "knowledge" / "skills.md"
    out = {}
    if not path.is_file():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = [c.strip() for c in line.split("|")]
        if len(parts) > 7 and parts[1] and not parts[1].startswith(("Skill", "---")):
            out[parts[1]] = [r.strip() for r in parts[6].split(",") if r.strip()]
    return out


def _owners(roles):
    mapped = []
    for r in roles:
        r = ROLE_ALIAS.get(r, r)
        if r in ROLE_NODES and r not in mapped:
            mapped.append(r)
    return mapped or ["lead"]


def _neutral(title):
    """Tiêu đề trong manifest mẫu không mang tên người hay tên dự án (tests/test_knowledge_seed.py)."""
    title = re.sub(r"(?i)lauren tan", "bài nói của tác giả", title)
    return re.sub(r"(?i)\bgdt\b", "dự án", title)


def _auto_node(node_id, kind, title, ref, owners):
    title = _neutral(title)
    return {
        "id": node_id, "kind": kind, "title": title, "state": "draft", "version": 1, "content_ref": ref,
        "owner_role": owners[0],
        "relations": [{"type": "owned_by", "target": f"Role:{o}"} for o in owners],
    }


def auto_nodes(root_dir):
    # File cục bộ chưa muốn đưa vào catalog (ví dụ bản nháp chưa commit): .local/catalog-exclude.txt, mỗi dòng một đường dẫn.
    excl = root_dir / ".local" / "catalog-exclude.txt"
    skipped = {l.strip() for l in excl.read_text(encoding="utf-8").splitlines() if l.strip()} if excl.is_file() else set()
    taken_refs = {r["content_ref"] for r in RAW_NODES} | skipped
    taken_ids = {r["id"] for r in RAW_NODES}
    out = []

    def add(kind, base, title, ref, owners):
        if ref in taken_refs:
            return
        node_id = f"{kind}:{base}"
        if node_id in taken_ids:
            node_id = f"{kind}:{kind.lower()}-{base}"
        taken_ids.add(node_id)
        taken_refs.add(ref)
        out.append(_auto_node(node_id, kind, title, ref, owners))

    for path in sorted((root_dir / "agents" / "protocols").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        owner = PROTOCOL_OWNER.get(path.stem, "lead")
        add("Requirement", _slug(path.stem), _h1(text, path.stem), f"agents/protocols/{path.name}", [owner])

    for path in sorted((root_dir / "agents" / "knowledge").rglob("*.md")):
        rel = path.relative_to(root_dir).as_posix()
        if path.name == "README.md" or "/review-rules/" in rel:
            continue
        text = path.read_text(encoding="utf-8")
        kind = "Source" if "/research/" in rel else "Design"
        owner = KNOWLEDGE_OWNER.get(path.stem, "lead")
        add(kind, _slug(path.stem), _h1(text, path.stem), rel, [owner])

    registry = _registry_roles(root_dir)
    for path in sorted((root_dir / ".agents" / "skills").glob("*/SKILL.md")):
        name = path.parent.name
        text = path.read_text(encoding="utf-8", errors="replace")
        fm = re.search(r"^description:\s*(.+)$", text, re.M)
        desc = re.sub(r"\s+", " ", fm.group(1)).strip().strip("\"'")[:90] if fm else ""
        title = f"{name}: {desc}" if desc else name
        add("Skill", _slug(name), title, f".agents/skills/{name}/SKILL.md", _owners(registry.get(name, [])))
    return out


def add_keywords_and_related(nodes):
    by_id = {n["id"]: n for n in nodes}
    by_ref = {n["content_ref"]: n["id"] for n in nodes}
    for nid, words in KEYWORDS.items():
        if nid in by_id:
            by_id[nid]["keywords"] = words

    def resolve(x):
        return x if x in by_id else by_ref.get(x)

    def link(a, b):
        if not a or not b or a == b:
            return
        have = {(r["type"], r["target"]) for r in by_id[a]["relations"]}
        rev = {(r["type"], r["target"]) for r in by_id[b]["relations"]}
        if ("related_to", b) in have or ("related_to", a) in rev:
            return
        by_id[a]["relations"].append({"type": "related_to", "target": b})

    for kind, members in RELATED_CLUSTERS:
        ids = [m for m in (resolve(x) for x in members) if m]
        if kind == "star":
            for other in ids[1:]:
                link(ids[0], other)
        else:
            for i, a in enumerate(ids):
                for b in ids[i + 1:]:
                    link(a, b)

    def degree(nid):
        n = sum(1 for r in by_id[nid]["relations"] if r["type"] == "related_to")
        return n + sum(1 for m in nodes for r in m["relations"] if r["type"] == "related_to" and r["target"] == nid)

    for n in nodes:
        hub = FALLBACK_HUB.get(n["kind"])
        if hub and n["kind"] != "Role" and hub in by_id and n["id"] != hub and degree(n["id"]) == 0:
            link(n["id"], hub)



def build_catalog_manifest(root_dir: Path) -> dict:
    """Tự động tính toán hash sha256 cho toàn bộ nodes và tạo manifest json chuẩn."""
    nodes = []
    extra = auto_nodes(root_dir)
    print(f"📦 Bắt đầu quét và tính toán sha256 cho {len(RAW_NODES)} nodes khai báo + {len(extra)} nodes tự đăng ký...")

    for raw in list(RAW_NODES) + extra:
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

    add_keywords_and_related(nodes)
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

    target_roles = ["dev", "qa", "reviewer", "ba", "architect", "ai-eng", "lead", "security", "designer"]
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
