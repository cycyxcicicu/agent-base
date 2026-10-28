# Chỉ mục tri thức dùng chung

Agent không đọc cả thư mục này. Tra bảng, mở đúng file khớp việc đang làm (tối đa vài file).

## Từ dự án gdt-workspace (bổ sung phần khung còn thiếu)

Nguồn: dự án gdt-workspace, đã dùng thật. Còn nhắc Mantis, TestLink, thư mục `doc/` là quy ước của gdt; dự án khác thay bằng công cụ của mình.

| Khi nào | Đọc |
|---|---|
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
| Bài nghiên cứu nền (Graphify, Lauren Tan) | `research/` |

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
