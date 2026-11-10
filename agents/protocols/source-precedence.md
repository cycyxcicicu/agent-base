> Task: T-14 · Epic: E2 · Vai: writer

# Thứ tự ưu tiên nguồn tài liệu khi có mâu thuẫn (Source Precedence Protocol)

Trong quá trình phân tích và phát triển, tác tử thường xuyên gặp tình huống nhiều tài liệu mô tả cùng một hành vi nhưng mâu thuẫn nhau (ví dụ: tài liệu tổng quan mâu thuẫn với đặc tả chi tiết, hoặc tài liệu cũ mâu thuẫn với mã nguồn đang chạy). Giao thức này quy định thứ tự giải quyết và trách nhiệm xử lý.

---

## 1. Bảng thứ tự ưu tiên mẫu (Có thể cấu hình theo từng dự án)

Khi xuất hiện xung đột thông tin giữa các tài liệu, áp dụng thứ tự ưu tiên từ cao xuống thấp như sau:

| Cấp | Nguồn tài liệu | Mô tả & Nguyên tắc áp dụng |
|---|---|---|
| **1** | **Quyết định con người bằng file** | Dấu phê duyệt của người dùng trong task card, phiếu rủi ro RK, hoặc file phê duyệt `docs/approvals/`. Luôn có giá trị cao nhất. |
| **2** | **Đặc tả kiến trúc & ADR đã duyệt** | Các tệp `docs/adr/` và `docs/spec/` ở trạng thái `Approved`. Thắng mọi tài liệu phân tích chung. |
| **3** | **Yêu cầu chức năng chi tiết (SRS/FDD)** | Các tệp trong `docs/requirements/` (mã R-xxx, BR-xxx). Chi tiết hơn thì thắng tổng quan. |
| **4** | **Mã nguồn đang chạy thật & Test suite** | Mã nguồn đã qua CI và bộ unit test hiện hành. Phản ánh sự thật vận hành, dùng để đối chiếu hiện trạng. |
| **5** | **Tài liệu chuyển đổi từ nguồn ngoài** | Các tệp Markdown trong `docs/converted/` được sinh từ file nguồn (.docx, .xlsx, .pdf). |
| **6** | **Tài liệu phác thảo / Đề xuất (Draft)** | Các file phân tích, ghi chú chưa duyệt trong `docs/analysis/` hoặc `docs/notes/inbox/`. |

---

## 2. Xử lý Nhiều Phiên bản của Cùng Một Tài Liệu (Single Active Spec · Supersede · Archive)

Khi trước đó đã có tài liệu bản cũ rồi người dùng tạo hoặc cập nhật **bản mới** để triển khai, agent BẮT BUỘC tuân thủ 4 quy tắc sau:

1. **Một bản Active Spec duy nhất**: Mỗi thư mục chức năng (`doc/features/<UC>/` hoặc `docs/spec/`) chỉ coi **1 tài liệu chính** là nguồn chân lý đang hiệu lực (`Active Source`, nên khai báo ngay đầu `README.md`: `> **Active Source:** <tên-file>`).
2. **Dời hoặc đánh dấu bản cũ (`archive/` / `SUPERSEDED`)**:
   - Khi sinh/gửi bản mới thay thế bản cũ, bản cũ cần dời vào thư mục `archive/` trong cùng chức năng (ví dụ `doc/features/<UC>/archive/`) **hoặc** chèn ngay đầu file cũ dòng:
     `> **STATUS: SUPERSEDED BY:** <tên-file-mới> — KHÔNG DÙNG ĐỂ CODE`
   - Task card thuộc thiết kế bị thay thế phải đổi trạng thái sang `superseded` hoặc `cancelled`.
3. **Chạy Pre-Code Doc Preflight trước khi đọc sâu / tra XERJ**:
   - Trước khi thiết kế hay code, chạy:
     `python3 ~/Documents/agent-base/scripts/doc-preflight.py --root <gốc-workspace> --uc <UC>`
   - Script kiểm tra tự động trên đĩa theo `mtime` mới nhất: bỏ qua `archive/`, `SUPERSEDED`, card `cancelled`/`superseded`, đồng thời bắt 2 bẫy chí mạng:
     - **`[BINARY-NEWER-THAN-MD]`**: File `.docx`/`.xlsx`/`.pdf` mới hơn `.md` -> **CẤM dùng `.md` cũ để code**; phải báo người dùng và chuyển đổi/đối chiếu sang `.md` trước.
     - **`[MULTIPLE-ACTIVE-DOCS]` / `[MULTIPLE-DRAWIO]`**: Tồn tại nhiều bản song song chưa dời vào `archive/` -> phải dừng 1 nhịp xác nhận bản mới nhất (`Active Source`), tuyệt đối không trộn lẫn 2 bản.
4. **Vượt qua XERJ cũ (`index_stale`)**: Khi tài liệu vừa tạo/sửa trên đĩa và `xerj_search` trả `_xerj.hints` có `index_stale`, **bắt buộc dùng `safe-search.py` + `read_file` đọc trực tiếp từ đĩa** trong thư mục chức năng đó, không dựa vào đoạn trích cũ trong XERJ.

---

## 3. Quy tắc xử lý khi mâu thuẫn: Bắt buộc báo cáo người dùng, tuyệt đối không im lặng chọn lựa

1. **Phát hiện mâu thuẫn**: Khi gặp hai nguồn có cấp ưu tiên ngang nhau hoặc cấp cao hơn có nội dung phi lý/lỗi thời, tác tử **TUYỆT ĐỐI KHÔNG TỰ Ý CHỌN MỘT BÊN VÀ IM LẶNG THỰC HIỆN**.
2. **Lập biên bản sai lệch**: Ghi nhận mâu thuẫn vào mục "Câu hỏi mở cho người dùng" hoặc báo cáo phân tích, nêu rõ:
   - Nguồn A (tên file, đoạn trích, ngày tháng).
   - Nguồn B (tên file, đoạn trích, ngày tháng).
   - Tác động tiềm ẩn nếu chọn A hoặc B.
3. **Chờ chỉ thị**: Nếu điểm mâu thuẫn ảnh hưởng tới logic cốt lõi, chuyển trạng thái task sang `blocked` và chờ người dùng ra quyết định.

---

## 4. Liên kết với Quy trình Nhập liệu (Intake Protocol)

Giao thức này bổ trợ cho [agents/protocols/intake.md](intake.md):
- Quy trình intake đảm bảo giữ nguyên bản gốc trong `docs/source/` và chuyển đổi trung thực sang `docs/converted/`.
- Khi đối chiếu tài liệu với code theo intake, nếu phát hiện độ lệch giữa tài liệu nghiệp vụ và code đang chạy, tác tử tuân thủ bảng ưu tiên trên để lập báo cáo đối chiếu, không tự ý sửa tài liệu gốc hay sửa code.
