> Task: T-18 · Epic: E2 · Vai: ba

# Danh sách yêu cầu thí điểm nền tảng tri thức và kiểm chứng (R-pilot)

- **Trạng thái**: Draft (Chờ người dùng duyệt bằng file)
- **Ngày lập**: 2026-10-28
- **Tác giả**: BA
- **Tuân thủ văn phong**: [agents/protocols/spec-writing.md](../protocols/spec-writing.md)

---

## Nhóm 1: Danh mục tri thức (Catalog) và Bộ kiểm tra tính toàn vẹn (Validator)

### R-01: Khai báo nguồn tri thức duy nhất qua Manifest
- **Mô tả**: Hệ thống phải cung cấp tệp định nghĩa danh mục tri thức tập trung `knowledge.manifest.json` làm nguồn sự thật duy nhất khai báo mọi tài liệu, quan hệ phụ thuộc và quyền đọc của các vai trò.
- **Tiêu chí nghiệm thu (A/C)**: Khi quản trị viên thêm hoặc sửa một node tri thức trong manifest, các công cụ sinh đồ thị và ngữ cảnh phải nhận diện được node đó mà không cần sửa mã nguồn ứng dụng.
- **Nguồn**: PDF 49 trang (trang 11, 22–24); T-11 spec §2.
- **Card thực hiện**: T-20.
- **Trạng thái**: Draft.

### R-02: Bộ kiểm tra tính toàn vẹn của tri thức (11 Quy tắc kiểm tra V00–V10)
- **Mô tả**: Hệ thống phải cung cấp công cụ kiểm chuẩn tự động (`scripts/catalog-validator.py` hoặc tương đương) phát hiện các lỗi cấu trúc tri thức: liên kết gãy, vòng lặp phụ thuộc, tài liệu mồ côi, tài liệu lỗi thời chưa cập nhật phiên bản.
- **Tiêu chí nghiệm thu (A/C)**: Khi manifest chứa liên kết trỏ tới tệp không tồn tại hoặc xuất hiện vòng phụ thuộc A -> B -> A, validator phải phát hiện, trả về Exit Code khác 0 và chỉ rõ đường dẫn lỗi.
- **Nguồn**: PDF 49 trang (trang 24); T-11 spec §2.
- **Card thực hiện**: T-20.
- **Trạng thái**: Draft.

---

## Nhóm 2: Ngữ cảnh hóa theo vai trò và Ngân sách Token

### R-03: Trích xuất ngữ cảnh tối thiểu theo từng vai trò
- **Mô tả**: Hệ thống phải cung cấp CLI trích xuất đúng tập con tài liệu cần thiết cho từng vai trò cụ thể dựa trên manifest, đảm bảo tác tử chỉ nạp từ 28% đến 59% dung lượng toàn bộ kho tài liệu.
- **Tiêu chí nghiệm thu (A/C)**: Khi thực thi lệnh lấy ngữ cảnh cho vai `dev`, hệ thống phải trả về danh sách tài liệu kiến trúc/spec liên quan và loại trừ các tài liệu chuyên biệt của `designer` hay `debt-hunter`.
- **Nguồn**: PDF 49 trang (trang 19, 25); T-11 spec §3.
- **Card thực hiện**: T-21.
- **Trạng thái**: Draft.

### R-04: Giới hạn ngân sách Token tất định
- **Mô tả**: Hệ thống phải tính toán ước lượng số lượng token tiêu thụ dựa trên kích thước tệp (`ceil(bytes / 3)`) và cảnh báo khi tổng ngữ cảnh vượt ngưỡng trần cho phép (ngưỡng mặc định 12.000 tokens).
- **Tiêu chí nghiệm thu (A/C)**: Khi tổng kích thước tài liệu nạp vào vượt quá ngưỡng cấu hình, CLI trích xuất phải hiển thị cảnh báo `WARN: Context exceeds token budget` và đề xuất cắt tỉa.
- **Nguồn**: PDF 49 trang (trang 25); T-11 spec §3.
- **Card thực hiện**: T-21.
- **Trạng thái**: Draft.

---

## Nhóm 3: Khám phá Task đồng nhất (Task Discovery)

### R-05: Hỗ trợ cấu trúc task card lồng trong thư mục Epic
- **Mô tả**: Hệ thống phải chuẩn hóa cơ chế tìm kiếm task card: hỗ trợ đồng thời cả dạng phẳng `tasks/T-<n>.md` và dạng lồng phân hệ `tasks/<epic_dir>/T-<n>.md` trên toàn bộ các công cụ nội bộ (`agent_core`, `task-board`, `card-audit`).
- **Tiêu chí nghiệm thu (A/C)**: Khi chạy lệnh `python scripts/task-board.py` hoặc gọi API tìm card trong `agent_core/cli.py`, hệ thống phải quét chính xác 100% các card nằm trong các thư mục con `tasks/E*-*/` mà không bỏ sót hoặc trùng lặp.
- **Nguồn**: Báo cáo phân tích hiện trạng T-08, T-11 inventory; gdt-workspace-mapping mục 2.
- **Card thực hiện**: T-22.
- **Trạng thái**: Draft.

