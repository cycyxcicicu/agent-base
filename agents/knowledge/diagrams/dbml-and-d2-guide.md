# Hướng Dẫn Thiết Kế Cơ Sở Dữ Liệu Với DBML & Kiến Trúc Với D2

> **Loại: tham khảo.** Hướng dẫn công cụ vẽ sơ đồ, không phải nguồn luật. Khi khác `AGENTS.md`, vai trò hoặc `agents/protocols/` thì theo các nơi đó (`agents/protocols/source-precedence.md`).
> **Khác với chuẩn:** ERD chuẩn của dự án là archify `erd` (hoặc draw.io); DBML chỉ là ngôn ngữ phụ để thiết kế schema bằng chữ. D2 cần cài công cụ riêng. Chuẩn nội dung sơ đồ: `../srs/chuan-ve-so-do.md`; công cụ nguồn của dự án: `quy-uoc-draw-io-va-archify.md`; phần chữ đi kèm sơ đồ: `mo-ta-hoat-dong-so-do.md`.

> **Mã định danh:** `dbml-and-d2-guide`  
> **Chuyên mục:** Kiến trúc, Trực quan hóa & Vẽ sơ đồ tự động  
> **Trạng thái:** `draft` (Chờ nghiệm thu con người)  

---

## 1. DBML (Database Markup Language) — Thiết Kế Schema & ERD Chuẩn Nhất

DBML (phát triển bởi Holistics) là ngôn ngữ mã nguồn mở chuẩn mực được thiết kế riêng để định nghĩa schema cơ sở dữ liệu quan hệ, dễ đọc hơn SQL DDL thuần và trực quan hơn XML.

### 1.1. Cú Pháp DBML Chuẩn Cho Đơn Hàng & Kế Toán

```dbml
// Dự án: Quản lý Đơn hàng & Kho
Project GDT_Accounting {
  database_type: 'PostgreSQL'
  Note: 'Schema quản lý đơn hàng, kho và khách hàng'
}

Table customers {
  id bigint [pk, increment]
  full_name varchar(255) [not null]
  phone varchar(20) [unique, not null]
  email varchar(255)
  created_at timestamp [default: `now()`]
  
  Note: 'Bảng thông tin khách hàng'
}

Table orders {
  id bigint [pk, increment]
  order_code varchar(50) [unique, not null, note: 'Mã đơn sinh tự động']
  customer_id bigint [not null, ref: > customers.id]
  total_amount decimal(15,2) [not null, default: 0]
  status order_status [not null, default: 'DRAFT']
  warehouse_id bigint [not null]
  created_at timestamp [default: `now()`]
  updated_at timestamp
  
  Indexes {
    customer_id
    (order_code, status) [name: 'idx_orders_code_status']
  }
}

Table order_items {
  id bigint [pk, increment]
  order_id bigint [not null, ref: > orders.id]
  product_id bigint [not null]
  quantity int [not null, default: 1]
  unit_price decimal(15,2) [not null]
}

Enum order_status {
  DRAFT [note: 'Mới tạo']
  CONFIRMED [note: 'Đã xác nhận']
  SHIPPING [note: 'Đang vận chuyển']
  DELIVERED [note: 'Giao thành công']
  CANCELLED [note: 'Đã hủy']
}

TableGroup SalesModule {
  customers
  orders
  order_items
}
```

### 1.2. Cách Sử Dụng DBML:
- Trực quan hóa online: Dán trực tiếp vào trang [https://dbdiagram.io](https://dbdiagram.io) để sinh ra ERD tự động.
- Xuất tài liệu: Dùng công cụ `dbdocs` để sinh website tài liệu schema tĩnh cho dự án.

---

## 2. D2 Language — Ngôn Ngữ Sơ Đồ Kiến Trúc Hiện Đại Tự Động Dàn Trang

D2 (Declarative Diagramming) là ngôn ngữ mới được thiết kế để khắc phục hoàn toàn nhược điểm tính toán hình học kém của LLM:
- **Tự động căn chỉnh layout (TALA layout engine)**: Không cần tọa độ `x, y`.
- **Hỗ trợ icon nhúng**: Nhúng icon web URL hoặc SVG có sẵn.
- **Hộp lồng nhau (Nested Containers)**: Thể hiện kiến trúc VPC, Subnet, Cluster cực kỳ tự nhiên.

### 2.1. Ví Dụ Cú Pháp D2

```d2
direction: right

client: Client Application {
  shape: person
  icon: https://icons.terrastruct.com/essentials%2F004-user.svg
}

cloud: Production Cloud VPC {
  style.fill: "#f8f9fa"
  
  gw: Spring Cloud Gateway {
    shape: rectangle
    style.stroke: "#28a745"
  }

  services: Microservices Cluster {
    iam: IAM Service (Port 8100)
    acct: Accounting Service (Port 8200)
  }

  data: Data Persistence {
    postgres: PostgreSQL Cluster {
      shape: cylinder
      icon: https://icons.terrastruct.com/dev%2Fpostgresql.svg
    }
    redis: Redis In-Memory {
      shape: cylinder
      icon: https://icons.terrastruct.com/dev%2Fredis.svg
    }
  }
}

client -> cloud.gw: HTTPS Request
cloud.gw -> cloud.services.iam: Validate Token
cloud.gw -> cloud.services.acct: Dispatch Order Event
cloud.services.acct -> cloud.data.postgres: Read/Write Transaction
cloud.services.acct -> cloud.data.redis: Distributed Lock
```
