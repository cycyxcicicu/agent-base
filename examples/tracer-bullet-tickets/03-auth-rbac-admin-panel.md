---
id: "TB-03"
title: "Bảng Quản trị Phân quyền RBAC và Nhật ký Audit"
status: "blocked"
blocked_by: ["TB-02"]
vertical_slice:
  schema: "Cột role trong users và bảng audit_logs ghi nhận hành động phân quyền"
  api: "Endpoint GET /api/admin/users và POST /api/admin/roles có guard requireRole('admin')"
  ui: "Giao diện Admin Table cho phép gán role kèm cảnh báo xác nhận modal"
  test: "Integration test: user thường gọi endpoint admin bị 403 Forbidden; admin gọi thành công"
---

# TB-03: Bảng Quản trị Phân quyền RBAC và Nhật ký Audit

**What to build (Từ góc nhìn End-to-End):**
Quản trị viên (admin) đăng nhập vào hệ thống, mở tab Quản trị `/admin`, xem danh sách thành viên, thay đổi vai trò (User -> Manager -> Admin), và mỗi thao tác cập nhật đều tự động lưu vết vào bảng `audit_logs`. Người dùng không có vai trò admin bị chặn với mã lỗi HTTP 403 Forbidden.

**Blocked by:**
TB-02: Bảo vệ Dashboard và Điều hướng Session.

**Acceptance Criteria:**
- [ ] Schema: Bảng `audit_logs` ghi nhận `actor_id`, `target_id`, `action`, `timestamp`.
- [ ] API: Endpoint `/api/admin/*` trả về 403 Forbidden đối với người dùng không có role admin.
- [ ] UI: Bảng quản trị danh sách người dùng với dropdown chọn quyền và nút lưu thay đổi.
- [ ] Test: Unit test xác minh middleware `requireRole('admin')` từ chối người dùng role 'member'.
