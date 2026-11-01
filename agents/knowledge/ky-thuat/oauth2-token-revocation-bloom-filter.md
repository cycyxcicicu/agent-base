# Chuyên Đề Thu Hồi Token OAuth2/OIDC & JWT Blacklisting Bằng Redis Bloom Filter

**Loại: tham khảo.**
> **Phân vùng**: Security, IAM & High-Throughput Token Management  
> **Phân quyền truy cập (RBAC)**: `["security", "architect", "dev"]`  
> **Nguồn đối chuẩn**: OWASP Token Revocation Guidelines, RedisBloom Documentation, Auth0 Identity Architecture  

---

## 1. Vấn Đề Lớn Của JWT: Stateless vs Tức Thì Thu Hồi (Instant Revocation)
- **Nghịch lý JWT Stateless**:
  - Ưu điểm lớn nhất của JWT là máy chủ không cần tra cứu DB/Redis ở mỗi request. Microservices chỉ cần giải mã public key (RSA/ECDSA) để xác thực.
  - Tuy nhiên, khi xảy ra sự kiện bảo mật (Người dùng bấm **Đăng xuất**, **Đổi mật khẩu**, hoặc tài khoản bị **Khóa do nghi ngờ hack**), token đã phát hành vẫn hoàn toàn hợp lệ cho đến khi hết hạn (TTL, vd: 15–60 phút).
- **Hạn chế của giải pháp lưu Blacklist thông thường**:
  - Nếu lưu từng chuỗi `jti` (JWT ID - 36 ký tự UUID) vào Redis Set/Key thông thường, hệ thống quy mô 10 triệu người dùng đăng xuất sẽ ngốn hàng Gigabyte RAM và làm chậm quá trình tra cứu.

---

## 2. Giải Pháp Tối Ưu: Redis Bloom Filter (O(k) & Siêu Tiết Kiệm RAM)
- **Nguyên lý cấu trúc dữ liệu Bloom Filter**:
  - Là mảng bit (Bit Array) kích thước $m$ bit, kết hợp với $k$ hàm băm độc lập (Hash Functions).
  - Khi thu hồi một token `jti`: Băm chuỗi qua $k$ hàm băm, bật các bit tại các vị trí tương ứng lên `1`.
  - Khi kiểm tra một request: Băm `jti` qua $k$ hàm băm.
    - Nếu có **bất kỳ bit nào bằng 0**: Chắc chắn $100\%$ token này **CHƯA BỊ THU HỒI** (Không bao giờ có False Negative). Request được đi tiếp ngay lập tức!
    - Nếu **toàn bộ các bit đều bằng 1**: Token có thể đã bị thu hồi (với tỷ lệ dương tính giả được cấu hình cực nhỏ, vd: $0.1\%$). Khi đó mới cần tra cứu xác nhận lần 2.

### Bảng So Sánh Bộ Nhớ RAM (10 Triệu Token Bị Thu Hồi)
| Cấu trúc dữ liệu | Bộ nhớ tiêu tốn | Thời gian truy vấn |
|---|---|---|
| **Redis String Keys** (`SET token:<jti> 1`) | $\sim 850\text{ MB}$ | $O(1)$ |
| **Redis Set** (`SADD blacklisted_tokens <jti>`) | $\sim 520\text{ MB}$ | $O(1)$ |
| **Redis Bloom Filter** (`BF.ADD blacklist <jti>`) | **$\sim 14.3\text{ MB}$ (Tiết kiệm >98%)** | **$O(k)$ cố định (<0.5ms)** |

---

## 3. Mã Nguồn Mẫu Triển Khai (Python / Redis-py)

```python
import redis

# Kết nối Redis hỗ trợ RedisBloom module
r = redis.Redis(host='localhost', port=6379, db=0)

BLOOM_FILTER_KEY = "auth:jwt_blacklist"

def initialize_blacklist_filter():
    """Khởi tạo Bloom Filter với dung lượng dự kiến 5.000.000 token, tỷ lệ lỗi 0.1%"""
    try:
        r.execute_command("BF.RESERVE", BLOOM_FILTER_KEY, 0.001, 5000000)
    except redis.exceptions.ResponseError as e:
        if "item exists" not in str(e).lower():
            raise e

def revoke_token(jti: str, ttl_seconds: int):
    """
    Thu hồi token khi người dùng đăng xuất hoặc đổi mật khẩu.
    Đưa jti vào Bloom Filter và lưu vào secondary set nhỏ để xử lý False Positive.
    """
    r.execute_command("BF.ADD", BLOOM_FILTER_KEY, jti)
    # Lưu phụ trợ có TTL tự hết hạn theo thời gian sống còn lại của JWT
    r.setex(f"blacklist:exact:{jti}", ttl_seconds, "1")

def is_token_revoked(jti: str) -> bool:
    """
    Kiểm tra nhanh xem token có bị thu hồi hay không.
    99.9% request sạch sẽ kết thúc ngay ở tầng Bloom Filter mà không tốn I/O.
    """
    exists_in_bloom = r.execute_command("BF.EXISTS", BLOOM_FILTER_KEY, jti)
    if exists_in_bloom == 0:
        return False  # Chắc chắn 100% hợp lệ!
    
    # 0.1% rơi vào trường hợp nghi ngờ: Tra cứu chính xác để loại trừ False Positive
    return r.exists(f"blacklist:exact:{jti}") == 1
```

---

## 4. Cơ Chế Xoay Vòng Filter Tránh Đầy Bộ Nhớ (Bloom Filter Rotation)
Vì Bloom Filter không thể xóa từng phần tử (`BF.DEL`), khi đạt đến ngưỡng giới hạn:
1. Duy trì 2 bộ lọc luân phiên: `Filter_Current` (đang ghi) và `Filter_Previous` (đọc dự phòng).
2. Khi chu kỳ TTL của JWT tối đa kết thúc (vd: sau 24h), xóa toàn bộ `Filter_Previous`, biến `Filter_Current` thành `Previous` và tạo mới `Current`.

