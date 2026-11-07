# Sổ tay dự án (PROJECT-NOTES)

Bộ nhớ chung của dự án cho mọi agent. **Đọc file này (và `docs/notes/inbox/`) trước khi bắt đầu việc.**

- Chỉ **Tech Writer** sửa file này, bằng cách gộp các ghi chú từ `docs/notes/inbox/` sau mỗi lần merge (xem `agents/protocols/handoff-note.md`).
- Mỗi mục có ID (N-001, N-002...), ngày, nguồn (T-xxx và agent), và **phạm vi ảnh hưởng** (file hoặc module).
- Mục hết đúng thì gạch bỏ và ghi lý do, đừng xóa im lặng.

## Trạng thái hiện tại

(một đoạn ngắn: dự án đang ở đâu, task nào đang chạy, điều gì đang chặn. Cập nhật sau mỗi merge)

## Lưu ý và bẫy đã gặp

| ID | Ngày | Nguồn | Phạm vi | Lưu ý |
|---|---|---|---|---|
| N-032 | 2026-11-07 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-033 | 2026-11-07 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-034 | 2026-11-07 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-035 | 2026-11-07 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-036 | 2026-11-07 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-037 | 2026-11-07 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-038 | 2026-11-07 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-039 | 2026-11-07 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-040 | 2026-11-07 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-015 | 2026-11-07 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy vội vàng code khi chưa vẽ sơ đồ: Tuyệt đối cấm nhảy vào viết code khi chưa hoàn thiện sơ đồ luồng Sequence Diagram phân làn Swimlane và hồ sơ đặc tả Spec-First. |
| N-016 | 2026-11-07 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy học vẹt code cũ: Khi tối ưu tính năng lọc, cấm bê nguyên logic cũ vào Use Case mới mà bắt buộc tự phản biện chuyển sang Generic Specification cho ws-library. |
| N-017 | 2026-11-07 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy hardcoded đường dẫn máy cá nhân: Không bao giờ gắn cứng /Users/... vào code hay script; bắt buộc dùng Smart Worktree Discovery và biến môi trường. |
| N-018 | 2026-11-07 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy tốn tài nguyên do Cronjob Polling: Thay vì polling quét liên tục làm nghẽn DB, bắt buộc dùng Async Event-Driven Worker kích hoạt theo sự kiện. |
| N-019 | 2026-11-07 | `HARVEST-ALL-CHATS` | Toàn cục | Bẫy khen sơ đồ mà không xem ảnh: Sơ đồ vẽ xong bắt buộc xuất ảnh PNG và xem lại trực quan bằng mắt, cấm nói "đẹp" mà chưa kiểm tra. |
| N-020 | 2026-11-07 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về luồng xuất đơn J&T: Không cần trạng thái trung gian chờ thừa thãi; bấm đẩy đơn là kết nối API J&T lấy Waybill và cập nhật ngay. |
| N-021 | 2026-11-07 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về ẩn/hiện cột kế toán: Cho phép lưu cấu hình hiển thị cột theo từng vai trò người dùng trong hệ thống kế toán nội bộ. |
| N-022 | 2026-11-07 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về chuyển giao môi trường: Luôn chạy scripts/doctor.py kiểm tra cổng và Git identity trước khi chạy dự án trên máy mới. |
| N-023 | 2026-11-07 | `HARVEST-ALL-CHATS` | Toàn cục | [Bài học] Bài học về bóc tách tri thức từ chat: Thường xuyên chạy harvest-chat để thu hoạch các bài học người dùng chỉ đạo trên cả Claude Code và Antigravity. |
| N-009 | 2026-11-05 | `LEARN` | Toàn cục | Xử lý đồng bộ ngay trong Webhook controller làm cạn connection pool; không so sánh timestamp eventTime dẫn đến event cũ đè event mới; không cấu hình Manual ACK làm mất đơn khi worker chết giữa chừng. |
| N-010 | 2026-11-05 | `LEARN` | Toàn cục | [Bài học] Mô hình tích hợp đối tác qua Webhook + RabbitMQ + Worker (ShopSyncConsumer): Fast-Path Direct Update qua Pessimistic Lock, Slow-Path Refetch API, Self-Healing Token Refresh (401), Overlap Window 15 phút chống rớt đơn và Dead-Letter Queue (DLQ). |
| N-012 | 2026-11-06 | `LEARN` | Toàn cục | Dùng fixed worker gây cạn DB pool; không tách luồng backfill làm nghẽn real-time; gom đa sàn vào 1 bảng làm phình schema; không mã hóa token at-rest. |
| N-013 | 2026-11-06 | `LEARN` | Toàn cục | [Bài học] Tổng hợp 10 kỹ thuật tinh hoa từ tiktok_shoppe_jt: (1) Worker Auto-Scaler dựa trên HikariCP; (2) Deadlock Watchdog daemon; (3) Phân loại lỗi và Self-healing; (4) Tách luồng Backfill khỏi Real-time; (5) Dynamic OAuth Credential Resolver; (6) Cổng vận đơn J&T/Pancake; (7) Physical Table + Logical View; (8) Mã hóa AES DB at-rest; (9) RabbitMQ Priority & Deduplication; (10) Fuzzy Header Excel Mapping. |
| N-003 | 2026-10-28 | `KNOWLEDGE-DIAGRAMS-EPIC` | Toàn cục | Bẫy tọa độ 2D của LLM: Tuyệt đối không để AI tính toán tọa độ x, y, width, height để sinh XML Draw.io thô vì tỷ lệ lệch dây nối và đè chữ lên tới 85%. Bắt buộc dùng Auto-Layout (CSV Import, D2, Mermaid, Diagrams Python). |
| N-004 | 2026-10-28 | `KNOWLEDGE-DIAGRAMS-EPIC` | Toàn cục | Tránh ô nhiễm bộ khung: Không commit dữ liệu runtime của dự án ngoài (inbox notes, task board, proposals) lên repo framework agent-base; bắt buộc duy trì vành đai cách ly trong .gitignore. |

