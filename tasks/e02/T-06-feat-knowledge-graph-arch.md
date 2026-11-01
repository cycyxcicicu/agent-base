---
id: T-06
size: medium
status: done
owner: architect
epic: E02
phase: GĐ2
outputs:
  - docs/spec/knowledge-graph-v2-architecture.md
branch: feature/06-knowledge-graph-arch
requirements: [REQ-KG-05]
scope_edit:
  - docs/spec/knowledge-graph-v2-architecture.md
scope_deny:
  - AGENTS.md
---

# T-06: Nghiên Cứu & Thiết Kế Kiến Trúc Knowledge Graph 2.0 Tối Ưu Cho AI

## Mục tiêu
Đánh giá toàn diện chuẩn Knowledge Graph hiện tại (146 nodes, JSON manifest) so với các chuẩn đồ thị tri thức AI tiên tiến trên thế giới (Graphify, MetaGPT SOPs, Aider RepoMap). Thiết kế kiến trúc Knowledge Graph 2.0 giúp: nạp siêu nhẹ, tìm kiếm O(1), phân vùng theo vai trò và hỗ trợ liên kết đa phương tiện (Ảnh + Markdown + Mã mẫu).

## Tài liệu tham chiếu
- Hệ thống hiện tại: `agent_core/knowledge/catalog.py`, `scripts/knowledge.py`.
- Các nguồn học tập: `LangGraph` (StateGraph), `Graphify` (Code graph), `MetaGPT` (Artifact-driven memory).

## Tiêu chuẩn Thiết kế Kiến trúc mới (Knowledge Graph 2.0):
1. **Hierarchical Taxonomy (Phân cấp cây tri thức rõ ràng)**:
   - Root ➔ Domain (Architecture, Database, Frontend, Workflow, Security) ➔ Topic ➔ Leaf Artifacts.
2. **Role-Based Access Control (RBAC)**:
   - Mỗi node khai báo danh sách vai trò được phép đọc: `accessible_by: ["architect", "dev"]`.
   - Ngăn chặn Agent này đọc lộn xộn tài liệu của Agent khác làm loãng context.
3. **Multi-Modal Linkage (Liên kết Ảnh - Code - Đặc tả)**:
   - Mỗi Node kỹ thuật cho phép liên kết 3 định dạng: `text_md`, `image_preview`, `template_code`.
4. **Token-Budget Bounded (Giới hạn ngân sách Token)**:
   - Mỗi kết quả tra cứu JIT không được vượt quá 800 tokens.

## Phân Rã Subtasks Kiểu Scrum & Phê Duyệt Kế Hoạch
- [x] **T-06.1** [Nghiên cứu đối chuẩn]: So sánh 4 mô hình Knowledge Representation cho Agent (JSON-LD, Tagged Markdown, Graph DB, Semantic Embeddings) · Assigned: `researcher`.
- [x] **T-06.2** [Thiết kế Schema 2.0]: Soạn thảo `schemas/knowledge-manifest-v2.schema.json` mở rộng trường `accessible_by`, `media_assets`, `sub_domain` · Assigned: `architect`.
- [x] **T-06.3** [Viết Đặc Tả Kiến Trúc]: Hoàn thiện tài liệu `docs/spec/knowledge-graph-v2-architecture.md` · Assigned: `architect`.

## Tiêu chí xong
- [x] Tài liệu kiến trúc Knowledge Graph 2.0 được phê duyệt.
- [x] Schema JSON mới tương thích ngược với 146 nodes hiện tại và hỗ trợ mở rộng.
