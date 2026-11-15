# Chu trình Thực thi Task, Đóng gói Hồ sơ & Tự Phản tư (Mục 18 & 20)

Tài liệu quy chuẩn đầy đủ cho Mục 18 và Mục 20 của `AGENTS.md`, giữ toàn văn các yêu cầu TDD/ATDD, TestLink XML, Excel SRS/FDD 14 sheets, Swarm Gate 2 và vòng phản tư Harness².

## 1. Quy Trình 5 Bước Bắt Buộc Khi Làm 1 Task (TDD, ATDD, SRS Excel, Gate 2)

Mọi chức năng mới hoặc task sửa đổi từ cỡ vừa trở lên bắt buộc đi đủ 5 bước trước khi viết code triển khai:

1. **Khảo sát hiện trạng & Phản biện (Clarification First):**
   - Đọc code và DB thật, đối chiếu với yêu cầu. Chưa rõ thì hỏi ngay trước khi làm, tuyệt đối không đoán mò.
   - **Xác định Vùng Ảnh Hưởng (Blast Radius) & Tree Model**: Xác định rõ thay đổi thuộc **Trunk Code** (Core, Infra, Shared State, Auth, DB - yêu cầu Deep Review) hay **Leaf Code** (Isolated UI/Endpoint - yêu cầu Feature Gating).
   - **Thủ hiểm Feature Gating (DoR)**: Nếu là tính năng mới hoặc Leaf Code, bắt buộc xác định ngay: Tên Feature Flag, trạng thái mặc định (`OFF`), và cơ chế Kill-Switch (tắt flag có lập tức an toàn không).
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
   - **Kiểm định giá trị test thật (Anti-Mock Rác)**: Tuyệt đối cấm viết mock rỗng để kéo coverage. Test bắt buộc assert đúng nghiệp vụ. Với tính năng có Feature Gating, bắt buộc có test case kiểm chứng luồng hoạt động khi Flag = ON và kiểm chứng fallback khi Flag = OFF.
   - Xuất file TestLink XML (`doc/features/<UC>/<UC>-testlink-cases.xml`) với Keyword chuẩn và cấu trúc 1-1.
4. **Đóng Gói Bộ Hồ Sơ Chuẩn & File Excel 14 Sheets:**
   - Bộ hồ sơ tại `doc/features/<UC>/`: Đặc tả (`<UC>-<slug>.md`), Thiết kế kỹ thuật (`<UC>-thiet-ke-ky-thuat.md`), Đối chiếu (`<UC>-doi-chieu.md`), Happy cases (`<UC>-happy-cases.md`), TestLink XML (`<UC>-testlink-cases.xml`), `hinh/`, `tasks/`.
   - File Excel SRS/FDD 14 sheets (`doc/features/<UC>/SRS_FDD_<UC>.xlsx`) theo mẫu chuẩn dự án.
5. **Thẩm Định Chéo Swarm Gate 2 & Phê Duyệt Trước Khi Code:**
   - Lập biên bản Gate 2 (`<UC>-bien-ban-tham-dinh-gate-2.md`): `architect` duyệt kiến trúc/JPA & Generic hóa; `reviewer` duyệt hiệu năng/DB lock/an toàn & **cơ chế Kill-Switch/Feature Gating**; `qa` duyệt ma trận bao phủ ATDD/TestLink.
   - **CẤM CODE KHI CHƯA ĐƯỢC DUYỆT (Áp dụng cho Task Vừa & Lớn / Tính năng mới).** Với việc nhỏ hoặc sửa lỗi cục bộ ($\le 2$ file, có ảnh/log): tự động kích hoạt làn **Fast-Path** trong `bug-repro.md`, chỉ cần 1 test case tái hiện đơn vị (Red → Green) ngay tại repo bị lỗi, miễn trừ lập TestLink XML và biên bản Gate 2 trước khi sửa code.
   - **Điểm Kiểm Tra & Chống Lỗi Dây Chuyền (Anti-Compounding Errors Checkpoint)**: Trước khi sửa file mã nguồn, BẮT BUỘC tạo checkpoint bằng `python3 scripts/task-checkpoint.py create --task <T-xx>`. Nếu sau 2 lần sửa mà test vẫn đỏ hoặc bế tắc, BẮT BUỘC chạy `python3 scripts/task-checkpoint.py rollback --task <T-xx>` để đưa workspace về trạng thái sạch ban đầu, tuyệt đối không sửa chồng chất lên code hỏng.

## 2. Cổng Kiểm Chống Thiếu Task, Sai Thuật Ngữ & Gian Lận Hoàn Thành

