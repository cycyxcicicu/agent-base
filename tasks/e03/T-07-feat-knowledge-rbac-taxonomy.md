---
id: T-07
size: large
status: done
owner: dev
epic: E03
phase: GĐ3
outputs:
  - agents/knowledge/
  - scripts/knowledge.py
branch: feature/07-knowledge-rbac-taxonomy
requirements: [REQ-KG-06]
scope_edit:
  - agents/knowledge/**
  - scripts/knowledge.py
  - agent_core/knowledge/**
scope_deny:
  - AGENTS.md
---

# T-07: Tái Cấu Trúc Kho Tri Thức Theo Phân Vùng Role-Based & Nạp Dữ Liệu Mới

## Mục tiêu
Tổ chức lại toàn bộ thư mục tri thức vật lý trong `agents/knowledge/` và đồ thị luận lý thành các phân vùng chuyên môn. Cập nhật `scripts/knowledge.py` để thực thi luật phân quyền: Agent thuộc vai nào chỉ được truy cập vào kho tri thức của vai đó, đồng thời nạp toàn bộ các tri thức chất lượng cao đã cào từ UML và M2MBA vào hệ thống.

## Phân Vùng Kho Tri Thức Cụ Thể:
- `agents/knowledge/architecture/`: Dành riêng cho `architect`, `lead` (ADR, Arc42, DDD Hexagonal, C4 model).
- `agents/knowledge/database/`: Dành riêng cho `dba`, `backend-dev` (JPA N+1, Indexing, Zero-downtime migration).
- `agents/knowledge/diagrams/`: Dành riêng cho `designer`, `architect` (14 loại sơ đồ UML, ảnh mẫu, quy chuẩn swimlane).
- `agents/knowledge/business-analysis/`: Dành riêng cho `ba`, `product` (Phân tích nghiệp vụ từ M2MBA, User Story, BR rules).
- `agents/knowledge/coding-standards/`: Dành riêng cho `dev`, `reviewer` (Alibaba P3C Java, Spring Boot TDD, Clean code).
- `agents/knowledge/quality-assurance/`: Dành riêng cho `qa`, `runner` (ATDD, TestLink XML, ISTQB test cases).
- `agents/knowledge/security/`: Dành riêng cho `security`, `sre` (CSO checklist, OWASP, LLM Red-teaming).

## Phân Rã Subtasks Kiểu Scrum & Phê Duyệt Kế Hoạch
- [x] **T-07.1** [Tái cấu trúc thư mục]: Di chuyển và sắp xếp lại các file tri thức trong `agents/knowledge/` vào 7 thư mục chuyên môn · Assigned: `writer`.
- [x] **T-07.2** [Nạp tri thức UML & M2MBA]: Chuyển các mẫu sơ đồ UML (kèm ảnh và template) và bài học M2MBA đã chọn lọc vào các thư mục tương ứng · Assigned: `analyst`.
- [x] **T-07.3** [Nâng cấp Engine RBAC]: Sửa `agent_core/knowledge/catalog.py` và `scripts/knowledge.py` để bổ sung cờ `--role <tên_vai>`: Chỉ trả về tri thức mà vai đó được quyền đọc (`accessible_by`) · Assigned: `dev`.
- [x] **T-07.4** [Tái tạo Catalog]: Chạy `python scripts/build-knowledge-catalog.py` sinh lại `knowledge-manifest.json` đạt chuẩn 100% không lỗi (148 nodes) · Assigned: `runner`.

## Tiêu chí xong
- [x] Thư mục tri thức được phân vùng gọn gàng, mạch lạc.
- [x] Lệnh `python scripts/knowledge.py query -q "..." --role dev` chỉ trả về tri thức của dev, không lộ tài liệu của DBA hay Security.
- [x] `python scripts/knowledge.py validate --root .` đạt 0 lỗi.
