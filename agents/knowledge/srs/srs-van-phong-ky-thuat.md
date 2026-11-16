> **Loại: tham khảo.**
> Nguồn: tách từ srs-fdd-writing-standard.md mục F

# Văn phong kỹ thuật khi viết tài liệu thiết kế SRS_FDD (Mục F)

Tài liệu thiết kế được viết **trước khi code**, để Dev, QA và Kế toán cùng đọc. Viết như một đặc tả kỹ thuật do người viết, không như bản tường thuật.

1. **Viết yêu cầu, không viết hiện trạng.** Dùng "Hệ thống phải…", "Hệ thống cho phép…", thì hiện tại, một ý một câu. Tài liệu thiết kế không chứa: "Đạt", "Lệch", "theo code", "Not run", "đã làm", "đề xuất". Đối chiếu với code đã có đặt ở file riêng `doc/features/<UC>/<UC>-doi-chieu.md`.
2. **A/C dạng điều kiện → kết quả**, kiểm chứng được: "Khi … thì …". Không dùng từ chung chung (nhanh, dễ dùng, phù hợp).
3. **Giá trị cụ thể:** giới hạn, số lượng, định dạng, thông báo ghi đúng nguyên văn. Chưa có giá trị thì ghi vào mục Câu hỏi mở, không viết vào nội dung.
4. **Thuật ngữ nghiệp vụ và nhãn giao diện** đúng như trên màn hình/ SRS. Tên class/ biến chỉ xuất hiện ở mục API, tác động và RTM.
5. **Không giải thích cách làm tài liệu** (không "Cách đọc", "Căn cứ suy ra", ghi chú về phương pháp). Nguồn ghi một dòng trong bảng đầu tài liệu.
6. **Phần chưa chốt dồn vào mục Câu hỏi mở** (mục cuối). Nội dung chính chỉ chứa điều đã chốt.
7. **Định dạng gọn:** bảng cho dữ liệu có cấu trúc, câu ngắn cho phần còn lại. Không emoji, không in đậm tràn lan, không gạch ngang dài làm dấu ngắt câu.
8. **Một thuật ngữ một nghĩa** trong toàn tài liệu.
9. **Thuật ngữ kỹ thuật chuyên ngành:** Giữ nguyên tiếng Anh gốc nếu dịch sang tiếng Việt bị gượng gạo, ngô nghê hoặc làm tối nghĩa (ví dụ: dùng *Swimlane* thay vì *bơi làn*; giữ nguyên *Controller, Service, Worker, Consumer, Producer, Queue, Payload, Webhook, State Machine, Deadlock, Race Condition, P99 Latency, Circuit Breaker, SSRF...*). Tuyệt đối không dịch gượng ép các khái niệm kỹ thuật chuẩn quốc tế.
