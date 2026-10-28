# Giao thức khởi tạo và tiếp nhận dự án (Project Onboarding Protocol)

Giao thức này hướng dẫn cách AI (`lead`, `analyst`, `ba`) tiếp nhận và cấu hình dự án mới khi mang `agent-base` sang một codebase khác.

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

4. **Lập bản đồ mã nguồn** (`analyst`, skill `codebase-map`):
   - Dựng `docs/CODEMAP.md` (bảng thư mục gốc, ranh giới module, luồng chính, nơi đặt thứ gì). Chỉ ghi điều đã liệt kê hoặc đọc thật, chỗ chưa kiểm ghi `(chưa kiểm)`. `architect` duyệt phần ranh giới.
   - (Tùy chọn, do người dùng quyết) Với codebase lớn, người dùng có thể tự cài Graphify và build `--code-only`; agent chỉ đọc kết quả theo skill. Agent không cài, không đặt hook.

5. **Báo cáo cho người dùng**:
   - Trình bày tóm tắt: Ngôn ngữ, Framework, CSDL phát hiện được, lệnh test được thiết lập, và đường dẫn `docs/CODEMAP.md`.
   - Hỏi người dùng xem có cần bổ sung ràng buộc kỹ thuật hay domain đặc thù nào vào `PROJECT.md` không.

---

## Kịch bản 2: Dự án mới toanh từ đầu (Greenfield Project)

Áp dụng khi: Người dùng chưa có code và mô tả ý tưởng/yêu cầu qua cửa sổ chat.

### Quy trình thực hiện:

1. **Thu thập và bóc tách yêu cầu (Vai `BA`)**:
   - Đọc kỹ mô tả ý tưởng của người dùng.
   - Nếu còn thiếu thông tin sống còn (công nghệ mong muốn, cơ sở dữ liệu, quy mô), đặt tối đa 2–3 câu hỏi trọng tâm.
   - Bóc tách yêu cầu thành danh sách `R-001`, `R-002`... lưu vào `docs/requirements/requirements.md` theo mẫu `agents/protocols/intake.md`.

2. **Thiết lập cấu hình (Vai `Lead`)**:
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

## Kịch bản 3: Dự án có sẵn tài liệu bàn giao, agent-base không lên git

Áp dụng khi: dự án đã có bộ tài liệu yêu cầu (vd thư mục `doc/` có mã yêu cầu, kế hoạch, tiêu chí nghiệm thu) và người dùng **không muốn đưa agent-base vào git** của dự án.

### Người dùng làm (AI không chạy được các lệnh git này)

Cách nhanh: `git init -b main` ở dự án, rồi từ thư mục agent-base chạy `python scripts/bootstrap-project.py --target <dự án> --mode hidden` (làm thay bước 1 và 3 dưới đây). Làm tay:

1. Copy phần khung (danh sách chính thức: `agents/manifest.txt`) vào gốc dự án: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `CODEX.md`, `PROJECT.md`, `agents/`, `scripts/`, `agent_core/`, `examples/`, `tools/viewer/`, `.agents/`, `.claude/`, `.githooks/`, `.kilo/agents/`. **Không** copy `.git`, `.kilo/worktrees/`, `.kilo/agent-manager.json`, và các file trùng tên với file thật của dự án (`README.md`, `.gitignore`, `.gitattributes`, `.env.example`, `tests/`, `infra/`, `.github/`). Tạo `tasks/` và `docs/` trống từ mẫu.
2. `git init -b main` **trước khi mở Kilo**. Thư mục chưa có git thì Kilo không nạp vai trong `.kilo/agents/`.
3. Giấu agent-base khỏi git bằng `.git/info/exclude` (chỉ nằm trên máy, không commit như `.gitignore`):
   ```
   .agents/
   .claude/
   .githooks/
   .github/
   .kilo/
   agents/
   agent_core/
   examples/
   scripts/
   tasks/
   docs/
   AGENTS.md
   CLAUDE.md
   CODEX.md
   GEMINI.md
   PROJECT.md
   ```
   Kiểm tra: `git status` chỉ còn file thật của dự án.
4. Chạy `python scripts/sync-adapters.py`, mở **đúng thư mục chứa `.kilo/`** làm workspace, chạy **Developer: Reload Window**.

### Lead / Architect làm

5. Điền `PROJECT.md` từ tài liệu bàn giao: bảng file tài liệu và khi nào đọc, **đúng tiền tố mã yêu cầu** của tài liệu (không đổi sang `R-xxx`), thứ tự ưu tiên khi nguồn mâu thuẫn, nguyên tắc bất biến, ngoài phạm vi, yêu cầu bảo mật dữ liệu, cấm sửa thư mục tài liệu bàn giao.
6. Thay bảng `tasks/EPICS.md` bằng epic thật của dự án và trình người dùng duyệt.

### Hệ quả cần nhớ

- Không dùng worktree (`scripts/new-worktree.*`, nút "New Worktree" của Kilo): worktree mới không có các file đã giấu, agent chạy trong đó không có quy tắc. Chạy mọi phiên ở chế độ **Local**, một Dev tại một thời điểm.
- `tasks/` và `docs/` không có trên git: sao lưu định kỳ ra ngoài.
- `agents/models.txt`: id model phải có tiền tố **tên provider trong cấu hình Kilo** (`~/.config/kilo/kilo.jsonc`), ví dụ `9router/ag/gemini-3.8-flash-medium`. Model chọn ở khung chat thắng model ghim; model ghim chỉ dùng khi Lead gọi agent con.

---

## Tiêu chí hoàn thành (DoD) của bước Onboarding

- [ ] `PROJECT.md` không còn chữ `(điền)` nào ở các mục bắt buộc.
- [ ] Đã chọn đúng file stack trong `agents/stacks/`.
- [ ] Chạy `powershell -File scripts/sync-adapters.ps1 -Check` trả về PASS (0 lỗi lệch).
- [ ] Người dùng đã xác nhận thông tin nhận diện là chính xác.
