# Bài học viết tài liệu thiết kế, vẽ sơ đồ và bàn giao (rút từ chức năng xuất đơn sang đối tác vận chuyển)

> **Loại: tham khảo.** Tổng hợp bài học từ thực tế dự án, không phải nguồn luật. Khi khác `AGENTS.md`, vai trò hoặc `agents/protocols/` thì theo các nơi đó.

Áp dụng cho **mọi agent** (Claude, Gemini, Codex...) khi viết đặc tả thiết kế, vẽ sơ đồ `.drawio` và đưa tài liệu cho người khác đọc. Rút ra từ một chức năng tích hợp API đối tác dùng hàng đợi, nhiều consumer và tiến độ thời gian thực. Phần nào còn mang tên dự án riêng nằm ở `.ai-rules/` của dự án đó, không ở đây.

## 1. Vì sao có agent vẽ xong rồi tự xem và sửa, có agent không

Không phải do một mô hình "giỏi hơn". Do ba điều, và **điều nào thiếu thì agent dừng sau lần vẽ đầu**:
1. **Có công cụ mở ảnh.** Agent xem được PNG thì thấy chữ đè, mũi tên xuyên ô, nhãn bị cắt.
2. **Có vòng lặp được giao:** vẽ, xuất ảnh, mở ảnh, liệt kê lỗi, sửa, lặp. Lần vẽ đầu hầu như luôn có lỗi bố cục; hình sạch là kết quả của 2 đến 3 vòng.
3. **Quy tắc ghi rõ là bắt buộc**, kèm cách xử lý khi không làm được.

Quy tắc cho mọi agent:
- Vẽ xong **phải xuất ảnh và xem từng ảnh** (chi tiết `quy-uoc-draw-io-va-archify.md` mục 7).
- Agent không xem được ảnh: chạy kiểm tra bằng máy (`scripts/diagram-describe.py <file> --page "<tên>" --check`, và kiểm tên có trong code nếu dự án có) rồi **ghi rõ "chưa kiểm tra bằng mắt"**. Cấm nói "sơ đồ đẹp". Kiểm tra bằng máy chỉ bắt lỗi cấu trúc và tên; **không bắt được** chữ đè hay đường xuyên ô, nên người dùng vẫn là cổng cuối.
- Không báo xong khi mới "xuất được file".

## 2. Sửa sơ đồ mà người dùng đã chỉnh tay

1. Người dùng thường mở `.drawio` và chỉnh định dạng. **Không sinh lại cả tab** để sửa một chữ: mất định dạng của họ.
2. Sửa tại chỗ: đọc bằng `xml.etree.ElementTree`, chỉ đổi thuộc tính `value` của ô cần sửa, giữ nguyên `id`, tọa độ, `style`. Ký tự `&` viết `&amp;`. Ghi xong `ET.parse` lại để chắc file hợp lệ, rồi xuất ảnh.
3. Chỉ vẽ lại nguyên tab khi người dùng nói rõ ("vẽ lại cho chuẩn"), và nói rõ tab nào bị thay.
4. Khi người dùng đổi thiết kế (bỏ một nút, bỏ một khái niệm), **quét mọi sơ đồ, tài liệu, danh sách câu hỏi mở** để bỏ khái niệm cũ. Đừng chỉ sửa file đang mở. Lỗi hay gặp: còn nút "Dừng", màn đã bỏ, bảng "đợt xuất" đã loại.

## 3. Vẽ luồng có hàng đợi và nhiều consumer

- Làn tối thiểu: người dùng, giao diện, API, **hàng đợi**, **consumer**, hệ thống ngoài, bảng dữ liệu nguồn sự thật. Không gộp "API gọi hệ thống ngoài" thành một nút.
- Mũi tên vào hàng đợi ghi **nội dung tin**: mã bản ghi, người thực hiện, thời điểm đưa vào và **loại việc** (ví dụ tạo mới hay làm lại), để consumer biết xử lý thế nào khi nhiều tin cùng hàng.
- Mỗi sơ đồ hoạt động có **một chấm bắt đầu và đúng một chấm kết thúc**; thành công, lỗi, bỏ qua đều dồn về chấm đó. Nhánh lỗi tô đỏ và có chữ "LỖI".
- Kết quả của từng bản ghi ghi **vào bảng nguồn sự thật**, không giữ trong bộ nhớ hay bảng "lô" phụ khi người dùng đã chọn bỏ.
- Hạn mức của đối tác (số yêu cầu mỗi giây, mỗi ngày) là một thành phần riêng (bộ điều tiết) và xuất hiện trong luồng.

