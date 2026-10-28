---
name: archify
description: Generate polished, interactive HTML and SVG architecture, workflow, sequence, data-flow, and state machine diagrams from typed JSON specifications.
triggers:
  - system map
  - architecture diagram
  - interactive diagram
  - data flow diagram
  - sequence diagram
  - workflow diagram
  - state diagram
  - erd diagram
  - table diagram
---

# Archify (Interactive System Architecture & Diagram Compiler)

> [!IMPORTANT]
> **Quy định bắt buộc của dự án**:
> 1. Mọi sơ đồ hệ thống, quy trình nghiệp vụ (Business Flow / Activity), trình tự gọi API (Sequence), luồng dữ liệu (Dataflow), lược đồ bảng (Table / ERD) và vòng đời trạng thái (State Lifecycle) **BẮT BUỘC** phải được biên dịch bằng **Archify Engine** từ file **Typed JSON IR**. Tuyệt đối không dùng Mermaid thô hoặc HTML chắp vá.
> 2. Công cụ biên dịch đã được tích hợp sẵn trong repo (độc lập 100%, chạy trên mọi máy qua Node.js >= 18):
>    - Shell/Script: `node scripts/run-archify.mjs <command>` (hoặc wrapper `.\archify` trên Windows, `./archify` trên macOS/Linux).
> 3. Toàn bộ file JSON đặc tả nguồn và file HTML kết xuất phải được lưu trữ trong thư mục chính duy nhất:
>    `docs/diagrams/`
> 4. Mọi sơ đồ tạo mới phải được gắn liên kết vào trang mục lục trung tâm:
>    `docs/diagrams/index.html`

---

## 1. Bản Đồ 5 Loại Sơ Đồ (Type Router)

| Loại (`<type>`) | Dùng cho trường hợp nào | Cấu trúc file mẫu trong repo |
|---|---|---|
| **`architecture`** | Kiến trúc tổng thể, hạ tầng cloud, ranh giới an toàn, cụm microservices, cấu trúc bảng dữ liệu (Table Schema / ERD) | `tools/archify/examples/web-app.architecture.json`<br>`docs/diagrams/humana-system.architecture.json` |
| **`workflow`** | Quy trình nghiệp vụ (Business Flows), biểu đồ hoạt động (Activity Diagrams), luồng phê duyệt, Tool Call Agent, Runbook CI/CD | `tools/archify/examples/agent-tool-call.workflow.json`<br>`tools/archify/examples/incident-response.workflow.json` |
| **`sequence`** | Trình tự gọi API theo thời gian thực, chuỗi xử lý Request/Response, luồng bất đồng bộ (SSE/Async worker), Trace log | `tools/archify/examples/cache-miss-request.sequence.json`<br>`tools/archify/examples/async-job-roundtrip.sequence.json` |
| **`dataflow`** | Đường ống dữ liệu (Data Pipelines), xử lý ETL/ELT, luồng RAG & Vector Embeddings, quản trị dòng dữ liệu (Lineage) | `tools/archify/examples/product-analytics.dataflow.json`<br>`tools/archify/examples/event-stream.dataflow.json` |
| **`lifecycle`** | Vòng đời trạng thái (State Machine), chuyển dịch trạng thái thực thể (Candidate, Booking, Quiz, Ticket), Retry / Terminal states | `tools/archify/examples/agent-run.lifecycle.json`<br>`tools/archify/examples/deployment-release.lifecycle.json` |

---

## 2. Quy Tắc Biên Dịch Từ Mermaid Sang Archify

Khi đọc sơ đồ cũ viết bằng Mermaid, không vẽ lại giao diện của Mermaid mà trích xuất ngữ nghĩa và cấu trúc sang Archify Typed JSON:
* `flowchart` / `graph` ➔ Chuyển thành **`workflow`** (dùng `schema_version: 2`) hoặc **`architecture`** (nếu là bản đồ thành phần).
* `sequenceDiagram` ➔ Chuyển thành **`sequence`**: Tác nhân thành `participants`, mũi tên thành `messages`, khối xử lý thành `activations`.
* `stateDiagram` / `stateDiagram-v2` ➔ Chuyển thành **`lifecycle`**: Các trạng thái và điều kiện chuyển dịch thành `states` và `transitions`.
* ERD / Table Relations ➔ Chuyển thành **`architecture`** (các node nhóm theo bảng, có trường dữ liệu và quan hệ FK).

---

## 3. Quy Chuẩn Thiết Kế & Thuộc Tính Bắt Buộc (Authoring Invariants)