---

## Nhóm 4: Cổng kiểm tra điều kiện nhận Task (`claim_task`)

### R-06: Kiểm tra các cổng tiền điều kiện (Gate G0–G5 & SEQ)
- **Mô tả**: Hệ thống phải cung cấp script chẩn đoán `scripts/claim-task.py` kiểm tra các điều kiện tiên quyết trước khi tác tử bắt tay vào làm: (1) Cổng người duyệt G0–G5 có giá trị thật trong file; (2) Thứ tự tuần tự SEQ không bị nhảy cóc; (3) Định nghĩa sẵn sàng (DoR) được đáp ứng; (4) Không bị chặn bởi ADR chưa duyệt.
- **Tiêu chí nghiệm thu (A/C)**: Khi card có phụ thuộc `blocked_by` chưa hoàn thành hoặc chưa có dấu `[x]` duyệt của người dùng trong file, lệnh `claim-task` phải từ chối với trạng thái `BLOCKED` và giải thích lý do cụ thể.
- **Nguồn**: PDF 49 trang (trang 21, 22, 28); T-11 spec §4.
- **Card thực hiện**: T-23.
- **Trạng thái**: Draft.

### R-07: Khai báo kế hoạch phạm vi tệp có chữ ký số (Scope Plan Commitment)
- **Mô tả**: Khi nhận task thành công ở chế độ cố vấn, hệ thống phải ghi nhận cam kết phạm vi file (`scope_edit`) kèm chữ ký băm (SHA256) của snapshot hiện tại làm căn cứ đối soát cho merge gate.
- **Tiêu chí nghiệm thu (A/C)**: Khi claim task hợp lệ, hệ thống sinh ra bản ghi cam kết lease (hoặc ghi chú handoff) chứa danh sách file dự kiến sửa và hash commit gốc.
- **Nguồn**: PDF 49 trang (trang 22, 29); T-11 spec §4.
- **Card thực hiện**: T-23.
- **Trạng thái**: Draft.

---

## Nhóm 5: Ma trận truy vết yêu cầu (RTM)

### R-08: Tự động sinh bảng RTM từ frontmatter Task Card và Manifest
- **Mô tả**: Hệ thống phải cung cấp công cụ sinh ma trận truy vết `scripts/generate-rtm.py` tổng hợp luồng liên kết: `Yêu cầu (R-xxx) -> Task Card (T-xxx) -> Files sở hữu -> Test Cases -> Bằng chứng nghiệm thu`.
- **Tiêu chí nghiệm thu (A/C)**: Khi thực thi lệnh sinh RTM, hệ thống phải tạo ra tệp báo cáo Markdown `docs/RTM.md` phản ánh chính xác các trường `requirements: [...]`, `scope_edit` và kết quả test của từng card.
- **Nguồn**: PDF 49 trang (trang 14, 21); T-11 spec §5.
- **Card thực hiện**: T-24.
- **Trạng thái**: Draft.

### R-09: Đối soát độc lập và phát hiện yêu cầu bị bỏ quên
- **Mô tả**: Hệ thống phải phát hiện và cảnh báo các yêu cầu R-xxx chưa được gán vào bất kỳ task card nào hoặc task card đã đánh dấu `done` nhưng thiếu bằng chứng test kiểm chứng.
- **Tiêu chí nghiệm thu (A/C)**: Khi tồn tại một yêu cầu R-xxx không có test case hoặc không có card thực thi, báo cáo RTM phải đánh dấu cảnh báo `MISSING_COVERAGE`.
- **Nguồn**: PDF 49 trang (trang 22, 30); T-11 spec §5.
- **Card thực hiện**: T-24.
- **Trạng thái**: Draft.

---

## Nhóm 6: Kiểm chứng thực tế (Proof) và Quy trình tái hiện lỗi 2 lần

### R-10: Thu thập gói bằng chứng kiểm chứng có gắn định danh phiên (Proof Bundle)
- **Mô tả**: Hệ thống phải hỗ trợ đóng gói bằng chứng thực thi (gồm lệnh đã chạy, exit code, output rút gọn, thời gian chạy và hash của commit kiểm thử) vào một cấu trúc dữ liệu JSON chuẩn mực.
- **Tiêu chí nghiệm thu (A/C)**: Khi chạy kiểm chứng trên fixture mẫu, hệ thống phải xuất ra tệp proof bundle hợp lệ theo schema định sẵn và có thể xác minh lại tính toàn vẹn của kết quả.
- **Nguồn**: T-11 spec §5; Lauren Tan verification skill.
- **Card thực hiện**: T-25.
- **Trạng thái**: Draft.

