# Năm Gói Tri Thức Bó Theo Loại Việc (Task Archetype Bundles)

> **Loại: tham khảo.** Tổng hợp đóng gói các quy chuẩn và kỹ năng theo 5 loại tác vụ điển hình để tra cứu nhanh, không phải nguồn luật. Khi khác `AGENTS.md`, vai trò hoặc `agents/protocols/` thì theo các nơi đó.

Quy định và tiêu chuẩn trong hệ thống rất nhiều (148+ nodes tri thức, 40+ protocols và skills). Để Agent và lập trình viên không phải tìm kiếm thủ công từng file, toàn bộ quy chuẩn thực tế được đóng gói thành **5 Gói Phản Ứng Nhanh (Task Archetypes)**. 

Khi nhận task thuộc loại nào, Agent tra cứu trực tiếp mã gói tương ứng qua lệnh:
`python3 scripts/knowledge.py query -q "archetype-<loại>" --budget 1200`

---

## 1. Gói Sửa Lỗi & Tái Hiện Bug (`archetype-bug`)

Áp dụng cho mọi task sửa lỗi (Bug fix, Hotfix, Defect từ Mantis hoặc người dùng báo).

- **Tri thức & Tiêu chuẩn Bắt buộc**:
  1. `agents/protocols/bug-repro.md`: Quy trình 4 bước tái hiện lỗi trên code hiện tại trước khi sửa. Tuyệt đối không đoán mò.
  2. `.agents/skills/systematic-debugging/SKILL.md`: Quy trình 4 pha gỡ lỗi gốc rễ (Isolate $\rightarrow$ Reproduce $\rightarrow$ Fix $\rightarrow$ Verify).
  3. `doc/delivery/defects/mantis/`: File CSV danh sách lỗi gốc để đối chiếu mã Mantis.
  4. `agents/protocols/test-cases.md`: Viết TestLink XML (Keyword = Mã Mantis) bao phủ kịch bản lỗi và được duyệt trước khi code.
- **Khóa phạm vi (Scope Gating)**:
  - `scope_edit`: Chỉ sửa đúng file chứa nguyên nhân gốc rễ và file test tương ứng.
  - `scope_deny`: Cấm sửa file kiến trúc, cấm đổi API signature chung.
- **Bằng chứng nghiệm thu**:
  - Chạy test trước khi sửa: Test FAIL (đỏ) đúng lý do.
  - Chạy test sau khi sửa: Test PASS (xanh) 100%, không gây hồi quy.
- **Hộp thư bàn giao**:
  - Ghi báo cáo vào: `doc/notes/inbox/<Task>/<Task>.<Subtask>-dev.md`.

---

## 2. Gói Cơ Sở Dữ Liệu & Migration (`archetype-database`)

Áp dụng khi thêm bảng, sửa cột, tạo index, tối ưu truy vấn hoặc can thiệp Liquibase/Flyway/PostgreSQL.

- **Tri thức & Tiêu chuẩn Bắt buộc**:
  1. `agents/protocols/risk-gate.md`: Lập phiếu rủi ro nếu có thao tác thay đổi dữ liệu lớn hoặc có nguy cơ mất mát.
  2. `.agents/skills/jpa-patterns/SKILL.md`: Chuẩn JPA/Hibernate, chống N+1 query, bắt buộc dùng `JOIN FETCH` hoặc `@EntityGraph`.
  3. `.agents/skills/postgres-patterns/SKILL.md`: Chuẩn đặt index, Composite Index, Partial Index, tránh Full Table Scan.
  4. `agents/knowledge/ky-thuat/chuan-sql-va-loi.md`: Quy chuẩn Liquibase (`author: ducnvh`, không sửa changeset cũ, luôn kèm rollback).
- **Khóa phạm vi (Scope Gating)**:
  - `scope_edit`: Chỉ file migration mới (`db/changelog/...`), Entity Java và Repository tương ứng.
  - `scope_deny`: Cấm sửa các changeset Liquibase cũ đã chạy trên production.
- **Bằng chứng nghiệm thu**:
  - Chạy `./mvnw compile test` hoặc migration test pass.
  - Lệnh `EXPLAIN ANALYZE` chứng minh câu truy vấn sử dụng Index, không quét tuần tự (Seq Scan).
- **Hộp thư bàn giao**:
  - Ghi báo cáo vào: `doc/notes/inbox/<Task>/<Task>.<Subtask>-dba.md`.

---

## 3. Gói Xây Dựng & Tối Ưu API (`archetype-api`)

