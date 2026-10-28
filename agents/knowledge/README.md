# Chỉ mục tri thức dùng chung

Agent không đọc cả thư mục này. Tra bảng, mở đúng file khớp việc đang làm (tối đa vài file), hoặc dùng lệnh trích xuất tự động:
`python scripts/knowledge.py context --root . --manifest agents/knowledge/knowledge-manifest.json --role <vai>`


## Gặp việc này thì tra từ khóa này

Không nạp sẵn. Gặp việc thuộc dòng nào thì chạy `python scripts/knowledge.py query -q "<từ khóa>" --role <vai>`; kết quả kèm tóm tắt, mục, và các nút liên quan nối bằng cạnh.

| Việc đang làm | Từ khóa gợi ý |
|---|---|
| Viết hoặc tối ưu SQL, JPA, chỉ mục | `sql chậm`, `jpa n+1`, `chỉ mục` |
| Đổi schema, migration | `migration không dừng hệ thống` |
| Vẽ hoặc mô tả sơ đồ | `sơ đồ hoạt động`, `mô tả sơ đồ`, `drawio` |
| Viết đặc tả SRS và sơ đồ từ đầu đến cuối | `viết srs quy trình`, `srs đặc tả`, `mẫu tài liệu` |
| Đổi yêu cầu đã duyệt | `thay đổi yêu cầu ccb` |
| Xử lý nhiều bug | `bug hàng loạt` |
| Viết test, TDD | `tdd spring boot`, `testcontainers` |
| Review code | `review code checklist` |
| Commit, nhánh, MR | `git commit nhánh` |
| Phát hành, bài học | `release note`, `bài học` |
| Kiến trúc, mẫu thiết kế | `clean architecture`, `ddd`, `saga outbox` |
| Bảo mật | `bảo mật audit`, `security` |
| Dùng AI, prompt | `prompt registry`, `ai sinh code` |
| Chia việc lớn | `wayfinder`, `chia task` |

Tra mà ra rỗng: thử từ đồng nghĩa (tiếng Anh hoặc Việt). Thêm cặp đồng nghĩa vào `agents/knowledge/synonyms.json` (sửa tay được). Tra không cần gõ dấu.

**Hook gợi ý tự động (tùy chọn, chỉ Claude Code):** `scripts/knowledge-hook.py` chèn 1–3 dòng gợi ý khi lời người dùng khớp rõ một chủ đề, im lặng nếu không. Mặc định tắt vì điểm khớp từ khóa không tách sạch lời thường khỏi lời có chủ đề; cổng đặt chặt (0/15 lời thường lọt, bắt khoảng 43% lời có chủ đề). Cách bật: xem đầu file `scripts/knowledge-hook.py`. Nhật ký tra cứu nằm ở `.local/knowledge-usage.jsonl` (cục bộ) để biết từ khóa nào cần bổ sung.

## 1. Tinh hoa từ 2 Notebook Tri thức (AI-Augmented SDLC & High-Velocity Agent)

Tổng hợp từ:
- **Notebook 1:** *Agile SDLC & Scrum Release Management* (CMMI Level 3, 13 Bước TDD, BACCM, RTM).
- **Notebook 2:** *Xây dựng niềm tin với kỹ sư AI* (Lauren Tan - SpaceX / Cursor: Verification Skills, Feature Map, Eval Playbook).

| Khi nào | Đọc |
|---|---|
| **Thực thi lập trình:** Chu trình 13 bước TDD/ATDD, dừng ở Bước 11 (Chờ xác nhận), quy ước thẻ `@rtm-ref` và 11 tiêu chí Definition of Done (DoD) | `quy-trinh/quy-trinh-13-buoc-tdd.md` |
| **Kiểm định chất lượng & Review:** Bộ 70 mục kiểm CMMI Level 3 phủ 8 nhóm chỉ số (CM, PPQA, TS, DAR, RSKM, VER/VAL, KG, REQM) và mẫu báo cáo nghiệm thu | `quy-trinh/cmmi-l3-70-muc-kiem.md` |
| **Phân tích nghiệp vụ & Sẵn sàng:** Mô hình 6 khái niệm lõi BACCM, quy trình Quản lý Yêu cầu (RD), Quản lý Thay đổi (CR) qua CCB và 7 tiêu chí Definition of Ready (DoR) | `quy-trinh/baccm-yeu-cau-va-cr.md` |
| **Tự xác minh & Giao diện:** Kỹ năng tự chứng minh qua Chrome DevTools Protocol (`CDP`), CPU/Heap traces, lập Feature Map UI và chia PR nguyên tử | `ky-thuat/verification-skills-cdp.md` |
| **Đánh giá Agent & Rào chắn:** Eval Playbook (chấm điểm bằng Judge Agent độc lập, tối ưu leo dốc `/loop` 10/10), Benny tự tái hiện bug và 5 tầng ràng buộc cứng | `ky-thuat/eval-playbook-va-hard-constraints.md` |
| **Quản trị Prompt & Tối ưu chi phí:** Prompt as Code, quy trình nghiệm thu Golden Prompts 3 bước, bảng chi phí sửa lỗi Shift-Left ($1\times \rightarrow 30\times$) và GitFlow Release Train | `ky-thuat/prompt-as-code-registry.md` |
| **Kiến trúc Clean & DDD:** Clean Architecture 4 tầng, Domain-Driven Design (Aggregate Root, Entity, Value Object, CQRS) và GoF Patterns |  |
| **Cơ sở dữ liệu & JPA:** Tối ưu hóa PostgreSQL (B-Tree, Covering Index), xử lý N+1, Dirty Checking và khóa Pessimistic/Optimistic |  |
| **Hạ tầng Kubernetes:** Cụm K8s Control Plane/Worker, chuẩn Manifests Production (RollingUpdate, Resource Limits, Probes) |  |

