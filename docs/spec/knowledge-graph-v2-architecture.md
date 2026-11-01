# Kiến Trúc Knowledge Graph 2.0: Tối Ưu Hóa Truy Xuất & Ngân Sách Token Cho Multi-Agent Swarm

> **Tài liệu**: Đặc tả thiết kế kỹ thuật (Architectural Specification)  
> **Tác giả**: Architect Agent  
> **Trạng thái**: APPROVED (Phê duyệt áp dụng)  
> **Phiên bản**: 2.0.0  
> **Tham chiếu Task**: T-06 (Epic E02)  

---

## 1. Bối Cảnh & Động Lực (Problem Statement)

Hệ thống `agent-base` phiên bản 1.0 quản lý 146 nodes tri thức thông qua file manifest phẳng (`agents/knowledge/knowledge-manifest.json`). Mặc dù cơ chế tra cứu động `scripts/knowledge.py query` đã giúp giảm tải việc nạp toàn bộ thư mục, hệ thống vẫn tồn tại 4 điểm nghẽn nghiêm trọng:
1. **Thiếu phân quyền theo vai trò (No RBAC)**: Bất kỳ Agent nào cũng có thể truy xuất vào bất kỳ node tri thức nào, dẫn đến việc `dev` nạp nhầm quy trình quản trị của `lead`, hoặc `qa` nạp nhầm spec triển khai của `devops`, làm loãng context.
2. **Context Bloat (>200k - 500k tokens)**: Một số skills khổng lồ (`ui-ux-pro-max` 3.78 MB, `diagram-design` 3.07 MB) và 20 file rules vai trò bị nạp tĩnh trực tiếp vào system prompt khiến chi phí khởi tạo một phiên làm việc quá lớn.
3. **Thiếu liên kết đa phương tiện (No Multi-Modal Linkage)**: Tri thức vẽ sơ đồ chỉ mô tả bằng text/Mermaid trần trụi, thiếu liên kết đến file ảnh mẫu thực tế (`.png`, `.svg`) và template vẽ máy (`.drawio`, `.json`).
4. **Phân vùng thư mục tự do**: Các file tri thức nằm rải rác trong `ky-thuat/`, `quy-trinh/`, `srs/` chưa được tổ chức theo cấu trúc phân cấp chặt chẽ (Taxonomy).

---

## 2. Kiến Trúc Knowledge Graph 2.0 (Toàn Cảnh)

Knowledge Graph 2.0 chuyển đổi từ đồ thị phẳng sang **Đồ thị phân cấp có kiểm soát truy cập (Hierarchical RBAC Knowledge Graph)** với 3 trụ cột chính:

```
                            [ ROOT REPOSITORY ]
                                     |
    +--------------------------------+--------------------------------+
    |                                |                                |
[DOMAIN 1: Architecture]   [DOMAIN 2: Business/BA]       [DOMAIN 3: Development]
    |                                |                                |
  +-+--+                           +-+--+                           +-+--+
  |    |                           |    |                           |    |
[UML] [DDD]                      [SRS] [BABOK]                    [TDD] [JPA]
  |    |                           |    |                           |    |
  * Leaf Nodes (Markdown Spec + DrawIO Template + Golden Image Asset) *
```

### 2.1. Bảy Phân Vùng Tri Thức Chuẩn (7 Taxonomy Domains)
1. `architecture/`: Mẫu kiến trúc Clean, Hexagonal DDD, Outbox, Caching, Sơ đồ UML 2.5 (Sequence, Class, Component).
2. `business/`: Phân tích nghiệp vụ BA, tiêu chuẩn BABOK, khung MBA, kỹ thuật phỏng vấn, Domain Glossary.
3. `development/`: Kỹ thuật lập trình Spring Boot, JPA/Hibernate, SQL Indexing, Clean Code, Anti-patterns.
4. `testing/`: Kỹ thuật ATDD/TDD 13 bước, BDD Gherkin, Testcontainers, TestLink XML, Boundary Testing.
5. `devops/`: CI/CD pipelines, Docker Distroless, Kubernetes manifests, Monitoring, Risk Gates.
6. `ai-engineering/`: Prompt as Code, RAG pipeline, Vector search, MCP tool calling, Multi-agent debate.
7. `management/`: CMMI Level 3 checklist, DoR/DoD, CCB Change Management, Release train.

---

## 3. Cơ Chế Phân Quyền Vai Trò (Role-Based Access Control - RBAC)

Mỗi node tri thức trong `knowledge-manifest.json` được bổ sung trường `roles: string[]`:

```json
{
  "id": "uml-activity-diagram-spec",
  "domain": "architecture",
  "path": "agents/knowledge/srs/uml-activity-diagrams.md",
  "roles": ["architect", "ba", "designer"],
  "summary": "Quy chuẩn vẽ Activity Diagram: bơi làn swimlane, 1 start, 1 end, nhánh lỗi màu đỏ.",
  "tags": ["uml", "activity", "diagram", "drawio"],
  "media_assets": {
    "diagram_template": "D:/test-repo/uml/activity-diagram/template.drawio",
    "json_spec": "D:/test-repo/uml/activity-diagram/template.json",
    "preview_image": "D:/test-repo/uml/activity-diagram/images/activity-diagram-overview.png"
  },
  "token_budget": 850
}
```

### Quy Tắc RBAC Thực Thi:
1. Khi Agent đóng vai `dev` gọi lệnh `scripts/knowledge.py query --role dev`, hệ thống **chỉ quét và trả về** các node có `"dev"` trong trường `roles`. Mọi node thuộc `management` hay `devops` bị ẩn hoàn toàn.
2. Nếu Agent cần truy cập tài liệu ngoài vai trò, nó phải gửi yêu cầu xin phân quyền hoặc thông qua Lead phân công subagent đúng vai.

---

## 4. Ngân Sách Token & Cơ Chế Nạp JIT (Just-In-Time)

* **Nguyên tắc "Zero-Shot Bloat"**: Nghiêm cấm nạp sẵn bất kỳ node tri thức nào vào System Prompt khởi động.
* **Ngân sách tối đa mỗi lần truy xuất**: **<= 1.200 tokens**.
* **Định dạng trả về siêu nén**: Khi query, hệ thống chỉ trả về:
  1. *Đường dẫn file* (`file://...`)
  2. *Tóm tắt lõi 3 dòng* (Core rules & hard constraints)
  3. *Mẫu code/XML ngắn nhất* (Minimal executable snippet)
  4. *Đường dẫn ảnh mẫu cục bộ* (Local preview image path)

---

## 5. Kế Hoạch Di Chuyển & Tương Thích Ngược (Migration Plan)

* **Giai đoạn 1**: Bổ sung parser RBAC trong `agent_core/knowledge/catalog.py` hỗ trợ cả định dạng v1 (mặc định cho phép tất cả các vai) và v2 (có trường `roles`).
* **Giai đoạn 2**: Tái cấu trúc thư mục `agents/knowledge/` thành 7 domains chuẩn và cập nhật manifest.
* **Giai đoạn 3**: Chạy `python scripts/refresh.py --check` đảm bảo 100% hash toàn vẹn không bị hỏng hóc.