Trước khi kết thúc lượt hoặc bàn giao sang `review`:
1. Đối chiếu toàn bộ checklist `- [ ] AC-xx` trong Task Card qua `scripts/task-gate.py --card <card> --strict-ac` (kiểm đồng thời `RH-1` test bị skip/disable, `RH-4` placeholder `TODO`/`NotImplemented`, `RH-10` xóa/sửa AC).
2. Kiểm tra luật cứng trên phần diff vừa làm qua `scripts/hard-check.py --changed-against <base>`.
3. Kiểm tra thuật ngữ Domain Glossary trên phần diff qua `scripts/glossary-check.py --changed-against <base>`.
4. **Bằng chứng Thẩm định Agentic (Proof-Driven Gate)**: Xuất trình đầy đủ khối `AGENTIC VALIDATION PROOF` trong Task Card và Handoff Note (xem `agents/protocols/launch-readiness.md`). Với file Frontend: bắt buộc có bằng chứng CDP/Browser (`Console errors: 0`).
5. **Kiểm chuẩn Hợp đồng Bàn giao (Handoff Schema Gate)**: Chạy `python3 scripts/handoff-validate.py --note <path-to-note> --strict-proof` để xác nhận note có đủ YAML Frontmatter chuẩn, tóm tắt hợp lệ và có bằng chứng lệnh test thật chạy qua, chống lỗi lệch pha Inter-Agent Misalignment (MAST #2).

## 3. Tự Động Phản Tư, Thu Hoạch & Tự Trị Học Hỏi (Autonomous Self-Learning Gate)

Agent **BẮT BUỘC TỰ KÍCH HOẠT** học hỏi và cập nhật tri thức một cách tự trị, TUYỆT ĐỐI KHÔNG CHỜ người dùng nhắc hay gõ lệnh:

1. **Trigger A — Tự Động Học Sau Khi Sửa Xong Bug / Test Xanh (Fast-Path & DoD Completion):**
   - Ngay sau khi test đơn vị chuyển Xanh (`Green`) và kiểm tra hard-check xong, trước khi thông báo cho người dùng, Agent tự động chạy ngầm:
     ```bash
     python3 ~/Documents/agent-base/scripts/knowledge.py learn --root ~/Documents/agent-base \
       --title "<Tên lỗi & giải pháp>" \
       --note "<Hiện tượng và nguyên nhân gốc rễ>" \
       --trap "<Bẫy kỹ thuật cần tránh>" \
       --decision "<Quyết định chuẩn hóa>"
     python3 ~/Documents/agent-base/scripts/harness-reflect.py --archive
     ```
   - Quá trình này hoàn tất trong $< 1$ giây, nạp bài học vào `PROJECT-NOTES.md` và tái biên dịch Knowledge Graph mà không làm phình context chat.

2. **Trigger B — Tự Động Thu Hoạch Khi Nhận Phản Hồi / Uốn Nắn Từ Người Dùng (User Feedback Reflex):**
   - Khi người dùng chỉnh đốn hành vi, phàn nàn về tốc độ, quy trình, hoặc ra lệnh mới (ví dụ: yêu cầu tự kích hoạt học hỏi, cấm tìm kiếm thừa, v.v.):
     - Agent nhận diện đây là **Sự Kiện Tri Thức Bậc Cao (Golden Learning Event)**.
     - Tự động chạy bộ thu hoạch chắt lọc từ các phiên chat:
       ```bash
       python3 ~/Documents/agent-base/scripts/harvest-chat.py --reflect
       python3 ~/Documents/agent-base/scripts/harness-reflect.py --archive
       ```
     - Cập nhật quy tắc trực tiếp vào quy chuẩn hệ thống nếu là chỉ thị về workflow.

3. **Trigger C — Cơ Chế Bảo Vệ & Phân Luồng Tri Thức (Dual-Channel Absorption):**
   - **Tri thức nghiệp vụ, bẫy code, quyết định kỹ thuật:** Tự động hấp thu 100% vào `PROJECT-NOTES.md` và Knowledge Graph, tự động lưu trữ note cũ sang `archive/`.
   - **Đề xuất sửa đổi Quy tắc Cốt lõi (Core Rules / Git Security):** Tự động tạo bản đề xuất `docs/proposals/PRP-xxx.md` (chống trùng lặp nếu đã có đề xuất tương tự) và báo cáo rõ để Con người thẩm định.
   - **Đồng bộ đa dự án & adapter:** Khi quy chuẩn chung thay đổi, tự động chạy `python3 ~/Documents/agent-base/scripts/sync-adapters.py` để toàn bộ 25+ adapters (Claude, Gemini, Codex, Cursor, Kilo) tại mọi workspace (`agent-base`, `gdt-workspace`, `tiktok_shoppe_jt`) lập tức kế thừa.