## 2. Từ dự án gdt-workspace (bổ sung phần khung còn thiếu)

Nguồn: dự án gdt-workspace, đã dùng thật. Còn nhắc Mantis, TestLink, thư mục `doc/` là quy ước của gdt; dự án khác thay bằng công cụ của mình.

| Khi nào | Đọc |
|---|---|
| Biết quy trình công ty yêu cầu gì (vòng SDLC, DoR/DoD, CR, kiểm thử, dùng AI, Git/CI-CD) và khung còn thiếu gì | `quy-trinh/quy-trinh-cong-ty.md` |
| Nhận một danh sách bug: lọc, gom nhóm, xếp ưu tiên, tái hiện từng nhóm trước khi sửa (bổ sung cho `protocols/bug-repro.md`, vốn xử lý từng bug) | `quy-trinh/xu-ly-bug-hang-loat.md` |
| Review code: checklist dữ liệu/SQL, giao dịch và đồng thời, lỗi và log | `ky-thuat/chuan-code-va-review.md` |
| Viết SQL, xử lý lỗi cơ sở dữ liệu, giao dịch, migration | `ky-thuat/chuan-sql-va-loi.md` |
| Vẽ sơ đồ: quy tắc theo loại (sequence, ERD, state, activity), checklist nộp sơ đồ (bổ sung cho `docs/design/diagram-guide.md`, vốn lo thẩm mỹ) | `srs/chuan-ve-so-do.md` |
| Viết tài liệu đặc tả theo mẫu SRS_FDD: văn phong, checklist, NFR, ba file mỗi chức năng | `srs/srs-fdd-writing-standard.md` |
| Chuẩn viết tài liệu kỹ thuật: Google Style, Microsoft Guide và The Good Docs Project (Diátaxis) | `srs/technical-writing-and-doc-standards.md` |
| Mẫu để viết (đặc tả, thiết kế kỹ thuật, Excel SRS_FDD, test report, TestLink) | thư mục `agents/templates/`, xem `agents/templates/README.md` |

## Sơ đồ (`diagrams/`)

Bắt đầu từ ba file đầu: chuẩn dự án đi trước, công cụ bổ sung chỉ khi dự án chọn.

| Khi nào | Đọc |
|---|---|
| Viết phần chữ mô tả hoạt động đi kèm sơ đồ (bước, nhánh, dữ liệu) để agent hiểu hết sơ đồ; đọc nhanh `.drawio` bằng `scripts/diagram-describe.py` | `diagrams/mo-ta-hoat-dong-so-do.md` |
| Chọn công cụ nguồn cho từng loại sơ đồ, viết và sửa `.drawio`, xuất ảnh, bài học vẽ bơi làn | `diagrams/quy-uoc-draw-io-va-archify.md` |
| Ma trận chọn công cụ vẽ sơ đồ; thứ tự áp dụng chuẩn dự án đi trước | `diagrams/diagrams-cheatsheet-and-decision-matrix.md` |
| Icon và bố cục hạ tầng AWS | `diagrams/aws-architecture-icons-guide.md` |
| Quy trình nghiệp vụ theo BPMN 2.0 (Camunda) | `diagrams/bpmn-20-camunda-guide.md` |
| Mô hình C4 bằng C4-PlantUML | `diagrams/c4-plantuml-guide.md` |
| Thiết kế schema bằng DBML; kiến trúc bằng D2 | `diagrams/dbml-and-d2-guide.md` |
| Sinh bản nháp `.drawio` có icon bằng CSV auto-layout | `diagrams/drawio-csv-autolayout.md` |
| Tra tên shape và icon khi viết `style` của draw.io | `diagrams/drawio-icons-index.md` |
| Cú pháp Mermaid cho sơ đồ nhỏ trong md | `diagrams/mermaid-syntax-guide.md` |
| Sinh sơ đồ bằng Python (cần cài gói, hỏi trước) | `diagrams/python-diagrams-and-drawpyo.md` |
| Mô hình C4 bằng Structurizr DSL | `diagrams/structurizr-dsl-guide.md` |
| Tra cứu cú pháp UML 2.5.1 | `diagrams/uml-25-guide.md` |

## Chuyên đề kỹ thuật và an ninh

