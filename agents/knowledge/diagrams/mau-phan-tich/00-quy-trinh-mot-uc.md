# Từ phân tích tới bộ sơ đồ của MỘT UC (đọc trước khi vẽ bất kỳ sơ đồ nào)

> **Danh sách mọi loại sơ đồ và loại nào chưa có công cụ: `agents/knowledge/diagrams/ma-tran-loai-so-do.md`.**
>
> **Loại: mẫu và quy trình cho agent.** Mỗi loại sơ đồ có một file `mau-phan-tich/<loại>.md` gồm: câu hỏi sơ đồ trả lời, ký hiệu và nghĩa, **phiếu phân tích** (lấy gì, từ đâu), **khung JSON** để điền, lỗi hay gặp. Công cụ vẽ: `python3 ~/Documents/agent-base/scripts/ve-so-do.py`. Khái niệm gốc và ảnh mẫu: `agents/knowledge/srs/uml-diagrams-mastery.md` (mục tra cứu). Chuẩn dự án và lệnh: `agents/knowledge/diagrams/quy-trinh-ve-so-do-bang-json.md`.

## 1. Nguyên tắc: phân tích TRƯỚC, vẽ SAU
Sơ đồ chỉ là cách trình bày kết quả phân tích. Agent vẽ sai vì bỏ qua phân tích, không vì không biết công cụ. Thứ tự bắt buộc cho mỗi sơ đồ:
1. **Biết sơ đồ này trả lời câu hỏi gì** (mục A của mỗi file loại). Không trả lời được câu hỏi đó thì chưa nên vẽ.
2. **Thu thập nguồn thật** (mục B): tài liệu yêu cầu, mã nguồn (XERJ, không grep thô), CSDL (truy vấn chỉ đọc), Liquibase.
3. **Điền phiếu phân tích** (mục C): mỗi dòng có cột "Nguồn" (đường dẫn file:dòng, bảng, tài liệu). Dòng không có nguồn thì ghi "giả định" hoặc bỏ, KHÔNG bịa.
4. **Điền khung JSON** (mục D) từ phiếu, chạy `--check-only`, sửa lỗi và cảnh báo.
5. **Sinh, xem ảnh, đối chiếu phiếu** (có thiếu dòng nào của phiếu trên hình không), nhúng vào tài liệu.

## 2. Thứ tự phân tích cho một UC và cái gì dùng lại cho cái gì
| Bước | Sơ đồ | Lấy từ | Kết quả dùng tiếp |
|---|---|---|---|
| 1 | Use case | Tài liệu yêu cầu, bảng vai trò (IAM), tài liệu UC mục tác nhân | Danh sách tác nhân (vai thật) và use case: là khung của tài liệu UC |
| 2 | Sequence | Lần theo lời gọi từ điểm vào (controller, job, listener) trong mã | Danh sách lớp và thứ tự gọi: là **đầu vào của activity và class** |
| 3 | Activity | Sequence cộng mọi điểm rẽ nhánh (`if`, `throw`, vòng lặp) trong các hàm đã đi qua | Luồng đầy đủ kèm nhánh lỗi |
| 4 | Class | Các lớp xuất hiện ở sequence, đọc field, hàm, `extends`, `implements` | Cấu trúc của chính các lớp đó |
| 5 | ERD | Entity và Liquibase của các bảng mà các hàm đọc hoặc ghi | Bảng, cột, khóa, chỉ mục liên quan |

Sơ đồ nào cũng chỉ vẽ **thứ nằm trong luồng của UC**. Lớp, bảng, cột không được UC chạm tới thì không vẽ (kể cả khi "có sẵn").

## 3. Bảng sự thật chung (mỗi loại thêm cột riêng, xem file loại)
| Tên (lớp, hàm, bảng, cột, vai, mã lỗi, con số) | Loại | Nguồn (file:dòng, bảng, tài liệu mục) | Đã kiểm trực tiếp? |
|---|---|---|---|
Quy tắc: mỗi tên và con số trên hình phải có đúng một dòng ở đây. Con số kích thước trang, giới hạn, ngưỡng lấy từ cấu hình hoặc tài liệu đã duyệt; không có thì không ghi số.

## 4. Đóng gói
Một UC một file `<UC>.spec.json` loại `bundle` gồm bốn tab: ERD, Class, Sequence, Activity (mẫu: `ve-so-do.py --mau bundle`). Use case vẽ ra file riêng `<UC>-use-case.drawio` (spec `<UC>-use-case.spec.json`). Thư mục: `doc/features/<UC>/hinh/`. Mẫu vàng để xem cách điền: `doc/features/UC-04-advanced-filter/hinh/*.spec.json` (xem cách làm, KHÔNG chép nội dung).

