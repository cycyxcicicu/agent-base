# Ghi chú cho agent sau (handoff note)

Sau khi xử lý xong việc của mình, **mỗi agent ghi lại những gì agent sau cần biết**. Task card ghi *việc này đã xong chưa*. Ghi chú này ghi *điều học được và điều cần cẩn thận* để người sau (và agent sau) khỏi đâm vào cùng một chỗ.

## Cơ chế: hộp thư đến rồi gộp

Nếu mọi agent sửa chung một file, các nhánh chạy song song sẽ xung đột. Vì vậy:

1. **Agent ghi vào hộp thư đến**: một file riêng cho mỗi lần làm, `docs/notes/inbox/<Task>-<agent>.md` (ví dụ `T-012-dev-a.md`). File tên riêng nên không bao giờ xung đột, và merge gate cho phép sẵn file này.
2. **Tech Writer gộp** vào `docs/PROJECT-NOTES.md` sau mỗi lần merge: đưa đúng mục, gộp trùng, giữ nguồn T-xxx, rồi xóa file hộp thư đã gộp (git vẫn giữ lịch sử).
3. **Agent bắt đầu việc** đọc cả `docs/PROJECT-NOTES.md` **và** các file chưa gộp trong `docs/notes/inbox/`.

Chỉ Tech Writer được sửa `docs/PROJECT-NOTES.md`. Agent khác chỉ ghi vào hộp thư đến.

## Mẫu

```markdown
Task: T-012        Agent: dev-a        Ngày: YYYY-MM-DD

## Đã làm
(1–3 dòng)

## Lưu ý cho agent sau
(bắt buộc. Nếu thật sự không có, ghi "không có lưu ý")
- Bẫy hoặc hành vi bất ngờ: (ví dụ: hàm X trả về null khi ..., cần kiểm tra trước khi dùng)
- Quyết định đã đưa ra và lý do:
- File hoặc khu vực dễ vỡ, cần cẩn thận: (đường dẫn cụ thể)
- Giả định chưa kiểm chứng:

## Việc dở dang hoặc nợ kỹ thuật
(việc chưa làm, làm tạm, cần làm lại)

## Ảnh hưởng đến task khác
(T-xxx nào cần biết, và cần biết gì)

## Đề xuất cập nhật quy ước hoặc tài liệu
(nếu phát hiện quy ước nên thêm vào `agents/stacks/` hoặc `PROJECT.md`)
```

## Quy tắc viết

- Viết cho người **chưa biết ngữ cảnh**: nêu đường dẫn cụ thể, không viết "như đã nói".
- Ngắn, mỗi ý một dòng. Điều đáng ghi là điều **không thể suy ra từ code hay git log**.
- Không ghi khóa bí mật, mật khẩu, token, dữ liệu cá nhân.
- Không ghi điều đã có trong code hoặc trong task card.
- Điều chưa chắc thì gắn nhãn "chưa xác minh".
- Ghi lại cả những hướng đã thử mà **không** chạy, để người sau khỏi thử lại.