| Khi nào | Đọc |
|---|---|
| Clean Architecture, DDD, mẫu thiết kế GoF | `ky-thuat/clean-architecture-and-ddd.md` |
| Kubernetes: kiến trúc, manifest production (chưa xác nhận dự án dùng) | `ky-thuat/kubernetes-architecture-and-manifests.md` |
| Kiểm thử E2E & Load Testing: Playwright và Grafana K6 | `ky-thuat/playwright-and-k6-testing.md` |
| Chuẩn Commit, API & Backstage: Conventional Commits, OpenAPI 3.0, Backstage | `ky-thuat/openapi-commits-and-backstage.md` |
| Tối ưu PostgreSQL, chỉ mục, JPA/Hibernate thực hành | `ky-thuat/sql-postgresql-and-jpa-hibernate.md` |
| PostgreSQL Partitioning, tối ưu hóa hiệu năng & Keyset Pagination | `ky-thuat/postgresql-partitioning-and-performance.md` |
| Redis Architecture Patterns & Enterprise Application Patterns (Martin Fowler) | `ky-thuat/redis-patterns-and-enterprise-architecture.md` |
| Clean Code, Refactoring & Google Engineering Practices | `ky-thuat/clean-code-and-refactoring-guide.md` |
| Chi tiết 23 GoF Design Patterns & Nguyên lý SOLID / GRASP | `ky-thuat/gof-design-patterns-and-solid.md` |
| Tối ưu Big-O, cấu trúc dữ liệu & Quản trị bộ nhớ JVM (Java 21) | `ky-thuat/big-o-and-jvm-performance-tuning.md` |
| Enterprise Integration Patterns (EIP) & Microservices Patterns (Saga, Outbox) | `ky-thuat/enterprise-integration-and-microservices-patterns.md` |
| SonarQube Quality Gates, HashiCorp Vault & Terraform (IaC) | `ky-thuat/sonarqube-vault-and-terraform.md` |
| Hệ thống phân tán, mô hình lưu trữ & Quorum Consensus (DDIA) | `ky-thuat/distributed-systems-and-ddia.md` |
| Apache Kafka, Apache Spark & Apache Iceberg Data Lakehouse | `ky-thuat/kafka-spark-and-iceberg-lakehouse.md` |
| Model Context Protocol (MCP) & BDD Testing với Cucumber | `ky-thuat/mcp-and-bdd-testing.md` |
| JUnit 5, Mockito, Testcontainers & Frontend Jest TDD | `ky-thuat/junit5-mockito-testcontainers-and-jest.md` |
| Chọn công nghệ, xem công nghệ đã duyệt | `tech-radar.md` |
| Đổi schema không gián đoạn (expand-contract) | `zero-downtime-migrations.md` |
| Frontend: RSC, store, compound component | `frontend-patterns.md` |
| Hạ tầng đám mây | `cloud-recipes.md` |
| Kiểm toán bảo mật, lệnh nguy hiểm | `cso-security-framework.md` |
| Kiểm thử ứng dụng AI/LLM | `llm-redteam-taxonomy.md` |
| Luật review theo ngôn ngữ hoặc loại file | `review-rules/` (`default.md` nếu không có file khớp) |

## Tham chiếu

| Khi nào | Đọc |
|---|---|
| Thuật ngữ của khung (task, card, vai trò...) | `glossary.md` |
| Dùng `scripts/verify.py` và `proof-check.py` | `verification-cli-runbook.md` |
| Kỹ năng đã duyệt, vai trò nào dùng | `skills.md` |
| Bài nghiên cứu nền (Graphify, Lauren Tan, Harness²: tự cải tiến harness) | `research/` |

## Khi hai nguồn mâu thuẫn

Áp dụng `agents/protocols/source-precedence.md`. Vì các file từ gdt bổ sung cho protocol chứ không thay thế, nếu một file ở đây trái `protocols/` thì theo protocol.

## Đã đối chiếu và không đưa vào

Khung đã có nội dung tương đương, nên không chép từ gdt-workspace (bản gốc vẫn ở `.ai-rules/` của gdt):

| Chủ đề | Khung đã có |
|---|---|
| Git, nhánh, commit, MR | `protocols/git-rules.md` |
| Kiểm thử, happy path, ISTQB | `protocols/test-cases.md`, `roles/qa.md` |
| Phản biện đề bài, 3 phương án | `protocols/challenger.md` |
| Quy trình, cổng, chia task | `protocols/task-loop.md`, `protocols/full-workflow.md`, `AGENTS.md` mục 2 và 16 |
| Quy ước code Java | `stacks/java.md` |

Cũng không đưa vì riêng công cụ hoặc dự án của gdt: quy trình TestLink/Mantis, mẫu Excel Copilot, hướng dẫn lệnh draw.io (chạy bằng script ở gốc workspace gdt), domain accounting/J&T, quy định gọi giữa service, SRS và bug của từng chức năng. Chưa xét: `doc/quy-trinh/` (149 file), công cụ vẽ sơ đồ trong `scripts/` ở gốc gdt.