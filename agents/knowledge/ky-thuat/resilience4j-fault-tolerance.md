# Chuyên Đề Khả Năng Chống Chịu Lỗi: Circuit Breaker (Resilience4j), Bulkhead & Retry Jitter

**Loại: tham khảo.**
> **Phân vùng**: High Availability, Microservices Architecture & Fault Tolerance  
> **Phân quyền truy cập (RBAC)**: `["architect", "dev", "sre", "devops"]`  
> **Nguồn đối chuẩn**: Resilience4j Official Guide, Netflix Hystrix Post-Mortem, AWS Architecture Center (Exponential Backoff and Jitter)  

---

## 1. Mẫu Thiết Kế Circuit Breaker (Bộ Ngắt Mạch)
- **Vấn đề sập đổ dây chuyền (Cascading Failure)**:
  - Khi một dịch vụ phụ thuộc (vd: Cổng thanh toán bên thứ ba) bị nghẽn mạng hoặc chết, các request gọi đến service đó sẽ bị block thread chờ timeout (vd: 30s).
  - Hàng trăm thread bị khóa làm cạn kiệt Connection Pool của ứng dụng chính, dẫn đến việc toàn bộ hệ thống bị treo cứng dù bản thân ứng dụng không có lỗi.
- **Máy trạng thái Circuit Breaker**:
  1. **CLOSED (Bình thường)**: Mọi request đi qua. Nếu tỷ lệ lỗi vượt ngưỡng (vd: $> 50\%$ trong 100 cuộc gọi gần nhất), mạch nhảy sang **OPEN**.
  2. **OPEN (Ngắt mạch)**: Mọi request gọi đến bị **chặn tức thì (Fail-Fast $0\text{ms}$)**, không gọi sang dịch vụ lỗi, chuyển thẳng sang hàm dự phòng (`fallback`). Giúp dịch vụ lỗi có thời gian tự hồi phục.
  3. **HALF-OPEN (Thử nghiệm)**: Sau thời gian chờ (vd: 10s), cho phép một số lượng nhỏ request (vd: 10 request) đi qua để thăm dò. Nếu thành công, mạch đóng lại (**CLOSED**); nếu vẫn lỗi, mạch tiếp tục mở (**OPEN**).

```
   +------------- (Tỷ lệ lỗi > 50%) ------------+
   │                                            ▼
[CLOSED]                                     [OPEN]
   ▲                                            │
   │                                            │ (Hết thời gian chờ, vd: 10s)
   │                                            ▼
   +------- (Thử nghiệm thành công) ------- [HALF-OPEN]
                                                │
                                                │ (Thử nghiệm vẫn lỗi)
                                                +---> Quay lại [OPEN]
```

---

## 2. Kỹ Thuật Bulkhead: Phân Vùng Cách Ly Tài Nguyên
- **Ý tưởng từ khoang tàu thủy (Ship Bulkhead)**: Chia con tàu thành nhiều khoang kín nước độc lập. Nếu một khoang bị thủng, nước chỉ tràn vào khoang đó, con tàu vẫn nổi.
- **Trong Microservices**: Tách riêng Thread Pool hoặc Semaphore cho từng dịch vụ gọi ra ngoài:
  - Nhóm 1: Thread Pool cho chức năng Đặt Hàng (100 threads).
  - Nhóm 2: Thread Pool cho chức năng Gửi Email Marketing (10 threads).
  - Nếu hệ thống Mail bị nghẽn, tối đa chỉ có 10 threads bị treo; 100 threads Đặt Hàng vẫn phục vụ khách mua bình thường.

---

## 3. Chiến Lược Retry: Exponential Backoff & Full Jitter
- **Vì sao không Retry dồn dập (Thundering Herd)?**
  - Khi 1.000 client cùng retry tại giây thứ 1, 2, 4, 8... chúng tạo ra những đỉnh sóng xung kích (Traffic Spikes) dập tắt hoàn toàn khả năng gượng dậy của máy chủ vừa khởi động lại.
- **Công thức Full Jitter (AWS Recommended)**:
  Thêm yếu tố ngẫu nhiên vào thời gian chờ để làm phẳng đường cong tải:
  $$\text{Sleep} = \text{random}(0, \; \min(\text{cap}, \; \text{base} \times 2^{\text{attempt}}))$$

---

## 4. Cấu Hình Chuẩn Resilience4j Trong Spring Boot (`application.yml`)

```yaml
resilience4j:
  circuitbreaker:
    instances:
      paymentService:
        slidingWindowType: COUNT_BASED
        slidingWindowSize: 100              # Xét 100 cuộc gọi gần nhất
        minimumNumberOfCalls: 20           # Tối thiểu 20 cuộc gọi mới bắt đầu tính tỷ lệ
        failureRateThreshold: 50           # Mở mạch nếu lỗi >= 50%
        slowCallRateThreshold: 70          # Mở mạch nếu 70% cuộc gọi bị chậm
        slowCallDurationThreshold: 2000ms  # Cuộc gọi > 2s coi là chậm
        waitDurationInOpenState: 10000ms   # Giữ trạng thái OPEN trong 10s
        permittedNumberOfCallsInHalfOpenState: 10 # Cho 10 cuộc gọi thử nghiệm
        automaticTransitionFromOpenToHalfOpenEnabled: true

  retry:
    instances:
      paymentService:
        maxAttempts: 3
        waitDuration: 500ms
        enableExponentialBackoff: true
        exponentialBackoffMultiplier: 2
        retryExceptions:
          - java.io.IOException
          - java.util.concurrent.TimeoutException
        ignoreExceptions:
          - com.company.exceptions.BusinessValidationException # Lỗi nghiệp vụ không được retry
```

```java
@Service
public class OrderService {

    @CircuitBreaker(name = "paymentService", fallbackMethod = "paymentFallback")
    @Retry(name = "paymentService")
    public PaymentResult executePayment(Order order) {
        return paymentClient.charge(order);
    }

    // Hàm dự phòng khi Circuit Breaker đang OPEN hoặc hết lượt Retry
    public PaymentResult paymentFallback(Order order, Throwable t) {
        log.warn("Cổng thanh toán tạm ngưng, chuyển sang hàng đợi xử lý sau: {}", t.getMessage());
        return PaymentResult.queued("Giao dịch đã được ghi nhận và sẽ xử lý tự động khi kết nối phục hồi.");
    }
}
```

