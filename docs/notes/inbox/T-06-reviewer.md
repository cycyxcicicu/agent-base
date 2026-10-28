> summary: T-06 reviewer: duyệt diff cổng T-06, kết luận đạt/trả lại
# Task: T-06 - Diff Review Gate

Task: T-06        Agent: reviewer        Ngày: 2026-10-25

- **Mục đích**: Thẩm định diff T-06 trước khi người dùng commit; xác nhận không vượt scope, logic cầu nối/validator đúng, test đủ, số liệu card khớp thực tế.
- **Đã làm**: đọc card + handoff QA/lead; chạy unittest (242 OK), check-skills (0 problem), link-skills --check (junction 31/31), đối chiếu 6 file skill đã tách, kiểm setup/CI. Đã đóng dấu `Diff Approved by reviewer` trong card.
- **Files đã sửa**: `tasks/E1-nen-tang/T-06.md` (chỉ 1 dòng Diff Approved), `docs/notes/inbox/T-06-reviewer.md`.
- **Skill đã chọn & áp dụng: `open-code-review`** (Favor precision over recall; phân loại Blocking/Non-blocking) và **`codebase-design`** (kiểm ranh giới SKILL.md ↔ references/).
- **Checklist đã tuân thủ**: (1) Chỉ đọc và chạy lệnh kiểm, không sửa code; (2) Mọi kết luận có lệnh + số liệu; (3) Tách rõ lỗi diff với điều kiện chặn merge do nhánh/cây bẩn.

## Verdict
ĐẠT. Không có lỗi blocking trong phạm vi T-06.

## Non-blocking (đề xuất task sau)
1. `check-skills.py` chỉ kiểm link trong `SKILL.md`, chưa quét `references/*.md` — nội dung đã chuyển sang đó nên link có thể gãy mà không bị bắt.
2. Vượt 500 dòng chỉ `WARN`, `--strict` không nâng thành problem → CI vẫn xanh nếu phình lại.
3. `link-skills.py --check` trả 0 cho thư mục copy khớp nội dung (có in cảnh báo) — dễ đọc nhầm là cầu nối thật.
4. 3 nhãn trong fence ```dot của `subagent-driven-development/SKILL.md` (dòng 88/117/118) còn nhắc `../requesting-code-review/...`.
5. 3 file `setup.*` chưa từng được git track; commit chúng dưới message "add discovery bridges" nên mô tả rộng hơn (ví dụ "wire setup and CI").

## Chặn merge (không phải lỗi diff)
`merge-gate.py` FAIL vì card chưa có trên nhánh base `develop` và hiện đang ở `main`. Người dùng cần tạo `feature/06-skill-spec-compliance`, commit theo kế hoạch trong card, rồi chạy lại merge gate với `--base develop`.
