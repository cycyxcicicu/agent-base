# Chi Tiết Gói Tri Thức Bó Theo Loại Việc (Phần 2: Gói 3 - 4)

> **Loại: tham khảo.**
> Nguồn: tách từ task-archetypes.md mục Gói 3 - 4.

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
