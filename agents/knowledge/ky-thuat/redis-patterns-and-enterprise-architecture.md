# Cẩm Nang Mẫu Kiến Trúc Redis & Enterprise Architecture Patterns (Martin Fowler)

> **Loại: tham khảo.**  
> **Mã định danh:** `redis-patterns-and-enterprise-architecture`  
> **Chuyên mục:** Kiến trúc Hệ thống Phân tán, Caching & Enterprise Design Patterns  
> **Nguồn gốc:** Redis Official Patterns Documentation, Martin Fowler (Patterns of Enterprise Application Architecture - PoEAA)  
> **Trạng thái:** `draft` (Chờ nghiệm thu con người)  

---

## 1. Các Mẫu Kiến Trúc Redis Chuyên Sâu (Redis Architecture Patterns)

Redis không chỉ là một kho Key-Value đơn giản, mà là công cụ nòng cốt để giải quyết các bài toán về hiệu năng và phân tán trong hệ thống Microservices.

```mermaid
flowchart TD
    App["Ứng Dụng (Spring Boot)"]
    Redis[("Redis In-Memory")]
    DB[("PostgreSQL Master")]

    App -->|1. Đọc Cache (Cache-Aside)| Redis
    Redis -.->|Miss| App
    App -->|2. Đọc CSDL khi Miss| DB
    App -->|3. Nạp lại Cache kèm TTL| Redis
    App -->|4. Khóa phân tán (Distributed Lock)| Redis
```

### 1.1. Phòng Chống Thảm Họa Cache Stampede (Thundering Herd)
Khi một Cache Key có lượng truy cập cực lớn (Hot Key) bị hết hạn (TTL Expired), hàng ngàn request đồng thời sẽ cùng thấy Cache Miss và cùng lúc dồn dập query vào CSDL, làm sập CSDL ngay lập tức.

**Hai giải pháp chuẩn hóa:**
1. **Khóa phân tán (Mutual Exclusion Lock):** Chỉ cho phép duy nhất request đầu tiên lấy được lock để truy vấn CSDL và tính toán lại cache; các request khác tạm dừng 50ms rồi đọc lại từ Redis.
2. **Thuật toán hết hạn xác suất (Probabilistic Early Expiration - XFetch):** Dự đoán trước thời điểm key sắp hết hạn và kích hoạt một tiến trình nền tính toán lại cache trước khi nó thực sự hết hạn.

### 1.2. Khóa Phân Tán An Toàn Tuyệt Đối Bằng Lua Script
Để tránh lỗi tiến trình này vô tình xóa nhầm khóa của tiến trình khác (khi tác vụ chạy quá hạn TTL), việc giải phóng khóa bắt buộc phải kiểm tra UUID thông qua **Lua Script nguyên tử (Atomic)**:

```java
// 1. Lấy khóa phân tán kèm UUID độc nhất và TTL 30 giây
String lockUuid = UUID.randomUUID().toString();
Boolean acquired = redisTemplate.opsForValue()
    .setIfAbsent("lock:order:10023", lockUuid, Duration.ofSeconds(30));

if (Boolean.TRUE.equals(acquired)) {
    try {
        // Thực thi nghiệp vụ trừ kho an toàn
        processOrderFulfillment(10023);
    } finally {
        // 2. Giải phóng khóa bằng Lua Script nguyên tử (chỉ xóa nếu UUID khớp)
        String luaScript = 
            "if redis.call('get', KEYS[1]) == ARGV[1] then " +
            "    return redis.call('del', KEYS[1]) " +
            "else " +
            "    return 0 " +
            "end";
        redisTemplate.execute(
            new DefaultRedisScript<>(luaScript, Long.class),
            Collections.singletonList("lock:order:10023"),
            lockUuid
        );
    }
}
```

### 1.3. Bộ Giới Hạn Tốc Độ Cửa Sổ Trượt (Sliding Window Rate Limiter)
Dùng cấu trúc dữ liệu **Sorted Set (ZSET)** để giới hạn số lượng request chính xác từng mili-giây (ví dụ: tối đa 10 request / giây / IP):
1. Xóa các request cũ hơn cửa sổ 1 giây: `ZREMRANGEBYSCORE rate:ip123 0 (now - 1000)`
2. Thêm request hiện tại vào ZSET: `ZADD rate:ip123 now now`
3. Đếm số lượng phần tử còn lại: `ZCARD rate:ip123`. Nếu `> 10` $\rightarrow$ Trả về mã lỗi `HTTP 429 Too Many Requests`.

---

## 2. Patterns of Enterprise Application Architecture (Martin Fowler - PoEAA)

Bộ mẫu thiết kế kinh điển của Martin Fowler là nền tảng kiến trúc đằng sau các framework hiện đại như Hibernate, Spring, Entity Framework.

### 2.1. So Sánh Active Record vs Data Mapper

| Tiêu chí | Active Record Pattern | Data Mapper Pattern (Chuẩn Clean Architecture) |
|---|---|---|
| **Đặc điểm** | Entity tự biết cách lưu chính mình: `order.save()`, `order.delete()` | Entity hoàn toàn là POJO thuần túy, không chứa mã SQL: `orderRepo.save(order)` |
| **Phụ thuộc** | Entity phụ thuộc chặt chẽ vào Database Schema và Driver | Entity độc lập 100% với CSDL; tầng Persistence Mapper gánh vác việc ánh xạ |
| **Phù hợp với** | Ứng dụng CRUD nhỏ, prototype, ít nghiệp vụ phức tạp | Hệ thống Enterprise quy mô lớn, Clean Architecture, Domain-Driven Design (DDD) |

### 2.2. Unit of Work (Đơn Vị Công Tác)
Thay vì thực thi một loạt lệnh `INSERT`, `UPDATE`, `DELETE` phân mảnh ngay khi code chạy, **Unit of Work** duy trì một danh sách các đối tượng bị ảnh hưởng trong suốt một phiên làm việc (Business Transaction):
- Theo dõi các đối tượng: Mới tạo (New), Đã sửa (Dirty), Đã xóa (Clean/Removed).
- **Lợi ích:** Gom nhóm và thực thi toàn bộ các câu lệnh SQL theo thứ tự tối ưu nhất trong một lần Flush duy nhất, giảm thiểu tối đa số lần round-trip mạng tới CSDL.

### 2.3. Identity Map (Bản Đồ Định Danh)
Đảm bảo rằng trong một phiên làm việc, **mỗi bản ghi trong CSDL chỉ được nạp vào bộ nhớ duy nhất một lần (1 Instance)**:
- Nếu đoạn code A gọi `findOrder(10)` và đoạn code B cũng gọi `findOrder(10)`, Hibernate sẽ trả về cùng một tham chiếu đối tượng trong bộ nhớ (First-level Cache) thay vì tạo ra 2 đối tượng khác nhau.
- **Lợi ích:** Ngăn ngừa mâu thuẫn trạng thái (Concurrency Inconsistency) và tiết kiệm RAM.

### 2.4. CQRS (Command Query Responsibility Segregation)
Martin Fowler định nghĩa việc phân tách rạch ròi giữa:
- **Command Model:** Thực hiện các hành vi thay đổi trạng thái (Create, Update, Cancel), áp dụng toàn bộ Business Rules và invariants.
- **Query Model:** Tối ưu hóa việc đọc dữ liệu, có thể đọc từ Materialized Views, ElasticSearch hoặc Read Replicas, hoàn toàn không nạp Aggregate Root phức tạp.