### R-11: Khung kiểm thử tái hiện lỗi độc lập 2 lần có Reset trạng thái
- **Mô tả**: Hệ thống phải cung cấp quy trình và công cụ kiểm thử tái hiện lỗi (`harness`): triệu chứng lỗi phải xuất hiện độc lập 2 lần có reset môi trường giữa 2 lần; khi có bản vá, lỗi phải biến mất ở cả 2 lần chạy trên bản vá.
- **Tiêu chí nghiệm thu (A/C)**: Khi chạy harness kiểm thử lỗi, hệ thống phải ghi nhận trạng thái: FAIL trên bản gốc (2 lần) và PASS trên bản vá (2 lần). Nếu không tái hiện được, hệ thống phải ghi nhận trung thực kết quả `UNREPRODUCED`.
- **Nguồn**: Quy trình Benny (Lauren Tan / poteto); GDT `xu-ly-bug-hang-loat.md`.
- **Card thực hiện**: T-26.
- **Trạng thái**: Draft.

### R-12: Xây dựng Feature Map cho bề mặt dòng lệnh (CLI Feature Map)
- **Mô tả**: Hệ thống phải xây dựng tệp `docs/design/feature-map.md` mô tả cách tiếp cận, công thức kích hoạt và kiểm chứng cho toàn bộ bề mặt dòng lệnh của khung (bootstrap, upgrade, verify, doctor).
- **Tiêu chí nghiệm thu (A/C)**: Khi kiểm tra tệp `feature-map.md`, tài liệu phải chứa đủ các trường: Sub-features, How to get to it, Driving it with harness, Gotchas cho từng lệnh CLI.
- **Nguồn**: Lauren Tan verification talk; skill `feature-map`.
- **Card thực hiện**: T-26.
- **Trạng thái**: Draft.

---

## Nhóm 7: Đánh giá kỹ năng có bằng chứng (Eval v2)

### R-13: Khung đánh giá chấm mù kỹ năng với tiêu chí khách quan (Opt-in)
- **Mô tả**: Hệ thống phải cung cấp công cụ đánh giá kỹ năng `scripts/skill-eval.py` (phiên bản đã xử lý triệt để lỗi định dạng chuỗi `{}`) hỗ trợ cơ chế chấm mù: candidate không thấy rubric, judge khác họ mô hình, chấm dựa trên trace thực thi thật.
- **Tiêu chí nghiệm thu (A/C)**: Khi chạy eval trên bộ fixture kiểm thử, công cụ phải thực thi thành công, trả về bảng điểm chi tiết theo rubric và không gặp lỗi ngoại lệ chuỗi trong môi trường Windows TEMP.
- **Nguồn**: Lauren Tan eval playbook; T-11 spec §6.
- **Card thực hiện**: T-27.
- **Trạng thái**: Draft.

---

## Nhóm 8: Đóng gói phân phối và Nâng cấp an toàn

### R-14: Kiểm chứng phân phối sạch và bảo toàn tùy chỉnh khi nâng cấp
- **Mô tả**: Hệ thống phải kiểm chứng công cụ `scripts/bootstrap-project.py` và `scripts/agent-base-diff.py`: (1) Bản phân phối mới không chứa rác thử nghiệm hay tệp riêng tư; (2) Khi nâng cấp dự án đã có, các tệp đã bị sửa đổi cục bộ phải được bảo toàn và phát hiện xung đột rõ ràng.
- **Tiêu chí nghiệm thu (A/C)**: Khi thực hiện nâng cấp trên dự án fixture có sửa đổi file template, công cụ diff/upgrade phải báo xung đột và giữ nguyên 100% nội dung tùy chỉnh của người dùng.
- **Nguồn**: T-08 contract; T-11 spec §7.
- **Card thực hiện**: T-25, T-28.
- **Trạng thái**: Draft.

---

## Câu hỏi mở cho Người dùng & BA

1. **Định dạng xuất RTM**: Người dùng muốn bảng RTM sinh ra ở định dạng Markdown thuần (`docs/RTM.md`) hay cần xuất thêm định dạng bảng tính nhị phân (`.xlsx`)?
2. **Cơ chế cưỡng chế claim_task**: Trong giai đoạn pilot, `claim_task` sẽ hoạt động ở chế độ chẩn đoán cố vấn (CLI advisory check) trước khi cân nhắc can thiệp hook pre-commit?
3. **Mức độ tích hợp Eval v2**: Bộ eval kỹ năng T-27 sẽ chạy định kỳ trên CI hay chỉ kích hoạt thủ công (opt-in) khi có thay đổi lớn ở kho kỹ năng?