## 4. Viết tài liệu thiết kế khi chưa có code

- **Không nhắc code:** không tên lớp, gói, hàm. Viết hiện trạng (As-Is), mục tiêu (To-Be) và bảng "dùng lại, thay thế, bỏ, thêm mới".
- **Dùng đúng tên của tài liệu đối tác** (tên API, tên trường, mã lỗi) lấy từ trang tài liệu gốc, không tự đặt tên A, B, C.
- Mỗi API ngoài có: mô tả (khi nào gọi, để làm gì), bảng request (trường, kiểu, bắt buộc, ghi chú), bảng response, mã lỗi và cách xử lý. Mỗi API nội bộ có request và response mẫu. Thiếu mô tả hoặc thiếu response là chưa đạt.
- Webhook hay callback của đối tác: **mỗi loại có khóa và bộ mã riêng**. Đọc từng trang, không gộp về một mẫu tự nghĩ. Cùng một số mã có thể khác nghĩa ở hai loại; lập bảng đối chiếu các bộ mã với trạng thái nội bộ.
- Điều chưa chắc: gắn nhãn `[CHƯA KIỂM CHỨNG]` (chưa chạy sandbox) hoặc `[ĐỀ XUẤT]` (thiết kế mới, cần duyệt). Điều này gồm cả điều tài liệu đối tác không nêu (ví dụ API in nhãn có trả link không).
- **Trước khi khẳng định "code chưa có xử lý X", grep và đọc code.** Từng khẳng định sai rằng code không xử lý mã trùng đơn trong khi code có.
- **Câu hỏi chờ xác nhận** là danh sách để chốt, mỗi câu có giá trị đề xuất và trạng thái; không viết như đã quyết. Câu nào chặn việc code thì nói rõ (cần hỏi nghiệp vụ, cần chạy sandbox).

## 5. Ảnh sơ đồ và link nguồn trong tài liệu

- Một file `.drawio` nhiều tab cho một chức năng; tên tab ổn định.
- Có tệp ánh xạ tên tab sang tên ảnh (ví dụ `_anh.json`) để tài liệu dẫn ảnh theo tên cố định, và xuất lại chỉ tab đã đổi (so băm). Màn hình mockup trong một tab lớn thì cắt theo khung.
- Dưới mỗi ảnh có dòng "Sơ đồ nguồn" trỏ tới tab trong draw.io. Link dạng `https://app.diagrams.net/?page-id=<id tab>#G<ID file Drive>` **chưa kiểm chứng** là nhảy đúng tab; `page-id` đổi nếu draw.io lưu lại file, khi đó gắn lại link.

## 6. Bàn giao lên Google Drive và Google Docs

Chi tiết lỗi định dạng: `agents/knowledge/srs/md-to-office-fidelity.md`. Thêm các điểm đã chạy thật:
- md là nguồn duy nhất; dựng docx ở máy; **chèn link tab trước khi dựng docx**.
- Không có CLI `gdrive` và công cụ Drive không tải được file vài MB: dùng trình duyệt (extension), bấm Mới, Tải tệp lên, tìm ô `input[type=file]` ẩn rồi gửi file. Không đọc cookie hay chuỗi truy vấn bằng JavaScript (bị chặn).
- Mở docx trong Google Docs, Tệp, Lưu dưới dạng Google Tài liệu. Kiểm bằng công cụ Drive: `mimeType` là Google Docs; đọc nội dung và đếm `§§`, `Table of Contents`, `{{`, `| ---` đều bằng 0, số dòng "Sơ đồ nguồn" khớp số ảnh. Xem trang, bảng, ảnh vừa trang vẫn phải nhìn; chưa nhìn thì ghi "chưa kiểm tra bằng mắt".
- Không commit, không đẩy khi chưa được nói rõ. Không xóa file người dùng đã tải lên.

## 7. Báo cáo trung thực khi nộp

Nói rõ: đã kiểm cái gì, chưa kiểm cái gì, còn lỗi gì chấp nhận được (ví dụ thiếu mục kiểm thử khi chưa viết test case), điều nào chặn việc tiếp theo. Không khẳng định điều chưa kiểm chứng.
