> Task: T-15 · Epic: E2 · Vai: architect

# Vòng đời Task 13 bước và 8 Cổng kiểm soát (Unified Task Lifecycle & Gate System)

Giao thức này hợp nhất quy trình phát triển phần mềm có AI hỗ trợ dựa trên tài liệu *AI in SDLC* (trang 21–29), kinh nghiệm thực tế của một dự án đã vận hành và khung làm việc `agent-base`.

---

## 1. Tám Cổng kiểm soát (Eight Quality Gates)

Mỗi task bắt buộc phải đi qua 8 cổng kiểm soát. Dấu duyệt chỉ hợp lệ khi có giá trị thật trong file (`agents/protocols/approval.md`); "ok" trong chat hoặc ô trống đều là chưa duyệt:

| Cổng | Nội dung kiểm soát | Người có thẩm quyền ghi | Trạng thái hợp lệ |
|---|---|---|---|
| **Cổng 0** | Nhật ký thay đổi phiên trước đã được duyệt | Con người (Lead/User) | `Approved` |
| **Cổng 1** | Duyệt đầu mục tài liệu và phạm vi yêu cầu | Con người (BA/Product/User) | `Xác nhận = Yes` |
| **Cổng 2** | Duyệt tài liệu thiết kế kỹ thuật chi tiết / spec | Con người (Architect/Tech Lead) | `Approved` |
| **Cổng 3** | Duyệt phương án ADR (khi có >= 2 lựa chọn kiến trúc) | Con người (Architect/User) | `Approved` |
| **Cổng 4** | Duyệt Actor, phân quyền và hệ thống giao tiếp ngoài | Con người (BA/Security/User) | `Approved` |
| **Cổng 5** | Duyệt WBS (giao việc: người phụ trách + hạn chót) | Con người (Lead/User) | `Approved` |
| **Cổng 6** | Xác nhận hoàn thành kỹ thuật (Technical Completion) | **CHỈ CON NGƯỜI TỰ TAY GHI** | `Hoàn thành` (cấm AI tự ghi) |
| **Cổng 7** | Nghiệm thu chức năng & giá trị (Sign-off Acceptance) | **CHỈ CON NGƯỜI TỰ TAY GHI** | `Xác nhận = Yes` (cấm AI tự ghi) |

---

## 2. Vòng lặp 13 bước thực thi một Task (13-Step Task Execution Loop)

Một task triển khai phải tuân thủ nghiêm ngặt 13 bước tuần tự theo 6 nhóm, không nhảy cóc:

