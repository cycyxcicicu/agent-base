# Ma Trận Quyết Định Công Cụ Vẽ Sơ Đồ Kiến Trúc Cho AI Agent

> **Loại: tham khảo.** Hướng dẫn công cụ vẽ sơ đồ, không phải nguồn luật. Khi khác `AGENTS.md`, vai trò hoặc `agents/protocols/` thì theo các nơi đó (`agents/protocols/source-precedence.md`).
> **Khác với chuẩn:** Ma trận bên dưới là lựa chọn rộng; **công cụ nguồn của dự án đi trước** (mục 0). Chuẩn nội dung sơ đồ: `../srs/chuan-ve-so-do.md`; công cụ nguồn của dự án: `quy-uoc-draw-io-va-archify.md`; phần chữ đi kèm sơ đồ: `mo-ta-hoat-dong-so-do.md`.

> **Mã định danh:** `diagrams-cheatsheet-and-decision-matrix`  
> **Chuyên mục:** Kiến trúc, Trực quan hóa & Vẽ sơ đồ tự động  
> **Trạng thái:** `draft` (Chờ nghiệm thu con người)  

---

## 0. Thứ Tự Áp Dụng: Chuẩn Dự Án Đi Trước

Đã đối chiếu với cách dự án đang vẽ (`quy-uoc-draw-io-va-archify.md`). Chọn công cụ theo thứ tự sau, chỉ xuống bảng ma trận ở mục 2 khi dự án chưa có lựa chọn cho loại sơ đồ đó:

| Loại sơ đồ | Công cụ nguồn của dự án (ưu tiên) | Công cụ bổ sung khi cần |
|---|---|---|
| Activity Swimlane, use case, luồng màn hình | draw.io `.drawio` (một file nhiều trang mỗi chức năng) | Draw.io CSV để sinh bản nháp có icon (`drawio-csv-autolayout.md`) |
| ERD, sequence, vòng đời trạng thái | archify (`.json`, sinh lại khi sửa) | DBML để thiết kế schema bằng chữ; Mermaid cho bản nhỏ trong md |
| Thành phần, triển khai, kiến trúc hệ thống | draw.io hoặc archify `architecture` | C4-PlantUML, Structurizr DSL, D2, Python `diagrams` (hạ tầng cloud) khi dự án chọn |
| Quy trình nghiệp vụ nhiều bộ phận (Swimlane) | draw.io (Swimlane) | BPMN 2.0 khi cần chuẩn quốc tế |
| Sơ đồ nhỏ nằm trong md | Mermaid | - |

Hai quy tắc đi kèm, áp dụng cho mọi công cụ:
1. **Mỗi sơ đồ có phần mô tả hoạt động bằng chữ** với số bước khớp sơ đồ (`mo-ta-hoat-dong-so-do.md`). Đọc nhanh một `.drawio`: `python scripts/diagram-describe.py <file.drawio>`.
2. **Tọa độ do bộ dàn trang tính** (mục 1 dưới đây). Với `.drawio`, dự án để agent khai báo làn và hàng, script tính tọa độ; viết XML tay chỉ cho sơ đồ nhỏ hoặc sửa file đã có.

---

## 1. Nguyên Tắc Cốt Lõi: Tránh Bẫy Tọa Độ (Coordinate Traps)

> [!CAUTION]
> **Rủi ro lớn nhất của LLM:** LLM tính toán không gian hình học 2D rất kém. Việc yêu cầu Agent tự sinh mã XML (`mxGraphModel`) của Draw.io kèm tọa độ (`x, y, width, height`) có xác suất hỏng bố cục lên tới 85% (đè chữ, lệch dây nối, hộp lồng nhau sai tỷ lệ).

**Quy tắc vàng cho Agent:** Luôn sử dụng các công cụ có **Auto-Layout Engine (Bộ dàn trang tự động)**. Agent chỉ khai báo các nút (Nodes), mối quan hệ (Connections) và biểu tượng (Icons); thuật toán đồ thị sẽ tự động tính toán tọa độ pixel.

