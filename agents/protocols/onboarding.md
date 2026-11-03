# Giao thức khởi tạo và tiếp nhận dự án (Project Onboarding Protocol)

Giao thức này hướng dẫn cách AI (`lead`, `analyst`, `ba`, `architect`) tiếp nhận, đặt vấn đề và cấu hình dự án mới khi mang `agent-base` sang một codebase khác.

---

## 0. Triết lý Nhập cuộc: Đặt Vấn Đề Trực Diện & Thiết Lập Bộ Nhớ Tri Thức Sống

Khi bước chân vào một dự án mới, **Agent tuyệt đối không được im lặng cắm đầu làm hoặc hỏi những câu vụn vặt**. Agent phải đóng vai trò là một kỹ sư trưởng/chuyên gia tư vấn: **Chủ động đặt vấn đề với người dùng ngay từ đầu** và **thiết lập ngay bộ khung lưu trữ tri thức** để khi dự án mở rộng, toàn bộ bài học và quy ước tự động được lưu vết.

### A. 4 Trụ Cột Đặt Vấn Đề với Người Dùng (Proactive Problem Framing)
Trước khi viết dòng code hay tài liệu đầu tiên, Agent bắt buộc phải phỏng vấn/làm rõ với người dùng 4 trụ cột cốt lõi:
1. **Bài toán gốc & Mục tiêu tối thượng (Core Problem Statement):**
   - Dự án này sinh ra để giải quyết nỗi đau lớn nhất nào của người dùng/doanh nghiệp?
   - Thước đo thành công của sản phẩm (North Star Metric / DoD) là gì?
2. **Cắt tỉa phạm vi quyết liệt (Ruthless Scope-Cut / In-scope vs Out-of-scope):**
   - Phiên bản tối thiểu (MVP) bắt buộc phải có những tính năng gì?
   - Cái gì dứt khoát **KHÔNG LÀM (Out-of-scope)** trong giai đoạn đầu để tránh phình to hệ thống?
3. **Hiện trạng kỹ thuật & Bãi mìn tiềm ẩn (Technical Baseline & Gotchas):**
   - Codebase hiện tại chỗ nào đang là "bãi mìn" (dễ vỡ, thiếu test, có nguy cơ khóa DB, nợ kỹ thuật nghiêm trọng)?
   - Có quy ước cứng nào của công ty bắt buộc phải tuân theo không (author Liquibase, branch flow, linter)?
4. **Ràng buộc đối tác & Rủi ro phụ thuộc (External Dependencies & Credentials):**
   - Dự án phụ thuộc vào API bên thứ 3 nào (J&T, Pancake, Cổng thanh toán, AI API)?
   - Đã có tài khoản Sandbox/Môi trường thử nghiệm chưa? Dữ liệu bảo mật (PII, blacklist, token) lưu trữ ở đâu?

> **Quy tắc đưa lựa chọn (The 3-Option Rule):** Khi phát hiện điểm mơ hồ, mâu thuẫn hoặc quyết định kiến trúc quan trọng, Agent không hỏi chung chung mà phải xuất trình **Ma trận 3 Phương án** (Lean MVP vs Cân bằng vs Toàn diện) kèm 1 khuyến nghị dứt khoát, lý do kỹ thuật và cách khắc phục rủi ro (theo `agents/protocols/challenger.md`).

---

### B. Thiết Lập Bộ Khung Lưu Trữ Tri Thức Sống (4-Tier Memory Skeleton)
Ngay trong bước Onboarding, Agent phải đảm bảo khung thư mục sau đã được khởi tạo để mọi Agent sau này tự động ghi nhận khi mở rộng dự án:

1. **`PROJECT.md` (Chứng minh thư dự án):** Tên dự án, stack công nghệ, lệnh build/test/run duy nhất, phạm vi In-scope / Out-of-scope, quy tắc bất biến.
2. **`docs/CODEMAP.md` (Bản đồ mã nguồn sống):** Cấu trúc thư mục, trách nhiệm từng package, luồng request mẫu. Khi thêm package/controller mới, Agent tự cập nhật file này.
3. **`docs/notes/inbox/` (Hộp thư bàn giao Task):** Nơi mỗi Agent ghi lại bẫy kỹ thuật (gotchas), cảnh báo khu vực dễ vỡ, việc dở dang dạng `<Task>-<slug>.md` sau mỗi phiên làm việc để không bao giờ bị xung đột Git.
4. **`docs/notes/PROJECT-NOTES.md` (Sổ tay tri thức tích lũy dài hạn):** Nơi Tech Writer định kỳ gộp các ghi chú từ `inbox/` vào làm "bộ nhớ vĩnh cửu" của dự án.
5. **`docs/architecture/adr/` (Sổ quyết định kiến trúc):** Nơi ghi nhận các quyết định kỹ thuật lớn (đổi thư viện, bỏ tích hợp ngoài, đổi cấu trúc bảng).
6. **`docs/requirements/glossary.md` (Từ điển thuật ngữ nghiệp vụ):** Định danh các khái niệm cốt lõi của domain để mọi người và AI dùng chung một ngôn ngữ.

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