Áp dụng khi thêm mới Endpoint REST, Controller, Service hoặc tích hợp giữa các Service.

- **Tri thức & Tiêu chuẩn Bắt buộc**:
  1. `.agents/skills/api-design/SKILL.md`: Chuẩn RESTful API (danh từ số nhiều, HTTP Status Codes 200/201/400/404/500, phân trang cursor/page).
  2. `.agents/skills/springboot-patterns/SKILL.md`: Kiến trúc phân tầng Controller $\rightarrow$ Service $\rightarrow$ Repository, DTO validation (`@Valid`).
  3. `agents/protocols/goi-giua-service.md`: Gọi qua Eureka Discovery Server hoặc API Gateway, không hardcode IP/Port.
  4. `agents/protocols/atomic-changes.md`: Đảm bảo API idempotent, xử lý ngoại lệ qua `@RestControllerAdvice`.
- **Khóa phạm vi (Scope Gating)**:
  - `scope_edit`: Controller, Service, DTO, Repository của service được chỉ định.
  - `scope_deny`: Cấm sửa file cấu hình Gateway chung khi chưa có phê duyệt.
- **Bằng chứng nghiệm thu**:
  - MockMvc Unit Tests & Integration Tests pass 100%.
  - Postman / cURL mẫu kèm response JSON chuẩn.
- **Hộp thư bàn giao**:
  - Ghi báo cáo vào: `doc/notes/inbox/<Task>/<Task>.<Subtask>-dev.md`.

---

## 4. Gói Đặc Tả SRS & Thiết Kế Kỹ Thuật (`archetype-srs`)

Áp dụng khi phân tích bài toán mới, viết hồ sơ đặc tả SRS_FDD, vẽ sơ đồ và chuẩn bị Gate 2.

- **Tri thức & Tiêu chuẩn Bắt buộc**:
  1. `agents/protocols/srs-workflow.md`: Quy trình đóng gói bộ hồ sơ Use Case trong `doc/features/<UC-tên>/`.
  2. `agents/knowledge/srs/srs-fdd-writing-standard.md`: Văn phong tài liệu đặc tả, bóc tách R-xxx và BR-xxx.
  3. `agents/knowledge/srs/chuan-ve-so-do.md`: Quy chuẩn vẽ sơ đồ (activity theo làn lớp, nhiều điểm bắt đầu và kết thúc, đen trắng, mỗi UC một `.drawio` bốn tab, 100% dữ liệu thật, xuất ảnh PNG nhúng Markdown; chi tiết `agents/knowledge/diagrams/quy-trinh-ve-so-do-bang-json.md`).
  4. `doc/governance/standards/cau-truc-chuan-srs-fdd-excel.md`: Mẫu file Excel 14 sheets Copilot.
- **Sản phẩm đầu ra bắt buộc**:
  - Bộ 3 file Markdown trong `doc/features/<UC>/` + File Excel 14 sheets + Sơ đồ `.drawio` + Ảnh `.png` + TestLink XML.
  - Biên bản thẩm định Swarm Gate 2 Review được ký duyệt.
- **Hộp thư bàn giao**:
  - Ghi báo cáo vào: `doc/notes/inbox/<Task>/<Task>-ban-giao-srs.md`.

---

## 5. Gói Điều Phối & Ủy Thác Subagent (`archetype-delegation`)

Áp dụng cho vai trò Lead khi bóc tách task, giao việc cho Dev/QA và thu gọn ngữ cảnh.

- **Tri thức & Tiêu chuẩn Bắt buộc**:
  1. `agents/protocols/context-budget.md`: Ba trần ngân sách token (Lead $\le$ 50k, Subagent $\le$ 30k, JIT Knowledge $\le$ 1.200).
  2. `agents/protocols/delegation-prompt.md`: Khuôn mẫu prompt ủy thác 8 thành phần, khóa kênh báo cáo.
  3. `agents/protocols/handoff-note.md`: Kiến trúc lưu trữ 4 tầng, lưu theo thư mục `inbox/<Task>/`.
  4. `scripts/notes-index.py`: Tra cứu và lọc báo cáo tự động bằng lệnh CLI `--task <Task>`.
- **Hành động cốt lõi**:
  - Bẻ task thành các subtasks hạt mịn (2–5 phút/phiên).
  - Không cho phép Subagent xả log thô ra chat chính (Zero-Chat Bleeding).
  - Flush trạng thái ra `BOARD.md` và kích hoạt `/compact` khi context $\ge 75\%$.
