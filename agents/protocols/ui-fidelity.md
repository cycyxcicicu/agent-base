# Giao thức giao diện: làm đúng mẫu và kiểm bằng mắt

Áp dụng cho mọi card có sửa giao diện (frontend, mobile). Lý do ra đời: card code từng `done` chỉ vì build qua, nhưng giao diện không giống mẫu người dùng yêu cầu, chưa ai mở app lên nhìn, và Dev tự viết lại mục tiêu card cho khớp với cái mình đã làm.

## 1. Card giao diện phải có 3 mục (Lead viết, Dev không được sửa)

1. **Mẫu tham chiếu**: liệt kê đường dẫn file mẫu cụ thể sẽ copy hoặc đối chiếu (ví dụ Plane: `frontend/apps/web/...`). Không ghi chung chung kiểu "theo phong cách Plane". Không có mẫu thì ghi nguồn thay thế (mockup, tài liệu) kèm đường dẫn.
2. **Kiểm tra bằng mắt**: từng màn hình, từng kích thước (375, 768, 1440px), và điều gì nhìn thấy thì đạt. Viết như câu người dùng xác nhận được, ví dụ "ở 375px thanh bên ẩn, mở bằng nút menu, nội dung không tràn ngang".
3. **Tiêu chí nghiệm thu đo được**, gồm ít nhất một dòng "khớp bố cục với <file mẫu>".

Dự án có giao diện nên có **Feature Map** (`agents/protocols/feature-map.md`, file `docs/design/feature-map.md`): Dev cập nhật khi đổi cấu trúc màn hình, QA dùng "Đường vào" và "Định vị phần tử" làm bước chuẩn khi kiểm bằng mắt.

## 2. Dev

- **Copy file mẫu rồi sửa**, không tự viết lại bố cục từ trí nhớ. Bỏ phần không cần (API, store), giữ license header, ghi vào `THIRD_PARTY_NOTICES.md`.
- **Không được sửa** các mục "Mục tiêu", "Mẫu tham chiếu", "Kiểm tra bằng mắt", "Tiêu chí" và tên card. Chỉ được tick ô tiêu chí, ghi nhật ký, file đã đổi, kết quả test. Làm được ít hơn card thì **ghi phần thiếu vào "Việc chưa xong"**, không viết lại card cho khớp với phần đã làm.
- **Không tự đặt `done`.** Xong thì đặt `review`. Chỉ `qa`, `reviewer` hoặc `lead` đặt `done`, sau khi có bằng chứng bằng mắt.
- Trước khi đặt `review`: chạy ứng dụng, tự mở từng màn hình trong card ở 375px và 1440px, ghi vào card những gì thấy.

## 3. QA và Reviewer (bằng chứng bằng mắt, bắt buộc để `done`)

1. Chạy ứng dụng (lệnh dev trong `PROJECT.md`), mở từng màn hình trong mục "Kiểm tra bằng mắt" ở 375, 768 và 1440px. Dùng công cụ trình duyệt/Playwright nếu có; không có thì báo Lead, không ghi "đạt" theo đoán.
   - **Quy chuẩn Viewport khi mở trình duyệt:**
     * **Mở có đầu (Headed / Người dùng xem bằng mắt):** BẮT BUỘC mở to cửa sổ (`args: ['--start-maximized']`) với `viewport: null` (hoặc Desktop 1440×900 trở lên) để giao diện tự động co giãn (auto-responsive) vừa khít với màn hình thật của máy tính. Tuyệt đối không mở cửa sổ to mà ép viewport bé tí 375px/390px lửng lơ bên góc trái.
     * **Kiểm tra Responsive đa thiết bị:** Quét tuần tự qua 3 mốc (Desktop 1440px, Tablet 768px, Mobile 375px/390px). Khi chụp ảnh Mobile, thực hiện qua headless hoặc đổi kích thước trong kịch bản test; không treo cửa sổ giả lập điện thoại cố định trên màn hình PC.
     * **Chỉ mở ứng dụng web thật (`http://localhost:3000`):** Tuyệt đối không dùng Playwright mở trực tiếp đường dẫn file Markdown tĩnh (`file://.../*.md`), vì trình duyệt không có CSS dàn trang responsive cho tài liệu thô.
2. Chụp màn hình lưu vào `docs/qa/screens/<Task>/<màn-hình>-<rộng>.png` (mọi dữ liệu trong app là dữ liệu giả, không chụp dữ liệu thật).
3. Đối chiếu với file mẫu trong card, lập bảng vào `docs/qa/<Task>-visual.md`: thành phần | file mẫu | thực tế | giống/lệch | cách sửa.
4. Kiểm **đủ chức năng của card có chạy được** (bấm thử, kéo thử), không chỉ nhìn tĩnh.
5. Phát hiện lệch mẫu, tràn, chồng lấn, chức năng không chạy: trả card về `doing` kèm bước tái hiện. Không đạt thì không `done`.

6. **Khi dùng Playwright (kích thước giả lập):** trước MỖI ảnh đặt kích thước bằng công cụ đổi cỡ cửa sổ (375x812, 768x1024, 1440x900), kiểm `window.innerWidth` đúng kích thước đã đặt, chụp toàn trang cho điện thoại. Kích thước giả lập GIỮ NGUYÊN ở lần đặt cuối, nên khi kiểm xong PHẢI đặt lại 1440x900 hoặc đóng trình duyệt, nếu không cửa sổ lớn vẫn hiển thị trang như điện thoại. Chạy ứng dụng của worktree trên cổng riêng và tắt máy chủ sau khi kiểm.

## 4. Lead

- Card giao diện thiếu 3 mục ở mục 1 thì không được giao cho Dev.
- Sau mỗi đợt (nhóm card), **dừng** và báo người dùng xem bản chạy thật. Người dùng nói "tiếp" mới mở card đợt sau.
- Khi Dev đổi nội dung card hoặc làm khác card (đọc card, so với kế hoạch): trả về `doing`, không chấp nhận.
- Tên và mục tiêu card trên `BOARD.md` phải khớp nội dung đã làm; lệch thì sửa card hoặc mở card bổ sung cho phần thiếu.
