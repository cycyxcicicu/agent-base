---
id: "TB-02"
title: "Bảo vệ Dashboard và Điều hướng Session"
status: "ready-for-agent"
blocked_by: ["TB-01"]
vertical_slice:
  schema: "Truy vấn bảng sessions để xác minh TTL và hiệu lực"
  api: "Middleware authGuard kiểm tra cookie trên mọi request dashboard"
  ui: "Trang Dashboard hiển thị thông tin người dùng và nút Đăng xuất"
  test: "E2E test kiểm tra redirect khi chưa đăng nhập và truy cập thành công khi có cookie"
---

# TB-02: Bảo vệ Dashboard và Điều hướng Session

**What to build (Từ góc nhìn End-to-End):**
Khi người dùng đã đăng nhập truy cập `/dashboard`, middleware đọc cookie session, truy vấn xác minh TTL hợp lệ và cho phép render trang Dashboard cá nhân hóa. Nếu cookie thiếu hoặc hết hạn, redirect ngay lập tức về `/login?redirect=/dashboard`.

**Blocked by:**
TB-01: Xác thực Session Cookie End-to-End.

**Acceptance Criteria:**
- [ ] Middleware: Chặn mọi request vào `/dashboard` nếu cookie `session_token` vắng mặt hoặc đã quá hạn trong bảng `sessions`.
- [ ] UI: Trang Dashboard hiển thị lời chào "Xin chào, {user.name}" và nút "Đăng xuất" kích hoạt lệnh xóa session.
- [ ] Test: Request không kèm cookie trả về redirect HTTP 302 về `/login`.
- [ ] Test: Request kèm cookie hợp lệ trả về HTTP 200 kèm HTML dashboard.
