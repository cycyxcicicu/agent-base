# Giao thức khởi tạo và tiếp nhận dự án (Project Onboarding Protocol)

Giao thức này hướng dẫn cách AI (`orchestrator`, `analyst`, `ba`) tiếp nhận và cấu hình dự án mới khi mang `agent-base` sang một codebase khác.

---

## Kịch bản 1: Dự án đã có sẵn code (Brownfield Project)

Áp dụng khi: Người dùng đưa `agent-base` vào một repository đã có code hoặc yêu cầu *"Quét và nhận diện dự án này"*.

### Quy trình thực hiện:

1. **Quét nhận diện tự động**:
   - Chạy lệnh:
     ```powershell
     powershell -File scripts/detect-project.ps1 -FillProjectMd
     ```
   - Script sẽ tự động phát hiện ngôn ngữ (Java, Node.js, Python, .NET, Go), cơ sở dữ liệu (PostgreSQL, MySQL...), message broker (RabbitMQ, Redis) và cập nhật `PROJECT.md`.

2. **Xác minh lại thông tin**:
   - Mở [PROJECT.md](file:///d:/OneDrive%20-%20concutobu/tiktok/fteck/agent-base/PROJECT.md) vừa sinh và đối chiếu:
     - Stack đã đúng file trong `agents/stacks/` chưa (ví dụ: `agents/stacks/java.md`).
     - Lệnh test (`testCmd`) và lệnh chạy (`runCmd`) có chính xác với cấu hình repo không.
   - Thử chạy lệnh test ở chế độ chỉ đọc (hoặc nhờ `runner`) để đảm bảo môi trường máy chạy được.

3. **Dọn dẹp và đồng bộ**:
   - (Tùy chọn) Xóa các file stack không dùng trong `agents/stacks/`, chỉ giữ lại stack của dự án và `_template.md`.
   - Chạy đồng bộ adapter:
     ```powershell
     powershell -File scripts/sync-adapters.ps1
     ```

4. **Báo cáo cho người dùng**:
   - Trình bày tóm tắt: Ngôn ngữ, Framework, CSDL phát hiện được, lệnh test được thiết lập.
   - Hỏi người dùng xem có cần bổ sung ràng buộc kỹ thuật hay domain đặc thù nào vào `PROJECT.md` không.

---

## Kịch bản 2: Dự án mới toanh từ đầu (Greenfield Project)

Áp dụng khi: Người dùng chưa có code và mô tả ý tưởng/yêu cầu qua cửa sổ chat.

### Quy trình thực hiện:

1. **Thu thập và bóc tách yêu cầu (Vai `BA`)**:
   - Đọc kỹ mô tả ý tưởng của người dùng.
   - Nếu còn thiếu thông tin sống còn (công nghệ mong muốn, cơ sở dữ liệu, quy mô), đặt tối đa 2–3 câu hỏi trọng tâm.
   - Bóc tách yêu cầu thành danh sách `R-001`, `R-002`... lưu vào `docs/requirements/requirements.md` theo mẫu `agents/protocols/intake.md`.

2. **Thiết lập cấu hình (Vai `Orchestrator`)**:
   - Điền [PROJECT.md](file:///d:/OneDrive%20-%20concutobu/tiktok/fteck/agent-base/PROJECT.md):
     - Tên dự án, mục tiêu một câu.
     - Chọn stack phù hợp (`java.md`, `node.md`, `python.md`...).
     - Điền các lệnh build, run, test tiêu chuẩn của stack đó.
     - Điền thuật ngữ và domain vào mục Domain.

3. **Chuẩn bị hạ tầng & Khung mã nguồn (Vai `Architect` & `DevOps`)**:
   - Nếu dự án backend cần CSDL hoặc Message Broker, chuẩn bị file `infra/docker-compose.dev.yml` (bật/tắt Postgres, Redis, RabbitMQ tương ứng).
   - Tạo khung thư mục cơ sở (`src/`, `tests/`).
   - Chạy:
     ```powershell
     powershell -File scripts/sync-adapters.ps1
     ```

4. **Trình bày và chờ duyệt**:
   - Trình bày danh sách `R-xxx`, kiến trúc đề xuất và kế hoạch task đầu tiên cho người dùng duyệt trước khi tạo task card.

---

## Tiêu chí hoàn thành (DoD) của bước Onboarding

- [ ] `PROJECT.md` không còn chữ `(điền)` nào ở các mục bắt buộc.
- [ ] Đã chọn đúng file stack trong `agents/stacks/`.
- [ ] Chạy `powershell -File scripts/sync-adapters.ps1 -Check` trả về PASS (0 lỗi lệch).
- [ ] Người dùng đã xác nhận thông tin nhận diện là chính xác.
