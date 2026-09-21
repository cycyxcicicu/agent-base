# Cloud & Infrastructure Architecture Recipes (Cẩm Nang Đám Mây Chuẩn Mực)

Tài liệu này chuẩn hóa các nguyên tắc kiến trúc hạ tầng điện toán đám mây, xác thực an toàn, quản lý kết nối và triển khai dịch vụ container hóa, đúc kết từ cẩm nang kỹ thuật của Google Cloud (`google-skills`).

---

## 1. Xác Thực Quyền Tối Thiểu (Least Privilege & Workload Identity)

### 1.1. Cấm Tuyệt Đối Hardcode Service Account Keys
- **Nguyên tắc**: Không bao giờ tải file `key.json` của Service Account về máy local hoặc commit vào repository Git.
- **Giải pháp**:
  - Khi chạy trên Cloud: Sử dụng **Workload Identity Federation** hoặc gán IAM Service Account trực tiếp vào Compute/Container resource.
  - Khi chạy local: Sử dụng `gcloud auth application-default login` để cấp token ngắn hạn (1 giờ), tự động xoay vòng.

### 1.2. Phân Quyền Hạt Mịn (Granular IAM Roles)
- Tránh cấp các quyền gộp nguy hiểm như `roles/owner` hoặc `roles/editor`.
- Chỉ cấp đúng quyền mà tiến trình thực tế cần (ví dụ: `roles/storage.objectViewer` thay vì `roles/storage.admin`).

---

## 2. Quản Lý Kết Nối & Khả Năng Chống Chịu (Connection Resiliency)

### 2.1. Exponential Backoff kèm Full Jitter
Khi gọi các API bên ngoài hoặc dịch vụ phân tán, mạng chập chờn hoặc lỗi quá tải (`429 Too Many Requests`, `503 Service Unavailable`) là điều không thể tránh khỏi.
- **Công thức chuẩn**:
  $$T_{\text{sleep}} = \text{random}(0, \min(T_{\text{max}}, T_{\text{base}} \times 2^{\text{attempt}}))$$
- **Tại sao cần Jitter?** Nếu 1.000 worker cùng gặp lỗi tại giây $t$ và cùng chờ đúng 2 giây để thử lại, chúng sẽ đồng loạt tấn công API tại giây $t+2$ gây ra hiệu ứng bão giật (*Thundering Herd Problem*). Thêm Jitter ngẫu nhiên làm giãn đều các lượt thử lại.

### 2.2. Ngắt Mạch (Circuit Breaker Pattern)
- Theo dõi tỷ lệ lỗi của dịch vụ đích trong cửa sổ trượt (sliding window).
- Khi tỷ lệ lỗi vượt ngưỡng (ví dụ: 5 lần lỗi liên tiếp), chuyển sang trạng thái `OPEN` để từ chối nhanh (fail-fast), tránh làm cạn kiệt tài nguyên cục bộ và cho hệ thống đích thời gian hồi phục.

---

## 3. Quy Chuẩn Triển Khai Container Không Trạng Thái (Stateless Containers)

### 3.1. Xử Lý Tín Hiệu Dừng Mượt Mà (Graceful Shutdown)
- Ứng dụng phải lắng nghe tín hiệu `SIGTERM` từ hệ thống điều phối (Cloud Run, Kubernetes).
- Khi nhận `SIGTERM`:
  1. Ngừng nhận request mới ngay lập tức.
  2. Hoàn thành nốt các request/task đang xử lý trong thời gian chờ (thường là 10–30 giây).
  3. Đóng an toàn các kết nối database pool và socket.
  4. Thoát với mã lỗi `0`.

### 3.2. Không Lưu State Lên Ổ Đĩa Cục Bộ
- Môi trường container là phù du (*ephemeral*). Bất kỳ file nào ghi lên filesystem cục bộ đều biến mất khi container scale-down hoặc restart.
- Toàn bộ dữ liệu bền vững phải lưu vào Cloud Storage (GCS/S3) hoặc cơ sở dữ liệu phân tán.
