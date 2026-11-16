# Cầu nối User Story -> Tiêu chí chấp nhận (A/C) -> Test Case

> **Loại: tham khảo.**
> Hướng dẫn thiết lập ma trận truy vết và chuyển đổi từ đặc tả sang kiểm thử.
> Liên quan: `danh-gia-user-story.md`, `istqb-test-engineering-playbook.md`, `agents/protocols/test-cases.md`.

## 1. Chuỗi chuyển đổi nghiệp vụ - kiểm thử

```
[Task cha (Epic/WBS)]
       │
       ▼ (Tách theo 4 tiêu chí tại danh-gia-user-story.md)
[User Story (US)]
       │
       ▼ (Bóc tách quy tắc nghiệp vụ BR-xx thành A/C)
[Tiêu chí chấp nhận (AC-01, AC-02...)]
       │
       ▼ (Áp dụng kỹ thuật ISTQB để sinh ca kiểm thử)
[Test Case (HP-00, HP-01, TC-01, TC-02...)]
```

## 2. Quy tắc truy vết hai chiều (Bidirectional Traceability)

1. **Từ nghiệp vụ sang A/C:** Mỗi quy tắc nghiệp vụ (BR-xx) trong User Story phải có ít nhất 1 A/C cụ thể (`AC-xx`). Không bỏ sót quy tắc.
2. **Từ A/C sang Test Case:** Mỗi A/C bắt buộc có ít nhất 1 Test Case (`TC-xx` hoặc Happy Path `HP-xx`).
3. **Truy ngược nguồn gốc:** Mỗi Test Case phải ghi rõ ID của A/C và Story (`Cover: US-xx -> AC-yy`).
4. **Khóa Ma trận RTM (Traceability Matrix):** Chuỗi khóa chuẩn hai chiều:
   `US -> BR-xx -> AC-yy -> TC-zz`
   - Cấm "Test case mồ côi" (orphan test): Test case không gắn với A/C nào.
   - Cấm "A/C bị bỏ sót" (uncovered AC): A/C không có ca kiểm thử tương ứng.

## 3. Bảng ánh xạ 4 tiêu chí sang Kỹ thuật Test

> **[ĐỀ XUẤT] (Chưa kiểm chứng trên dự án thực tế - người dùng duyệt trước khi áp dụng)**

| Tiêu chí | Phân loại | Lát cắt kiểm thử | Kỹ thuật ISTQB khuyến nghị |
|---|---|---|---|
| **Tương tác** | Rõ ràng | UI tĩnh, Form nhập, API schema | Phân vùng tương đương (EP), Giá trị biên (BVA) |
| | Động | Render trạng thái, thêm/xóa node | Chuyển trạng thái (State Transition), DOM assert |
| | Với người | Chờ xác nhận, streaming, timeout | State Transition, Timeout test, Cancellation |
| **Quy tắc** | 1 quy tắc | Kiểm tra đúng/sai đơn lẻ | 1 Happy Path + 1 Negative Test Case |
| | 1 - 3 | Tổ hợp điều kiện giữa các ràng buộc | Bảng quyết định (Decision Table), EP, BVA |
| | > 3 | Luồng phức tạp (nên tách story) | Decision Table thu gọn, Classification Tree |
| **Thực thể** | 1 thực thể | Tính toàn vẹn của 1 bảng/đối tượng | Schema validation, CRUD validation |
| | 1 - 3 | Quan hệ bảng, khóa ngoại, giao dịch | Integration Test, Transaction Rollback, Cascade |
| | > 3 | Luồng nhiều bảng (nên tách story) | Concurrency Test, Deadlock, E2E Workflow |
| **Thao tác** | Tạo | Thêm bản ghi, tạo file, gửi tin | Positive create, Negative trùng khóa/thiếu trường |
| | Cập nhật | Sửa dữ liệu, đổi trạng thái | BVA trường sửa, Optimistic Lock / Concurrency |
| | Đọc, Xóa | Phân trang, lọc, xóa mềm/cứng | Authorization test, Non-existent ID, Boundary Page |

## 4. Định dạng chuẩn liên kết Test Case

- **Test ID:** `TC-[US]-[AC_ID]-[STT]` (Ví dụ: `TC-LOGIN-AC01-01`).
- **Mục tiêu & Căn cứ:** Nêu rõ kiểm tra điều kiện gì của `AC_ID` và kỹ thuật áp dụng (EP, BVA, Decision Table...).
- **Dữ liệu đại diện:** Giá trị đầu vào/kỳ vọng cụ thể, không viết chung chung.
