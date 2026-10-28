# Mẫu tin nhắn giữa các agent

Dùng cho Swarm Board, nhắn thẳng giữa phiên, hoặc hộp thư MCP. Mọi tin nhắn theo đúng mẫu này để không lạc đề và không tốn token.

```
Từ: dev-a          Đến: architect
Loại: câu hỏi | thông báo | yêu cầu | bị chặn
Task: T-12
Nội dung: (1–3 câu, đủ ngữ cảnh, không tham chiếu mơ hồ)
Cần trả lời trước: (nếu có)
```

## Quy tắc

1. Người nhận không biết gì về ngữ cảnh của bạn: nêu đủ thông tin, không viết "như đã nói".
2. Tin nào dẫn đến quyết định hoặc bàn giao phải được chép vào task card. Board và hộp thư chỉ là kênh báo, task card mới là bản ghi chính thức.
3. Board không đánh thức hay giao việc cho ai. Việc cần hành động phải do Lead giao.
4. `bị chặn`: đổi trạng thái card sang `blocked`, ghi lý do và điều cần để gỡ.
5. Không tự sửa file của task khác, gửi `yêu cầu` cho chủ task.

## Ví dụ

```
Từ: dev-a          Đến: dev-b
Loại: thông báo
Task: T-12
Nội dung: Tôi vừa đổi chữ ký hàm validateToken(token) thành validateToken(token, now). Nếu module của bạn (T-013) gọi hàm này, cần thêm tham số thứ hai.
Cần trả lời trước: không
```

---

## Chuẩn Định Dạng Giao Tiếp Hành Động Trước (Action-First Communication)
*(Hấp thụ từ `ayghri/i-have-adhd` nhằm triệt tiêu quá tải nhận thức)*

Mọi phản hồi hoặc trao đổi hướng tới con người hoặc giữa các agent cần tuân thủ 5 quy tắc vàng:

1. **Đưa hành động lên đầu (Lead with the next action)**: Dòng đầu tiên là lệnh shell cần chạy, đường dẫn file cần mở, hoặc quyết định cần chọn. Tuyệt đối không mở đầu bằng 1-2 đoạn văn dạo đầu dài dòng.
2. **Số hóa nhiệm vụ nhiều bước**: Nếu việc có trên 1 bước, bắt buộc dùng danh sách đánh số `1. 2. 3.`. Mỗi bước là 1 hành động nguyên tử.
3. **Ước lượng thời gian cụ thể**: Ghi rõ thời gian ước tính (ví dụ: `~2 phút`, `~15 phút`), tránh dùng từ mơ hồ như "một lát", "chờ tí".
4. **Kết thúc bằng đúng 1 hành động tiếp theo**: Nếu còn việc dở, chỉ rõ ĐÚNG MỘT việc con người có thể làm ngay trong dưới 2 phút.
5. **Triệt tiêu văn hoa rườm rà (No conversational fluff)**: Cắt bỏ các câu chào hỏi, xin lỗi, cảm ơn khách sáo ("Rất vui được hỗ trợ bạn", "Tôi xin phép..."). Đi thẳng vào nội dung kỹ thuật.
6. **Bắt buộc 100% Tiếng Việt**: Toàn bộ trao đổi với người dùng, tin nhắn giữa các agent, báo cáo to-dos, task card và handoff note phải dùng Tiếng Việt. Chỉ dùng tiếng Anh cho code, tên biến/hàm, keyword kỹ thuật, tên file và commit message Git.