### A. Định danh & Thành phần Node (Component Types)
* `type`: Bắt buộc thuộc các loại chuẩn:
  - `frontend`: Giao diện người dùng, Web app, Mobile app, Form UI.
  - `backend`: API Gateway, Backend service, Controller, Worker.
  - `database`: PostgreSQL, Redis, Cache, Storage, Vector DB.
  - `security`: Auth, Policy Guard, PII Masking, Rate Limiter, Rule Engine.
  - `messagebus`: Queue, Event Bus, Kafka, Redis/arq, Webhook.
  - `cloud`: Cloud provider, CDN, External API, Google Meet, S3.
  - `external`: Người dùng, Khách hàng, Ứng viên, Đối tác bên ngoài.

### B. Kiểu Đường Nối (Edge Variants & Roles)
* `variant`:
  - `default`: Luồng thông thường.
  - `emphasis`: Luồng chính (Happy Path), hành động trọng tâm.
  - `security`: Luồng kiểm tra an ninh, xác thực JWT, RBAC.
  - `dashed`: Luồng bất đồng bộ, event emit, notification ngầm.
* `role`:
  - `error`: Nhánh lỗi, từ chối, rollback (tự động đổi màu cảnh báo).
  - `branch`: Nhánh rẽ điều kiện.

### C. Quy chuẩn Phân Làn (Swimlanes & Phases cho Workflow v2)
* Sử dụng `schema_version: 2`.
* `lanes`: Phân chia tối thiểu 3-5 làn rõ ràng (ví dụ: `ui` - Người dùng/Giao diện, `backend` - Xử lý nghiệp vụ, `policy` - Kiểm tra & Ngoại lệ, `storage` - Dữ liệu & Nhật ký).
* `phases`: Chia các giai đoạn theo cột (`fromCol` đến `toCol`).
* `mainPath`: Mảng ID các node chính tạo thành Happy Path xuyên suốt từ đầu đến cuối.

### D. Quy chuẩn Sơ đồ Tuần tự (Sequence)
* `participants`: Danh sách các bên tham gia theo thứ tự từ trái sang phải.
* `messages`: Mỗi bước có `y` tăng dần (ví dụ cách nhau 25-35px), có nhãn rõ ràng kèm protocol (`GET /api`, `200 JSON`).
* `activations`: Khối chữ nhật thể hiện thời gian tiến trình sở hữu tài nguyên.
* `cards`: Tối thiểu 2 thẻ tổng kết ở cuối (Happy Path và Fallback / Security Policy).

### E. Quy chuẩn Vòng đời Trạng thái (Lifecycle)
* Cột chính (`0..4`) dành cho luồng trạng thái thành công.
* Hàng bên dưới dành cho trạng thái ngoại lệ (`failure`), chờ (`waiting`) và kết thúc (`terminal`).

---

## 4. Vị Trí Schema Chuẩn & File Mẫu Trong Repo

Khi tạo mới một sơ đồ JSON, Agent **BẮT BUỘC ĐỌC TRỰC TIẾP** schema và ví dụ tương ứng:
* **JSON Schemas:**
  - `tools/archify/schemas/workflow.schema.json`
  - `tools/archify/schemas/sequence.schema.json`
  - `tools/archify/schemas/lifecycle.schema.json`
  - `tools/archify/schemas/dataflow.schema.json`
  - `tools/archify/schemas/architecture.schema.json`
  - `tools/archify/schemas/common.schema.json`
* **Ví dụ mẫu hoàn chỉnh:**
  - `tools/archify/examples/agent-tool-call.workflow.json`
  - `tools/archify/examples/cache-miss-request.sequence.json`
  - `tools/archify/examples/agent-run.lifecycle.json`
  - `tools/archify/examples/product-analytics.dataflow.json`
  - `tools/archify/examples/web-app.architecture.json`

---

## 5. Quy Trình 3 Bước Tự Động (Fast Authoring Loop)

### Bước 1: Viết Candidate JSON
Tạo file JSON đặc tả đặt tại: `docs/diagrams/<tên-sơ-đồ>.<type>.json`.
Đặt `meta.quality_profile: "standard"` hoặc `"showcase"`.

### Bước 2: Kiểm Tra Hợp Lệ (Validate Bắt Buộc)
Trước khi bàn giao hoặc render, chạy lệnh validate:
```powershell
node scripts/run-archify.mjs validate <type> docs/diagrams/<file>.<type>.json
```
Lệnh phải trả về `0 errors`. Nếu có lỗi schema hoặc va chạm vị trí (collision), đọc mã lỗi và sửa lại file JSON.

### Bước 3: Render Ra HTML & Gắn Vào Mục Lục
Biên dịch ra file HTML hoàn chỉnh:
```powershell
node scripts/run-archify.mjs render <type> docs/diagrams/<file>.<type>.json docs/diagrams/<file>.html
```
Sau khi file HTML sinh ra, cập nhật đường dẫn vào `docs/diagrams/index.html`.
