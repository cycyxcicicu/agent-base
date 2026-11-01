# Cẩm Nang Phân Tích & Thiết Kế Hệ Thống Theo Case Study Thực Chiến (SourceMaking UML Airport)

**Loại: tham khảo.** Nguồn: [SourceMaking UML 2.0 Tutorial & Case Study](file:///d:/congty/agent-base/assets/sourcemaking-uml/INDEX.md).  
Kho dữ liệu cục bộ: [assets/sourcemaking-uml/](file:///d:/congty/agent-base/assets/sourcemaking-uml/) (71 bài viết, 227 sơ đồ chuẩn).  
Vai trò áp dụng: `ba`, `architect`, `analyst`, `dev`.  

---

## 1. Bối Cảnh Case Study: Hệ Thống Phục Vụ Hành Khách Sân Bay (UML Airport)

Case Study chọn một nghiệp vụ kinh điển nhưng có độ phức tạp cao, đòi hỏi sự kết hợp chặt chẽ giữa con người, quy trình vật lý và hệ thống phần mềm: **Khu vực phục vụ hành khách xuất phát tại sân bay (Passenger Departure Services)**.

```
+-------------------------------------------------------------------------------------------------------+
|                                    UML AIRPORT - DEPARTURE LIFECYCLE                                  |
|                                                                                                       |
|  [Hành khách] ---> (1. Check-in Counter) ---> (2. Security Gate) ---> (3. Boarding Gate) ---> [Máy bay] |
|                           |                                                 |                         |
|                           v                                                 v                         |
|                 (Baggage Handling System)                          (Departure Control System)         |
+-------------------------------------------------------------------------------------------------------+
```

### Các tác nhân và ranh giới hệ thống:
1. **Hành khách (Passenger):** Khởi tạo quy trình xuất phát, xuất trình vé, ký gửi hành lý, nhận thẻ lên tàu bay (Boarding Pass).
2. **Nhân viên làm thủ tục (Check-in Agent):** Tác nhân nội bộ hỗ trợ kiểm tra giấy tờ, kiểm tra trọng lượng hành lý, gán ghế và in thẻ.
3. **Nhân viên cửa lên tàu (Gate Agent):** Quét mã thẻ lên tàu, kiểm đếm số lượng hành khách thực tế, đối soát với danh sách chuyến bay.
4. **Hệ thống xử lý hành lý (Baggage Handling System - BHS):** Vận chuyển, soi chiếu và đưa hành lý vào khoang máy bay.
5. **Hệ thống điều khiển khởi hành (Departure Control System - DCS):** Ứng dụng CNTT trung tâm quản lý toàn bộ dữ liệu chuyến bay, ghế ngồi và trạng thái hành khách.

---

## 2. Khung Phương Pháp 4 Tầng Mô Hình Hóa (4-Layer Modeling Framework)

SourceMaking đưa ra quy chuẩn mô hình hóa từ cấp độ Nghiệp vụ tổ chức (Business) xuống cấp độ Hệ thống phần mềm (IT System) và Tích hợp liên hệ thống (Integration):

```
       +-------------------------------------------------------------+
       |   TẦNG 1: MÔ HÌNH HÓA HỆ THỐNG NGHIỆP VỤ (BUSINESS SYSTEM)   |
       |     - External: Business Use Cases, Business Activity (Swimlanes)|
       |     - Internal: Business Workers, Business Entities, Packages |
       +-------------------------------------------------------------+
                                      |
                                      v
       +-------------------------------------------------------------+
       |     TẦNG 2: MÔ HÌNH HÓA HỆ THỐNG CNTT (IT SYSTEMS MODELING) |
       |     - User View: Use Case Sequence (Query vs Mutation Events)|
       |     - Structural: Class Diagram (Static vs Dynamic Rules)   |
       |     - Behavioral: Statechart Diagram (Ticket/Baggage Life)  |
       |     - Interaction: Internal Sequence & Communication Diagram|
       +-------------------------------------------------------------+
                                      |
                                      v
       +-------------------------------------------------------------+
       |  TẦNG 3: MÔ HÌNH HÓA TÍCH HỢP HỆ THỐNG (SYSTEM INTEGRATION) |
       |     - Process View: Async Integration Sequence (DCS <-> BHS) |
       |     - Static View: Message Transformation (Domain <-> XML)  |
       +-------------------------------------------------------------+
```

---

## 3. Tầng 1: Mô Hình Hóa Hệ Thống Nghiệp Vụ (Modeling Business Systems)

### 3.1. Góc Nhìn Ngoài (External View — Business Use Case & Business Activity)
- **Business Use Case:** Biểu diễn giá trị mà doanh nghiệp mang lại cho khách hàng bên ngoài (Passenger).
  - Use case: *Check-in Passenger* (Bao gồm kiểm tra vé, gán ghế, in thẻ lên tàu và nhận hành lý).
  - Use case: *Board Flight* (Xác thực hành khách lên máy bay, đóng chuyến).
- **Business Activity Diagram (Bắt buộc dùng Swimlanes):**
  - Làn 1: **Passenger** (Xuất trình vé -> Đặt hành lý lên cân -> Nhận boarding pass).
  - Làn 2: **Check-in Agent** (Quét vé -> Xác nhận thông tin -> Nhập số cân -> In thẻ hành lý -> In thẻ lên tàu).
  - Làn 3: **Baggage Conveyor / Handler** (Tiếp nhận hành lý -> Đọc mã vạch -> Phân loại vào cửa ra tàu bay).

> **Ảnh mẫu tham chiếu:**
> - `assets/sourcemaking-uml/images/img_19.jpg`: Sơ đồ Use Case tổng thể khu vực khởi hành.
> - `assets/sourcemaking-uml/images/img_25.jpg`: Sơ đồ Activity phân làn nghiệp vụ Check-in.

### 3.2. Góc Nhìn Trong (Internal View — Business Workers & Business Entities)
- **Business Worker:** Người thực hiện quy trình nghiệp vụ (`Check-in Agent`, `Gate Agent`, `Security Guard`).
- **Business Entity:** Các thực thể nghiệp vụ có vòng đời thực tế:
  - `Ticket` (Vé máy bay điện tử).
  - `Boarding Pass` (Thẻ lên tàu bay).
  - `Baggage` (Kiện hành lý ký gửi, kèm Baggage Tag).
  - `Flight` (Chuyến bay cụ thể kèm ngày giờ và cổng).
- **Business Package Diagram:** Phân chia ranh giới giữa các phòng ban: *Passenger Services*, *Baggage Logistics*, *Flight Operations*, *Security Operations*.

---

## 4. Tầng 2: Mô Hình Hóa Hệ Thống CNTT (Modeling IT Systems)

### 4.1. Góc Nhìn Người Dùng (User View): Phân Biệt Sự Kiện Truy Vấn vs Đột Biến (Query vs Mutation)
SourceMaking áp dụng nguyên lý kiến trúc hiện đại (tiền thân của CQRS) ngay trong đặc tả UML:

| Loại Sự Kiện | Bản Chất Nghiệp Vụ | Ví Dụ Trong Sân Bay | Đặc Điểm Kỹ Thuật |
|---|---|---|---|
| **Query Event** (Sự kiện truy vấn) | Người dùng hỏi thông tin, hệ thống đọc dữ liệu và hiển thị | Xem sơ đồ ghế trống, tra cứu giờ cất cánh, kiểm tra tình trạng vé | Không đổi trạng thái (Idempotent), cache được, không ghi log biến động |
| **Mutation Event** (Sự kiện đột biến) | Người dùng thực hiện hành động làm thay đổi trạng thái của thực thể | Chọn ghế 12A, in thẻ lên máy bay, ký gửi kiện hành lý 18kg | Thay đổi trạng thái DB (State transition), cần transaction, bắt buộc audit log |

### 4.2. Góc Nhìn Cấu Trúc (Structural View): Class Diagram & Business Rules
- **Quan hệ giữa các lớp:**
  - `Flight` 1 -- * `Seat` (Composition: Xóa Flight thì xóa cấu hình Seat của chuyến).
  - `Passenger` 1 -- * `Ticket` (Association).
  - `Ticket` 1 -- 0..1 `BoardingPass` (Aggregation/Association).
  - `FrequentFlyer` extends `Passenger` (Inheritance / Generalization).
- **Quy tắc nghiệp vụ tĩnh (Static Rules):**
  - Ràng buộc cấu trúc: Một hành khách chỉ có tối đa 1 thẻ lên tàu bay cho 1 chặng bay.
  - Trọng lượng hành lý tiêu chuẩn: `weight <= 20kg` (vượt quá tính phí quá cước).
- **Quy tắc nghiệp vụ động (Dynamic Rules):**
  - Chỉ cho phép Check-in khi trạng thái chuyến bay là `OPEN_FOR_CHECKIN` (thường mở trước 24h và đóng trước 45 phút khởi hành).

### 4.3. Góc Nhìn Hành Vi (Behavioral View): Statechart Diagram (State Machine)
Quản lý trạng thái là hạt nhân sống còn của hệ thống hàng không:
- **Vòng đời của Vé máy bay (Ticket Lifecycle):**
  `ISSUED` -> *(Check-in Event)* -> `CHECKED_IN` -> *(Boarding Event)* -> `BOARDED` -> `COMPLETED`.
  *(Nhánh ngoại lệ: Hủy vé -> `CANCELLED`; Vắng mặt -> `NO_SHOW`).*
- **Vòng đời Kiện Hành Lý (Baggage Lifecycle):**
  `CHECKED` -> *(Conveyor Transfer)* -> `SECURITY_SCREENED` -> *(Ramp Loading)* -> `LOADED_ON_AIRCRAFT` -> `CLAIMED`.
  *(Nhánh lỗi: Nghi vấn an ninh -> `HELD_FOR_INSPECTION`; Thất lạc -> `MISHANDLED`).*

> **Ảnh mẫu tham chiếu:**
> - `assets/sourcemaking-uml/images/img_67.jpg`: Sơ đồ State Machine vòng đời Vé máy bay.
> - `assets/sourcemaking-uml/images/img_73.jpg`: Sơ đồ State Machine kiểm soát hành lý.

---

## 5. Tầng 3: Mô Hình Hóa Tích Hợp Hệ Thống (System Integration)

Khi hệ thống nội bộ (DCS) cần giao tiếp với các hệ thống toàn cầu (Global Distribution System - GDS/CRS) hoặc hệ thống ngoại vi (BHS):
1. **Process View (Luồng tích hợp bất đồng bộ):**
   - Sử dụng Sequence Diagram biểu diễn bắt tay 3 bước: Request -> Ack/Nack -> Asynchronous Event Callback.
2. **Static View & Message Transformation:**
   - Dữ liệu nghiệp vụ nội bộ (`Ticket`, `Passenger`, `Baggage`) được ánh xạ (Transform) sang cấu trúc thông điệp chuẩn (IATA Type B Message / XML Web Service).
   - Đảm bảo ranh giới Seam sạch: Khi cấu trúc DB nội bộ thay đổi, lớp Transformation giữ nguyên cấu trúc Message giao tiếp ngoài.

---

## 6. Sổ Tra Cứu Nhanh & Lệnh CLI Cho Agent

Tất cả 227 sơ đồ thực tế của SourceMaking đã được lập chỉ mục đầy đủ trong [agents/knowledge/IMAGE_REGISTRY.json](file:///d:/congty/agent-base/agents/knowledge/IMAGE_REGISTRY.json). Các Agent có thể tra cứu tức thì bằng lệnh CLI:

```bash
# 1. Tra cứu sơ đồ tổng quan sân bay
python scripts/knowledge.py image -q "airport"

# 2. Tra cứu sơ đồ State Machine (vòng đời vé, hành lý)
python scripts/knowledge.py image -q "statechart"

# 3. Tra cứu sơ đồ tuần tự tích hợp hệ thống
python scripts/knowledge.py image -q "integration sequence"

# 4. Trích xuất đúng một bài viết chi tiết từ kho SourceMaking
python scripts/knowledge.py section --file assets/sourcemaking-uml/pages/modeling-it-systems/query-events-and-mutation-events/README.md --heading "Mutation"
```
