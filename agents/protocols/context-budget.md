> Task: T-16 · Epic: E2 · Vai: architect

# Giao thức Quản trị Ngân sách Context và Điều phối Multi-Agent (Context Budget & Multi-Agent Isolation Protocol)

Giao thức này quy chuẩn hóa cơ chế quản lý cửa sổ ngữ cảnh (Context Window), cách ly phiên giữa **Lead (Orchestrator)** và **Subagents (Thực thi)**, và quy tắc duy trì trạng thái khi chạy các phiên dài hạn (Long-running sessions 4–6+ tiếng) mà không bị tràn bộ nhớ hoặc suy giảm nhận thức.

---

## 1. Nguyên tắc Ba Trần Ngân Sách (Three Token Budgets)

Để một hệ thống AI vận hành liên tục qua nhiều khâu mà không chạm trần 200k–500k tokens, mỗi chủ thể chỉ được tiêu thụ trong trần ngân sách được phân bổ:

| Chủ thể | Trần token hoạt động | Phạm vi nạp ngữ cảnh | Nguyên tắc kiểm soát |
|---|---|---|---|
| **Lead (Orchestrator)** | ≤ 50.000 tokens | `PROJECT.md`, `BOARD.md`, Task Cards mục tiêu, `INDEX.md`, tóm tắt 3 dòng từ Subagents | **Zero-Execution Leaks**: Cấm Lead đọc raw logs, test outputs hàng nghìn dòng, hoặc diff chi tiết. Lead chỉ nhìn thấy trạng thái và đồ thị nhiệm vụ (DAG). |
| **Subagent (Worker/Specialist)** | ≤ 30.000 tokens (cho 1 Subtask) | Task card con, `scope_edit`, 1-2 file liên quan trực tiếp, test suite tương ứng | **Fresh & Ephemeral**: Mỗi Subtask chạy trong một instance/context riêng biệt. Hoàn thành xong thì thoát và trả kết quả, không giữ phiên lâu. |
| **JIT Knowledge (Tra cứu)** | ≤ 1.200 tokens (mỗi truy vấn) | Kết quả từ `python scripts/knowledge.py query -q "<chủ đề>" --role <vai>` | **Just-In-Time Injection**: Cấm đọc toàn bộ tài liệu dự án vào ngữ cảnh; chỉ nạp đúng node tri thức cần thiết cho bước hiện tại. |

---

## 2. Nguyên tắc Cách ly Ngữ cảnh: Không Rò Rỉ Chat (Zero-Chat Bleeding Directive)

1. **Subagent không xả log thô vào chat của Lead**:
   - Khi chạy test hoặc kiểm tra mã nguồn sinh ra hàng trăm dòng log, Subagent BẮT BUỘC chuyển hướng (redirect) hoặc ghi toàn bộ dữ liệu thô vào file báo cáo chi tiết:
     `docs/notes/inbox/<Task>/<Task>.<Subtask>-<agent>.md` (Tầng 1 - Raw Execution Artifact).
2. **Kênh trao đổi cha - con chỉ nhận Micro-Summary 3 dòng**:
   - Tin nhắn hoàn thành của Subagent gửi về cho Lead (hoặc tool response) chỉ chứa tối đa 3-5 dòng theo mẫu:
     ```markdown
     - Hoàn thành: [Mã Subtask] - [Hành động cốt lõi đã làm]
     - Bằng chứng: [Lệnh test đã chạy] -> [Kết quả PASS/FAIL cụ thể, ví dụ: 46/46 OK]
     - Báo cáo chi tiết: `docs/notes/inbox/<Task>/<Task>.<Subtask>-<agent>.md`
     ```

---

## 3. Cơ chế Điểm Kiểm Soát Bền Vững (Stateful Checkpoints) cho Phiên 6 Tiếng

Khi một task yêu cầu chạy liên tục 4–6 tiếng qua nhiều vai trò (Lead -> BA -> Architect -> Dev -> QA -> Writer), AI **không được tin tưởng vào bộ nhớ tạm thời của đoạn hội thoại (Conversation Memory)**. Mọi trạng thái phải được bền vững hóa (persisted) ra hệ thống tệp tin:

1. **Ghi nhận trạng thái trước khi chuyển giao**:
   - Trước khi gọi Subagent tiếp theo hoặc trước khi kết thúc một khâu, Lead bắt buộc cập nhật tiến độ vào:
     - Thẻ task: `tasks/T-<số>.md` (mục Tiến độ / Checklist).
     - Bảng điều phối: `tasks/BOARD.md` (hoặc `doc/delivery/tasks/BOARD.md`).
     - Hộp thư ghi chú: `docs/notes/inbox/`.
2. **Khôi phục trạng thái tức thì (State Rehydration)**:
   - Nếu phiên làm việc bị ngắt kết nối, gặp lỗi timeout, hoặc được compact: Agent chỉ cần đọc lại `BOARD.md` và đúng file `tasks/T-<số>.md` đang làm là khôi phục 100% ngữ cảnh mà không cần cuộn lại lịch sử chat.

---

## 4. Ngưỡng Kích Hoạt Thu Gọn Ngữ Cảnh (Auto-Compact Triggers)

Việc thu gọn ngữ cảnh (Compact) phải diễn ra có kiểm soát để tránh mất thông tin kiến trúc:

| Điều kiện kích hoạt | Hành động của Lead / Runtime | Cách bảo toàn dữ liệu |
|---|---|---|
| **Context đạt ≥ 75% ngưỡng tối đa** (hoặc > 150k tokens) | Kích hoạt lệnh `/compact` hoặc để runtime thực hiện auto-truncation | Toàn bộ bằng chứng đã nằm tại `docs/notes/inbox/` và `tasks/`, bản tóm tắt compact chỉ cần giữ mục tiêu và task hiện tại. |
| **Hoàn thành 1 Epic hoặc Chuyển giao giữa các Cổng lớn (Gate 2 -> Gate 5)** | Chủ động thực hiện checkpoint và compact | Ghi biên bản bàn giao vào `docs/notes/inbox/`, chạy `python scripts/notes-index.py` để cập nhật `INDEX.md`, sau đó bắt đầu phiên/khâu mới sạch sẽ. |
| **Gặp lỗi `Compaction exhausted` hoặc suy giảm nhận thức (Looping)** | **DỪNG LẠI NGAY LẬP TỨC**. Không cố sửa sai trong cùng phiên. | Spawn một phiên mới tinh (Fresh Session), nạp lại trạng thái từ task card và tiếp tục. |

---

## 5. Áp dụng trên các Công nghệ Runtime Khác Nhau

- **Google Antigravity**:
  - Dùng `invoke_subagent(TypeName, Role, Prompt, Workspace='branch'|'share')`. Subagent chạy trong tiến trình riêng, giao tiếp qua `send_message`. Khung chat chính không bị ô nhiễm log.
- **Claude Code**:
  - Dùng cơ chế Subagent Task Delegation; tự động kích hoạt `/compact` khi token phình to; dùng hooks (`PreToolUse` / `PostToolUse`) để giám sát dung lượng file đọc.
- **Kilo Code / Roo Code**:
  - Dùng Profile/Role switching kết hợp Context Window Truncation (tự động cắt tỉa các block terminal cũ). Subagent xả artifact ra `docs/notes/inbox/` theo chuẩn chung.
