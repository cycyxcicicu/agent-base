# Cẩm Nang Toàn Diện 22+ Loại Sơ Đồ UML 2.5 & Chuẩn Mực Vẽ Cho AI Agent

**Loại: tham khảo.**
> **Phân vùng**: Architecture & System Design  
> **Phân quyền truy cập (RBAC)**: `["architect", "ba", "designer"]`  
> **Nguồn đối chuẩn**: `https://www.uml-diagrams.org/` & Trạm tri thức cục bộ `assets/uml/`  
> **Sổ bộ ảnh sơ đồ**: `agents/knowledge/IMAGE_REGISTRY.json` (392 ảnh đã lập chỉ mục)

---

## 1. Năm Quy Tắc Bắt Buộc Khi Vẽ Sơ Đồ Trong Dự Án (Hard Constraints)
1. **Phân làn (Swimlane) rõ ràng**: Luôn chia tách rõ rệt giữa Người dùng (Frontend), Hệ thống (Backend Service) và Cơ sở dữ liệu (Database/3rd Party).
2. **Đúng 1 điểm bắt đầu & Đúng 1 điểm kết thúc duy nhất**: Nghiêm cấm sơ đồ có nhiều điểm kết thúc trôi nổi.
3. **Nhánh lỗi bắt buộc màu đỏ (`#dc2626` / `#ff0000`)**: Các nhánh Rollback, Validate thất bại, Timeout phải được làm nổi bật và có mã lỗi.
4. **100% dữ liệu thực từ Code & Database**: Không dùng tên giả định kiểu "Hàm 1", "Bảng A"; phải dùng đúng tên Entity, Endpoint REST, Repository thật.
5. **Luôn đóng gói File DrawIO & Ảnh PNG sắc nét**: Mọi sơ đồ phải lưu mã nguồn tại `doc/features/<UC>/hinh/<UC>.drawio` và xuất ảnh PNG nhúng vào tài liệu Markdown.

---

## 2. Tám Loại Sơ Đồ Cốt Lõi (Core 8) Bắt Buộc Cho Dự Án Thực Chiến

Toàn bộ 392 ảnh mẫu gốc và template DrawIO XML đã được lưu trữ sẵn sàng tại `assets/uml/`:

| STT | Loại Sơ Đồ | Phân Nhóm | Thư Mục Tri Thức Cục Bộ | Ứng Dụng Trong Hồ Sơ Gate 2 |
|---|---|---|---|---|
| 1 | **Class Diagram** | Structure | `ssets/uml/class-diagram/` | Thiết kế Entity JPA, DTOs, Repository, quan hệ Aggregation vs Composition |
| 2 | **Sequence Diagram** | Interaction | `ssets/uml/sequence-diagram/` | Luồng tương tác API, phân mảnh Alt (rẽ nhánh), Loop, Par (song song) |
| 3 | **Activity Diagram** | Behavior | `ssets/uml/activity-diagram/` | Luồng nghiệp vụ, bơi làn đa tầng, rẽ nhánh Decision, gộp luồng Fork/Join |
| 4 | **State Machine Diagram** | Behavior | `ssets/uml/state-machine-diagram/` | Vòng đời đơn hàng, vé, thanh toán (Draft ➔ Pending ➔ Success / Cancelled) |
| 5 | **Use Case Diagram** | Behavior | `ssets/uml/use-case-diagram/` | Biên hệ thống, tác nhân Actor, quan hệ bắt buộc `<<include>>` & mở rộng `<<extend>>` |
| 6 | **Component Diagram** | Structure | `ssets/uml/component-diagram/` | Ranh giới các module phần mềm, Cổng Ports & Connectors (Provided / Required) |
| 7 | **Deployment Diagram** | Structure | `ssets/uml/deployment-diagram/` | Cụm máy chủ K8s, Docker Container Distroless, Database nodes |
| 8 | **Package Diagram** | Structure | `ssets/uml/package-diagram/` | Cấu trúc phân chia packages, namespace code và kiểm soát phụ thuộc |

---

## 3. Danh Mục Sơ Đồ Mở Rộng (22+ Loại Theo Cây Phân Loại UML 2.5)
- **Cấu trúc mở rộng**: `Object Diagram`, `Model Diagram`, `Composite Structure Diagram` (`internal-structure`, `collaboration-use`), `Manifestation Diagram`, `Network Architecture Diagram`, `Profile Diagram` (`stereotype`, `tagged-values`).
- **Hành vi mở rộng**: `Information Flow Diagram`, `Protocol State Machine Diagram`, `Communication Diagram`, `Timing Diagram`, `Interaction Overview Diagram`.

---

## 4. Cách Tra Cứu Ảnh Mẫu Sơ Đồ Trong IMAGE_REGISTRY.json
Khi Agent chuẩn bị vẽ sơ đồ cho một task cụ thể:
```bash
# Tìm ảnh mẫu cho Sequence Alt fragment (rẽ nhánh)
python scripts/knowledge.py image -q "sequence alt"

# Tìm ảnh mẫu quan hệ Class Diagram (Binary Association, Aggregation)
python scripts/knowledge.py image -q "binary association"

# Tìm ảnh mẫu sơ đồ Use Case include
python scripts/knowledge.py image -q "use case include"
```
Agent đọc đường dẫn ảnh trả về, tham khảo cách vẽ chuẩn OMG UML 2.5, sau đó vẽ cho bài toán thật và lưu vào `doc/features/<UC>/hinh/`.