---

## 2. Ma Trận Lựa Chọn Công Cụ (Decision Matrix)

| Mục tiêu sơ đồ | Công cụ khuyến nghị | Định dạng đầu ra | Ưu điểm cốt lõi | Nhược điểm / Lưu ý |
|---|---|---|---|---|
| **Hiển thị trực tiếp trong Markdown/PR/Docs** | **Mermaid.js** | Khối mã ` ```mermaid ` | Render trực tiếp trên GitHub/GitLab/VS Code, hỗ trợ Iconify từ v11+ | Không chỉnh sửa kéo thả trực tiếp được |
| **Sơ đồ Kiến trúc Hệ thống có Icon Cloud (AWS/GCP/K8s) mở trên Draw.io** | **Draw.io CSV Import** | Đoạn text CSV (Header `# style`) | Draw.io tự động tính layout, dùng toàn bộ kho Icon chuẩn của Draw.io | Người dùng copy paste vào Draw.io qua `Arrange -> Insert -> Advanced -> CSV` |
| **Kiến trúc hạ tầng Cloud xuất ra ảnh chất lượng cao tự động** | **Python `diagrams`** | Script Python $\rightarrow$ `.png` | Tự động căn chỉnh hoàn hảo bằng Graphviz, có sẵn hàng trăm icon AWS, GCP, K8s, PostgreSQL | Cần môi trường Python có cài Graphviz |
| **Sinh trực tiếp file `.drawio` bằng Python để chỉnh sửa tay** | **Python `drawpyo`** | Script Python $\rightarrow$ `.drawio` | Xuất thẳng file XML Draw.io chuẩn không bị lỗi cú pháp | Cần code Python định nghĩa hierarchy/tree |
| **Thiết kế Cơ sở Dữ liệu (ERD / Schema Relational)** | **DBML** | Khối text `.dbml` | Ngôn ngữ chuyên dụng cho CSDL, hỗ trợ 1-1, 1-n, n-n, composite key | Cần công cụ dbdocs / dbdiagram.io để render |
| **Kiến trúc phân tầng C4 (Context, Container, Component)** | **C4-PlantUML** | Khối text `@startuml ... @enduml` | Chuẩn kiến trúc doanh nghiệp, có thư viện sprite icon phong phú | Cần PlantUML server hoặc extension VS Code |
| **Kiến trúc mạng/luồng tự động dàn trang hiện đại** | **D2 Language** | Khối text `.d2` | Thuật toán dàn trang tốt hơn Graphviz/Mermaid, hỗ trợ icon và container lồng | Cần cài binary D2 CLI |
| **Quy trình nghiệp vụ chuẩn doanh nghiệp** | **BPMN 2.0 (Camunda)** | Khối XML BPMN | Chuẩn quốc tế OMG cho quy trình nghiệp vụ (Exclusive Gateway, Service Task) | Cần Camunda Modeler để mở |

---

## 3. Bản Đồ Hướng Dẫn Chi Tiết (Navigation Map)

- [Draw.io CSV Auto-Layout Guide](drawio-csv-autolayout.md): Cú pháp CSV tự động dàn trang có icon trong Draw.io.
- [Draw.io Icon Index](drawio-icons-index.md): Danh mục tên Shape và Icon chuẩn trong Draw.io (AWS4, GCP2, Azure, K8s, Cisco).
- [Mermaid Syntax Guide](mermaid-syntax-guide.md): Cú pháp Mermaid v11, architecture-beta và Iconify icons.
- [C4-PlantUML Guide](c4-plantuml-guide.md): C4 Model và Sprites icon AWS/Azure/GCP/Kubernetes.
- [DBML & D2 Guide](dbml-and-d2-guide.md): Thiết kế ERD với DBML và kiến trúc với D2.
- [Python Diagrams & Drawpyo Guide](python-diagrams-and-drawpyo.md): Tự động hóa vẽ sơ đồ bằng code Python.
