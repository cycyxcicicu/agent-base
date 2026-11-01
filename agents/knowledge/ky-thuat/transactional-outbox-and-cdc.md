# Chuyên Đề Giao Dịch Phân Tán: Transactional Outbox Pattern & Debezium CDC

**Loại: tham khảo.**
> **Phân vùng**: Distributed Transactions, Event-Driven Architecture & Data Streaming  
> **Phân quyền truy cập (RBAC)**: `["architect", "dba", "dev", "devops"]`  
> **Nguồn đối chuẩn**: Chris Richardson (Microservices Patterns), Debezium Documentation, Martin Kleppmann (DDIA)  

---

## 1. Cạm Bẫy Lớn: Bài Toán "Dual-Write" Trong Microservices
- **Kịch bản sai lầm phổ biến**:
  ```java
  @Transactional
  public void createOrder(Order order) {
      // 1. Lưu đơn hàng vào Database
      orderRepository.save(order);
      
      // 2. Bắn sự kiện sang Kafka
      kafkaTemplate.send("order-created-topic", new OrderCreatedEvent(order));
  }
  ```
- **Rủi ro sập đổ tính nhất quán (Inconsistency)**:
  - Nếu DB commit thành công nhưng máy chủ bị sập nguồn ngay trước khi gửi Kafka $\rightarrow$ Mất message, các service khác (Kho vận, Thanh toán) không nhận được sự kiện!
  - Nếu gửi Kafka trước nhưng DB commit bị lỗi (Duplicate Key, DB chết) $\rightarrow$ Kafka đã bắn tin nhắn giả (Phantom Message), các service con xử lý đơn hàng không hề tồn tại trong DB!
  - Giao thức 2PC (Two-Phase Commit / XA Transactions) vừa chậm chạp, vừa làm giảm tính sẵn sàng và không được hỗ trợ tốt trên hạ tầng đám mây.

---

## 2. Mẫu Thiết Kế Transactional Outbox
- **Nguyên lý cốt lõi**:
  - Ghi cả hai hành động: **(1) Lưu Entity nghiệp vụ** và **(2) Ghi Event vào bảng `outbox`** trong **CÙNG MỘT GIAO DỊCH DATABASE NỘI BỘ (Local ACID Transaction)**.
  - Nhờ cơ chế ACID của CSDL quan hệ (PostgreSQL, MySQL), hoặc cả hai cùng thành công, hoặc cả hai cùng rollback. Hoàn toàn không có trạng thái lấp lửng.

```
Request Tạo Đơn Hàng
      │
      ▼
[Bắt đầu Giao Dịch Local ACID]
      ├── 1. INSERT INTO orders (id, total, status) VALUES (...)
      └── 2. INSERT INTO outbox_events (id, topic, payload) VALUES (...)
[COMMIT Giao Dịch Thành Công 100%]
      │
      ▼ (Bản ghi nằm an toàn trong bảng Outbox & WAL)
```

---

## 3. Chuyển Đổi Dữ Liệu Tự Động Bằng Debezium CDC (Change Data Capture)
- Thay vì dùng tiến trình định kỳ truy vấn DB (`SELECT * FROM outbox WHERE processed = false`), vốn gây áp lực tải lớn (Polling Load) và khóa bảng (Lock contention):
- **Debezium CDC**:
  - Đóng vai trò như một PostgreSQL Standby Replica, kết nối và đọc trực tiếp luồng **Write-Ahead Log (WAL / pg_logical)** ở mức nhị phân.
  - Bắt các sự kiện INSERT vào bảng `outbox_events` với độ trễ cực thấp ($< 10\text{ms}$).
  - Tự động đẩy message vào Apache Kafka mà không cần can thiệp vào mã nguồn backend.
  - Đảm bảo cam kết phân phối **At-Least-Once Delivery** (Ít nhất một lần). Bên nhận message chỉ cần áp dụng cơ chế Idempotent Consumer (dựa vào `event_id`).

```
[Postgres Database]
   │
   ├── Bảng 'orders'
   └── Bảng 'outbox_events' ──(Ghi nhị phân)──> [PostgreSQL WAL Engine]
                                                       │
                                                       ▼ (Logical Replication)
                                              [Debezium CDC Connector]
                                                       │
                                                       ▼ (Streaming OTLP)
                                              [Apache Kafka Cluster]
                                                       │
                                        ┌──────────────┴──────────────┐
                                        ▼                             ▼
                              [Payment Service]              [Inventory Service]
```

---

## 4. Cấu Trúc Bảng Outbox Mẫu & DDL Chuẩn (PostgreSQL)

```sql
CREATE TABLE outbox_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(255) NOT NULL, -- vd: 'Order'
    aggregate_id VARCHAR(255) NOT NULL,   -- vd: 'ORD-1092'
    event_type VARCHAR(255) NOT NULL,     -- vd: 'OrderCreated'
    payload JSONB NOT NULL,               -- Toàn bộ dữ liệu event dạng JSON
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Chỉ mục hỗ trợ nếu muốn dọn rác định kỳ các event đã cũ
CREATE INDEX idx_outbox_created_at ON outbox_events (created_at);
```

### Mã Nguồn Triển Khai Trong Service (Spring Boot)

```java
@Service
@RequiredArgsConstructor
public class OrderApplicationService {

    private final OrderRepository orderRepository;
    private final OutboxEventRepository outboxRepository;
    private final ObjectMapper objectMapper;

    @Transactional
    public Order createOrder(CreateOrderCommand cmd) throws JsonProcessingException {
        // 1. Nghiệp vụ lưu đơn
        Order order = Order.createNew(cmd);
        orderRepository.save(order);

        // 2. Ghi sự kiện vào Outbox trong cùng transaction DB
        OrderCreatedEvent event = new OrderCreatedEvent(order.getId(), order.getTotal(), order.getCreatedAt());
        OutboxEvent outboxRecord = OutboxEvent.builder()
            .aggregateType("Order")
            .aggregateId(order.getId().toString())
            .eventType("OrderCreated")
            .payload(objectMapper.writeValueAsString(event))
            .build();
        outboxRepository.save(outboxRecord);

        return order; // Kết thúc transaction an toàn tuyệt đối
    }
}
```

