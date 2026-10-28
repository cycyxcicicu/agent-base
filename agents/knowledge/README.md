# Chỉ mục tri thức dùng chung

Agent không đọc cả thư mục này. Tra bảng, mở đúng file khớp việc đang làm (tối đa vài file), hoặc dùng lệnh trích xuất tự động:
`python scripts/knowledge.py context --root . --manifest agents/knowledge/knowledge-manifest.json --role <vai>`

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
| Mẫu để viết (đặc tả, thiết kế kỹ thuật, Excel SRS_FDD, test report, TestLink) | thư mục `agents/templates/`, xem `agents/templates/README.md` |

## Chuyên đề kỹ thuật và an ninh

| Khi nào | Đọc |
|---|---|
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
