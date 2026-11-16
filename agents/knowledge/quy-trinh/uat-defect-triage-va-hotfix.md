# Phân loại Lỗi & Quy trình Hotfix UAT (UAT Defect Triage & Hotfix)

> **Loại: tham khảo.** Hướng dẫn phân định lỗi trong đợt nghiệm thu UAT, xử lý mâu thuẫn yêu cầu và quy trình hotfix hỏa tốc.
> Liên quan: `uat-handoff-va-sign-off.md`, `xu-ly-bug-hang-loat.md`, `protocols/bug-repro.md`.

## 1. Phân loại Phản hồi UAT (Triage Matrix)

Trong đợt UAT, phản hồi của người dùng/khách hàng được phân loại thành 3 nhóm rõ ràng để tránh bẫy phình phạm vi (Scope Creep):

| Nhóm phản hồi | Dấu hiệu nhận biết | Người xử lý | Hành động quy định |
|---|---|---|---|
| **1. Bug Thực thụ (Defect)** | Code chạy sai đặc tả SRS/FDD đã duyệt, throw lỗi 500, crash, mất dữ liệu | Dev + QA | Gán Severity, tạo nhánh hotfix sửa ngay trên Staging |
| **2. Làm rõ (Clarification)** | Đặc tả chưa rõ ràng, người dùng hiểu khác Dev, UI gây hiểu nhầm | BA + PO | BA giải thích; nếu cần chỉnh text/nhãn nhỏ thì sửa ngay |
| **3. Yêu cầu mới (CR)** | Nghiệp vụ phát sinh mới, nằm ngoài phạm vi User Story và A/C đã ký | BA + Lead | **Cấm sửa ngay.** Lập phiếu CR đưa vào Backlog sprint sau |

## 2. Thang Đo Mức Độ Nghiêm Trọng (Severity) & Thời Hạn Xử Lý

Mọi bug nhóm 1 bắt buộc đánh giá theo ma trận sau:

- **S1 - Critical (Khẩn cấp):** Hệ thống sập, mất dữ liệu, chặn luồng chính (HP-00). *SLA:* Phản hồi $\le 15$ phút, xử lý xong $\le 2$ giờ.
- **S2 - High (Nghiêm trọng):** Chức năng chính gãy, không có đường vòng thay thế (no workaround). *SLA:* Xử lý trong ngày ($\le 8$ giờ).
- **S3 - Medium (Trung bình):** Chức năng phụ hỏng, có đường vòng tạm thời để hoàn thành tác vụ. *SLA:* Sửa trong đợt UAT hoặc Sprint sau.
- **S4 - Low (Nhẹ):** Lỗi chính tả, căn lề UI, góp ý trải nghiệm. *SLA:* Xem xét đưa vào backlog.

## 3. Quy trình Hotfix UAT Hỏa tốc (Fast-Track Workflow)

Khi phát hiện bug mức S1 hoặc S2 trong phiên UAT:

```
[Báo Defect] ──> [BA/QA Xác nhận & Anchor] ──> [Nhánh Hotfix] ──> [Test Đỏ -> Xanh] ──> [Deploy Staging] ──> [Verify & Đóng]
```

1. **Xác nhận lỗi:** QA kiểm tra và bóc mỏ neo tái hiện (log, ảnh lỗi, bước thực hiện).
2. **Tạo nhánh:** Tạo nhánh cá nhân từ nhánh test UAT (`hotfix/uat-<id>-<mô tả>`).
3. **Sửa code có bảo hiểm (TDD):**
   - Viết 1 test case tái hiện đúng lỗi (Test Đỏ).
   - Sửa code tối thiểu để test chuyển sang Xanh.
   - Kiểm tra không gây hồi quy các ca test cũ.
4. **Deploy & Kiểm chứng:** Deploy lại bản vá lên Staging, thông báo người dùng UAT kiểm tra lại và cập nhật trạng thái defect sang `Resolved`.

## 4. Quy tắc Chặn Phình Phạm Vi (Anti-Scope Creep Rule)

- Bất kỳ yêu cầu nào thay đổi Data Schema, thêm cột DB, hoặc thay đổi luồng thanh toán/hạch toán trong lúc UAT đều bị **từ chối sửa hỏa tốc**.
- Mọi thay đổi vượt quá 2 file hoặc ảnh hưởng Trunk code bắt buộc qua CCB (Change Control Board) phê duyệt trước khi chạm vào mã nguồn.
