> Task: T-16 · Epic: E2 · Vai: analyst

# Đề xuất thay đổi AGENTS.md và các file Vai trò (Người dùng tự xem xét & áp dụng)

- **Trạng thái**: Proposed (Chỉ người dùng có quyền áp dụng)
- **Ngày lập**: 2026-10-28
- **Tác giả**: Analyst
- **Nguyên tắc**: Tác tử AI **tuyệt đối không tự ý sửa** `AGENTS.md` hoặc `agents/roles/**`. Tài liệu này biên soạn các đề xuất sửa đổi nguyên văn để người dùng trực tiếp xem xét, quyết định và tự áp dụng qua phiếu rủi ro RK.

---

## Bảng tổng hợp 6 đề xuất thay đổi

| # | File đích & Vị trí | Đoạn hiện tại vs Đề xuất nguyên văn | Lý do | Nguồn tham chiếu | Rủi ro & Tác động bản sinh (`sync-adapters.py`) |
|---|---|---|---|---|---|
| **1** | `AGENTS.md`<br/>(Mục 16: Cổng duyệt kế hoạch) | **Hiện tại**: `Chỉ code sau khi đóng dấu [x] Plan Approved by <vai> trong card. thiếu duyệt = cấm code.`<br/><br/>**Đề xuất**: `Chỉ code sau khi có đủ hai điều kiện: (1) Reviewer verdict (tư vấn) đạt yêu cầu; (2) Dòng [x] Người dùng duyệt phạm vi bằng file được chính con người ghi nhận trong card hoặc bảng duyệt. Thiếu duyệt của người dùng = cấm code.` | Tránh việc mô hình AI tự đóng dấu duyệt thay cho con người; phân định rõ nhận xét của AI chỉ mang tính tư vấn kỹ thuật. | `agents/protocols/approval.md` (T-13), `docs/adr/ADR-13-file-approval.md`, PDF trang 22, 28. | **Rủi ro**: Thấp (chặt chẽ hơn).<br/>**Tác động**: Sửa `AGENTS.md` sẽ sinh lại `GEMINI.md` và `.agents/rules/agents-core.md`. Cần chạy `scripts/sync-adapters.ps1`. |
| **2** | `AGENTS.md`<br/>(Mục 4: Quy định git) | **Hiện tại**: `commit dùng danh tính người dùng kèm Co-Authored-By.`<br/><br/>**Đề xuất**: `commit dùng danh tính người dùng; việc kèm dòng Co-Authored-By tuân thủ mục Attribution commit trong PROJECT.md (mặc định bật; nếu dự án cấu hình none thì không thêm trailer này).` | Cho phép các dự án doanh nghiệp có chính sách bảo mật/chống dấu vết AI lựa chọn tắt trailer theo cấu hình dự án mà không vi phạm quy tắc chung. | `PROJECT.md` (T-17), `agents/protocols/git-rules.md`, kinh nghiệm GDT (X1). | **Rủi ro**: Không có.<br/>**Tác động**: Sinh lại `GEMINI.md` và `.agents/rules/agents-core.md`. |
| **3** | `agents/roles/qa.md`<br/>(Mục Quy tắc kiểm thử) | **Hiện tại**: `(Chưa có quy định chi tiết về thứ tự kịch bản và phân quyền đóng lỗi)`<br/><br/>**Đề xuất bổ sung**: `- Happy case trước code: phối hợp cùng Dev chốt kịch bản test trước khi lập trình.<br/>- Khi sửa lỗi: Dev chỉ được đặt trạng thái Resolved; CHỈ QA HOẶC CON NGƯỜI MỚI CÓ QUYỀN CLOSE sau khi tái kiểm chứng đạt.<br/>- Tuyệt đối không tự ý ghi Passed khi chưa chạy lệnh bằng chứng thật.` | Chuẩn hóa quy trình QA chuyên nghiệp, tránh việc Dev tự sửa tự đóng lỗi hoặc AI báo cáo khống test qua. | `agents/protocols/test-cases.md` (T-15), GDT `qa-process.md`. | **Rủi ro**: Thấp.<br/>**Tác động**: Sinh lại `.agents/rules/role-qa.md`, `.kilo/agents/qa.md`, `.claude/agents/qa.md`. |
| **4** | `agents/roles/reviewer.md`<br/>(Mục Chế độ kiểm tra) | **Hiện tại**: `(Chủ yếu rà soát diff mã nguồn và checklist kỹ thuật)`<br/><br/>**Đề xuất bổ sung**: `- Chế độ Kiểm tra Tuân thủ Độc lập (Process Audit / Chế độ A4): Kiểm tra đối soát 3 chiều giữa git diff ↔ kế hoạch file (scope_edit) ↔ ma trận truy vết RTM; chỉ reviewer được xác nhận 'Đã đối soát qua công cụ'. Nhận xét của reviewer là verdict tư vấn, không thay thế chữ ký duyệt của con người.` | Tận dụng vai trò Reviewer sẵn có để thực thi nhiệm vụ của Agent 4 (A4 trong SDLC) mà không cần tạo thêm vai mới làm phân mảnh đội hình. | `agents/protocols/task-loop.md` (T-15), PDF trang 22, 29, 30. | **Rủi ro**: Không có.<br/>**Tác động**: Sinh lại `.agents/rules/role-reviewer.md`, `.kilo/agents/reviewer.md`, `.claude/agents/reviewer.md`. |
| **5** | `agents/roles/lead.md`<br/>(Mục Điều phối & Cổng dừng) | **Hiện tại**: `(Giao việc, phân cỡ, giữ bảng task)`<br/><br/>**Đề xuất bổ sung**: `- Quản lý 8 cổng kiểm soát (Gate G0–G7): Cổng 6 (Hoàn thành kỹ thuật) và Cổng 7 (Nghiệm thu chức năng) bắt buộc con người tự tay ghi.<br/>- Điều phối vòng 13 bước: sau bước 12, Lead yêu cầu đội dừng toàn bộ ở trạng thái 'Chờ xác nhận', khóa task kế tiếp theo SEQ để chờ con người trực tiếp nghiệm thu.` | Thiết lập cơ chế phanh dừng tất định, ngăn AI tự động chạy tràn lan sang các task kế tiếp khi chưa có nghiệm thu thực tế của người dùng. | `agents/protocols/task-loop.md` (T-15), PDF trang 21, 22. | **Rủi ro**: Không có.<br/>**Tác động**: Sinh lại `.agents/rules/role-lead.md`, `.kilo/agents/lead.md`, `.claude/agents/lead.md`. |
| **6** | `agents/roles/ba.md`<br/>(Mục Nhiệm vụ phân tích) | **Hiện tại**: `(Rút yêu cầu R-xxx, BR-xxx)`<br/><br/>**Đề xuất bổ sung**: `- Tuân thủ nghiêm ngặt 8 nguyên tắc văn phong đặc tả (Hệ thống phải..., A/C Khi... thì..., dồn câu hỏi mở về cuối; tách biệt bộ 3 file: yêu cầu, thiết kế kỹ thuật, đối chiếu hiện trạng).<br/>- Duy trì và đối chiếu từ điển thuật ngữ miền dự án (Domain Glossary), phân định rõ nghĩa và phản nghĩa của từng khái niệm.` | Nâng cao chất lượng tài liệu đặc tả, giúp các mô hình AI đọc hiểu chính xác, không suy diễn lung tung. | `agents/protocols/spec-writing.md` (T-14), `docs/requirements/glossary.md` (T-18). | **Rủi ro**: Không có.<br/>**Tác động**: Sinh lại `.agents/rules/role-ba.md`, `.kilo/agents/ba.md`, `.claude/agents/ba.md`. |

---

## Hướng dẫn người dùng áp dụng (Khi chấp thuận)

1. Lập phiếu rủi ro `docs/risk/RK-<n>.md` với nội dung sửa đổi file được bảo vệ (`AGENTS.md`, `agents/roles/*`) và chuyển trạng thái `Status: APPROVED`.
2. Áp dụng từng nội dung đề xuất ở bảng trên vào các tệp nguồn tương ứng.
3. Chạy lệnh đồng bộ hóa adapters:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/sync-adapters.ps1
   ```
4. Kiểm tra lại tính đồng bộ:
   ```powershell
   python scripts/sync-adapters.py --check
   ```
