# Chuyên Đề Kiến Trúc Tích Hợp Bất Đồng Bộ, Worker Auto-Scaler & Chống Deadlock Concurrency

**Loại: tham khảo.**
> **Phân vùng**: High Availability, Microservices Integration & Concurrency Management  
> **Phân quyền truy cập (RBAC)**: `["architect", "dev", "dba", "sre", "data-eng"]`  
> **Nguồn đối chuẩn**: Spring AMQP Official Manual, PostgreSQL Concurrency & Locking Guide, RFC 2104 (HMAC), High Performance Java Persistence (Vlad Mihalcea)  

---

## 1. Mẫu Kiến Trúc Đồng Bộ Bất Đồng Bộ (Sync-then-Serve & Fast Ingestion Gate)

### 1.1 Vấn đề cốt lõi
Khi tích hợp các hệ thống bên thứ ba (Sàn TMĐT, Cổng thanh toán, Logistics, CRM), việc gọi API trực tiếp từ giao diện người dùng (Serving) hoặc xử lý logic nghiệp vụ nặng ngay trong HTTP Webhook (Ingestion) là nguyên nhân hàng đầu gây sập hệ thống (Traffic Spikes, Rate-limiting, Connection Pool Exhaustion).

### 1.2 Giải pháp Sync-then-Serve
1. **Tách rời 2 luồng:**
   * **Luồng Ghi (Ingestion):** Webhook chỉ làm nhiệm vụ xác minh chữ ký HMAC-SHA256 $\rightarrow$ đóng gói vào `Message Envelope` bất biến $\rightarrow$ đẩy vào Message Broker (RabbitMQ) $\rightarrow$ trả về `HTTP 200 OK` ngay lập tức ($< 50\text{ms}$).
   * **Luồng Đọc (Serving):** Giao diện người dùng đọc 100% từ Database nội bộ (PostgreSQL).
2. **Kỹ thuật Dual-Path Worker:**
   * **Fast-Path (Direct Update):** Nếu Webhook đã chứa đủ thông tin (đổi trạng thái đơn), Worker dùng Pessimistic Lock (`findForUpdate`), so sánh `event_time > db_time` rồi cập nhật trực tiếp DB mà không tốn lượt gọi API nào lên bên thứ ba.
   * **Slow-Path (Refetch Full Detail):** Nếu là sự kiện tạo mới thiếu dữ liệu, Worker mới gọi REST API đối tác để kéo chi tiết và Upsert vào DB.

---

## 2. Kỹ Thuật Tự Động Co Giãn Worker Theo Tài Nguyên (Resource-Aware Worker Auto-Scaler)

### 2.1 Điểm mù của cấu hình Worker cố định
Đa phần các service Spring Boot cấu hình cứng số lượng worker cố định (`concurrency = N`). Khi tải thấp gây lãng phí tài nguyên; khi tải đột biến (Flash Sale) thì worker không xử lý kịp hoặc nếu tăng quá cao sẽ chiếm hết kết nối của Database Connection Pool (`HikariCP`), làm chết Web API.

### 2.2 Thuật toán Auto-Scaler tự thân (Runtime Autoscaler)
Cứ mỗi 10 giây một lần, service tự động đo đạc 4 chỉ số qua JMX và Hikari Pool MXBean:
1. `backlog`: Số lượng tin nhắn đang xếp hàng trong Queue.
2. `cpu`: Tải CPU của tiến trình JVM (`osBean.getProcessCpuLoad()`).
3. `heap`: Tỷ lệ bộ nhớ Heap đã dùng.
4. `db`: Tỷ lệ bận của Connection Pool (`pool.getActiveConnections() / pool.getMaximumPoolSize()`).

```java
// CÔNG THỨC RÀO CHẮN AN TOÀN CHO DATABASE (Safe Maximum):
// Luôn dành ra ít nhất 3 connection cho Web API người dùng, không để worker nuốt trọn DB:
int dbLimit = pool == null ? config.getMax() : Math.max(config.getMin(), hikari.getMaximumPoolSize() - 3);
int cpuLimit = runtime.availableProcessors() * 2;
int memoryLimit = (int) (runtime.maxMemory() / workerBytes);
int safeMax = Math.min(config.getMax(), Math.min(cpuLimit, Math.min(memoryLimit, dbLimit)));

// TÍNH TOÁN NHU CẦU THEO SỐ MESSAGE TỒN ĐỌNG (Demand):
int demand = Math.max(config.getMin(), (int) Math.ceil((backlog + inFlightCount) / (double) backlogPerWorker));
demand = Math.min(demand, safeMax);

// CO GIÃN RUNTIME KHÔNG CẦN RESTART:
if (demand > desired && room && cooldownPassed) {
    container.setMaxConcurrentConsumers(target);
    container.setConcurrentConsumers(target); // Tăng worker
} else if (demand < desired && backlog == 0 && cooldownPassed) {
    container.setConcurrentConsumers(target); // Hạ worker (graceful stop)
    container.setMaxConcurrentConsumers(target);
}
```

