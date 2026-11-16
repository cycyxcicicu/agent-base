# Kiến Trúc Offline-First & Đồng Bộ Dữ Liệu Di Động (Mobile Offline-First & Sync)

> **Loại: tham khảo.** Quy chuẩn thiết kế ứng dụng di động hoạt động không phụ thuộc mạng, lưu trữ cục bộ và giải quyết xung đột đồng bộ.
> Liên quan: `agents/roles/role-mobile.md`, `transactional-outbox-and-cdc.md`.

## 1. Triết Lý Kiến Trúc Offline-First

Trong môi trường di động, kết nối mạng luôn chập chờn. Kiến trúc Offline-First coi CSDL cục bộ là **Nguồn dữ liệu chân lý duy nhất cho UI**:
- **Đọc dữ liệu:** UI luôn đọc trực tiếp từ CSDL cục bộ (SQLite, Room, WatermelonDB, Hive) $\rightarrow$ Giao diện mở tức thì, zero-spinner.
- **Ghi dữ liệu:** Mọi thao tác Create/Update/Delete ghi ngay vào DB cục bộ và cập nhật UI lập tức (Optimistic UI), sau đó ghi nhận vào Hàng đợi đồng bộ (*Mutation Queue*).

```
[UI] <── (Đọc/Ghi tức thì) ──> [Local Database]
                                      │
                                      ▼
                            [Mutation Queue (Outbox)]
                                      │ (Sync ngầm khi có mạng)
                                      ▼
                            [Backend Cloud API]
```

## 2. Hàng Đợi Đồng Bộ Cục Bộ (Local Mutation Queue)

Mọi thay đổi khi offline được lưu vào bảng `outbox_mutations`:
- **Cấu trúc bản ghi:** `id`, `entity_type`, `entity_id`, `mutation_type` (`CREATE`/`UPDATE`/`DELETE`), `payload_json`, `idempotency_key`, `status` (`PENDING`, `SYNCING`, `FAILED`), `retry_count`.
- **Nguyên tắc an toàn:**
  - Client tự sinh `idempotency_key` (UUID v4) cho mỗi thao tác. Khi có mạng, gửi key này lên Backend để chống trùng lặp dữ liệu dù mạng bị ngắt giữa chừng.
  - Quá trình sync áp dụng *Exponential Backoff with Jitter* khi thử lại, tránh dồn request làm sập server.

## 3. Chiến Lược Giải Quyết Xung Đột (Conflict Resolution)

Khi cùng một bản ghi bị sửa ở 2 thiết bị khác nhau trong lúc offline:

| Chiến lược | Cơ chế xử lý | Khi nào áp dụng |
|---|---|---|
| **Server Wins (Khuyến nghị)** | Server là chân lý. Dùng trường `version` (Optimistic Locking). Nếu client version cũ hơn, server từ chối 409 Conflict | Dữ liệu nghiệp vụ tài chính, tồn kho, phân quyền |
| **Field-Level Merge** | Server so khớp từng trường dữ liệu, chỉ cập nhật các trường thực sự thay đổi mà không ghi đè toàn bộ object | Profile người dùng, form nhiều tab độc lập |
| **Client Wins** | Ghi đè toàn bộ dữ liệu server bằng bản ghi mới nhất từ client | Nhật ký cá nhân, ghi chú cá nhân |
| **Manual User Resolution** | Hiển thị màn hình so sánh 2 phiên bản (Local vs Server) để người dùng tự chọn | Tài liệu soạn thảo phức tạp, hợp đồng |

## 4. Kiểm Thử Khả Năng Ngoại Tuyến (Offline Testing Checklist)

- [ ] Tắt kết nối mạng (Airplane mode), thực hiện tạo/sửa dữ liệu $\rightarrow$ UI cập nhật mượt mà không crash.
- [ ] Bật lại mạng $\rightarrow$ Dữ liệu tự động đẩy lên server trong vòng 10 giây.
- [ ] Giả lập mạng chập chờn (Packet loss 50%, latency 5000ms) $\rightarrow$ Không có duplicate records.
