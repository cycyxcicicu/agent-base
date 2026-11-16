# Quy trình Bàn giao & Nghiệm thu UAT (UAT Handoff & Sign-Off)

> **Loại: tham khảo.** Quy chuẩn bàn giao sang môi trường UAT/Staging và tiêu chí ký duyệt nghiệm thu trước khi lên Production.
> Liên quan: `srs-dor-dod-va-dong-goi.md`, `chuan-form-happy-path-va-test-plan-excel.md`.

## 1. Vị trí trong SDLC & Mục tiêu

UAT là chốt chặn cuối cùng kiểm chứng phần mềm đáp ứng đúng nhu cầu nghiệp vụ thực tế của người dùng:
```
[Kiểm thử Nội bộ] ──> [Bàn giao UAT (Staging)] ──> [Phiên UAT] ──> [Ký Sign-Off] ──> [Launch Gate]
```

## 2. Tiêu chuẩn Sẵn sàng Bàn giao (DoR for UAT)

Trước khi bàn giao cho khách hàng/PO, phải đạt đủ 5 điều kiện:
1. **Môi trường ổn định:** Build deploy thành công lên Staging, APM/Logs hoạt động bình thường.
2. **Kiểm thử nội bộ đạt:** 100% Unit/Integration Test pass; Golden Thread (HP-00) và Happy Path (HP-01..n) chạy thông suốt.
3. **Không có lỗi chặn:** 0 lỗi tồn đọng mức Critical (S1) hoặc High (S2).
4. **Dữ liệu UAT sẵn sàng:** Đã nạp đủ Master Data, tài khoản theo RBAC và dữ liệu mô phỏng nghiệp vụ thực (đã ẩn danh thông tin nhạy cảm PII).
5. **Tài liệu đính kèm:** Release Notes, danh sách chức năng nghiệm thu và file Excel Kịch bản UAT.

## 3. Quy trình Điều phối Phiên UAT

- **Bước 1 (Kick-off):** BA/QA demo (30–45 phút) giới thiệu Use Case mới và luồng thao tác chuẩn.
- **Bước 2 (Thực thi kiểm thử):** Người dùng/PO kiểm thử theo 2 luồng:
  - *Theo kịch bản:* Chạy danh sách ca test trong file Excel UAT.
  - *Tự do (Exploratory):* Thử nghiệm theo thói quen vận hành thực tế.
- **Bước 3 (Ghi nhận phản hồi):** Mọi bất thường ghi vào kênh defect tập trung (Mantis/Jira/Sheet UAT), cấm chat riêng lẻ.

## 4. Tiêu chí Ký duyệt Nghiệm thu (Sign-Off Matrix)

Bản build chỉ được duyệt vượt qua UAT khi thỏa mãn ma trận sau:

| Tiêu chí | Ngưỡng bắt buộc | Hành động khi vi phạm |
|---|---|---|
| **Tỷ lệ đạt (Pass Rate)** | $\ge 95\%$ tổng ca test UAT | Bổ sung ca test / chạy lại luồng gãy |
| **Lỗi Critical (S1 - Sập/Mất dữ liệu)** | **0 lỗi** | Chặn phát hành, hotfix khẩn cấp |
| **Lỗi High (S2 - Hỏng nghiệp vụ chính)** | **0 lỗi** | Chặn phát hành, sửa trong phiên UAT |
| **Lỗi Medium (S3 - Lỗi phụ/Giao diện)** | $\le 3$ lỗi (phải có Workaround) | Đưa vào backlog Sprint sau |
| **Lỗi Low (S4 - Góp ý/Chính tả)** | Ghi nhận vào Backlog | Chấp thuận nghiệm thu |

## 5. Mẫu Biên bản Nghiệm thu UAT (Sign-Off Certificate)

Biên bản nghiệm thu gồm:
- **Thông tin đợt UAT:** Tên chức năng/Version, Ngày nghiệm thu, URL Staging.
- **Thống kê kết quả:** Tổng ca test | Đạt (Pass) | Không đạt (Fail) | Tỷ lệ %.
- **Lỗi tồn đọng:** Mã defect, Mức độ, Workaround tạm thời, Người cam kết sửa.
- **Chữ ký xác nhận:** Đại diện BA, Đại diện QA, và Product Owner / Khách hàng.
