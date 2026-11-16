# Bản Đồ Định Tuyến Kỹ Thuật Test Theo Lát Cắt Bài Toán

> **Loại: tham khảo.**
> Nguồn: tách từ istqb-test-engineering-playbook.md mục III & IV.
> Hướng dẫn nhận diện cấu trúc bài toán/code để chọn đúng kỹ thuật kiểm thử ISTQB.

## 1. Bản Đồ Định Tuyến Kỹ Thuật Heuristic

| Lát cắt bài toán | Tín hiệu nhận diện trong PRD / Code | Kỹ thuật đặc trị | Mục tiêu kiểm thử cốt tử |
|---|---|---|---|
| **1. Dữ liệu** | Dải số, độ dài chuỗi, ngày tháng, tiền tệ | **EP + BVA 2-point** | Bắt lỗi "Off-by-one", tràn số, ký tự dị |
| **2. Logic** | Nhiều `if-else` lồng nhau, bảng giá, voucher | **Decision Table (DTT)** | Bắt sót nhánh ẩn, mâu thuẫn chính sách |
| **3. Bộ lọc Form** | Màn hình tìm kiếm nhiều dropdown, checkbox | **Pairwise Testing** | Bắt xung đột 2 tham số, chống nổ tổ hợp |
| **4. Trạng thái** | Cột `status` với Enum (`DRAFT`, `SHIPPED`...) | **State Transition (STT)** | Bắt lỗi nhảy cóc lậu, thao tác đơn đã đóng |
| **5. Quyền hạn** | Đa Role (Admin, Telesale, Khách), đa Tenant | **CRUD Matrix + IDOR** | Bắt lỗ hổng leo quyền ngang/dọc, tráo ID |
| **6. Tranh chấp** | Trừ kho Flash Sale, chuyển tiền, trừ số dư | **Concurrency / Race Condition** | Bắt bán âm kho, sai số dư khi đồng thời |
| **7. Giao tiếp ngoài**| Cổng thanh toán, Webhook, API bên thứ 3 | **Idempotency (bắn 3 lần)** | Bắt ghi nhận 2 lần, treo timeout mạng |
| **8. Dữ liệu lớn** | Batch job, import file Excel 100k dòng | **Boundary Volumes + Rollback** | Bắt tràn Heap OOM, dữ liệu đứt gánh |

## 2. Bộ Kích Hoạt Tự Động Từ Mã Nguồn (Agentic Code Triggers)

Khi đọc Task Card hoặc quét file mã nguồn, tự động kích hoạt kỹ thuật tương ứng:

| Tín hiệu trong Mã Nguồn | Lát cắt kích hoạt | Kỹ thuật ISTQB bắt buộc áp dụng |
|---|---|---|
| `@RequestParam`, `@PathVariable`, DTO | Dữ liệu đầu vào | Rút EP + BVA (2-point biên) |
| `BigDecimal`, phép tính `+ - * /`, chuỗi `if` | Logic nghiệp vụ | Rút Bảng Quyết Định (Decision Table) |
| Nhiều Dropdown, Checkbox filter tổ hợp | Bộ lọc tổ hợp | Rút Ma trận trực giao Pairwise |
| Enum status, `changeStatus()`, State pattern | Vòng đời & Trạng thái | Rút STT (0-switch + Cạnh lậu trái phép) |
| `@PreAuthorize`, `SecurityContext`, Role | Quyền hạn & Sở hữu | Rút Ma trận CRUD + IDOR Negative Test |
| `@Transactional`, `@Version`, Pessimistic Lock | Đồng thời & Tranh chấp | Rút Race Condition Multithread Testing |
| `RestTemplate`, `WebClient`, Webhook, API | Giao tiếp bên ngoài | Rút Idempotency (Gửi lặp 3 lần + Timeout) |
| `List<T>` lớn, `MultipartFile`, BatchJob | Dữ liệu lớn & Khối lượng | Rút Boundary Volumes + Rollback Test |
