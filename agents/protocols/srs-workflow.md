# Quy trình viết SRS và sơ đồ (khung dùng chung)

Đây là **nguồn chính** cho việc viết đặc tả (SRS) và sơ đồ. `spec-writing.md` chỉ giữ phần văn phong; `knowledge/srs/srs-fdd-writing-standard.md` là tham khảo cho dự án dùng mẫu Excel SRS_FDD. Khi các file mâu thuẫn thì theo file này (`source-precedence.md`).

## 1. Khung và dự án tách nhau

- `agent-base` chỉ chứa **quy trình, mẫu, công cụ**. **Không** chép tài liệu của dự án vào đây.
- Tài liệu của dự án nằm trong chính dự án. Hai khóa trong `PROJECT.md` cho biết ở đâu:

| Khóa trong `PROJECT.md` | Ý nghĩa | Mặc định của khung |
|---|---|---|
| `Thư mục tài liệu` | gốc mọi tài liệu của dự án | `docs` |
| `Thư mục SRS` | nơi đặt SRS từng chức năng và sơ đồ | `docs/spec` |

Dự án đã có sẵn thư mục riêng (ví dụ `doc/srs`) thì ghi vào `PROJECT.md`, không đổi tên thư mục theo khung.

---

## 1b. Phân cấp quy mô tài liệu (Tailoring Policy — May đo theo dự án)

Không phải dự án nào cũng cần WBS, RTM 23 cột hay bộ hồ sơ Excel 14 tab cồng kềnh. Khung `agent-base` phân chia rõ 2 chế độ áp dụng:

1. **Chế độ Agile / Tinh gọn (Lightweight Mode — Mặc định cho dự án vừa & nhỏ, MVP, dịch vụ đơn lẻ):**
   - **Hồ sơ:** Sử dụng bộ ba file Markdown (`UC-xx.md`, `UC-xx-thiet-ke.md`, `UC-xx-doi-chieu.md`) và sơ đồ dạng ảnh nhúng tại `hinh/`.
   - **Quản lý công việc:** Dùng Task Card hạt mịn (`tasks/T-xx.md`) hoặc bảng Kanban của dự án/Jira/GitLab.
   - **Không bắt buộc:** Không cần lập file Excel `SRS_FDD_<UC>.xlsx`, không cần WBS Gantt hay Function_RTM phức tạp nếu không có yêu cầu từ khách hàng/thầu.

2. **Chế độ Enterprise / Tuân thủ CMMI-L3 (Enterprise Mode — Dự án tài chính, kế toán, hệ thống lõi lớn):**
   - **Hồ sơ:** Đóng gói thêm file Excel `SRS_FDD_<UC>.xlsx` chuẩn 13 tab theo mẫu Copilot (`_SRS_FDD_AI-Agent-Copilot.xlsx`), có đầy đủ WBS chi tiết DoD, Function_RTM 23 cột, cổng duyệt con người (File-based GATE), Risk_Register và ADR_Log.
   - **Nguyên tắc linh hoạt (May đo ngay trong Excel):** Sử dụng tab `DauMucTaiLieuCanLam` để chọn `Sử dụng: Yes/No` cho từng sheet (ví dụ: đã quản lý task trên Jira thì WBS có thể chọn `No` kèm lý do giải trình).

3. **Nguyên tắc kỹ thuật BẮT BUỘC cho MỌI DỰ ÁN (Bất kể chế độ nào):**
   - **Tư duy BA thực chiến (Code Reality & Edge Cases):** Trước khi viết đặc tả, bắt buộc phải đọc code hiện trạng. Không được chỉ viết Happy Path, bắt buộc phải suy diễn các ca biên thực tế (như ca chia đơn khi nhân viên nghỉ, thu hồi, concurrency locking, audit trail).
   - **Quy chuẩn sơ đồ:** Hoạt động (Activity) bơi làn phải có **ĐÚNG 1 Start — ĐÚNG 1 End, nhánh lỗi màu đỏ**. Mockup phải đánh số tròn `①..⑦` trỏ xuống danh sách API.
   - **Phản biện trung thực (Anti-Flattery):** Không vuốt đuôi khi người dùng đưa ra phương án rủi ro; đưa 3 lựa chọn kèm khuyến nghị và biện pháp phòng ngừa rủi ro.
   - **Nghiệm thu bằng File (File-based GATE):** Duyệt qua file task/RTM, không duyệt miệng qua chat.

## 2. Bộ file của một chức năng (nằm trong `Thư mục SRS`)

| File | Nội dung |
|---|---|
| `UC-<nn>-<loại>-<mô tả>.md` | **Đặc tả**: hệ thống phải làm gì (mẫu `agents/templates/srs-chuc-nang/srs-chuc-nang-template.md`) |
| `UC-<nn>-<loại>-<mô tả>-thiet-ke.md` | **Thiết kế kỹ thuật**: xây thế nào (mẫu `thiet-ke-ky-thuat-template.md`) |
| `UC-<nn>-<loại>-<mô tả>-doi-chieu.md` | **Đối chiếu** code thật với đặc tả (chỉ khi đã có code) |
| `hinh/` | nguồn và ảnh sơ đồ; một chức năng một file `.drawio` nhiều trang |

Tên theo `task-card.md` mục "Đặt tên task": loại việc (`feat`, `fix`, `docs`...) rồi việc gì, ví dụ `UC-03-feat-huy-don-van-chuyen.md`.