## Quyết định quan trọng

(tóm tắt một dòng kèm liên kết tới ADR trong `docs/adr/`)

| ID | Ngày | Quyết định | ADR |
|---|---|---|---|
| N-041 | 2026-11-07 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-042 | 2026-11-07 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-043 | 2026-11-07 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-044 | 2026-11-07 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-024 | 2026-11-07 | Quyết định áp dụng tư duy Generic-First: Mọi logic lọc và tìm kiếm dùng chung toàn hệ thống phải đưa vào ws-library với kiểu Generic <T>. | Theo `HARVEST-ALL-CHATS` |
| N-025 | 2026-11-07 | Quyết định quy trình 3 phương án đối trọng: Mỗi lần đề xuất giải pháp bắt buộc phải có 3 phương án (A: bám code cũ, B: over-engineering, C: tối ưu đúng trọng tâm) và 1 khuyến nghị dứt khoát. | Theo `HARVEST-ALL-CHATS` |
| N-026 | 2026-11-07 | Quyết định đối soát vận đơn J&T Express: Đẩy đơn trực tiếp nhận mã Waybill và đối soát cước tự động với sàn TikTok Shop & Shopee. | Theo `HARVEST-ALL-CHATS` |
| N-027 | 2026-11-07 | Quyết định chuẩn hóa đa nền tảng: Bác sĩ chẩn đoán scripts/doctor.py Mục 7 tự động phát hiện OS, Git identity, thư mục worktree và xung đột cổng. | Theo `HARVEST-ALL-CHATS` |
| N-011 | 2026-11-05 | Áp dụng Sync-then-Serve: Webhook xác thực HMAC đẩy queue trả 200 OK ngay; Worker prefetch=1 manual ACK; findForUpdate chống race condition; Overlap 15 phút cronjob quét bù. | Theo `LEARN` |
| N-014 | 2026-11-06 | Áp dụng trọn bộ 10 patterns trong docs/architecture/10-CHUYEN-DE-KIEN-TRUC-CHUYEN-SAU.md làm blueprint cho các dự án kết nối bên thứ 3. | Theo `LEARN` |
| N-005 | 2026-10-28 | Quyết định chuẩn hóa sơ đồ kiến trúc Draw.io thông qua định dạng CSV Auto-Layout (Header # style, # connect, # layout: auto) và Python diagrams thay vì viết XML mxGraphModel trực tiếp. | Theo `KNOWLEDGE-DIAGRAMS-EPIC` |
| N-006 | 2026-10-28 | Quyết định phân tách tri thức: Giữ nguyên doc/ và .ai-rules/ ở gốc workspace làm la bàn chung; agent-base chỉ sao phần dùng chung được (quy trình, chuẩn, mẫu) vào agents/knowledge và agents/templates, dữ liệu dự án ở lại bên ngoài. | Theo `KNOWLEDGE-DIAGRAMS-EPIC` |

## Quy ước phát hiện thêm

- **[N-045 - 2026-11-07]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-046 - 2026-11-07]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-047 - 2026-11-07]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-048 - 2026-11-07]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

- **[N-028 - 2026-11-07]** (`HARVEST-ALL-CHATS`): Quy ước kiểm tra sơ đồ bằng mắt: Mọi sơ đồ Draw.io vẽ ra bắt buộc xuất ảnh PNG và xem lại trực quan trước khi kết luận đạt yêu cầu.
- **[N-029 - 2026-11-07]** (`HARVEST-ALL-CHATS`): Quy ước giải trình Git Diff: Khi cập nhật AGENTS.md, giải thích rõ ràng cho người dùng nguồn gốc ~2.000 dòng diff do cơ chế nhân bản sang 25+ adapters.
- **[N-030 - 2026-11-07]** (`HARVEST-ALL-CHATS`): Quy ước Zero-Chat Bleeding: Cấm xả log kiểm thử dài vào khung chat, luôn ghi chi tiết ra file note và chỉ báo tóm tắt 3 dòng.
- **[N-031 - 2026-11-07]** (`HARVEST-ALL-CHATS`): Quy ước quản lý Git Worktrees tập trung: 100% Worktrees tạo tại thư mục tập trung ngoài workspace và cập nhật sổ bộ qua worktree-manager.py.

- **[N-007 - 2026-10-28]** (`KNOWLEDGE-DIAGRAMS-EPIC`): Khi người dùng cần sơ đồ kiến trúc có thể chỉnh sửa tay trên Draw.io, Agent ưu tiên xuất khối mã CSV kèm hướng dẫn 4 bước Insert CSV vào diagrams.net.
- **[N-008 - 2026-10-28]** (`KNOWLEDGE-DIAGRAMS-EPIC`): Mọi node tri thức mới sinh ra từ chu trình phản tư luôn mang trạng thái state: draft và phải qua 11 Validators CMMI L3 trước khi con người nghiệm thu.

(điều chưa có trong `agents/stacks/` hay `PROJECT.md`. Khi đã ổn định thì đề xuất đưa vào các file đó và ghi ở đây là đã chuyển)

## Việc dở dang và nợ kỹ thuật

| ID | Ngày | Nguồn | Mô tả | Ưu tiên |
|---|---|---|---|---|

## Giả định chưa kiểm chứng

| ID | Ngày | Nguồn | Giả định | Cách kiểm chứng |
|---|---|---|---|---|

## Câu hỏi còn mở cho người dùng

| ID | Ngày | Câu hỏi | Trạng thái |
|---|---|---|---|