## 5. Điều chung cấm làm
Bịa tên, bịa số; gộp hai vai vào một tác nhân; gộp nhiều lớp vào một làn hoặc một đối tượng mà không ghi rõ; thêm làn "Nhánh lỗi" không phải lớp; để cảnh báo tồn đọng không giải thích; không xem ảnh; ghi đè bộ sơ đồ người dùng đã chỉnh tay.

## 6. Mỗi sơ đồ dùng python nào, JSON nào, mẫu nào (bảng tra một chỗ)
Tất cả đi qua MỘT công cụ python `~/Documents/agent-base/scripts/ve-so-do.py`; khác nhau ở trường `type` của file JSON.

| Sơ đồ | `type` trong JSON | Mẫu phân tích và khung JSON | JSON mẫu in bằng lệnh | Kiểm riêng |
|---|---|---|---|---|
| Use case | `usecase` | `mau-phan-tich/use-case.md` | `ve-so-do.py --mau usecase` | tác nhân không nối, vòng include/extend, tên chung chung |
| Sequence | `sequence` | `mau-phan-tich/sequence.md` | `--mau sequence` | thông điệp trỏ đối tượng không có, kind sai |
| Activity | `activity` | `mau-phan-tich/activity.md` | `--mau activity` | nút mồ côi, nhánh thiếu nhãn, chồng nhãn, đè hộp |
| Class | `class` | `mau-phan-tich/class.md` | `--mau class` | quan hệ trỏ lớp không có, đè hộp |
| ERD | `erd` | `mau-phan-tich/erd.md` | `--mau erd` | cột không tồn tại, đường dùng chung |
| Cả bộ một UC | `bundle` | mục 4 ở trên | `--mau bundle` | bốn tab |
| Trạng thái | `statemachine` | `mau-phan-tich/state-machine.md` | `--mau statemachine` | trạng thái cụt, không với tới, initial hoặc final sai |
| Thành phần | `component` | `mau-phan-tich/component.md` | `--mau component` | giao diện không ai dùng, thành phần cô lập |
| Triển khai | `deployment` | `mau-phan-tich/deployment.md` | `--mau deployment` | nút không đường nối, nút hai cha |
| Gói | `package` | `mau-phan-tich/package.md` | `--mau package` | phụ thuộc vòng |
Một lệnh in JSON mẫu; chạy `--check-only` kiểm hình thức; chạy không cờ để sinh `.drawio` và `.png`.

**Luật không đè (bắt buộc): nét không đè nét, nét không xuyên hộp, chữ không đè chữ hay hộp; xem `quy-trinh-ve-so-do-bang-json.md` mục 4.12. Mỗi cảnh báo của `--check-only` phải sửa trước khi xuất ảnh, rồi mở ảnh nhìn lại.**

## 7. VÒNG LẶP bắt buộc: agent vẽ, kiểm, sửa, xem
1. **Agent vẽ** (Gemini, Claude, Codex...) theo mục 1 tới 5: phiếu phân tích, JSON, sinh, xem ảnh.
2. **Kiểm cả bộ** bằng công cụ thứ hai:
   `python3 ~/Documents/agent-base/scripts/kiem-bo-so-do.py doc/features/<UC>/hinh [--xerj] [--doc <UC>.md] [--ghi báo-cáo.md]`
   Công cụ này kiểm thứ `ve-so-do.py` không bắt: đủ bộ (bundle bốn tab và use case), ảnh có cũ hơn spec, `.drawio` có bị sửa tay, làn activity là "Nhánh lỗi" hay gộp Người dùng với Giao diện, điểm kết thúc chưa ghi kết quả, tác nhân là thành phần nội bộ hoặc nằm trong tên hệ thống hoặc gộp hai vai, tên lớp ở sequence và activity không có trong sơ đồ lớp, các con số trên hình cần nguồn, tên lớp chưa thấy trong XERJ (`--xerj`).
3. **Đọc báo cáo ba mức:**
   - **LỖI:** bắt buộc sửa, mã thoát 1.
   - **CẢNH BÁO:** sửa, hoặc ghi lý do chấp nhận (ví dụ làn gộp hai lớp có chủ đích).
   - **XEM TAY:** công cụ không tự kết luận được; agent kiểm chứng với nguồn thật (mã nguồn, CSDL, tài liệu) rồi ghi kết quả vào phiếu.
4. **Sửa JSON** theo báo cáo (không sửa `.drawio` sinh ra), chạy lại bước 2 cho tới khi 0 LỖI và mọi CẢNH BÁO đã giải quyết.
5. **Người (hoặc agent thứ hai) duyệt:** mở từng ảnh; đối chiếu phiếu và nguồn thật; hỏi "mỗi `if`, `throw` trong các hàm đã đi qua có trên activity chưa".
Quy tắc: agent KHÔNG tự báo "xong" khi chưa chạy bước 2 và chưa xem ảnh. Báo cáo cuối nêu đường dẫn spec, kết quả `kiem-bo-so-do`, số CẢNH BÁO còn lại và lý do, danh sách XEM TAY đã kiểm.