5. **Báo cáo và Đặt vấn đề trực diện với người dùng (Kickoff Problem Framing)**:
   - Trình bày tóm tắt: Ngôn ngữ, Framework, CSDL phát hiện được, lệnh test được thiết lập, và đường dẫn `docs/CODEMAP.md`.
   - **Chủ động đặt vấn đề theo 4 trụ cột ở Mục 0.A**: Xác định bài toán cốt lõi, phạm vi MVP (In-scope vs Out-of-scope), các bãi mìn kỹ thuật/nợ kỹ thuật đang có trong codebase, và ràng buộc bên thứ 3.
   - Khởi tạo sẵn bộ khung lưu trữ tri thức 4 cấp (Mục 0.B) để mọi Agent sau này tự động ghi nhận bài học và bẫy kỹ thuật vào `docs/notes/inbox/`.

---

## Kịch bản 2: Dự án mới toanh từ đầu (Greenfield Project)

Áp dụng khi: Người dùng chưa có code và mô tả ý tưởng/yêu cầu qua cửa sổ chat.

### Quy trình thực hiện:

1. **Thu thập và Đặt vấn đề bóc tách yêu cầu (Vai `BA` & `Lead`)**:
   - Đọc kỹ mô tả ý tưởng của người dùng.
   - **Đặt vấn đề trực diện theo 4 trụ cột Mục 0.A**: Bóc tách bài toán gốc vs giải pháp đề xuất (XY Problem), xác định thước đo thành công, cắt tỉa phạm vi quyết liệt (Must-Have vs Nice-to-Have).
   - Nếu có nhiều hướng tiếp cận kiến trúc/công nghệ, xuất trình **Ma trận 3 Phương án** (Lean MVP vs Cân bằng vs Toàn diện) kèm 1 khuyến nghị dứt khoát theo `challenger.md`.
   - Bóc tách yêu cầu thành danh sách `R-001`, `R-002`... lưu vào `docs/requirements/requirements.md` theo mẫu `agents/protocols/intake.md`.

2. **Thiết lập cấu hình & Bộ khung lưu trữ tri thức (Vai `Lead`)**:
   - Điền [PROJECT.md](file:///d:/OneDrive%20-%20concutobu/tiktok/fteck/agent-base/PROJECT.md): Tên dự án, mục tiêu một câu, stack chuẩn, lệnh test/run, domain glossary.
   - Thiết lập bộ khung 4 cấp (Mục 0.B): `CODEMAP.md`, `docs/notes/inbox/`, `PROJECT-NOTES.md`, `docs/architecture/adr/`.

3. **Chuẩn bị hạ tầng & Khung mã nguồn (Vai `Architect` & `DevOps`)**:
   - Nếu dự án backend cần CSDL hoặc Message Broker, chuẩn bị file `infra/docker-compose.dev.yml` (bật/tắt Postgres, Redis, RabbitMQ tương ứng).
   - Tạo khung thư mục cơ sở (`src/`, `tests/`).
   - Chạy:
     ```powershell
     powershell -File scripts/sync-adapters.ps1
     ```

4. **Trình bày phương án và Chờ duyệt (File-based GATE)**:
   - Trình bày danh sách `R-xxx`, kiến trúc đề xuất và kế hoạch task đầu tiên cho người dùng duyệt trước khi tạo task card. Không bắt đầu code khi người dùng chưa chốt phạm vi.

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
- [ ] Đã chủ động đặt vấn đề với người dùng theo 4 trụ cột Mục 0.A (Bài toán gốc, Ranh giới Scope In/Out, Bãi mìn kỹ thuật, Rủi ro phụ thuộc ngoài).
- [ ] Đã thiết lập sẵn bộ khung lưu trữ tri thức sống 4 cấp (Mục 0.B): `PROJECT.md`, `docs/CODEMAP.md`, `docs/notes/inbox/`, `docs/notes/PROJECT-NOTES.md`, `docs/architecture/adr/`.
- [ ] Chạy `powershell -File scripts/sync-adapters.ps1 -Check` trả về PASS (0 lỗi lệch).
- [ ] Người dùng đã xác nhận thông tin nhận diện và chốt phạm vi MVP trước khi bắt đầu code.
