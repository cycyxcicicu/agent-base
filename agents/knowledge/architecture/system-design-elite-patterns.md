# Mười Sáu Bản Thiết Kế Kiến Trúc Tinh Hoa (ByteByteGo Elite System Design)

**Loại: tham khảo.** Nguồn: [ByteByteGo System Design 101](file:///d:/congty/agent-base/assets/system-design-elite/INDEX.md).  
Kho dữ liệu cục bộ: [assets/system-design-elite/](file:///d:/congty/agent-base/assets/system-design-elite/) (16 bài viết tinh tuyển, 16 infographic chuẩn).  
Vai trò áp dụng: `architect`, `dba`, `dev`, `ba`, `data-eng`.  

---

## 1. Trụ Cột 1: Mở Rộng Cơ Sở Dữ Liệu Quy Mô Lớn (Big Tech Database Scaling)

### 1.1. Bài Học Mở Rộng PostgreSQL 100X Tại Figma (`IMG-0691`)
Khi lượng người dùng tăng 200% và cơ sở dữ liệu phình to gấp 100 lần, Figma không vội đập bỏ PostgreSQL mà nâng cấp qua 3 giai đoạn kiến trúc chuẩn mực:
1. **Nâng cấp dọc & Đệm kết nối (Vertical Scaling & PgBouncer):** Nâng instance lên cấu hình lớn nhất (`r5.24xlarge`), tạo thêm Read Replicas để phân tách luồng đọc/ghi, và bắt buộc đặt `PgBouncer` phía trước để gom và quản lý hàng chục nghìn connection pool.
2. **Phân vùng dọc (Vertical Partitioning):** Tách các bảng có lưu lượng truy cập khổng lồ (`Figma Files`, `Organizations`) sang các cụm database vật lý riêng biệt với instance PgBouncer độc lập.
3. **Phân vùng ngang & Sharding (Horizontal Partitioning):** Khi bảng vượt hàng tỷ bản ghi và dung lượng nhiều Terabytes, Figma sharding bảng theo `Org ID` (Colocated Sharding), đảm bảo các truy vấn liên quan đến cùng một tổ chức luôn nằm trên cùng 1 shard.

### 1.2. Bài Học Discord Lưu Trữ Hàng Nghìn Tỷ Tin Nhắn (`IMG-0692`)
- **Vấn đề:** Ban đầu Discord dùng MongoDB -> chuyển sang Apache Cassandra. Nhưng khi chạm ngưỡng hàng nghìn tỷ tin nhắn, Cassandra gặp vấn đề nghiêm trọng về độ trễ đọc (Read Latency) do JVM Garbage Collection Pause và bảo trì SS-Table Compaction quá nặng.
- **Giải pháp:** Chuyển đổi toàn bộ sang **ScyllaDB** (CSDL tương thích hoàn toàn với Cassandra nhưng viết bằng C++, kiến trúc Seastar asynchronous framework, non-blocking I/O và Zero-GC), giúp P99 Latency giảm từ hàng giây xuống dưới 5ms!

### 1.3. Bốn Giải Thuật Phân Vùng CSDL & Consistent Hashing (`IMG-0694`, `IMG-0695`)
- **Range-Based Sharding:** Chia theo dải giá trị (ví dụ: User ID 1-1.000.000). Dễ cài đặt nhưng dễ sinh nút thắt cổ chai (Hot Spot) trên dải dữ liệu mới nhất.
- **Hash-Based Sharding:** Dùng hàm hash `hash(key) % N`. Phân bổ đều dữ liệu nhưng cực kỳ đau đớn khi thêm hoặc bớt node (phải rehash toàn bộ DB).
- **Consistent Hashing (Bắt buộc dùng Virtual Nodes):**
  - Đưa cả Node server và Data key lên một vòng tròn băm 360 độ (Hash Ring).
  - Khi thêm hoặc bớt 1 server, chỉ một phần nhỏ dữ liệu liền kề bị di chuyển ($K/N$ keys), không ảnh hưởng toàn mạng.
  - Sử dụng **Virtual Nodes (Node ảo)** để chia đều tải trọng, triệt tiêu hoàn toàn hiện tượng phân bổ lệch.

---

## 2. Trụ Cột 2: Hệ Thống Thanh Toán & Tài Chính Chịu Lỗi Cao (Resilient Fintech & Payments)

### 2.1. Mười Nguyên Tắc Thanh Toán Bền Bỉ Của Shopify (`IMG-0696`)
Shopify xử lý hàng chục tỷ USD mỗi năm thông qua 10 nguyên tắc kiến trúc:
1. **Idempotency tuyệt đối:** Mọi yêu cầu trừ tiền phải có `Idempotency-Key` do client sinh ra.
2. **Asynchronous Ledger Processing:** Tách biệt luồng trừ tiền trực tiếp với luồng ghi sổ cái kế toán thông qua hàng đợi bất đồng bộ.
3. **Exponential Backoff with Jitter:** Khi cổng thanh toán ngân hàng lỗi, thử lại có độ trễ giãn cách ngẫu nhiên để không dội bom DDoS đối tác.
4. **Circuit Breaker:** Tự động ngắt kết nối cổng thanh toán gặp sự cố và chuyển hướng sang cổng dự phòng (Fallback PSP).

### 2.2. Chống Trùng Lặp Thanh Toán (How to Avoid Double Payment — `IMG-0697`)
Cơ chế bảo vệ 3 lớp chống khách hàng bị trừ tiền 2 lần:
```
[Client] ---> POST /pay (Idempotency-Key: uuid-123) ---> [API Gateway]
                                                                |
                                                                v
                                                [Check Deduplication Table]
                                                ├── Đã xử lý? -> Trả kết quả cũ ngay (Không gọi Ngân hàng)
                                                └── Chưa có?  -> Bọc Unique Lock -> Gọi Ngân hàng -> Lưu Cache
```

### 2.3. Quy Trình Đối Soát Tài Chính Ba Bên (Three-Way Reconciliation — `IMG-0699`)
Hệ thống thanh toán bắt buộc phải có pipeline đối soát chạy tự động định kỳ vào cuối ngày (EOD):
- Đối chiếu **Báo cáo sao kê ngân hàng (Bank Statement)** $\longleftrightarrow$ **Dữ liệu cổng trung gian (PSP Statement)** $\longleftrightarrow$ **Sổ cái nội bộ (Internal Ledger)** để phát hiện lệch dòng tiền, hoàn tiền sót hoặc gian lận.

---

## 3. Trụ Cột 3: Bộ Nhớ Đệm & Đồng Thời Phân Tán (Caching & Distributed Concurrency)

### 3.1. Bốn Cạm Bẫy Sụp Đổ Hệ Thống Do Cache (`IMG-0700`)
1. **Cache Avalanche (Sập hàng loạt):** Hàng triệu key hết hạn cùng một giây $\rightarrow$ Toàn bộ traffic đánh thẳng vào CSDL làm sập DB. *Khắc phục: Thêm jitter ngẫu nhiên vào TTL (`TTL = 3600s + rand(0, 300s)`).*
2. **Cache Breakdown (Sập vì Hot Key):** Một key cực hot (ví dụ: tin khuyến mãi Black Friday) hết hạn đúng lúc cao điểm $\rightarrow$ Hàng chục nghìn request đồng thời lao vào DB để tạo lại cache. *Khắc phục: Dùng Mutex Lock tại tầng ứng dụng khi tái tạo cache.*
3. **Cache Penetration (Xuyên thủng cache):** Kẻ xấu liên tục query các key không hề tồn tại trong hệ thống (User ID = -9999) $\rightarrow$ Cache luôn miss, DB bị quét cạn kiệt tài nguyên. *Khắc phục: Dùng **Bloom Filter** chặn ngay từ cổng hoặc cache giá trị `null` với TTL ngắn.*
4. **Cache Stampede:** Tần suất đọc và ghi đè quá cao làm CPU nghẽn. *Khắc phục: Áp dụng thuật toán Probabilistic Early Expiration (XFetch).*

### 3.2. Khóa Phân Tán & Rủi Ro Clock Drift (`IMG-0703`)
- Khi chạy hàng trăm microservices song song, khóa CSDL thông thường không đủ. Cần dùng **Distributed Lock (Redis Redlock)**.
- **Rủi ro chí tử:** GC Pause (Java dừng toàn bộ luồng) hoặc Clock Drift làm khóa hết hạn trong khi tiến trình vẫn đang ghi dữ liệu!
- **Giải pháp chuẩn:** Bắt buộc kết hợp **Fencing Token** (Mã tăng dần duy nhất). CSDL đích chỉ chấp nhận giao dịch có Fencing Token lớn hơn token trước đó.

---

## 4. Trụ Cột 4: Hàng Đợi & Xử Lý Dòng Dữ Liệu (Kafka & Streaming Architecture)

### 4.1. Vì Sao Apache Kafka Lại Cực Nhanh? (`IMG-0704`)
Kafka có thể nuốt hàng triệu messages/giây trên một máy chủ thông thường nhờ 4 thiết kế phần cứng:
1. **Tuần tự trên đĩa (Sequential Disk I/O):** Ghi đĩa tuần tự nhanh ngang ngửa ghi vào RAM ngẫu nhiên.
2. **Tận dụng Page Cache của HĐH:** Không tốn chi phí quản lý bộ nhớ của JVM, giao toàn bộ việc cache đĩa cho Linux kernel.
3. **Kỹ thuật Zero-Copy (DMA - Direct Memory Access):** Chuyển trực tiếp dữ liệu từ file trên đĩa qua Socket mạng thông qua lệnh hệ thống `sendfile()`, không bao giờ sao chép dữ liệu thừa qua user-space.
4. **Gom lô & Nén dữ liệu (Batching & End-to-End Compression).**

### 4.2. Làm Sao Để Đảm Bảo Kafka Tuyệt Đối Không Mất Tin Nhắn? (`IMG-0705`)
Cấu hình chuẩn sản xuất cho hệ thống tài chính / giao dịch:
- Phía Producer: `acks=all` (hoặc `acks=-1`) — chỉ báo thành công khi tất cả bản sao in-sync đã ghi nhận.
- Phía Broker: `min.insync.replicas=2` và `replication.factor=3`.
- Phía Consumer: `enable.auto.commit=false` — chỉ commit offset sau khi nghiệp vụ đã xử lý và ghi DB thành công.

---

## 5. Sổ Tra Cứu Nhanh & Lệnh CLI Cho Agent

Tất cả 16 sơ đồ kiến trúc đỉnh cao này đã được định danh và lưu trữ cục bộ tại [assets/system-design-elite/images/](file:///d:/congty/agent-base/assets/system-design-elite/images/).

```bash
# 1. Tra cứu sơ đồ mở rộng Postgres của Figma
python scripts/knowledge.py image -q "figma"

# 2. Tra cứu sơ đồ chống trùng tiền (Idempotency)
python scripts/knowledge.py image -q "double payment"

# 3. Tra cứu sơ đồ 4 cạm bẫy Cache sập hệ thống
python scripts/knowledge.py image -q "cache wrong"

# 4. Tra cứu sơ đồ giải thích vì sao Kafka nhanh
python scripts/knowledge.py image -q "kafka fast"
```

