# Cẩm Nang Cú Pháp Mermaid & Tích Hợp Draw.io

> **Loại: tham khảo.** Hướng dẫn công cụ vẽ sơ đồ, không phải nguồn luật. Khi khác `AGENTS.md`, vai trò hoặc `agents/protocols/` thì theo các nơi đó (`agents/protocols/source-precedence.md`).
> **Khác với chuẩn:** Dùng cho sơ đồ nhỏ nằm trong md. Khung xem md có thể không vẽ Mermaid, nên luôn kèm mô tả chữ (`mo-ta-hoat-dong-so-do.md`). Chuẩn nội dung sơ đồ: `../srs/chuan-ve-so-do.md`; công cụ nguồn của dự án: `quy-uoc-draw-io-va-archify.md`; phần chữ đi kèm sơ đồ: `mo-ta-hoat-dong-so-do.md`.

> **Mã định danh:** `mermaid-syntax-guide`  
> **Chuyên mục:** Kiến trúc, Trực quan hóa & Vẽ sơ đồ tự động  
> **Trạng thái:** `draft` (Chờ nghiệm thu con người)  

---

## 1. Tổng Quan & Cơ Chế Import Vào Draw.io

Mermaid.js là ngôn ngữ vẽ sơ đồ bằng văn bản (Text-to-Diagram) phổ biến nhất hiện nay, được hỗ trợ nguyên bản trên GitHub, GitLab, Notion, Obsidian và Antigravity Markdown Artifacts.

**Tích hợp với Draw.io:**
Người dùng có thể vẽ nhanh bằng Mermaid rồi chuyển sang Draw.io để kéo thả chỉnh sửa nâng cao:
👉 **`Arrange` $\rightarrow$ `Insert` $\rightarrow$ `Advanced` $\rightarrow$ `Mermaid`** $\rightarrow$ Dán mã Mermaid vào và bấm Insert. Draw.io sẽ tự động dựng hình và dàn trang hoàn chỉnh.

---

## 2. Các Mẫu Sơ Đồ Mermaid Phổ Biến

### 2.1. Sequence Diagram (Luồng Giao Dịch / API Gọi Nhau)

```mermaid
sequenceDiagram
    autonumber
    actor User as Khách Hàng
    participant GW as API Gateway
    participant Order as Accounting Service
    participant Pay as Cổng Thanh Toán
    participant DB as PostgreSQL

    User->>GW: POST /api/v1/orders (Tạo đơn hàng)
    GW->>Order: Forward kèm JWT Bearer
    activate Order
    Order->>DB: INSERT order (Status: CREATED)
    Order->>Pay: Khởi tạo giao dịch thanh toán
    Pay-->>Order: Trả về Payment URL
    Order-->>GW: 201 Created (Kèm paymentUrl)
    deactivate Order
    GW-->>User: Hiển thị trang thanh toán
```

### 2.2. Flowchart & Subgraphs (Phân Vùng Kiến Trúc)

> [!IMPORTANT]
> **Quy tắc an toàn Mermaid:** Luôn bọc nhãn có dấu ngoặc đơn hoặc ký tự đặc biệt trong dấu ngoặc kép: `id["Nhãn (Chi tiết)"]`. Tránh dùng thẻ HTML phức tạp bên trong node.

```mermaid
flowchart TD
    subgraph ClientZone ["Phân Vùng Truy Cập"]
        Web["Web Frontend (React)"]
        Mobile["Mobile App (Flutter)"]
    end

    subgraph PlatformZone ["Hạ Tầng Nền Tảng"]
        GW["API Gateway (Port 8080)"]
        Eureka["Discovery Server (Eureka)"]
        Config["Config Server"]
    end

    subgraph BusinessZone ["Nghiệp Vụ Lõi (Microservices)"]
        IAM["ws-iam (Auth, Menu, Staff)"]
        Acct["accounting-service (Orders, Warehouse)"]
    end

    subgraph StorageZone ["Lưu Trữ Dữ Liệu"]
        PG[(PostgreSQL Master)]
        Redis[(Redis Cache)]
        MQ[RabbitMQ Broker]
    end

    Web & Mobile --> GW
    GW --> Eureka
    GW --> IAM & Acct
    IAM --> PG
    Acct --> PG & Redis & MQ
```

---

## 3. Mermaid v11: Architecture Diagram (architecture-beta)

Từ phiên bản Mermaid v11+, cú pháp `architecture-beta` cho phép mô tả kiến trúc hạ tầng trực tiếp kết hợp bộ biểu tượng Iconify:

```mermaid
architecture-beta
    group api(logos:aws-api-gateway)[API Gateway]
    group compute(logos:aws-lambda)[Compute Core]
    group db(logos:aws-rds)[Database Cluster]

    service gw in api: Gateway Router
    service worker in compute: Order Processor
    service postgres in db: Primary DB

    gw:B -- T:worker
    worker:R -- L:postgres
```

---

## 4. Entity-Relationship Diagram (ERD / Database Schema)

```mermaid
erDiagram
    ORDER ||--|{ ORDER_ITEM : contains
    ORDER }|--|| CUSTOMER : places
    ORDER ||--o| PAYMENT : has

    ORDER {
        bigint id PK
        string order_code UK "Mã đơn hàng duy nhất"
        bigint customer_id FK
        decimal total_amount "Tổng tiền thanh toán"
        string status "Trạng thái đơn hàng"
        timestamp created_at
    }

    ORDER_ITEM {
        bigint id PK
        bigint order_id FK
        bigint product_id FK
        int quantity "Số lượng"
        decimal unit_price "Đơn giá"
    }
```
