> **Loại: tham khảo.**
> Nguồn: tách từ srs-fdd-writing-standard.md mục E, L (phần 1)

# Chuẩn sơ đồ & Vị trí dòng neo Excel SRS_FDD — Phần 1: Sơ đồ Kiến trúc & Hệ thống

## E. Sơ đồ
- Các loại sơ đồ của mẫu + cách vẽ chuẩn: `doc/governance/templates/03-srs-fdd-template-v3/md/so-do-trong-mau.md` (mục 3). Quy tắc chính: **số bước trong sơ đồ khớp số bước trong bảng use-case; số vòng trong mockup khớp số service**; sequence gom bước thành *transaction* có ghi chú; ERD dùng tên bảng/ cột thật; không dùng ví dụ của dự án khác.
- SRS dạng md: **ưu tiên Mermaid** (`flowchart`, `sequenceDiagram`, `erDiagram`, `stateDiagram-v2`) cho sơ đồ mới; hỏi người dùng nếu chưa chắc trình xem md hiển thị được. Sơ đồ có sẵn (drawio/ ảnh) thì **dẫn đường dẫn**, không mô tả bịa lại.
- Tối thiểu mỗi chức năng: luồng (use-case/ activity), sequence (≥ 2 thành phần gọi nhau), ERD các bảng chạm tới, wireframe (dẫn mockup), state diagram nếu đổi trạng thái đơn.

## L. Bản Đồ 13 Sơ Đồ & Vị Trí Dòng Neo Chuẩn Trong File Excel SRS_FDD (Sơ đồ 1 đến 7)

Khi xuất hoặc điền vào file Excel SRS_FDD (`SRS_FDD_Template-v3.0.xlsx` hoặc `_SRS_FDD_AI-Agent-Copilot.xlsx`), Agent BẮT BUỘC tuân thủ vị trí neo và bảng thuyết minh đi kèm:

| STT | Tên Sơ Đồ | Sheet Nằm Trong | Dòng Neo (Row) | Bảng Thuyết Minh Bằng Chữ Đi Kèm Dưới Ảnh |
|---|---|---|---|---|
| **1** | **Luồng nghiệp vụ tổng quan (BPMN)** | `Component_Detail_Design` | Dòng 12 (Cột G) | Bảng bơi làn 4 cột: *Bước, Làn (Actor), Hành động, Dữ liệu, Bước kế tiếp*. |
| **2** | **Sơ đồ phân rã WBS dạng cây** | `Component_Detail_Design` | Dòng 26 | Cây phân cấp: Dự án $\rightarrow$ Phase $\rightarrow$ Work Package $\rightarrow$ Tasks. |
| **3** | **Bản đồ luồng màn hình (Screen Flow)** | `Component_Detail_Design` | Dòng 73 | Sơ đồ chuyển trang: Mã màn hình nguồn $\rightarrow$ Sự kiện bấm $\rightarrow$ Màn đích. |
| **4** | **Wireframe Board (Figma Overview)** | `Component_Detail_Design` | Dòng 95 | Bảng tổng thể các màn hình thu nhỏ nối với nhau. |
| **5** | **Package & Component hệ thống** | `Component_Detail_Design` | Dòng 138 | Khối module (A..L), mũi tên quan hệ "Use" giữa các service. |
| **6** | **Kiến trúc phần mềm chi tiết (Software Arch)** | `Component_Detail_Design` | Dòng 112 | Phân tầng: Interaction $\rightarrow$ Orchestrator $\rightarrow$ Core $\rightarrow$ DB kèm 12 bước đánh số. |
| **7** | **Sơ đồ Triển khai hạ tầng (Deployment)** | `Component_Detail_Design` | Dòng 245 | Internet $\rightarrow$ Firewall $\rightarrow$ Nginx Proxy $\rightarrow$ Containers $\rightarrow$ DB. |
