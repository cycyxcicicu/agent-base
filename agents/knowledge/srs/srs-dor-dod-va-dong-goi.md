> **Loại: tham khảo.**
> Nguồn: tách từ srs-fdd-writing-standard.md mục M

# Chuẩn Hóa Đóng Gói Excel SRS_FDD 11 Sheets & Vòng Đời DoR/DoD (Mục M, Chốt 04/11/2026)

### 1. Quy chuẩn Cổng DoR (Bắt buộc thực hiện NGAY KHI NHẬN TASK):
*Tuyệt đối không đợi code xong mới hồi cứu tài liệu. Khi nhận task, Agent bắt buộc lập ngay:*
1. **Khảo sát Hiện trạng (As-Is):** Đọc code thật, kiểm tra DB thật, xác định rõ điểm nghẽn/lỗi hiện tại và nguyên nhân.
2. **Xác định Mục tiêu (To-Be):** Nêu rõ hành vi hệ thống và trạng thái dữ liệu sau khi hoàn thành.
3. **Đề xuất Hướng xử lý (Solution):** Đưa ra **3 phương án + 1 khuyến nghị dứt khoát**, kèm lý do và cách khắc phục rủi ro.
4. **Đăng ký trước 2 Người duyệt (2 Approvers):**
   * *Reviewer 1 (Dev):* Chịu trách nhiệm thiết kế, code và unit test.
   * *Lead Approver 2:* Nắm kiến trúc, phê duyệt MR trên GitLab.
5. **Khung RTM & TestLink XML trước khi code:** Bóc tách mã yêu cầu (`YC`) và lập bộ test cases (Happy Path & Edge Cases) để QA duyệt phạm vi trước khi code.

### 2. Quy chuẩn Cổng DoD & Đóng gói Bàn giao:
1. **Review code 2 người:** Phê duyệt độc lập trên Merge Request GitLab, gắn mã Ticket và commit SHA.
2. **Cập nhật Full RTM:** Bắt buộc có cột **Danh sách tệp code thay đổi thực tế** lấy từ `git diff --name-status` của MR.
3. **Gói phát hành CMMI-L3 (`doc/delivery/packages/<MÃ-GÓI>/`):** Đủ 4 file (`package-manifest.md`, `deployment-runbook.md`, `rollback-plan.md`, `uat-signoff.md`).
4. **Chuẩn hóa Excel SRS_FDD đúng 11 Sheet chuẩn Copilot (Cấm xé vụn 20-30 tabs):**
   - `Muc_Luc_Va_Thong_Tin`: PJT_Definition + Bảng so sánh Hiện trạng & Mục tiêu (`As-Is ➔ To-Be ➔ Solution ➔ Lợi ích mang lại`) + Mục lục hyperlink + Bản đồ mã liên kết.
   - `NhatKyThayDoi`: Lịch sử sửa đổi tài liệu + Checklist 14 hạng mục thiết kế.
   - `Component_Detail_Design`: Kiến trúc, Hạ tầng RabbitMQ, Chi tiết kỹ thuật, Tác động & Triển khai.
   - `YeuCau_UserStories`: Tác nhân (Actors) + Danh sách User Stories (US-01 đến US-07).
   - `Use-Case_ChiTiet`: Đóng gói trọn vẹn Use Case theo trục dọc (mô tả ➔ Activity bơi làn ➔ Sequence ➔ Vòng đời ➔ ERD ➔ API). Nhúng toàn bộ ảnh sơ đồ vào đây, cấm sinh sheet `Hinh_So_Do` riêng. Sử dụng kỹ thuật `EnhancedFreeSheet` tự động mở rộng cột cho bảng dữ liệu rộng (ERD, API).
   - `WBS_Planning`: Bảng phân việc WBS chi tiết.
   - `Function_RTM`: Function RTM + RTM Code & Test (MR GitLab, 2 Approvers, Git diff files).
   - `Ma_Tran_Truy_Vet`: Lưới ma trận trực quan WBS x (UC, YC, TC) có hyperlink nội bộ nhảy tới đúng dòng dữ liệu chi tiết.
   - `TDD_TestScenario_Cases`: Bảng định nghĩa Happy Path (luồng E2E xương sống) vs Happy Case (ca test cụ thể Dev viết TRƯỚC KHI CODE) + Scenarios theo luồng + Danh sách 20 Test Cases chi tiết (Full Test Steps, Expected Results, Preconditions từ TestLink XML).
   - `Test_Execution_Report`: Báo cáo kết quả kiểm thử (Unit test PASS, Load test, CDP verification).
   - `Risk_And_ADR`: Sổ theo dõi rủi ro kỹ thuật + Sổ quyết định kiến trúc + Câu hỏi mở.