---

## 3. Concurrency Control: Khóa Bi Quan & Watchdog Daemon Tự Phá Deadlock

### 3.1 Khóa bi quan tại mức dòng (Row-level Pessimistic Lock)
Chống ghi đè trạng thái và tranh chấp ghi giữa nhiều Worker chạy song song:
```java
@Lock(LockModeType.PESSIMISTIC_WRITE)
@Query("SELECT o FROM OrderEntity o WHERE o.tenant = :tenant AND o.code = :code")
Optional<OrderEntity> findForUpdate(@Param("tenant") Tenant tenant, @Param("code") String code);
```
SQL sinh ra: `SELECT * FROM orders WHERE tenant_id = 1 AND code = 'ORD-001' FOR UPDATE;`

### 3.2 Daemon Watchdog Giám Sát `pg_stat_activity`
Để chống tình trạng một transaction giữ lock bị treo mạng bên ngoài làm nghẽn toàn bộ hệ thống, một daemon script chạy độc lập truy vấn danh mục khóa:
```sql
SELECT DISTINCT blocking_locks.pid AS blocker_pid, 
       age(clock_timestamp(), blocking_activity.xact_start) AS duration
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks 
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted
  AND age(clock_timestamp(), blocking_activity.xact_start) > interval '60 seconds';
```
Nếu phát hiện process giữ khóa vượt quá 60 giây, daemon tự động thực thi:
`SELECT pg_terminate_backend(blocker_pid);` để giải phóng hàng đợi DB ngay lập tức.

---

## 4. Quản Trị Đa Tenant OAuth 2.0 & Ký Chữ Ký HMAC-SHA256 Chống Timing Attack

### 4.1 Dynamic Credential Resolver
Không hardcode biến credentials trong file cấu hình tĩnh. Mọi đối tượng Client đều đi qua một Resolver để nạp đúng App Key/Secret và Access Token của từng Tenant:
```java
public ThirdPartyCredentials resolve(TenantAccount tenant) {
    if (tenant.getCustomAppKey() != null) {
        return new ThirdPartyCredentials(tenant.getCustomAppKey(), decrypt(tenant.getCustomAppSecret()));
    }
    return defaultSystemCredentials;
}
```

### 4.2 Chống Tấn Công Timing Attack Khi Verify Chữ Ký
Tuyệt đối không so sánh chữ ký bằng `String.equals()` vì toán tử này dừng ngay ở byte sai đầu tiên, tạo cơ hội cho kẻ tấn công đo đạc độ trễ mạng để vét cạn chữ ký.
Bắt buộc dùng so sánh thời gian không đổi (**Constant-Time Comparison**):
```java
// Chuẩn an toàn tuyệt đối:
boolean isValid = MessageDigest.isEqual(
    expectedSignature.getBytes(StandardCharsets.UTF_8),
    headerSignature.trim().getBytes(StandardCharsets.UTF_8)
);
```

---

## 5. Chốt Chặn Quét Bù Định Kỳ (Sliding Overlap Window) & Self-Healing Token

1. **Overlap Window 15 phút chống rớt đơn:**
   * Cronjob quét bù định kỳ để phòng ngừa sự cố mạng làm rơi Webhook.
   * Công thức gối đầu: `searchStartTime = lastSuccessWatermark - 15 phút`. Giúp triệt tiêu hoàn toàn rủi ro chênh lệch đồng hồ (Clock Drift) và độ trễ lập chỉ mục của bên thứ ba.
2. **Self-Healing Token Refresh (Mã lỗi HTTP 401):**
   * Sử dụng khóa đồng bộ theo từng Tenant (`synchronized (tokenLock.get(tenantId))`).
   * Khi gặp lỗi 401: Duy nhất 1 luồng đi refresh token $\rightarrow$ lưu token mới vào DB $\rightarrow$ Thử lại request ngay tại chỗ (`inline retry`). Các luồng sau khi chờ khóa xong sẽ thấy token mới và tiếp tục chạy mà không bị đứt gãy.
3. **Dead-Letter Queue (DLQ):**
   * Message cấu trúc rác/lỗi không thể cứu được: chuyển ngay sang DLQ và ACK để giải phóng Queue chính.

