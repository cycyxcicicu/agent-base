# Hướng Dẫn Tự Động Hóa Vẽ Sơ Đồ Draw.io Bằng CSV Auto-Layout

> **Loại: tham khảo.** Hướng dẫn công cụ vẽ sơ đồ, không phải nguồn luật. Khi khác `AGENTS.md`, vai trò hoặc `agents/protocols/` thì theo các nơi đó (`agents/protocols/source-precedence.md`).
> **Khác với chuẩn:** Dùng để sinh nhanh **bản nháp** `.drawio` có icon. Sau khi người đã chỉnh tay, `.drawio` là nguồn, không sinh lại đè (`quy-uoc-draw-io-va-archify.md` mục 1). Chuẩn nội dung sơ đồ: `../srs/chuan-ve-so-do.md`; công cụ nguồn của dự án: `quy-uoc-draw-io-va-archify.md`; phần chữ đi kèm sơ đồ: `mo-ta-hoat-dong-so-do.md`.

> **Mã định danh:** `drawio-csv-autolayout`  
> **Chuyên mục:** Kiến trúc, Trực quan hóa & Vẽ sơ đồ tự động  
> **Trạng thái:** `draft` (Chờ nghiệm thu con người)  

---

## 1. Giới Thiệu Tính Năng CSV Import Của Draw.io

Thay vì cố gắng sinh hàng trăm dòng XML `mxGraphModel` phức tạp kèm tọa độ hình học thủ công, Agent chỉ cần sinh một đoạn **CSV có gắn Header Cấu Hình**.

Khi người dùng mở Draw.io (trên web hoặc desktop) và chọn:
👉 **`Arrange` $\rightarrow$ `Insert` $\rightarrow$ `Advanced` $\rightarrow$ `CSV...`** (hoặc dán trực tiếp đoạn text CSV vào canvas), Draw.io sẽ:
1. Đọc cấu hình style và kết nối ở phần Header.
2. Tự động tra cứu hình dáng/icon trong kho stencil.
3. Kích hoạt bộ thuật toán **Auto-Layout (Dàn trang tự động)** để xếp vị trí các hộp, tính toán khoảng cách và uốn dây nối đẹp mắt, không bao giờ bị đè chữ hay lệch tọa độ.

---

## 2. Cấu Trúc Header Cấu Hình CSV Chuẩn

Đầu file CSV bắt đầu bằng các dòng `#` để cấu hình quy tắc dựng hình:

```csv
## 1. Định nghĩa nhãn hiển thị (HTML formatting)
# label: <div style="font-weight:bold;font-size:13px;">%name%</div><div style="font-size:11px;color:#555;">%desc%</div>

## 2. Định nghĩa hình dạng và Icon (gán động từ cột shape, fill, stroke)
# style: shape=%shape%;fillColor=%fill%;strokeColor=%stroke%;html=1;whiteSpace=wrap;verticalAlign=middle;

## 3. Định nghĩa cơ chế nối dây tự động (từ cột refs sang cột id)
# connect: {"from": "refs", "to": "id", "style": "curved=1;endArrow=block;endFill=1;strokeWidth=2;strokeColor=#4A90E2;"}

## 4. Kích thước mặc định và khoảng cách giữa các node
# width: auto
# height: auto
# padding: 15
# nodespacing: 50
# levelspacing: 60

## 5. Thuật toán dàn trang tự động (Auto-Layout)
## Các giá trị hợp lệ: auto | horizontaltree | verticaltree | organic | circle
# layout: horizontaltree

## 6. Các cột chỉ dùng cho cấu hình, không in ra nhãn
# ignore: id,shape,fill,stroke,refs
```

---

## 3. Ví Dụ Thực Tế: Kiến Trúc Microservices Đơn Hàng & Kho

Đoạn mã mẫu sau đây sẵn sàng để Agent sinh ra cho người dùng:

```csv
## GDT Microservices Architecture
# label: <b style="font-size:12px;">%name%</b><br><span style="font-size:10px;color:#666;">%desc%</span>
# style: shape=%shape%;fillColor=%fill%;strokeColor=%stroke%;html=1;whiteSpace=wrap;align=center;verticalLabelPosition=bottom;verticalAlign=top;
# namespace: gdt-arch-
# connect: {"from": "refs", "to": "id", "style": "curved=1;endArrow=block;strokeWidth=1.5;strokeColor=#333333;"}
# width: 60
# height: 60
# nodespacing: 45
# levelspacing: 55
# layout: horizontaltree
# ignore: id,shape,fill,stroke,refs
id,name,shape,fill,stroke,refs,desc
1,Khách Hàng (Web/Mobile),mxgraph.aws4.mobile,#E1D5E7,#9673A6,,Giao diện đặt hàng
2,API Gateway (Port 8080),mxgraph.aws4.api_gateway,#FFE6CC,#D79B00,1,Spring Cloud Gateway
3,IAM Service (Port 8100),mxgraph.aws4.cognito,#F8CECC,#B85450,2,Xác thực & Menu
4,Accounting Service (Port 8200),mxgraph.aws4.ecs,#D5E8D4,#82B366,2,Đơn hàng & Kho
5,PostgreSQL Database,mxgraph.aws4.rds_postgresql,#DAE8FC,#6C8EBF,3;4,CSDL chính
6,Redis Cache & Lock,mxgraph.aws4.elasticache_redis,#FFF2CC,#D6B656,4,Bộ nhớ đệm & Lock đơn
7,RabbitMQ Broker,mxgraph.aws4.mq,#E1D5E7,#9673A6,4,Đồng bộ sự kiện
```

---

## 4. Hướng Dẫn Thao Tác Cho Người Dùng

1. Mở trang web [https://app.diagrams.net](https://app.diagrams.net) (hoặc phần mềm Draw.io Desktop).
2. Tạo một biểu đồ mới (Blank Diagram).
3. Trên thanh công cụ, chọn: **`Arrange` $\rightarrow$ `Insert` $\rightarrow$ `Advanced` $\rightarrow$ `CSV...`**.
4. Xóa nội dung mẫu có sẵn, dán toàn bộ đoạn mã CSV ở trên vào khung và bấm **`Import`**.
5. Draw.io sẽ lập tức vẽ ra toàn bộ hệ thống sơ đồ kiến trúc hoàn chỉnh, căn chỉnh thẳng hàng và gắn đúng Icon chuẩn!