## 3. Các bước và người làm

| # | Bước | Vai | Ra gì |
|---|---|---|---|
| 1 | Nhận yêu cầu, phản biện đề bài (`challenger.md`), nhập tài liệu gốc (`intake.md`) | product, ba | yêu cầu R-xxx đã rõ |
| 2 | Chọn hạng mục cần làm trong mẫu, ghi nguồn đối chiếu | ba, analyst | khung SRS |
| 3 | Viết đặc tả theo văn phong `spec-writing.md`: mệnh lệnh khẳng định, lượng hóa, câu hỏi mở dồn cuối | ba, architect | đặc tả `Draft` |
| 4 | Vẽ sơ đồ tối thiểu (mục 4) theo `knowledge/srs/chuan-ve-so-do.md` và `knowledge/diagrams/quy-uoc-draw-io-va-archify.md` | designer, architect | nguồn sơ đồ + ảnh |
| 5 | Viết **mô tả hoạt động** cho từng sơ đồ, số bước khớp sơ đồ (`knowledge/diagrams/mo-ta-hoat-dong-so-do.md`) | designer, ba | bảng bước dưới mỗi ảnh |
| 6 | Viết tiêu chí nghiệm thu `AC-xx` và ca kiểm thử (`test-cases.md`): mỗi `AC` có ít nhất một ca | qa | bảng ca kiểm thử có cột `A/C ref` |
| 7 | **Tự kiểm**: `python scripts/srs-check.py <file>` và `python scripts/diagram-describe.py <file.drawio> --check` | người viết | báo cáo sạch lỗi |
| 8 | Soát chéo (Solution-Pair, `pair-review.md`), rồi người dùng duyệt (`approval.md`) | reviewer | đặc tả `Approved` |
| 9 | Cập nhật truy vết `python scripts/rtm.py` và ghi đường dẫn nguồn sơ đồ | dev, qa | RTM khớp |

Không bước nào được bỏ qua để chạy trước. Đổi nghiệp vụ thì làm lại từ bước 3, sơ đồ trước rồi mô tả rồi đặc tả (`change-request.md` nếu đặc tả đã duyệt).

## 4. Sơ đồ tối thiểu cho một chức năng

| Chức năng có... | Cần sơ đồ |
|---|---|
| luồng xử lý nào | hoạt động (bơi làn) hoặc use case |
| từ hai thành phần gọi nhau | sequence |
| đọc hoặc ghi cơ sở dữ liệu | ERD các bảng chạm tới, hoặc ghi rõ **"không thêm bảng"** |
| đổi trạng thái | sơ đồ trạng thái (vòng đời) |
| màn hình | wireframe hoặc mockup, luồng màn hình |

Mỗi sơ đồ có **mô tả hoạt động bằng chữ** ngay dưới ảnh (bước 5), và dẫn tới file nguồn.

## 5. Công cụ

| Việc | Lệnh |
|---|---|
| Kiểm một đặc tả | `python scripts/srs-check.py <file.md>` (thêm `--strict` để cảnh báo cũng là lỗi) |
| Kiểm mọi đặc tả của dự án | `python scripts/srs-check.py --all` (đọc `Thư mục SRS` trong `PROJECT.md`) |
| Kiểm **hồ sơ hoàn chỉnh** trước bàn giao | `python scripts/srs-check.py --full <file.md>`: bắt thêm Nhật ký thay đổi, Hạng mục thiết kế, WBS, RTM, rủi ro, câu hỏi chờ xác nhận và use-case đủ tiền điều kiện, luồng chính, luồng thay thế, luồng lỗi. Khung: `knowledge/srs/ho-so-hoan-chinh-khung-bat-buoc.md` |
| Chuyển md sang docx để lên Google Docs | `python scripts/md_to_docx.py <file.md> <file.docx>` (cần `pandoc`); lỗi hay gặp: `knowledge/srs/md-to-office-fidelity.md` mục 4 |
| Đọc và kiểm sơ đồ `.drawio` | `python scripts/diagram-describe.py <file.drawio> [--check]` |
| Truy vết yêu cầu | `python scripts/rtm.py` |

`srs-check.py` **lỗi** (mã thoát 1) khi: thiếu mục bắt buộc (tác nhân, use case hoặc user story, tiêu chí nghiệm thu, sơ đồ, yêu cầu phi chức năng, kiểm thử, câu hỏi mở), ảnh sơ đồ không tồn tại, một `AC-xx` không có ca kiểm thử nào, sơ đồ `.drawio` được dẫn tới vi phạm quy tắc. **Cảnh báo**: từ cảm tính ("nhanh", "mượt", "trực quan"...), ảnh không có mô tả bước, thiếu ERD hay trạng thái khi văn bản nhắc tới bảng hay trạng thái, câu hỏi mở không nằm cuối.

## 6. Khung chưa có

- Công cụ **sinh** `.drawio` từ dữ liệu và xuất đặc tả ra Excel SRS_FDD: dự án nào cần thì dùng công cụ của dự án. Khung cung cấp mẫu Excel và hướng dẫn (`agents/templates/srs-fdd/`), chưa cung cấp bộ chuyển.
- Mặc định sơ đồ nhỏ vẽ Mermaid trong md; sơ đồ lớn dùng `.drawio` theo `quy-uoc-draw-io-va-archify.md`.
