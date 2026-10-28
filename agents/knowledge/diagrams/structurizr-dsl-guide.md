# Cẩm Nang Ngôn Ngữ Structurizr DSL (Chuẩn C4 Model Của Simon Brown)

> **Loại: tham khảo.** Hướng dẫn công cụ vẽ sơ đồ, không phải nguồn luật. Khi khác `AGENTS.md`, vai trò hoặc `agents/protocols/` thì theo các nơi đó (`agents/protocols/source-precedence.md`).
> **Khác với chuẩn:** Cần Structurizr (Lite hoặc CLI) để dựng góc nhìn, chưa có trong khung; chỉ dùng khi dự án chọn mô hình C4 bằng DSL. Chuẩn nội dung sơ đồ: `../srs/chuan-ve-so-do.md`; công cụ nguồn của dự án: `quy-uoc-draw-io-va-archify.md`; phần chữ đi kèm sơ đồ: `mo-ta-hoat-dong-so-do.md`.

> **Mã định danh:** `structurizr-dsl-guide`  
> **Chuyên mục:** Kiến trúc, Trực quan hóa & Vẽ sơ đồ tự động  
> **Trạng thái:** `draft` (Chờ nghiệm thu con người)  

---

## 1. Tổng Quan Về Structurizr DSL

**Structurizr DSL** (Domain Specific Language) là ngôn ngữ chính thức được sáng tạo bởi Simon Brown (cha đẻ của mô hình C4) nhằm biến kiến trúc phần mềm thành mã nguồn (**Architecture as Code**).
- Thay vì vẽ các hộp và đường rời rạc, Structurizr DSL định nghĩa một **Mô hình kiến trúc duy nhất (Single Model)**.
- Từ mô hình duy nhất đó, hệ thống tự động suy ra nhiều góc nhìn (Views) khác nhau: System Context, Container, Component, Dynamic và Deployment.

---

## 2. Cú Pháp Khai Báo Structurizr DSL Chuẩn

Một file Structurizr DSL (`workspace.dsl`) bao gồm 3 khối chính:
1. **`model`**: Định nghĩa con người, hệ thống, container, component và mối quan hệ.
2. **`views`**: Định nghĩa các góc nhìn cần kết xuất và bộ lọc hiển thị.
3. **`configuration` / `styles`**: Định nghĩa màu sắc, hình dáng và icon.

### 2.1. File Mẫu Hoàn Chỉnh: Hệ Thống Đơn Hàng & Kế Toán GDT

```dsl
workspace "GDT Accounting & Order System" "Kiến trúc hệ thống quản lý đơn hàng và kế toán" {

    model {
        // 1. Con người (Actors / People)
        customer = person "Khách Hàng" "Người mua hàng và theo dõi đơn" "Customer"
        staff = person "Nhân Viên Kế Toán" "Quản lý đơn hàng, xuất hóa đơn và đối soát" "Internal"

        // 2. Hệ thống phần mềm chính (Software System)
        gdtSystem = softwareSystem "Hệ Thống GDT" "Nền tảng xử lý đơn hàng, kho và kế toán" {
            // Level 2: Containers
            webApp = container "Web Frontend" "Giao diện quản lý đơn hàng và kế toán" "React, Vite" "WebBrowser"
            apiGateway = container "API Gateway" "Cổng định tuyến, xác thực và rate limiting" "Spring Cloud Gateway"
            
            iamService = container "IAM Service" "Dịch vụ xác thực người dùng, phân quyền và menu" "Spring Boot, Java 21"
            accountingService = container "Accounting Service" "Quản lý vòng đời đơn hàng, kho hàng và đối soát" "Spring Boot, Java 21" {
                // Level 3: Components
                orderController = component "OrderController" "Cung cấp REST API xử lý đơn hàng" "Spring MVC"
                orderService = component "OrderService" "Xử lý logic nghiệp vụ và luồng trạng thái đơn" "Spring Service"
                orderRepository = component "OrderRepository" "Truy vấn và lưu vết đơn hàng" "Spring Data JPA"
            }

            database = container "Database Cluster" "Lưu trữ dữ liệu quan hệ chính" "PostgreSQL 16" "Database"
            cache = container "Cache & Lock" "Bộ nhớ đệm và khóa phân tán đơn hàng" "Redis 7" "Database"
            messageQueue = container "Event Broker" "Truyền tải sự kiện đồng bộ trạng thái đơn" "RabbitMQ 3" "Queue"
        }

        // 3. Hệ thống bên ngoài (External Systems)
        jntSystem = softwareSystem "J&T Express Philippines" "Hệ thống bưu cục vận chuyển đối tác" "External"

        // 4. Các mối quan hệ (Relationships)
        customer -> webApp "Đặt hàng và tra cứu" "HTTPS"
        staff -> webApp "Quản lý đơn và đối soát" "HTTPS"
        webApp -> apiGateway "Gửi API Requests" "JSON/HTTPS"
        
        apiGateway -> iamService "Xác thực JWT Bearer" "HTTP"
        apiGateway -> accountingService "Điều hướng yêu cầu nghiệp vụ" "HTTP"

        accountingService -> database "Đọc/Ghi dữ liệu giao dịch" "JDBC (HikariCP)"
        accountingService -> cache "Distributed Lock & Cache đơn" "RESP"
        accountingService -> messageQueue "Publish sự kiện OrderStatusChanged" "AMQP"
        accountingService -> jntSystem "Đẩy vận đơn và đồng bộ hành trình" "REST API"

        // Quan hệ nội bộ Component
        orderController -> orderService "Gọi nghiệp vụ"
        orderService -> orderRepository "Lưu trữ dữ liệu"
        orderRepository -> database "Thực thi SQL"
    }

    views {
        // Góc nhìn Level 1: System Context
        systemContext gdtSystem "SystemContext" {
            include *
            autolayout lr
        }

        // Góc nhìn Level 2: Containers
        container gdtSystem "Containers" {
            include *
            autolayout tb
        }

        // Góc nhìn Level 3: Components
        component accountingService "AccountingComponents" {
            include *
            autolayout tb
        }

        // Định nghĩa Styles hiển thị
        styles {
            element "Person" {
                shape Person
                background #08427B
                color #ffffff
            }
            element "Software System" {
                background #1168BD
                color #ffffff
            }
            element "Container" {
                background #438DD5
                color #ffffff
            }
            element "Database" {
                shape Cylinder
                background #85BEE9
                color #000000
            }
            element "External" {
                background #999999
                color #ffffff
            }
        }
    }
}
```

---

## 3. Cách Xuất Sơ Đồ Từ Structurizr DSL

1. **Công cụ Structurizr CLI**:
   - Xuất sang PlantUML: `structurizr-cli export -workspace workspace.dsl -format plantuml`
   - Xuất sang Mermaid: `structurizr-cli export -workspace workspace.dsl -format mermaid`
   - Xuất sang D2: `structurizr-cli export -workspace workspace.dsl -format d2`
2. **Structurizr Lite**: Chạy Docker container để hiển thị sơ đồ tương tác trực tiếp trên trình duyệt qua cổng 8080.
