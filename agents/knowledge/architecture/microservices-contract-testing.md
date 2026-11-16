# Kiểm Thử Hợp Đồng Vi Dịch Vụ (Consumer-Driven Contract Testing)

> **Loại: tham khảo.** Quy chuẩn kiểm thử tương thích API phân tán bằng Consumer-Driven Contract Testing (Pact / Spring Cloud Contract).
> Liên quan: `clean-architecture-and-ddd.md`, `goi-giua-service.md`, `openapi-commits-and-backstage.md`.

## 1. Vấn Đề Của Vi Dịch Vụ & Tại Sao Cần Contract Testing

Trong kiến trúc Microservices, kiểm thử tích hợp toàn phần (E2E Integration Test) rất chậm, tốn kém và không ổn định (flaky) do phụ thuộc nhiều service đồng thời.
- **Giải pháp:** *Consumer-Driven Contract Testing (CDCT)* — Cho phép Consumer (phía gọi) và Provider (phía cung cấp API) kiểm thử độc lập mà vẫn bảo đảm 100% tương thích khi tích hợp.

```
[Consumer Tests] ──> [Sinh Hợp Đồng Pact JSON] ──> [Pact Broker] ──> [Provider Xác Thực]
                                                                            │
                                                                   [can-i-deploy: PASS]
```

## 2. Quy Trình 4 Bước Hoạt Động Cốt Lõi

1. **Consumer định nghĩa Hợp đồng:** Consumer viết unit test với Mock Provider, định nghĩa rõ ràng kỳ vọng: Request (Path, Method, Headers, Body) $\rightarrow$ Expected Response (Status, Payload Schema). Khi test xanh, công cụ tự động sinh file hợp đồng `pact.json`.
2. **Publish Hợp đồng:** File hợp đồng được đẩy lên kho lưu trữ tập trung (*Pact Broker* hoặc Artifact repository).
3. **Provider xác thực độc lập:** Provider tải hợp đồng về và chạy test nội bộ (tự replay lại các request trong file Pact vào Controller thật) để kiểm chứng mình có trả về đúng schema mà Consumer mong đợi không.
4. **Cổng kiểm tra phát hành (`can-i-deploy`):** Trước khi merge hoặc deploy một service lên Production, CI/CD chạy lệnh kiểm tra xem phiên bản Provider hiện tại có tương thích với phiên bản Consumer đang chạy trên Production không.

## 3. Phân Biệt Thay Đổi Phá Vỡ (Breaking Changes)

- **Thay đổi tương thích ngược (Non-breaking):**
  - Thêm endpoint mới.
  - Thêm trường mới vào response JSON (với điều kiện Consumer tuân thủ nguyên lý *Tolerant Reader* — chỉ đọc trường cần dùng, bỏ qua trường lạ).
- **Thay đổi phá vỡ hệ thống (Breaking Change):**
  - Đổi tên trường hoặc đổi kiểu dữ liệu (`number` $\rightarrow$ `string`).
  - Xóa bỏ một trường dữ liệu có sẵn trong hợp đồng.
  - Thêm trường bắt buộc (`required`) vào request payload.
  $\implies$ Bắt buộc phải nâng phiên bản API (`/api/v2/...`) hoặc duy trì song song trong giai đoạn chuyển tiếp.

## 4. Best Practices Khi Viết Hợp Đồng

- **Matcher linh hoạt:** Dùng Type Matcher (khớp kiểu dữ liệu) hoặc Regex Matcher thay vì so khớp giá trị tĩnh tuyệt đối (tránh gãy test do ID hoặc ngày giờ thay đổi).
- **Tránh nhồi nhét logic:** Hợp đồng chỉ kiểm tra ranh giới giao tiếp (Schema, Headers, Status code, Nullability), không dùng để thay thế Unit test logic nghiệp vụ.