| Nhóm | Bước | Hoạt động chi tiết | Trách nhiệm | Tương ứng trong agent-base (Hiện có / Cần bổ sung) |
|---|---|---|---|---|
| **① Phân tích & Test trước** | **1** | Phân tích bài toán, bóc tách yêu cầu và ràng buộc | BA / Dev | `challenger.md` (3 phương án + 1 khuyến nghị) |
| | **2** | Lập tài liệu kiến trúc; ghi nhận ADR nếu có >= 2 lựa chọn (chờ Cổng 3 duyệt) | Architect | `docs/adr/ADR-*.md` (trạng thái `Proposed`) |
| | **3** | **Viết kịch bản test trước khi code**: lập `TDD_TestCases` (happy path, biên) và BDD scenarios; **người duyệt kịch bản trước khi code** | QA / Dev | `agents/protocols/test-cases.md`, `qa.md` |
| **② Nhận task** | **4** | **Cổng tiền kiểm `claim_task`**: kiểm tra tự động G0–G5, tuần tự SEQ, DoR #1–#7, không bị ADR chặn, khai báo cam kết file (`scope_edit`) | Dev / Runner | Hiện tại: kiểm tra tay. Đang xây dựng: CLI `claim-task.py` (T-23) |
| **③ Thực thi** | **5** | Viết mã nguồn đúng phạm vi đã cam kết; mỗi file có chú thích `@rtm-ref`; nếu phát sinh ngoài phạm vi phải `amend_plan` có lý do | Dev | `scope_edit` trong task card; `merge-gate.ps1` chặn sửa ngoài phạm vi |
| **④ Test & Báo cáo** | **6** | Chạy kiểm thử tự động: Unit test & Integration test đạt 100% PASS | Dev / Runner | Lệnh rút gọn `python -m unittest -q` / `pytest -q` |
| | **7** | Tái hiện lỗi trên môi trường thật (nếu là task bug); xác nhận kiểm chứng | Dev / QA | `bug-repro.md`, Feature Map (T-26) |
| | **8** | Xuất báo cáo kiểm thử `Test_Execution_Report` gắn commit revision | QA / Runner | Proof bundle schema (T-11 spec §5, T-25) |
| **⑤ RTM & Đối soát** | **9** | Dev cập nhật trạng thái chức năng sang "Đã thực hiện" (không tự nhận Đã nghiệm thu) | Dev | Chuyển task card sang trạng thái `review` |
| | **10** | **Kiểm tra tuân thủ độc lập (Chế độ A4)**: đối soát diff git ↔ kế hoạch file ↔ RTM; **chỉ A4 được xác nhận "Đã đối soát qua công cụ"** | Reviewer / Process QA | Chế độ audit của `reviewer`/`qa`; `merge-gate` đối soát tự động |
| **⑥ Nhật ký & Dừng** | **11** | Soạn thảo ghi chú bàn giao hoặc nhật ký thay đổi ở trạng thái `Draft` | Dev / Writer | `docs/notes/inbox/<Task>-<agent>.md` (<= 80 dòng) |
| | **12** | Chạy kiểm chứng trên môi trường local, chuẩn bị sẵn sàng cho người dùng đánh giá | Dev / DevOps | Chạy local / headless test runner |
| | **13** | **DỪNG LẠI và đặt trạng thái "Chờ xác nhận"**: tác tử dừng toàn bộ hoạt động, khóa task kế tiếp theo SEQ để chờ con người trực tiếp nghiệm thu Cổng 6 và Cổng 7 | Toàn đội tác tử | Khóa tuần tự; con người tự tay đổi sang `done` |

---

## 3. Quy tắc xử lý lỗi và thay đổi yêu cầu: Chạy lại đủ vòng

- Khi phát sinh lỗi trong quá trình review hoặc người dùng thay đổi yêu cầu:
  1. Tuyệt đối **không sửa vội hoặc rút gọn quy trình** với lý do "lỗi nhỏ".
  2. Bắt buộc tạo task con hoặc subtask bug (ví dụ `T-12_Bug` hoặc `ChangeRequest_01`).
  3. Subtask này phải **thực hiện lại đầy đủ 13 bước**: tái hiện lỗi -> viết test case hỏng -> duyệt kịch bản -> sửa tối thiểu -> chạy test pass 100% -> đối soát độc lập -> chờ người dùng nghiệm thu.

---

## 4. Xử lý các điểm mâu thuẫn trong tài liệu gốc PDF

Trong quá trình đối chiếu tài liệu *AI in SDLC*, phát hiện 2 mâu thuẫn nội bộ:
1. **58 vs 70 mục kiểm tuân thủ của Agent 4**: Trang 30 liệt kê 70 mục (8 nhóm R4·K6·T7·G9·D10·C10·P12·S12) trong khi trang 22 ghi 58 mục.
   - *Cách giải quyết trong agent-base*: Giai đoạn pilot áp dụng bộ tiêu chí tối giản tập trung vào 8 cổng kiểm soát và merge-gate; chưa áp đặt toàn bộ 70 mục kiểm CMMI cồng kềnh.
2. **11 bước vs 13 bước giữa bản 26 trang và 49 trang**: Bản slide 26 trang rút gọn còn 11 bước, bản 49 trang mở rộng 13 bước (bổ sung bước dừng Cổng 6/7 và `claim_task`).
   - *Cách giải quyết trong agent-base*: Áp dụng chuẩn **13 bước** của bản 49 trang vì nó định nghĩa rõ ràng trần dừng và ranh giới con người nghiệm thu.
3. **Vai trò Agent 4 (A4)**: Không tạo một vai trò mới riêng biệt làm cồng kềnh hệ thống; **A4 được triển khai như một chế độ kiểm định tuân thủ (Process Audit Mode) của vai `reviewer` và `qa`**.
