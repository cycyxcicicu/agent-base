# Thư Mục Quản Lý Cookies & Xoay Vòng Tài Khoản (Cookie Rotation)

Thư mục này dùng để lưu trữ cookies cấu hình cho hệ thống Gemini Deep Research và Multi-Account Rotation.

## 1. Các hình thức cấu hình
Hệ thống `tools/cookie_rotation/account_manager.py` tự động nhận diện tài khoản theo 2 cách (tự động ưu tiên):
1. **File `cookies/all_accounts.json`**: Danh sách JSON các tài khoản.
2. **File `.env`**: Các biến môi trường `GEMINI_SECURE_1PSID`, `GEMINI_SECURE_1PSIDTS`, `GEMINI_SECURE_1PSID_2`,...

## 2. Cơ chế xoay vòng khi hết hạn (Auto-Rotation & Refresh)
1. **Lỗi 1016 / Token Hết Hạn (`__Secure-1PSIDTS` expired)**:
   - Hệ thống tự động gọi Google RPC (`RotateCookiesPage`) thông qua `curl_cffi` mô phỏng Chrome 124.
   - Lấy token `__Secure-1PSIDTS` mới mà KHÔNG cần người dùng đăng nhập lại.
   - Tự động lưu đè token mới vào `.env` và `account_X.json`.
2. **Lỗi 429 / Quota Resource Exhausted (Chạm hạn ngạch)**:
   - Hệ thống đưa tài khoản vào trạng thái cooldown 300 giây.
   - Tự động chuyển đổi (failover) sang tài khoản tiếp theo trong pool theo thuật toán Round-Robin.
   - Khi hết 300s, tài khoản tự động được mở lại và tham gia vòng xoay.

## 3. Các lệnh điều khiển nhanh
```bash
# Kiểm tra danh sách tài khoản trong pool
python tools/cookie_rotation/account_manager.py --status

# Làm mới token thủ công cho toàn bộ tài khoản
python tools/cookie_rotation/account_manager.py --sync

# Chạy test kiểm tra kết nối tới tất cả tài khoản
python tools/cookie_rotation/account_manager.py --test

# Chạy unit tests xác thực toàn bộ logic xoay vòng
python tests/test_cookie_rotation.py
```
