# BÁO CÁO PHÂN TÍCH CHUYÊN SÂU 22+ LOẠI SƠ ĐỒ UML 2.5 & DANH BẠ ẢNH (ARCHITECT STREAM)
> Chuyên viên thực hiện: **Marcus (Principal Architect)** | Thời gian: 2026-11-01 12:35:11

## 1. TỔNG QUAN TẬP SƠ ĐỒ ĐÃ BÓC TÁCH
- **Tổng số phân loại sơ đồ**: 21 loại
- **Nhóm Sơ Đồ Cốt Lõi (Core 8)**: 8 loại (Áp dụng bắt buộc trong tài liệu Gate 2)
- **Nhóm Sơ Đồ Mở Rộng / Chuyên sâu**: 13 loại (Dùng khi cần thiết kế phức tạp)
- **Tổng số hình ảnh sơ đồ đã lập chỉ mục**: 392 ảnh

## 2. MA TRẬN 8 SƠ ĐỒ CỐT LÕI (CORE 8) DÀNH CHO DỰ ÁN THỰC CHIẾN

| STT | Sơ Đồ | Vai Trò Chính | Số Ảnh Minh Họa | Ứng Dụng Trong Hồ Sơ Gate 2 |
|---|---|---|---|---|
| 1 | **Class Diagram (Cấu trúc lớp, Entity, DTO, Quan hệ)** | `architect` / `ba` | 55 ảnh | Vẽ trong file `<UC>-thiet-ke-ky-thuat.md` & DrawIO |
| 2 | **Activity Diagram (Quy trình nghiệp vụ, Bơi làn, Fork, Join)** | `architect` / `ba` | 54 ảnh | Vẽ trong file `<UC>-thiet-ke-ky-thuat.md` & DrawIO |
| 3 | **Deployment Diagram (Môi trường máy chủ, Docker container)** | `architect` / `ba` | 31 ảnh | Vẽ trong file `<UC>-thiet-ke-ky-thuat.md` & DrawIO |
| 4 | **Component Diagram (Ranh giới module, Cổng Ports & Connectors)** | `architect` / `ba` | 27 ảnh | Vẽ trong file `<UC>-thiet-ke-ky-thuat.md` & DrawIO |
| 5 | **Use Case Diagram (Tác nhân Actor, Hệ thống, Include, Extend)** | `architect` / `ba` | 27 ảnh | Vẽ trong file `<UC>-thiet-ke-ky-thuat.md` & DrawIO |
| 6 | **State Machine Diagram (Vòng đời đối tượng, Guard, Event)** | `architect` / `ba` | 16 ảnh | Vẽ trong file `<UC>-thiet-ke-ky-thuat.md` & DrawIO |
| 7 | **Sequence Diagram (Luồng tuần tự, Đồng bộ/Bất đồng bộ, Alt, Loop)** | `architect` / `ba` | 14 ảnh | Vẽ trong file `<UC>-thiet-ke-ky-thuat.md` & DrawIO |
| 8 | **Package Diagram (Cấu trúc phân gói, Phụ thuộc module)** | `architect` / `ba` | 7 ảnh | Vẽ trong file `<UC>-thiet-ke-ky-thuat.md` & DrawIO |

## 3. DANH SÁCH SƠ ĐỒ MỞ RỘNG (CHỌN LỌC KHI CẦN)

| Sơ Đồ Mở Rộng | Số Ảnh | Đánh Giá Áp Dụng |
|---|---|---|
| **Uml Examples** | 86 ảnh | Tham khảo |
| **Profile Diagram** | 17 ảnh | Tham khảo |
| **Communication Diagram** | 13 ảnh | Tham khảo |
| **Manifestation Diagram** | 9 ảnh | Tham khảo |
| **Network Architecture Diagram** | 7 ảnh | Tham khảo |
| **Timing Diagram** | 7 ảnh | Tham khảo |
| **Protocol State Machine** | 6 ảnh | Tham khảo |
| **Interaction Overview Diagram** | 5 ảnh | Tham khảo |
| **Model Diagram** | 5 ảnh | Tham khảo |
| **Composite Structure Diagram** | 4 ảnh | Tham khảo |
| **Information Flow Diagram** | 2 ảnh | Tham khảo |
| **Images** | 0 ảnh | Hàn lâm ít dùng |
| **Object Diagram** | 0 ảnh | Hàn lâm ít dùng |

## 4. QUY TẮC CHUYỂN ĐỔI ẢNH THÀNH DRAWIO CHUẨN DỰ ÁN
Khi Agent cần vẽ sơ đồ cho một Use Case:
1. **Tra cứu Sổ bộ ảnh** `IMAGE_REGISTRY.json` để lấy mẫu chuẩn của phần tử (VD: cách vẽ Alt fragment, cách vẽ Port, Fork/Join).
2. **Tuân thủ 5 quy tắc chuẩn (.ai-rules/srs/chuan-ve-so-do.md)**:
   - Bơi làn (swimlane) rõ ràng giữa các tầng kiến trúc.
   - Đúng 1 điểm bắt đầu và ĐÚNG 1 điểm kết thúc duy nhất.
   - Nhánh lỗi luôn tô màu đỏ `#dc2626` có chú thích mã lỗi.
   - 100% dữ liệu thật từ code/DB.
   - Xuất file `.drawio` nhiều tab kèm file ảnh `.png` độ nét cao lưu tại `doc/features/<UC>/hinh/`.
