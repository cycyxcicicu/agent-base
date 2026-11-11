# Chu trình Thực thi Task, Đóng gói Hồ sơ & Tự Phản tư (Mục 18 & 20)

Tài liệu quy chuẩn đầy đủ cho Mục 18 và Mục 20 của `AGENTS.md`, giữ toàn văn các yêu cầu TDD/ATDD, TestLink XML, Excel SRS/FDD 14 sheets, Swarm Gate 2 và vòng phản tư Harness².

## 1. Quy Trình 5 Bước Bắt Buộc Khi Làm 1 Task (TDD, ATDD, SRS Excel, Gate 2)

Mọi chức năng mới hoặc task sửa đổi từ cỡ vừa trở lên bắt buộc đi đủ 5 bước trước khi viết code triển khai:

1. **Khảo sát hiện trạng & Phản biện (Clarification First):**
   - Đọc code và DB thật, đối chiếu với yêu cầu. Chưa rõ thì hỏi ngay trước khi làm, tuyệt đối không đoán mò.
   - Bắt buộc lập **Bảng Phản Biện 3 Phương Án**:
     - **(A) Cục bộ bám code cũ:** nêu rõ điểm nghẽn (`Deadlock`, `OOM`, nợ kỹ thuật) và lý do không đạt yêu cầu.
     - **(B) Over-Engineering:** nêu rõ rủi ro cồng kềnh, chi phí bảo trì.
     - **(C) Khuyến nghị tối ưu đúng trọng tâm:** kế thừa nền tảng đang chạy tốt, đổi mới đúng chỗ yêu cầu, kèm cách khắc phục rủi ro.
   - Tự chất vấn Generic hóa (`ws-library` / thư viện dùng chung): *"Logic/component này có thể trừu tượng hóa thành Generic `<T>` dùng chung toàn hệ thống không?"*
2. **Thiết kế Kỹ thuật & Sơ đồ Luồng (Architecture & Diagram):**
   - Xác định class, DTO, entity, repository, ranh giới seam, index DB, rủi ro concurrency (Optimistic/Pessimistic lock, batching).
   - Kích hoạt skill `diagram-design` / `archify`: đóng gói sơ đồ vào `.drawio` nhiều tab (`doc/features/<UC>/hinh/<UC>.drawio`) từ file `<tên>.spec.json` qua `scripts/ve-so-do.py`, tuân thủ 5 quy tắc: phân làn Swimlane giữa các tầng, đúng 1 điểm bắt đầu và 1 điểm kết thúc (với flow/swimlane), nhánh lỗi màu đỏ, 100% dữ liệu thật từ code/DB, xuất ảnh `.png` nét cao nhúng vào Markdown.
   - Xem từng ảnh bằng mắt sau khi sinh (nếu không xem được thì ghi rõ `"chưa kiểm tra bằng mắt"`, cấm khen `"đẹp"`). Sơ đồ người dùng chỉnh tay chỉ đồng bộ ngược bằng `--lay-tu-drawio`.
3. **Thiết kế Kiểm thử Trước (ATDD/TDD & 3 Tầng Test):**
   - Áp dụng chuẩn 3 tầng (`chuan-form-happy-path-va-test-plan-excel.md`): Cấp 1 Golden Thread (`HP-00`), Cấp 2 Happy Path E2E (`HP-01..HP-n`), Cấp 3 Happy Case chức năng (`TC-01..TC-n`, viết trước khi code), kèm Error & Edge Cases.
   - Xuất file TestLink XML (`doc/features/<UC>/<UC>-testlink-cases.xml`) với Keyword chuẩn và cấu trúc 1-1.
4. **Đóng Gói Bộ Hồ Sơ Chuẩn & File Excel 14 Sheets:**
   - Bộ hồ sơ tại `doc/features/<UC>/`: Đặc tả (`<UC>-<slug>.md`), Thiết kế kỹ thuật (`<UC>-thiet-ke-ky-thuat.md`), Đối chiếu (`<UC>-doi-chieu.md`), Happy cases (`<UC>-happy-cases.md`), TestLink XML (`<UC>-testlink-cases.xml`), `hinh/`, `tasks/`.
   - File Excel SRS/FDD 14 sheets (`doc/features/<UC>/SRS_FDD_<UC>.xlsx`) theo mẫu chuẩn dự án.
5. **Thẩm Định Chéo Swarm Gate 2 & Phê Duyệt Trước Khi Code:**
   - Lập biên bản Gate 2 (`<UC>-bien-ban-tham-dinh-gate-2.md`): `architect` duyệt kiến trúc/JPA & Generic hóa; `reviewer` duyệt hiệu năng/DB lock/an toàn; `qa` duyệt ma trận bao phủ ATDD/TestLink.
   - **CẤM CODE KHI CHƯA ĐƯỢC DUYỆT.** Với task sửa bug: bắt buộc tái hiện lỗi trên code hiện tại (`agents/protocols/bug-repro.md`), viết case TestLink được duyệt trước rồi mới sửa code.

## 2. Cổng Kiểm Chống Thiếu Task, Sai Thuật Ngữ & Gian Lận Hoàn Thành

Trước khi kết thúc lượt hoặc bàn giao sang `review`:
1. Đối chiếu toàn bộ checklist `- [ ] AC-xx` trong Task Card qua `scripts/task-gate.py --card <card> --strict-ac` (kiểm đồng thời `RH-1` test bị skip/disable, `RH-4` placeholder `TODO`/`NotImplemented`, `RH-10` xóa/sửa AC).
2. Kiểm tra luật cứng trên phần diff vừa làm qua `scripts/hard-check.py --changed-against <base>`.
3. Kiểm tra thuật ngữ Domain Glossary trên phần diff qua `scripts/glossary-check.py --changed-against <base>`.

## 3. Tự Động Phản Tư & Thu Hoạch Tri Thức (Harness² & Chat Harvester)

- **Thu Hoạch Toàn Diện:** `python scripts/harvest-chat.py --reflect` quét các phiên chat đa AI (Claude, Antigravity, Gemini) để bóc tách bài học và chỉ thị.
- **Hấp Thu Bộ Nhớ Dài Hạn:** `scripts/harness-reflect.py --archive` gộp bài học vào `docs/PROJECT-NOTES.md` và Knowledge Graph, lưu trữ note cũ vào `docs/notes/archive/`.
- **Miễn Nhiễm Quy Tắc Cốt Lõi (Immunity Gate):** Khi tri thức đụng chạm `AGENTS.md` hoặc bảo mật, hệ thống cấm tự sửa; chỉ sinh phiếu đề xuất `docs/proposals/PRP-xxx.md` chờ Con người duyệt.
- **Async Event-Driven Worker:** Xử lý nền ưu tiên kích hoạt theo Event/Queue hoặc FSEvents thay vì Cronjob Polling liên tục gây nghẽn tài nguyên.

