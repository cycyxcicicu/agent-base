# Khung Kiểm Toán An Ninh 4 Chiều (CSO Framework) & Lệnh Nguy Hiểm (/careful)

> **Tài liệu chuẩn kỹ thuật dành cho Security Officer, Reviewer và DevOps**  
> **Nguồn tri thức:** Trích xuất và chuẩn hóa từ `garrytan/gstack` (`/cso` & `/careful`)

---

## 1. Khung Kiểm Toán An Ninh 4 Chiều (CSO 4-Scope Audit)

Mọi cuộc kiểm toán an ninh trong `agent-base` được phân tách độc lập thành 4 trục để không bỏ sót bất kỳ mắt xích yếu nào:

### Trục 1: Kiểm toán Mã Nguồn (`--code`)
- **Lỗ hổng tiêm mã (Injection)**: SQL Injection, Command Injection, Template Injection. Kiểm tra mọi câu truy vấn xem có dùng Parameterized Queries / ORM an toàn hay không.
- **Xác thực & Phân quyền (Auth & IDOR)**: Kiểm tra Insecure Direct Object References (IDOR). Bất kỳ endpoint nào nhận `id` của bản ghi đều phải xác minh quyền sở hữu của người dùng hiện tại đối với `id` đó.
- **Bảo vệ dữ liệu nhạy cảm**: Kiểm tra không ghi mật khẩu, token, API key vào log hoặc trả về trong response payload.
- **SSRF (Server-Side Request Forgery)**: Khi ứng dụng fetch URL do người dùng cung cấp (ví dụ: webhook, crawler, preview link), bắt buộc phải chặn dải IP nội bộ (`127.0.0.1`, `10.0.0.0/8`, `192.168.0.0/16`, `169.254.169.254`).

### Trục 2: Kiểm toán Hạ Tầng & Cấu Hình (`--infra`)
- **Cổng dịch vụ & Tường lửa**: Cơ sở dữ liệu (Postgres 5432, Redis 6379, MySQL 3306) tuyệt đối không được mở public ra Internet (0.0.0.0). Chỉ lắng nghe trên `localhost` hoặc mạng nội bộ Docker.
- **Quyền hạn container**: Dockerfile không được chạy dưới quyền `root`. Bắt buộc khai báo user không đặc quyền (`USER appuser`).
- **Tệp môi trường**: File `.env`, `.env.local` bắt buộc phải nằm trong `.gitignore`. Không bao giờ commit secret lên git.

### Trục 3: Kiểm toán Chuỗi Cung Ứng Thư Viện (`--supply-chain`)
- **Quét CVE trong lockfile**: Định kỳ kiểm tra `package-lock.json`, `pnpm-lock.yaml`, `poetry.lock`, `requirements.txt`.
- **Ghim phiên bản (Pinning Versions)**: Luôn ghim chính xác phiên bản thư viện để tránh rủi ro Dependency Confusion hoặc tác giả bên thứ ba cập nhật bản có mã độc.

### Trục 4: Kiểm toán Kỹ Năng & Plugin Ngoại Lai (`--skills`)
- **Soi mã độc trong Prompt & Script**: Kiểm tra các file `SKILL.md` tải về từ bên ngoài. Tuyệt đối không để lọt các đoạn text ẩn (HTML comment mờ ám), URL lạ, hoặc lệnh tải script ngầm (`curl | bash`).

---

## 2. Bảng Tra Cứu Lệnh Nguy Hiểm & Ngoại Lệ An Toàn (/careful)

Áp dụng trong hệ thống phân quyền của `agent-base` (thông qua `bash_ask` và `bash_deny`):

| Lệnh / Mẫu nguy hiểm | Mức độ rủi ro | Trạng thái xử lý | Giải thích |
|---|:---:|:---:|---|
| `rm -rf /` hoặc `rm -rf *` | Cực kỳ nguy hiểm | **CẤM HOÀN TOÀN (`bash_deny`)** | Xóa sạch dữ liệu hệ thống |
| `git push --force` / `git push -f` | Nguy hiểm | **CẤM HOÀN TOÀN (`bash_deny`)** | Viết đè lịch sử Git của nhóm |
| `git reset --hard` | Nguy hiểm | **CẤM HOÀN TOÀN (`bash_deny`)** | Làm mất toàn bộ thay đổi chưa commit |
| `git checkout .` / `git restore .` | Nguy hiểm | **HỎI XÁC NHẬN (`bash_ask`)** | Hủy bỏ công sức code chưa lưu |
| `DROP TABLE` / `DROP DATABASE` | Nguy hiểm | **HỎI XÁC NHẬN (`bash_ask`)** | Mất cấu trúc và dữ liệu DB |
| `TRUNCATE` | Nguy hiểm | **HỎI XÁC NHẬN (`bash_ask`)** | Xóa sạch bảng dữ liệu |
| `kubectl delete namespace/pod` | Nguy hiểm | **HỎI XÁC NHẬN (`bash_ask`)** | Làm gián đoạn dịch vụ production |
| `docker system prune -a` | Nguy hiểm | **HỎI XÁC NHẬN (`bash_ask`)** | Xóa sạch toàn bộ container và image |

### Các Ngoại Lệ An Toàn Được Phép Chạy Ngay:
Các thư mục build/cache sau đây được phép dọn dẹp mà không cần cảnh báo:
- `rm -rf node_modules`
- `rm -rf dist`, `rm -rf build`, `rm -rf out`
- `rm -rf __pycache__`, `rm -rf .pytest_cache`
- `rm -rf .turbo`, `rm -rf .cache`, `rm -rf coverage`
