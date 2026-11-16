> **Loại: tham khảo.**
> Nguồn: tách từ srs-fdd-writing-standard.md mục L (phần 2)

# Chuẩn sơ đồ & Vị trí dòng neo Excel SRS_FDD — Phần 2: Sơ đồ Chi tiết & Ô Công thức

## L. Bản Đồ 13 Sơ Đồ & Vị Trí Dòng Neo Chuẩn (Sơ đồ 8 đến 13)

| STT | Tên Sơ Đồ | Sheet Nằm Trong | Dòng Neo (Row) | Bảng Thuyết Minh Bằng Chữ Đi Kèm Dưới Ảnh |
|---|---|---|---|---|
| **8** | **Trục tích hợp giữa các hệ thống** | `Component_Detail_Design` | Dòng 275 | Luồng gọi API đối tác (Pancake, J&T, Ngân hàng) kèm Protocol & Port. |
| **9** | **Sơ đồ bơi làn chi tiết (Activity Swimlane)** | `Use-Case01..n` | Dòng 129 | 2 làn "Người dùng" và "Hệ thống", hình thoi rẽ nhánh điều kiện hợp lệ/không hợp lệ. |
| **10** | **Wireframe màn hình chi tiết** | `Use-Case01..n` | Dòng 28 | Màn hình giao diện chi tiết, **đánh số ô 1..7 tương ứng với bảng Business Rules bên cột H**. |
| **11** | **Sơ đồ tuần tự giao dịch (Sequence Diagram)** | `Use-Case01..n` | Dòng 136 | Lifelines: Client $\rightarrow$ Gateway $\rightarrow$ Controller $\rightarrow$ DB; có khung `LOOP` và `ALT`. |
| **12** | **Sơ đồ thực thể CSDL (ERD)** | `Use-Case01..n` | Dòng 168 | Ký hiệu chân quạ, bảng có PK/FK, kiểu dữ liệu và quan hệ 1-N. |
| **13** | **Bảng Screen Items chi tiết (Kiểu Nhật)** | Sheet `20210620` | Dòng 1 | Bảng mô tả từng nút bấm: `Item Name`, `Type`, `IOE`, `Required`, `Data Type`, `Max Length`, `Default Value`, `Error Message`. |

### Nguyên Tắc Ô Công Thức (Bất Di Bất Dịch):
- **CẤM GHI ĐÈ CÔNG THỨC**:
  * `NhatKyThayDoi`: Cột A (`=ROW()-1`).
  * `PJT_Definition`: Ô `B3` (`=B2`).
  * `WBS_Planning`: Cột E (`=D/6.4`), Cột H (công thức `WORKDAY`), Cột I (`=WORKDAY(H, Duration-1)`), Dòng tổng cha (`=SUM(con)`).
  * `Use-Case01`: Ô *Mức độ của UC* (công thức đếm số bước tính độ phức tạp).
