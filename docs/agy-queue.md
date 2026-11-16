# agy-queue: chạy kiểm thử hàng loạt bằng nhiều lượt agy

Công cụ: `scripts/agy-queue.py` (dùng `scripts/agy-acp-bridge.py`). Cấu hình mẫu: `examples/agy-queue.config.json`.

## Cách dùng
1. Viết file cấu hình (mẫu ở trên): thư mục case (`case_glob`), thư mục kết quả, file hướng dẫn cho agy, regex mã case, và mỗi lượt một thư mục `--dir` riêng (bridge khóa theo `--dir`, trùng thì thoát mã 4).
2. Kiểm hạn mức: `agy --print "/usage"`. Hết thì không chạy.
3. `python3 scripts/agy-queue.py plan --config C --workdir W`: tính case còn lại, chia phần tối đa 12 case, cân tải cho các lượt, sinh brief và `queue-<lượt>.txt` trong `W` (để `W` ngoài repo).
4. Mỗi lượt chạy nền một tiến trình: `agy-queue.py run --config C --workdir W --lane A`.
5. Theo dõi: `agy-queue.py watch ...` (mỗi dòng in ra là một sự kiện, dùng với Monitor) hoặc `status`.
6. Sau khi xong: gộp file phần thành một file theo đơn vị, kiểm lại kết quả, rồi mới ghi hệ thống quản lý test.

## Bài học đã đo (đừng lặp lại lỗi cũ)
- Tối đa **3 lượt cùng lúc**: nhiều hơn tràn RAM (mỗi lượt mở một Chrome tab).
- Phiên agy tối đa **3600 giây**; hết giờ thì file kết quả dở dang. Vì vậy chia phần tối đa 12 case.
- Bridge thoát mã 0 cả khi hết quota ("Individual quota reached", 0 token). Công cụ tự đọc đầu ra và dừng lượt, không bỏ qua hàng đợi.
- Quota tính theo tài khoản agy. Đổi tài khoản giữa chừng làm lượt đang chạy sai; đổi thì dừng lượt trước.
- Công cụ trình duyệt đôi khi chưa kết nối: brief bắt agy thử lại ngay, không được nói "đang chờ" (agy kết thúc lượt khi nói vậy).
- Lỗi 400 INVALID_ARGUMENT thoáng qua làm phiên chết ở 0 token: thử lại là qua (runner thử lại 12 lần, cách 30 giây).
- Chỉ đếm dòng **đã chạy thật** (Pass/Fail/Blocked/Chờ duyệt ghi). File kết quả dở dang hoặc dòng Blocked vì trình duyệt/quota không tính là xong, nếu không phần còn lại bị bỏ sót.
- agy có thể điền cả bảng khi chạy lại; chỉ lấy mã case thuộc phần được giao.
- Không ghi dữ liệu dùng chung bằng agy (quyền bị từ chối); chuẩn bị dữ liệu mẫu bằng script SQL và để người dùng chạy.
- Tab Chrome mở dư: brief yêu cầu mở một tab và đóng đúng tab đó khi xong.

## Mô hình theo tài khoản (đo ngày 16/11/2026)
- **Danh sách mô hình và hạn mức khác nhau theo tài khoản agy, và đổi theo thời điểm.** Cùng một máy, lúc chỉ thấy Gemini 3.8 Flash (High/Medium/Low), lúc có thêm Claude Sonnet 4.6 (Thinking), Claude Opus 4.6 (Thinking), GPT-OSS 120B (Medium); Gemini 4 (Carbon/Argon/Hydrogen) có lúc "Unavailable".
- **`--model` nhận tên hiển thị**, ví dụ `--model "Claude Sonnet 4.6 (Thinking)"`. Các dạng id như `claude-sonnet-4-6-medium` hay `claude-sonnet-4-6-thinking` bị báo "not recognized". Id `claude-sonnet-5-5-medium` chạy được lúc đó nhưng sau bị loại khỏi danh sách.
- **Trước mỗi đợt chạy:** gõ `agy --model "x" --print "ok"`. Nếu báo không nhận, lỗi in kèm "Available models" của tài khoản hiện tại, chọn từ đó. Kiểm `agy --print "/usage"` để biết nhóm hạn mức nào còn.
- Hạn mức chia nhóm ("Gemini" riêng, "Claude and GPT" riêng; mỗi nhóm có giới hạn tuần và 5 giờ). Một nhóm về 0% thì mô hình nhóm kia vẫn có thể chạy; đổi nhóm là cách tiếp tục khi chưa thể đổi tài khoản.
- Cấu hình `model` trong file config của `agy-queue` phải là tên có trong danh sách của tài khoản đang dùng.
