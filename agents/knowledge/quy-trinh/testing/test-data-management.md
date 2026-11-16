# Quản Trị Dữ Liệu Kiểm Thử (Test Data Management - TDM)

> **Loại: tham khảo.** Chiến lược thiết kế, làm mờ dữ liệu nhạy cảm (PII) và quản trị vòng đời Test Data trong kiểm thử phần mềm.
> Liên quan: `istqb-test-engineering-playbook.md`, `agents/protocols/test-cases.md`.

## 1. Ba Tầng Dữ Liệu Kiểm Thử (Test Data Pyramid)

1. **Tầng Unit Test (Mock & Fake Data):** Dùng Mockito, Instancio, Faker sinh dữ liệu giả lập trong bộ nhớ. Không chạm vào CSDL thật, thực thi $\le 5$ms.
2. **Tầng Integration Test (Fixtures & Containers):** Khởi tạo PostgreSQL qua Testcontainers. Nạp dữ liệu nền bằng file SQL Fixture hoặc Liquibase test dataset. Tự rollback sau mỗi bài test.
3. **Tầng E2E / UAT (Sanitized Production Data):** Dữ liệu trích xuất từ Production nhưng **bắt buộc phải qua quy trình làm mờ ẩn danh (Anonymization)**.

## 2. Quy Chuẩn Làm Mờ Dữ Liệu Nhạy Cảm (PII Masking)

Tuyệt đối cấm mang dữ liệu khách hàng thật lên môi trường Dev/Staging:

| Loại thông tin | Quy tắc làm mờ (Masking Rule) | Ví dụ sau khi che |
|---|---|---|
| **Họ và tên** | Thay bằng từ điển tên mẫu ngẫu nhiên | `Nguyễn Văn Thử Nghiệm` |
| **Email** | Chuyển đuôi về domain kiểm thử nội bộ | `user_9921@test.local` |
| **Số điện thoại** | Giữ đầu số thử nghiệm, che số giữa | `0900009921` |
| **Số CCCD / CMND** | Sinh ngẫu nhiên theo thuật toán kiểm tra checksum | `001090999999` |
| **Số thẻ ngân hàng** | Dùng dãy BIN test chuẩn quốc tế | `4111111111111111` |
| **Mật khẩu** | Băm lại toàn bộ về mật khẩu dev cố định | Băm BCrypt của `Dev@12345` |

## 3. Danh Mục Dữ Liệu Biên Bắt Buộc (Boundary & Chaos Data)

Mọi bộ test dữ liệu đầu vào bắt buộc phải chứa các mẫu dữ liệu "ác hiểm":
- **Giá trị rỗng & khoảng trắng:** `null`, chuỗi rỗng `""`, chuỗi toàn dấu cách `"   "`, chuỗi ngắt dòng `\n\r`.
- **Ký tự đặc biệt & Đa ngữ:** Ký tự có dấu tiếng Việt UTF-8, ký tự Trung/Nhật/Ả Rập (RTL), Emoji đa tầng (👨‍👩‍👧‍👦).
- **Tải trọng tấn công (Attack Payloads):** Payload XSS (`<script>alert(1)</script>`), SQLi (`' OR '1'='1`), XPath injection.
- **Biên số học cực hạn:** Số 0, số âm, số nguyên tối đa `Long.MAX_VALUE` ($9 \times 10^{18}$), số tiền lẻ làm tròn ($0.00000001$).

## 4. Dọn Dẹp Dữ Liệu Sau Test (Data Teardown & Isolation)

- **Cô lập trạng thái:** Mỗi ca test phải tự tạo dữ liệu độc lập, cấm phụ thuộc vào dữ liệu do ca test trước sinh ra.
- **Rollback tự động:** Sử dụng `@Transactional` trên các lớp test Spring Boot để tự động hoàn tác mọi thay đổi DB sau khi chạy xong.
- **Dọn dẹp bảng trung gian:** Với các luồng không thể rollback (kết nối Kafka/S3 local), bắt buộc khai báo phương thức `@AfterEach` để xóa dữ liệu rác.
