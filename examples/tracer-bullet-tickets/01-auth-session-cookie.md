---
id: "TB-01"
title: "Xác thực Session Cookie End-to-End"
status: "done"
blocked_by: []
vertical_slice:
  schema: "Thêm bảng sessions liên kết với users"
  api: "Endpoint POST /api/auth/login set HttpOnly cookie"
  ui: "Form đăng nhập với client-side validation"
  test: "Integration test kiểm tra Set-Cookie header"
---

# TB-01: Xác thực Session Cookie End-to-End

**What to build (Từ góc nhìn End-to-End):**
Người dùng nhập email/mật khẩu tại form đăng nhập, hệ thống xác thực thông tin, cấp phát session ID ngẫu nhiên lưu vào database và trả về `HttpOnly, Secure, SameSite=Strict` cookie trên trình duyệt.

**Blocked by:**
None (Can start immediately).

**Acceptance Criteria:**
- [x] Schema: Bảng `sessions` có `id`, `user_id`, `expires_at`, `created_at`.
- [x] API: `POST /api/auth/login` trả về HTTP 200 kèm header `Set-Cookie: session_token=...; HttpOnly; Path=/; SameSite=Strict`.
- [x] UI: Form đăng nhập hiển thị lỗi inline khi nhập sai mật khẩu; redirect sang trang đích khi đăng nhập thành công.
- [x] Test: Test tự động giả lập gửi request đăng nhập đúng trả về cookie hợp lệ; gửi sai mật khẩu trả về HTTP 401 không kèm cookie.
