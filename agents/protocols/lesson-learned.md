# Bài học sau mỗi lần làm (lesson learned)

Nguồn: quy trình công ty (`quy-trinh-cong-ty.md` mục 1 và 4). Bổ sung cho `handoff-note.md`: ghi chú bàn giao nói *điều agent sau cần biết về chỗ này*; bài học nói *điều cả đội nên làm khác lần sau*.

## Khi nào ghi

- Sau khi đóng một task có lỗi lọt, làm lại, hoặc chậm so với ước lượng.
- Sau mỗi lần phát hành (cùng lúc với `release-note.md`).
- Sau sự cố (kèm post-mortem của `sre`).

## Cách ghi

1. Trong ghi chú bàn giao `docs/notes/inbox/<Task>-<agent>.md`, thêm mục `## Bài học` (bỏ trống nếu không có). Mỗi bài học ba dòng:
   - **Chuyện gì xảy ra:** sự việc, có số liệu nếu có.
   - **Nguyên nhân gốc:** không đổ lỗi cho người.
   - **Lần sau làm gì:** hành động cụ thể, kiểm chứng được.
2. `writer` gộp vào mục `## Bài học chung` của `docs/PROJECT-NOTES.md` sau mỗi lần merge (cơ chế hộp thư đến như `handoff-note.md`).
3. Bài học lặp lại từ hai lần trở lên thì đề xuất biến thành luật cứng (`hard-rules.md`) hoặc sửa protocol; đề xuất ghi vào `docs/proposals/` cho người dùng quyết.

## Quy tắc

Chỉ ghi điều có bằng chứng. Mỗi bài học phải có hành động. Không ghi chung chung kiểu "cần cẩn thận hơn".
