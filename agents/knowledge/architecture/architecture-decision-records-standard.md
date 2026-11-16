# Quy Chuẩn Lập Bản Ghi Quyết Định Kiến Trúc (Architecture Decision Record - ADR)

> **Loại: tham khảo.** Quy chuẩn lập và quản trị vòng đời các quyết định kiến trúc quan trọng trong dự án theo chuẩn Michael Nygard.
> Liên quan: `clean-architecture-and-ddd.md`, `system-design-elite-patterns.md`.

## 1. Mục Đích & Nguyên Tắc Cốt Tử

Mã nguồn chỉ thể hiện *Hệ thống đang hoạt động như thế nào* (`How`), nhưng hoàn toàn không giải thích được *Tại sao lại thiết kế như vậy* (`Why`).
- **Mục đích của ADR:** Lưu vết bối cảnh và sự đánh đổi (Trade-offs) đằng sau mỗi quyết định kỹ thuật lớn.
- **Nguyên tắc bất biến:** Một ADR đã được chấp thuận (`ACCEPTED`) là **bất biến (Immutable)**. Tuyệt đối không sửa lại quyết định cũ trong file đã duyệt. Khi đổi kiến trúc, lập ADR mới và gắn nhãn ADR cũ là `SUPERSEDED by ADR-xxx`.

## 2. Cấu Trúc 5 Phần Chuẩn Mực Của Một ADR

Mỗi file lưu tại `doc/architecture/adr/ADR-[Số]-[Tên-ngắn].md` gồm 5 phần:

1. **Tiêu đề & Trạng thái (Title & Status):**
   - Định danh: `ADR-001: Sử Dụng Redis Cache-Aside Cho Danh Mục Sản Phẩm`.
   - Trạng thái: `PROPOSED` (Đang đề xuất) | `ACCEPTED` (Đã duyệt) | `REJECTED` (Từ chối) | `DEPRECATED` (Hết hạn) | `SUPERSEDED by ADR-xxx` (Bị thay thế).
2. **Bối cảnh (Context):**
   - Vấn đề gặp phải: Lưu lượng truy cập cao làm DB PostgreSQL chạm 95% CPU; thời gian đọc danh mục chậm (P99 $> 1.2$s).
   - Ràng buộc: Không được tăng chi phí phần cứng DB, dữ liệu danh mục thay đổi không quá 1 lần/ngày.
3. **Quyết định (Decision):**
   - Giải pháp chọn: Áp dụng mô hình Caching Cache-Aside với Redis Cluster, thiết lập TTL cố định 4 giờ, chủ động xóa cache (Eviction) khi có sự kiện cập nhật qua Kafka event.
4. **Hệ quả & Đánh đổi (Consequences):**
   - *Tích cực (Ưu điểm):* Giảm 80% tải đọc DB, P99 latency giảm về $< 15$ms.
   - *Tiêu cực (Hạn chế):* Chấp nhận dữ liệu có thể bị trễ tối đa vài giây trong lúc đợi Kafka event; tăng độ phức tạp hạ tầng khi phải duy trì cụm Redis.
5. **Các phương án thay thế đã bị loại bỏ (Alternatives Considered):**
   - *Phương án A (Local Cache In-Memory):* Bị loại vì dữ liệu không nhất quán giữa các instance pods.
   - *Phương án B (Tăng cấu hình DB PostgreSQL):* Bị loại vì chi phí tăng gấp 4 lần.

## 3. Khi Nào Bắt Buộc Phải Lập ADR?

Lập ADR khi quyết định có tính chất "One-way Door" (khó đảo ngược):
- Chọn hoặc thay đổi framework cốt lõi, ORM, hệ quản trị CSDL, Message Queue.
- Thay đổi cấu trúc phân tầng hoặc mô hình giao tiếp giữa các service.
- Quyết định chiến lược bảo mật, phân quyền (RBAC/ABAC) hoặc cơ chế xác thực.
- Quyết định hy sinh tính nhất quán (Eventual Consistency) để đổi lấy hiệu năng cao.
