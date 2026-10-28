# Feature Map: bản đồ giao diện cho agent

Lý do: agent chạy được ứng dụng vẫn lúng túng nếu không biết tính năng nằm ở đâu trên giao diện. Báo lỗi của người dùng thường mơ hồ ("nút này đơ ???", một ảnh chụp màn hình) và agent đoán mò. Feature Map nói rõ **khu vực nào, vào bằng đường nào, thao tác bằng gì, tìm phần tử bằng gì**, nên agent khớp được báo lỗi với đúng màn hình, tự mở ra, tái hiện lỗi và xác minh sau khi sửa.

Áp dụng cho dự án có giao diện (web, desktop, mobile). Dự án chỉ có backend thì bỏ qua.

## 1. Ai viết, ở đâu

- File: `docs/design/feature-map.md` (một file, hoặc mỗi cụm tính năng một file nếu lớn, nối bằng mục lục).
- **Khởi tạo**: `designer` hoặc `qa` dùng skill `feature-map` chế độ `create` (`.agents/skills/feature-map/SKILL.md`): quét code giao diện, dựng bản nháp, kiểm trên ứng dụng thật, người dùng duyệt.
- **Duy trì**: Dev đổi cấu trúc giao diện (thêm màn hình, đổi đường vào, đổi selector) thì dùng skill chế độ `maintain`: cập nhật các mục bị ảnh hưởng **trong cùng task** và ghi vào card. QA thấy Feature Map lệch ứng dụng thật thì trả card về `doing`.
- **Máy kiểm lệch** (luật cứng, không chờ ai nhớ): `python scripts/feature-map-check.py` đối chiếu bản đồ với mã: đường dẫn trong `File nguồn` còn tồn tại không, `data-testid` trong `Định vị` còn xuất hiện trong mã không, mỗi mục đủ trường bắt buộc không. Thêm `--changed-against <nhánh-gốc>` để cảnh báo file giao diện đổi mà không thuộc mục nào. Có lỗi lệch thì thoát mã 1; CI chạy nó khi dự án có `docs/design/feature-map.md`. Tên trường trong mục phải đúng như mẫu bên dưới (`Khu vực`, `Đường vào`, `Định vị`, `File nguồn`, `Kiểm tra nhanh`) thì máy mới đọc được.
- Chỉ ghi điều quan sát được hoặc đọc được từ code. Chỗ chưa kiểm chứng ghi `(chưa kiểm)`, không đoán.
- **Bắt đầu ở máy nội bộ**: tạo và kiểm Feature Map trên máy bạn để quan sát agent thao tác thật, rồi mới tính tới chạy ngầm hay trên đám mây.

## 2. Nội dung bắt buộc cho mỗi tính năng

| Mục | Ý nghĩa |
|---|---|
| Khu vực | Vùng trên giao diện (thanh bên trái, tab PR bên phải, khung hội thoại...) |
| Đường vào | Các bước từ màn hình chính đến tính năng, kèm URL nếu có |
| Điều kiện | Cần đăng nhập vai nào, dữ liệu mẫu nào, cờ tính năng nào |
| Thao tác | Phím tắt, nút, cử chỉ kích hoạt |
| Định vị phần tử | `data-testid`, id, role + tên (dùng cho Playwright hoặc CDP) |
| File nguồn | Đường dẫn component chính, để từ báo lỗi tìm ra code |
| Kiểm tra nhanh | Một câu "thấy gì thì tính năng chạy đúng" |

## 3. Cách dùng

- **Khi nhận báo lỗi mơ hồ**: làm theo `agents/protocols/bug-repro.md`: tìm trong Feature Map, mở đúng màn hình theo "Đường vào", tái hiện trên `main`, rồi mới kết luận (kèm dẫn chứng, xem `definition-of-done.md`).
- **Khi QA kiểm bằng mắt** (`ui-fidelity.md` mục 3): dùng "Kiểm tra nhanh" và "Định vị phần tử" làm bước chuẩn.
- Có một dự án đã dùng Playwright thì selector trong Feature Map phải khớp với selector trong test.

Mục nào có **tính năng phụ** (ví dụ thanh bên có thu gọn, ghim, tìm kiếm) thì thêm dòng `- Tính năng phụ: <danh sách, mỗi cái kèm cách bật và selector nếu cần>`; trường này không bắt buộc và máy kiểm không đòi.

## 4. Mẫu

```markdown
# Feature Map: <tên dự án>
Cập nhật: YYYY-MM-DD bởi <vai> | Phiên bản ứng dụng: <mã>

## F-01 Hộp tìm kiếm tài liệu
- Khu vực: thanh bên trái, phần đầu
- Đường vào: Đăng nhập (vai HR) > Trang chủ > thanh bên > "Tài liệu" (/documents)
- Điều kiện: có ít nhất 1 tài liệu mẫu
- Thao tác: nhấn `/` để focus; Enter để tìm
- Tính năng phụ: lọc theo loại (nút `data-testid="doc-filter"`), xóa nhanh bằng Esc
- Định vị: `[data-testid="doc-search-input"]`, nút `role=button name="Tìm"`
- File nguồn: `frontend/src/features/documents/Search.tsx`
- Kiểm tra nhanh: gõ "hợp đồng" ra danh sách lọc trong dưới 1 giây, không tràn ngang ở 375px
```
