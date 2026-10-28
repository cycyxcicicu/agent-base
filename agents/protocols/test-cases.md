> Task: T-15 · Epic: E2 · Vai: architect

# Tiêu chuẩn thiết kế kịch bản kiểm thử (Test Cases Design Protocol)

Giao thức này quy định phương pháp thiết kế kịch bản kiểm thử có kỷ luật, đảm bảo mọi ca kiểm thử được thiết kế và phê duyệt **trước khi viết mã nguồn**.

---

## 1. Các nguyên tắc cốt lõi

1. **Test-First (Viết kịch bản trước khi code)**: Kịch bản kiểm thử phải được lập ngay từ Bước 3 của vòng đời task; cấm nhảy vào code khi chưa có kịch bản test.
2. **Luồng thiết kế tuần tự**: Bắt đầu từ **Happy Path** (luồng thuận lợi cơ bản nhất) → **Happy Cases** (các luồng thuận chi tiết có dữ liệu hợp lệ) → **Biên & Ngoại lệ** (Negative / Edge Cases).
3. **Áp dụng 4 kỹ thuật thiết kế ISTQB**:
   - *Phân vùng tương đương (Equivalence Partitioning - EP)*: Gom nhóm dữ liệu hợp lệ và không hợp lệ.
   - *Phân tích giá trị biên (Boundary Value Analysis - BVA)*: Kiểm tra các điểm giá trị tại ngưỡng (min, min-1, max, max+1).
   - *Bảng quyết định (Decision Table)*: Kiểm tra tổ hợp nhiều điều kiện logic phức tạp.
   - *Chuyển đổi trạng thái (State Transition)*: Kiểm tra tính đúng đắn của máy trạng thái qua các sự kiện.
4. **Mỗi bước một hành động cụ thể**: Mỗi bước kiểm thử phải gồm hành động đo lường được và kết quả quan sát được (Observable Result), không viết mơ hồ ("nhập dữ liệu và kiểm tra").
5. **Duyệt kịch bản bằng file trước khi code**: Danh sách test cases phải được con người phê duyệt bằng dấu trong file trước khi Dev tiến hành lập trình.
6. **Cấm AI tự ghi "Passed"**: Kết quả chỉ được đánh dấu Passed khi có bằng chứng chạy thật (Exit code 0, log output kiểm thử tự động, hoặc trace CDP).
7. **Phân định thẩm quyền Dev vs QA**: Khi sửa lỗi, **Dev chỉ được đổi trạng thái sang `Resolved`**; **CHỈ QA HOẶC CON NGƯỜI MỚI CÓ QUYỀN ĐÓNG (`Closed`)** sau khi tái kiểm chứng đạt.

---

## 2. Mẫu bảng kịch bản kiểm thử chuẩn

```markdown
| Mã Case | Phân loại | Kỹ thuật ISTQB | Tiền điều kiện | Các bước thực hiện | Kết quả mong đợi quan sát được | Kết quả thực tế | Trạng thái |
|---|---|---|---|---|---|---|---|
| TC-01 | Happy Path | Phân vùng tương đương | Người dùng đã đăng ký tài khoản | 1. Nhập username hợp lệ<br/>2. Nhập password đúng<br/>3. Bấm Đăng nhập | Chuyển hướng tới Dashboard, hiển thị thông báo "Chào mừng" | [Output / Hash] | Draft / Passed / Failed |
```

---

## 3. Ví dụ minh họa trung lập: Tính năng Đăng nhập người dùng

| Mã Case | Phân loại | Kỹ thuật ISTQB | Tiền điều kiện | Các bước thực hiện | Kết quả mong đợi quan sát được | Trạng thái duyệt |
|---|---|---|---|---|---|---|
| **TC-AUTH-01** | Happy Path | Phân vùng tương đương | Tài khoản `user_test` đang hoạt động, mật khẩu `Pass@123` | 1. Truy cập `/login`<br/>2. Nhập username `user_test`<br/>3. Nhập mật khẩu `Pass@123`<br/>4. Bấm "Đăng nhập" | Trả về mã trạng thái HTTP 200, cấp JWT cookie `auth_token`, chuyển hướng về `/dashboard`. | Draft (Chờ người duyệt) |
| **TC-AUTH-02** | Happy Case | Phân vùng tương đương | Tài khoản `user_test` có bật ghi nhớ phiên | 1. Nhập thông tin đúng<br/>2. Tích chọn "Ghi nhớ đăng nhập 30 ngày"<br/>3. Bấm "Đăng nhập" | Cookie `auth_token` có thuộc tính `Max-Age = 2592000` (30 ngày). | Draft (Chờ người duyệt) |
| **TC-AUTH-03** | Ngoại lệ | Phân vùng tương đương | Tài khoản `user_test` tồn tại | 1. Nhập username `user_test`<br/>2. Nhập sai mật khẩu `WrongPass`<br/>3. Bấm "Đăng nhập" | HTTP 401 Unauthorized, hiển thị thông báo lỗi "Tên đăng nhập hoặc mật khẩu không đúng". Không lộ username có tồn tại hay không. | Draft (Chờ người duyệt) |
| **TC-AUTH-04** | Biên | Phân tích giá trị biên (BVA) | Tài khoản `user_test` tồn tại | 1. Nhập sai mật khẩu liên tiếp 5 lần | Tại lần thứ 5, tài khoản bị tạm khóa 15 phút, trả về HTTP 429 Too Many Requests, hiển thị thời gian mở khóa. | Draft (Chờ người duyệt) |
| **TC-AUTH-05** | Biên | Phân tích giá trị biên (BVA) | Tài khoản `user_test` đang bị tạm khóa | 1. Thử đăng nhập lại tại phút thứ 14 | Hệ thống từ chối ngay, không kiểm tra mật khẩu, giữ nguyên thời gian khóa còn lại. | Draft (Chờ người duyệt) |
| **TC-AUTH-06** | Ngoại lệ | Bảng quyết định | Tài khoản bị vô hiệu hóa bởi Admin | 1. Nhập username và password đúng của tài khoản bị khóa | HTTP 403 Forbidden, thông báo "Tài khoản đã bị ngừng kích hoạt, vui lòng liên hệ hỗ trợ". | Draft (Chờ người duyệt) |
