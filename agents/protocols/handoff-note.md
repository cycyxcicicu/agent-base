# Ghi chú cho agent sau (handoff note)

Sau khi xử lý xong việc của mình, **mỗi agent ghi lại những gì agent sau cần biết**. Task card ghi *việc này đã xong chưa*. Ghi chú này ghi *điều học được và điều cần cẩn thận* để người sau (và agent sau) khỏi đâm vào cùng một chỗ.

## Cơ chế: hộp thư đến rồi gộp

Nếu mọi agent sửa chung một file, các nhánh chạy song song sẽ xung đột. Vì vậy:

1. **Agent ghi vào hộp thư đến**: một file riêng cho mỗi lần làm, `docs/notes/inbox/<Task>-<slug>-<agent>.md` (ví dụ `T-13-fix-loi-xuat-excel-dev-a.md`). File tên riêng nên không bao giờ xung đột, và merge gate cho phép sẵn file này.
2. **Tech Writer gộp** vào `docs/PROJECT-NOTES.md` sau mỗi lần merge: đưa đúng mục, gộp trùng, giữ nguồn T-xxx, rồi ghi danh sách file đã gộp vào kế hoạch commit để **người dùng** xóa (lịch sử vẫn nằm trong git).
3. **Agent bắt đầu việc** đọc cả `docs/PROJECT-NOTES.md` **và** các file chưa gộp trong `docs/notes/inbox/`.

Chỉ Tech Writer được sửa `docs/PROJECT-NOTES.md`. Agent khác chỉ ghi vào hộp thư đến.

## Mẫu 1: Ghi chú Task chính (Standard Handoff Note)
Áp dụng khi một vai trò hoàn thành hoặc tạm dừng phiên của một Task card lớn (`docs/notes/inbox/<Task>-<slug>-<agent>.md`, ví dụ `T-12-dev.md`).

```markdown
> summary: (một dòng, ≤120 ký tự — note này nói về gì, agent nào cần đọc)

Task: T-12        Agent: dev-a        Ngày: YYYY-MM-DD

## Đã làm
(1–3 dòng)

## Lưu ý cho agent sau
(chỉ khi có điều agent sau cần biết. Nếu không có, bỏ qua cả ghi chú)
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

## Thay đổi dùng chung cho agent-base
(bắt buộc nếu đã sửa file khung trong `agents/manifest.txt`: script, protocol, vai, mẫu. Ghi: file, sửa gì, vì sao, dùng chung được không. Không sửa thì ghi "không có". Xem `agents/protocols/agent-base-sync.md`)
```

## Mẫu 2: Ghi chú Subtask siêu gọn (Micro Subtask Handoff Note - AGENTS.md §16)
Áp dụng cho từng **Subagent** sau khi hoàn thành 1 Subtask hạt mịn (một mục đích, vừa một phiên ngắn khoảng 2–5 phút).
- **Quy tắc đặt tên file**: Gom gọn vào thư mục mang tên Task `docs/notes/inbox/<Task>/<Task>.<Subtask>-<agent>.md` (ví dụ: `docs/notes/inbox/T-57/T-57.1-dev.md`, `docs/notes/inbox/T-57/T-57.2-dba.md`) giúp quản lý lâu dài không bị lẫn lộn giữa các task; hoặc lưu trực tiếp tại `docs/notes/inbox/<Task>.<Subtask>-<agent>.md`.
- **Mẫu (3–5 dòng, tối ưu token, không viết dài dòng)**:

```markdown
# Subtask: T-57.1 - <Tiêu đề Subtask>
> summary: (một dòng, ≤120 ký tự)
- **Mục đích**: (Làm gì và để đạt mục tiêu/kết quả gì)
- **Đã làm**: (1–2 dòng tóm tắt việc vừa làm)
- **Files đã sửa**: `<file1>`, `<file2>`
- **Kết quả test**: (lệnh rút gọn, vd: `pytest -q <file> PASS` hoặc `alembic upgrade head PASS`)
- **Bàn giao cho Subtask kế tiếp**: (điều Subagent của subtask tiếp theo cần biết để làm tiếp mà không bị bỡ ngỡ)
```

## Quy tắc viết

- **Giới hạn độ dài**: Mỗi note phải **≤ 80 dòng**. Ghi sự thật + quyết định + đường dẫn cụ thể, không chép lại tài liệu.
- Viết cho người **chưa biết ngữ cảnh**: nêu đường dẫn cụ thể, không viết "như đã nói".
- Ngắn, mỗi ý một dòng. Điều đáng ghi là điều **không thể suy ra từ code hay git log**.
- Không ghi khóa bí mật, mật khẩu, token, dữ liệu cá nhân.
- Không ghi điều đã có trong code hoặc trong task card.
- Điều chưa chắc thì gắn nhãn "chưa xác minh".
- Ghi lại cả những hướng đã thử mà **không** chạy, để người sau khỏi thử lại.
