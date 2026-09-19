# Mẫu tin nhắn giữa các agent

Dùng cho Swarm Board, nhắn thẳng giữa phiên, hoặc hộp thư MCP. Mọi tin nhắn theo đúng mẫu này để không lạc đề và không tốn token.

```
Từ: dev-a          Đến: architect
Loại: câu hỏi | thông báo | yêu cầu | bị chặn
Task: T-012
Nội dung: (1–3 câu, đủ ngữ cảnh, không tham chiếu mơ hồ)
Cần trả lời trước: (nếu có)
```

## Quy tắc

1. Người nhận không biết gì về ngữ cảnh của bạn: nêu đủ thông tin, không viết "như đã nói".
2. Tin nào dẫn đến quyết định hoặc bàn giao phải được chép vào task card. Board và hộp thư chỉ là kênh báo, task card mới là bản ghi chính thức.
3. Board không đánh thức hay giao việc cho ai. Việc cần hành động phải do Orchestrator giao.
4. `bị chặn`: đổi trạng thái card sang `blocked`, ghi lý do và điều cần để gỡ.
5. Không tự sửa file của task khác, gửi `yêu cầu` cho chủ task.

## Ví dụ

```
Từ: dev-a          Đến: dev-b
Loại: thông báo
Task: T-012
Nội dung: Tôi vừa đổi chữ ký hàm validateToken(token) thành validateToken(token, now). Nếu module của bạn (T-013) gọi hàm này, cần thêm tham số thứ hai.
Cần trả lời trước: không
```
