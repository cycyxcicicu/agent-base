# Cẩm Nang SecOps, Bảo Mật Thanh Toán Fintech & Phòng Thủ API

**Loại: tham khảo.**
> **Phân vùng**: Security, FinTech & API Protection  
> **Phân quyền truy cập (RBAC)**: `["security", "architect", "dev", "dba"]`  
> **Nguồn đối chuẩn**: PCI-DSS v4.0 Standard, Stripe Engineering, Cloudflare Security, OWASP API Security Top 10  

---

## 1. Chuẩn PCI-DSS v4.0 & Kỹ Thuật Tokenization / PAN Vaulting
- **Nguyên tắc cốt lõi (CDE Isolation)**:
  - Vùng dữ liệu chủ thẻ (Cardholder Data Environment - CDE) phải được cô lập vật lý hoặc mạng logic (VPC Peering/Firewall) với hệ thống ứng dụng chung.
  - Tuyệt đối không bao giờ ghi số thẻ đầy đủ (PAN - Primary Account Number) hay mã CVV/CVC vào cơ sở dữ liệu ứng dụng, file log, cache Redis hay biến môi trường.
- **Kỹ thuật Tokenization (PAN Vaulting)**:
  - Khi khách hàng nhập thông tin thẻ, SDK phía Client (như Stripe Elements) gửi trực tiếp về Token Vault an toàn độc lập.
  - Token Vault mã hóa thẻ bằng thuật toán đối xứng **AES-256-GCM** (khóa KMS được luân chuyển 90 ngày một lần), lưu trữ trong DB mã hóa độc lập.
  - Trả về cho backend ứng dụng một chuỗi `token_id` vô nghĩa (`tok_1Nxxxx`). Backend chỉ lưu `token_id`, 4 số cuối thẻ (`last4`) và thương hiệu thẻ (`brand`) để hiển thị UI.

```
[Khách Hàng] --- (Dữ liệu thẻ đầy đủ) ---> [Token Vault KMS AES-256]
     |                                             |
 (Gửi Token ID)                              (Sinh Token ID ngẫu nhiên)
     v                                             |
[Backend App] <------- (Nhận token_id) ------------+
  (Chỉ lưu token_id + last4, không dính phạm vi PCI-DSS)
```

---

## 2. Thuật Toán Token Bucket Rate Limiting qua Redis Lua Script
- **Vấn đề**: Các thuật toán Fixed Window dễ bị tấn công burst traffic ở biên chuyển giao chu kỳ (gấp đôi tải).
- **Nguyên lý Token Bucket**:
  - Bucket có dung lượng tối đa $B$. Mỗi giây nạp vào $r$ tokens.
  - Mỗi request đến cần lấy 1 token. Nếu bucket rỗng, từ chối với HTTP 429 Too Many Requests.
  - Tránh Race Condition phân tán: Bắt buộc dùng **Redis Lua Script** để tính toán thời gian trôi qua và cấp token một cách nguyên tử (atomic):

```lua
-- KEYS[1]: Khóa rate limit (vd: ratelimit:ip:192.168.1.1)
-- ARGV[1]: Dung lượng tối đa (Bucket capacity)
-- ARGV[2]: Tốc độ nạp (Tokens per millisecond)
-- ARGV[3]: Thời điểm hiện tại (Current timestamp in ms)
-- ARGV[4]: Số token cần lấy (Mặc định 1)

local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])
local requested = tonumber(ARGV[4])

local data = redis.call('HMGET', key, 'tokens', 'last_updated')
local tokens = tonumber(data[1])
local last_updated = tonumber(data[2])

if tokens == nil then
    tokens = capacity
    last_updated = now
else
    local delta = math.max(0, now - last_updated)
    tokens = math.min(capacity, tokens + delta * rate)
    last_updated = now
end

if tokens >= requested then
    tokens = tokens - requested
    redis.call('HMSET', key, 'tokens', tokens, 'last_updated', last_updated)
    redis.call('PEXPIRE', key, math.ceil((capacity - tokens) / rate))
    return 1 -- Chấp thuận request
else
    redis.call('HMSET', key, 'tokens', tokens, 'last_updated', last_updated)
    return 0 -- Từ chối request (HTTP 429)
end
```

---

## 3. Thu Hồi Token OAuth2/OIDC Tức Thì Bằng Redis Bloom Filter
- **Nghịch lý JWT Stateless**: JWT giảm tải cho DB do không cần tra cứu session mỗi request, nhưng khi người dùng bấm "Đăng xuất" hoặc đổi mật khẩu, JWT vẫn có hiệu lực cho đến khi hết hạn (TTL).
- **Giải pháp Redis Bloom Filter**:
  - Khi người dùng đăng xuất, đưa `jti` (JWT ID) hoặc `token_signature` vào **Redis Bloom Filter** với TTL bằng thời gian sống còn lại của token.
  - Ưu điểm:
    - **Tốc độ O(k)**: Kiểm tra siêu tốc với $k$ hàm băm, độ trễ $< 1\text{ms}$.
    - **Tiết kiệm RAM vượt trội**: 10 triệu token bị thu hồi chỉ tốn ~12MB RAM (thay vì hàng trăm MB nếu lưu chuỗi string nguyên bản).
    - **Xác suất dương tính giả (False Positive)**: Cấu hình tỷ lệ lỗi $< 0.1\%$. Nếu Bloom Filter báo "có thể đã thu hồi", thực hiện tra cứu fallback thứ cấp vào tập Set nhỏ để quyết định cuối cùng.

---

## 4. Phòng Thủ OWASP API Security Top 10 Trong Thực Chiến
1. **BOLA (Broken Object Level Authorization - API1)**:
   - *Lỗ hổng*: Client gửi `GET /api/orders/1002`, backend chỉ kiểm tra user đã login chưa mà quên kiểm tra `order.user_id == current_user.id`.
   - *Khắc phục*: Mọi truy vấn DB phải đính kèm tenant/user scope: `SELECT * FROM orders WHERE id = :id AND user_id = :currentUser`.
2. **BOPLA (Broken Object Property Level Authorization - API3)**:
   - *Lỗ hổng*: Mass assignment cho phép client gửi payload JSON `{"role": "ADMIN", "is_verified": true}` khi đăng ký tài khoản.
   - *Khắc phục*: Dùng DTOs riêng biệt (Data Transfer Object) với validate chặt chẽ (`@NotNull`, `@Pattern`), cấm ánh xạ trực tiếp Request Body vào Entity DB.
3. **SSRF (Server-Side Request Forgery - API7)**:
   - *Lỗ hổng*: Tính năng webhook gửi HTTP POST tới URL do người dùng cung cấp, bị lợi dụng gọi vào metadata cloud nội bộ (`http://169.254.169.254/`).
   - *Khắc phục*: Chặn toàn bộ dải IP riêng tư (RFC 1918: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.1`) trước khi tạo kết nối mạng.

