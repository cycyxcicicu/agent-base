# Chi Tiết Gói Tri Thức Bó Theo Loại Việc (Phần 1: Gói 1 - 2)

> **Loại: tham khảo.**
> Nguồn: tách từ task-archetypes.md mục Gói 1 - 2.

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
