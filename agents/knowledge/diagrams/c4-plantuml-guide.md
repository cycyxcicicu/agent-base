# Cẩm Nang C4 Model Với C4-PlantUML & Bộ Icon Sprites

> **Loại: tham khảo.** Hướng dẫn công cụ vẽ sơ đồ, không phải nguồn luật. Khi khác `AGENTS.md`, vai trò hoặc `agents/protocols/` thì theo các nơi đó (`agents/protocols/source-precedence.md`).
> **Khác với chuẩn:** Cần PlantUML (Java) hoặc dịch vụ vẽ ngoài, chưa có trong khung; chỉ dùng khi dự án chọn C4-PlantUML. Sơ đồ thành phần mặc định vẽ bằng draw.io hoặc archify `architecture`. Chuẩn nội dung sơ đồ: `../srs/chuan-ve-so-do.md`; công cụ nguồn của dự án: `quy-uoc-draw-io-va-archify.md`; phần chữ đi kèm sơ đồ: `mo-ta-hoat-dong-so-do.md`.

> **Mã định danh:** `c4-plantuml-guide`  
> **Chuyên mục:** Kiến trúc, Trực quan hóa & Vẽ sơ đồ tự động  
> **Trạng thái:** `draft` (Chờ nghiệm thu con người)  

---

## 1. Tổng Quan Về Mô Hình C4 Model

Mô hình C4 (Simon Brown) là chuẩn mực kiến trúc doanh nghiệp phân rã hệ thống thành 4 tầng zoom:
1. **Level 1 — System Context:** Hệ thống tương tác với ai (Người dùng, Hệ thống bên ngoài).
2. **Level 2 — Container:** Các ứng dụng độc lập thực thi (Web App, Mobile App, API Gateway, Microservice, Database, Message Broker).
3. **Level 3 — Component:** Các thành phần nội bộ bên trong 1 Container (Controllers, Services, Repositories, Adapters).
4. **Level 4 — Code:** Sơ đồ lớp UML hoặc mã nguồn thực tế.

---

## 2. Cú Pháp C4-PlantUML Kèm Icon Sprites

C4-PlantUML cho phép nhúng trực tiếp biểu tượng từ thư viện chuẩn của AWS, Azure, GCP, Kubernetes và Logos.

```plantuml
@startuml "c4-container-diagram"
!include <C4/C4_Container>

' Khai báo thư viện Sprites Icon
!define DEVICONS https://raw.githubusercontent.com/tupadr3/plantuml-icon-font-sprites/master/devicons
!define FONTAWESOME https://raw.githubusercontent.com/tupadr3/plantuml-icon-font-sprites/master/font-awesome-5
!include DEVICONS/react.puml
!include DEVICONS/java.puml
!include DEVICONS/postgresql.puml
!include DEVICONS/redis.puml
!include FONTAWESOME/users.puml

LAYOUT_LEFT_RIGHT()
SHOW_PERSON_OUTLINE()

Person(customer, "Khách Hàng", "Người đặt mua sản phẩm", $sprite="users")

System_Boundary(c1, "Hệ Thống Quản Lý Kế Toán & Đơn Hàng") {
    Container(spa, "Single-Page App", "React, Vite", "Giao diện quản lý nghiệp vụ", $sprite="react")
    Container(gateway, "API Gateway", "Spring Cloud Gateway", "Điều hướng route & xác thực tập trung", $sprite="java")
    Container(iam, "IAM Service", "Spring Boot", "Quản lý người dùng, phân quyền, menu", $sprite="java")
    Container(acct, "Accounting Service", "Spring Boot", "Đơn hàng, kho, CSKH, đối soát", $sprite="java")
    
    ContainerDb(db, "Relational Database", "PostgreSQL", "Lưu trữ đơn hàng và giao dịch", $sprite="postgresql")
    ContainerDb(cache, "In-Memory Cache", "Redis", "Khóa phân tán và bộ đệm đơn", $sprite="redis")
}

System_Ext(jnt, "Hệ Thống J&T Philippines", "Bưu cục giao hàng đối tác")

Rel(customer, spa, "Truy cập & Thao tác", "HTTPS")
Rel(spa, gateway, "Gọi API", "JSON/HTTPS")
Rel(gateway, iam, "Xác thực JWT", "HTTP")
Rel(gateway, acct, "Điều phối yêu cầu", "HTTP")

Rel(acct, db, "Đọc/Ghi dữ liệu", "JDBC")
Rel(acct, cache, "Cache & Distributed Lock", "RESP")
Rel(acct, jnt, "Đẩy vận đơn & Tra cứu hành trình", "REST API")

@enduml
```

---

## 3. Quy Ước Thiết Kế Cho AI Agent

1. **Luôn mô tả công nghệ:** Mỗi `Container(...)` bắt buộc phải có tham số thứ 3 là công nghệ (ví dụ: `"React, Vite"`, `"Spring Boot 3"`, `"PostgreSQL 16"`).
2. **Luôn ghi rõ giao thức kết nối:** Mọi liên kết `Rel(from, to, "Mô tả", "Giao thức")` phải chỉ rõ giao thức (ví dụ: `"JSON/HTTPS"`, `"JDBC"`, `"gRPC"`, `"AMQP"`).
3. **Màu sắc và phân vùng:** Sử dụng `System_Boundary(...)` để phân chia ranh giới giữa các service nội bộ và đối tác bên ngoài (`System_Ext`).
