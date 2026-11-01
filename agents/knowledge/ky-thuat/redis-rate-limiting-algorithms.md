# Chuyên Đề Thuật Toán Rate Limiting Phân Tán Với Redis & Lua Scripts

**Loại: tham khảo.**
> **Phân vùng**: Architecture, API Protection & Distributed Systems  
> **Phân quyền truy cập (RBAC)**: `["architect", "security", "dev"]`  
> **Nguồn đối chuẩn**: Stripe Rate Limiting Architecture, Cloudflare DDoS Protection, Redis Engineering  

---

## 1. So Sánh 4 Thuật Toán Giới Hạn Tốc Độ (Rate Limiting)

| Thuật toán | Cơ chế hoạt động | Ưu điểm | Nhược điểm | Trường hợp sử dụng chuẩn |
|---|---|---|---|---|
| **Fixed Window Counter** | Đếm số request trong 1 khung giờ cố định (vd: 100 req / phút 10:00). | Cực kỳ nhẹ, dễ cài đặt bằng `INCR` và `EXPIRE`. | Bị lỗi Burst gấp đôi ở ranh giới giao giữa 2 cửa sổ. | API nội bộ, tải thấp. |
| **Sliding Window Log** | Lưu timestamp của từng request vào Redis Sorted Set (`ZADD`). | Chính xác $100\%$, chống burst tuyệt đối. | Tốn nhiều bộ nhớ RAM nếu lưu lượng request lớn. | Cổng đăng nhập, xác thực OTP tài khoản. |
| **Sliding Window Counter** | Kết hợp trọng số giữa cửa sổ trước và cửa sổ hiện tại. | Nhẹ gần bằng Fixed Window nhưng mượt mà hơn nhiều. | Tính toán xấp xỉ xác suất (lệch $\sim 5\%$). | API Gateway cho hàng triệu người dùng. |
| **Token Bucket** | Nạp token với tốc độ không đổi $r$, dung lượng bucket tối đa $B$. | Cho phép xử lý một đợt bùng nổ ngắn (Burst) nhưng chặn tải duy trì. | Cần lưu cả timestamp lẫn số lượng token còn lại. | **Chuẩn công nghiệp** (AWS, Stripe, Cloudflare). |

---

## 2. Mã Nguồn Mẫu Chuẩn: Token Bucket Bằng Redis Lua Script (Atomic)
- **Vấn đề cần giải quyết**: Trong môi trường phân tán (Cluster nhiều Web Server), việc đọc token từ Redis, tính toán thời gian trôi qua rồi ghi ngược lại sẽ gây ra **Race Condition** nếu không thực hiện nguyên tử.
- **Giải pháp**: Đóng gói toàn bộ logic vào **Redis Lua Script** (được Redis thực thi đơn luồng nguyên tử, độ trễ $< 1\text{ms}$):

```lua
-- File: rate_limiter_token_bucket.lua
-- KEYS[1]: Khóa rate limit (vd: "rate:limiter:user:1001")
-- ARGV[1]: Dung lượng tối đa của Bucket (Capacity B)
-- ARGV[2]: Tốc độ nạp token trên mỗi giây (Refill Rate r)
-- ARGV[3]: Timestamp thời điểm hiện tại tính bằng giây (Now)
-- ARGV[4]: Số lượng token cần tiêu thụ (Requested tokens, thường là 1)

local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])
local requested = tonumber(ARGV[4])

-- Lấy dữ liệu hiện tại từ Hash
local data = redis.call('HMGET', key, 'tokens', 'last_updated')
local current_tokens = tonumber(data[1])
local last_updated = tonumber(data[2])

if current_tokens == nil then
    -- Lần đầu tiên truy cập, khởi tạo bucket đầy
    current_tokens = capacity
    last_updated = now
else
    -- Tính toán số token được nạp thêm trong khoảng thời gian trôi qua
    local elapsed = math.max(0, now - last_updated)
    current_tokens = math.min(capacity, current_tokens + elapsed * rate)
    last_updated = now
end

if current_tokens >= requested then
    -- Đủ token: Trừ token và chấp thuận
    current_tokens = current_tokens - requested
    redis.call('HMSET', key, 'tokens', current_tokens, 'last_updated', last_updated)
    -- Đặt thời gian sống (TTL) vừa đủ để dọn rác bộ nhớ khi không còn request
    local ttl = math.ceil((capacity - current_tokens) / rate) + 60
    redis.call('EXPIRE', key, ttl)
    return {1, math.floor(current_tokens)} -- 1 = Allowed, Số token còn lại
else
    -- Không đủ token: Từ chối với mã 429
    redis.call('HMSET', key, 'tokens', current_tokens, 'last_updated', last_updated)
    return {0, math.floor(current_tokens)} -- 0 = Denied
end
```

---

## 3. Tích Hợp Vào Spring Boot Filter / Interceptor

```java
@Component
public class DistributedRateLimitFilter extends OncePerRequestFilter {

    private final RedisTemplate<String, String> redisTemplate;
    private final RedisScript<List> tokenBucketScript;

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {
        String clientIp = resolveClientIp(request);
        String redisKey = "ratelimit:ip:" + clientIp;
        long now = System.currentTimeMillis() / 1000;

        // Cấu hình: Bucket chứa tối đa 20 token, nạp 5 token/giây
        List<Object> result = redisTemplate.execute(
            tokenBucketScript,
            Collections.singletonList(redisKey),
            "20", "5", String.valueOf(now), "1"
        );

        Long allowed = (Long) result.get(0);
        Long remainingTokens = (Long) result.get(1);

        response.setHeader("X-RateLimit-Remaining", String.valueOf(remainingTokens));

        if (allowed == 1) {
            filterChain.doFilter(request, response);
        } else {
            response.setStatus(429); // HTTP 429 Too Many Requests
            response.setContentType("application/json");
            response.getWriter().write("{\"error\": \"Rate limit exceeded. Please retry later.\"}");
        }
    }
}
```

