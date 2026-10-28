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
| N-003 | 2026-10-28 | `KNOWLEDGE-DIAGRAMS-EPIC` | Toàn cục | Bẫy tọa độ 2D của LLM: Tuyệt đối không để AI tính toán tọa độ x, y, width, height để sinh XML Draw.io thô vì tỷ lệ lệch dây nối và đè chữ lên tới 85%. Bắt buộc dùng Auto-Layout (CSV Import, D2, Mermaid, Diagrams Python). |
| N-004 | 2026-10-28 | `KNOWLEDGE-DIAGRAMS-EPIC` | Toàn cục | Tránh ô nhiễm bộ khung: Không commit dữ liệu runtime của dự án ngoài (inbox notes, task board, proposals) lên repo framework agent-base; bắt buộc duy trì vành đai cách ly trong .gitignore. |

## Quyết định quan trọng

(tóm tắt một dòng kèm liên kết tới ADR trong `docs/adr/`)

| ID | Ngày | Quyết định | ADR |
|---|---|---|---|
| N-005 | 2026-10-28 | Quyết định chuẩn hóa sơ đồ kiến trúc Draw.io thông qua định dạng CSV Auto-Layout (Header # style, # connect, # layout: auto) và Python diagrams thay vì viết XML mxGraphModel trực tiếp. | Theo `KNOWLEDGE-DIAGRAMS-EPIC` |
| N-006 | 2026-10-28 | Quyết định phân tách tri thức: Giữ nguyên doc/ và .ai-rules/ ở gốc workspace làm la bàn chung; agent-base chỉ sao phần dùng chung được (quy trình, chuẩn, mẫu) vào agents/knowledge và agents/templates, dữ liệu dự án ở lại bên ngoài. | Theo `KNOWLEDGE-DIAGRAMS-EPIC` |

## Quy ước phát hiện thêm

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
