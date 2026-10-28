# Thay đổi nguyên tử (PR nhỏ, một ý)

Lý do: một PR vài nghìn dòng không ai duyệt nổi, khó khoanh vùng khi lỗi, khó hoàn tác, và làm lịch sử git mất giá trị làm ngữ cảnh cho agent sau. PR nhỏ thì Reviewer đọc được hết, `merge-gate` kiểm được, hoàn tác chỉ một commit.

Nguồn ý tưởng: bài nói của Lauren Tan (theo bản NotebookLM của người dùng, còn là nguồn thứ cấp). Bài **không đặt trần cứng** cho cỡ PR: từ khoảng 50 dòng đến khoảng 1.000 dòng tùy việc. Điều bài nhấn mạnh là **mục đích**: PR nguyên tử để lịch sử git rõ ràng (làm ngữ cảnh cho agent sau) và rollback dễ. Vì vậy ngưỡng của agent-base **chỉ cảnh báo, không chặn**, và là lựa chọn của dự án, chỉnh được.

## Quy tắc

1. **Một thay đổi logic một commit, một ý một PR.** Tách riêng refactor, đổi tên, format, cấu hình, test, tính năng (xem `agents/protocols/git-rules.md`).
2. **Cỡ mong muốn: từ vài chục đến vài trăm dòng đổi** (thêm + xóa, không tính lockfile, thư mục build, card, ghi chú bàn giao). Việc thật sự không tách được thì lớn hơn cũng được, miễn vẫn một ý và có lý do (quy tắc 5).
3. **`scripts/merge-gate.py` cảnh báo** khi vượt ngưỡng (mặc định 600 dòng, do agent-base chọn, không phải con số của bài). Đổi ngưỡng bằng một trong ba cách, ưu tiên từ trên xuống:
   - `--max-lines N` khi chạy cổng;
   - biến môi trường `MERGE_GATE_MAX_LINES`;
   - dòng `| Giới hạn dòng thay đổi | N |` trong `PROJECT.md`.
   Thêm `--strict-size` để vượt ngưỡng thì cổng FAIL (dùng khi dự án đã quen PR nhỏ).
4. **Vượt ngưỡng thì tách**, đừng nới ngưỡng cho vừa:
   - theo lát cắt dọc (một luồng hẹp từ giao diện đến dữ liệu), mỗi lát có test của nó;
   - tách phần chuẩn bị (đổi tên, di chuyển file, thêm hàm mới chưa ai gọi) thành PR riêng đi trước;
   - dùng Subtask `T-<n>.<k>` (AGENTS.md mục 16): mỗi subtask một PR.
5. **Ngoại lệ có lý do** (di chuyển thư mục lớn, sinh mã, di trú dữ liệu): ghi lý do và số dòng vào card, Reviewer xác nhận rồi mới chạy cổng không `--strict-size`. Thay đổi hàng loạt phải qua cổng rủi ro (`risk-gate.md`).

## Reviewer

PR vượt ngưỡng mà không có ngoại lệ ghi trong card thì **trả lại để tách**, không duyệt gộp.
