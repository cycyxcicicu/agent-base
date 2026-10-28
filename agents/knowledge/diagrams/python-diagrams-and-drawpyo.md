# Hướng Dẫn Tự Động Hóa Vẽ Sơ Đồ Bằng Python (Diagrams & Drawpyo)

> **Loại: tham khảo.** Hướng dẫn công cụ vẽ sơ đồ, không phải nguồn luật. Khi khác `AGENTS.md`, vai trò hoặc `agents/protocols/` thì theo các nơi đó (`agents/protocols/source-precedence.md`).
> **Khác với chuẩn:** `diagrams` và `drawpyo` là gói PyPI bên thứ ba, chưa cài trong khung: **hỏi người dùng trước khi `pip install`** (`AGENTS.md` mục 0). Chuẩn nội dung sơ đồ: `../srs/chuan-ve-so-do.md`; công cụ nguồn của dự án: `quy-uoc-draw-io-va-archify.md`; phần chữ đi kèm sơ đồ: `mo-ta-hoat-dong-so-do.md`.

> **Mã định danh:** `python-diagrams-and-drawpyo`  
> **Chuyên mục:** Kiến trúc, Trực quan hóa & Vẽ sơ đồ tự động  
> **Trạng thái:** `draft` (Chờ nghiệm thu con người)  

Đối với các AI Agent có khả năng thực thi code/tool, cách tiếp cận an toàn và chất lượng cao nhất là **viết mã Python để thư viện chuyên dụng tự động tính toán hình học**.

---

## 1. Thư Viện Python `diagrams` (mingrammer/diagrams)

Thư viện `diagrams` là chuẩn mực vẽ kiến trúc hạ tầng trong Python (dựa trên Graphviz). Thư viện tích hợp sẵn biểu tượng vector độ nét cao của AWS, GCP, Azure, Kubernetes, và On-Premise (PostgreSQL, Redis, RabbitMQ, Nginx...).

### 1.1. Mã Nguồn Mẫu Vẽ Kiến Trúc GDT

```python
# generate_architecture.py
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Users
from diagrams.onprem.network import Internet
from diagrams.programming.framework import Spring
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Rabbitmq

with Diagram("Kien Truc He Thong Accounting", show=False, direction="LR"):
    users = Users("Nhan Vien / Khach Hang")
    
    with Cluster("VPC Production"):
        gateway = Spring("API Gateway\n(Port 8080)")
        
        with Cluster("Microservices"):
            iam = Spring("IAM Service\n(Port 8100)")
            acct = Spring("Accounting Service\n(Port 8200)")
            
        with Cluster("Data Tier"):
            db = PostgreSQL("PostgreSQL Master")
            cache = Redis("Redis Cache & Lock")
            mq = Rabbitmq("RabbitMQ Events")

    users >> Edge(label="HTTPS") >> gateway
    gateway >> iam
    gateway >> acct
    
    acct >> db
    acct >> cache
    acct >> mq
```

**Kết quả:** Xuất thẳng ra file ảnh PNG chất lượng cao, căn chỉnh thẳng hàng, không bao giờ bị đè chữ!

---

## 2. Thư Viện Python `drawpyo` — Sinh File `.drawio` Chỉnh Sửa Tay Được

Khi người dùng yêu cầu: *"Tôi muốn một file `.drawio` để tôi mở bằng phần mềm Draw.io kéo thả thêm"*, Agent nên sử dụng thư viện **`drawpyo`** thay vì viết tay XML thô.

### 2.1. Mã Nguồn Mẫu Với Drawpyo

```python
# generate_drawio_file.py
import drawpyo
from drawpyo.diagram_types import TreeDiagram

# 1. Khởi tạo biểu đồ dạng cây tự động căn chỉnh vị trí (Tree Diagram)
tree = TreeDiagram(
    file_path="./docs/design",
    file_name="he_thong_kho.drawio",
    direction="right",
    level_spacing=100,
    item_spacing=60
)

# 2. Tạo nút gốc (Root Node)
gateway = drawpyo.diagram.Object(
    value="Spring Cloud API Gateway",
    shape="rounded_rectangle",
    fill_color="#ffe6cc",
    stroke_color="#d79b00"
)
tree.add_root(gateway)

# 3. Tạo các nút con (Child Nodes)
iam = drawpyo.diagram.Object(
    value="IAM Service (Auth/Menu)",
    shape="rounded_rectangle",
    fill_color="#dae8fc",
    stroke_color="#6c8ebf"
)
acct = drawpyo.diagram.Object(
    value="Accounting Service (Don/Kho)",
    shape="rounded_rectangle",
    fill_color="#d5e8d4",
    stroke_color="#82b366"
)

tree.add_connection(gateway, iam)
tree.add_connection(gateway, acct)

# 4. Xuất file .drawio hoàn chỉnh
tree.write()
print("Đã tạo thành công file he_thong_kho.drawio chuẩn định dạng XML!")
```

**Ưu điểm:** `drawpyo` tự động tính tọa độ cấp cây (`TreeDiagram`), đóng gói thành file `.drawio` chuẩn, người dùng chỉ việc mở Draw.io lên là có sơ đồ đẹp ngay.
