# Khung bắt buộc của hồ sơ hoàn chỉnh một chức năng

> **Loại: tham khảo.**
> **Mã định danh:** `ho-so-hoan-chinh-khung-bat-buoc`
> **Chuyên mục:** Chuẩn hóa SRS/FDD trước bàn giao
> **Nguồn gốc:** Bài học dự án gdt-workspace (UC-01 Xuất Excel, C.I.149): hồ sơ viết dựa trên một hồ sơ cũ thay vì template nên thiếu Nhật ký, Hạng mục thiết kế và use-case chi tiết.

## Vấn đề

Một hồ sơ hoàn chỉnh bị thiếu mục dù tri thức và template đều có sẵn, vì ba lý do: (1) người viết (hoặc script sinh tài liệu) lấy **hồ sơ đã có** làm khuôn thay cho template; (2) hai khung cùng tồn tại mà không quy định khung nào là chuẩn; (3) checklist chỉ là danh sách tick tay, không có công cụ kiểm.

## Quy tắc

1. **Template là chuẩn** (khung 16 mục). Hồ sơ cũ chỉ là phần mở rộng, không thay thế template.
2. Hồ sơ hoàn chỉnh bắt buộc có: **Nhật ký thay đổi**, **Hạng mục thiết kế**, Tác nhân và yêu cầu có A/C, sơ đồ có mô tả, **use-case chi tiết** (tiền điều kiện, luồng chính khớp số bước sơ đồ, luồng thay thế, luồng ngoại lệ hoặc lỗi), WBS, RTM, kịch bản kiểm thử, rủi ro, ADR, **câu hỏi chờ xác nhận** (tách khỏi "đã giải quyết").
3. Ô "Người xác nhận", "Người duyệt" **để trống cho người**. Không tự ghi Pass, Hoàn thành, Approved.
4. Hồ sơ sinh bằng script thì **sửa script**, không sửa tay file đầu ra.
5. Số liệu (số ca, số hình, số endpoint) khớp file thật; tên bảng, API, lớp đối chiếu code.

## Kiểm trước bàn giao

```bash
python3 scripts/srs-check.py --full <file.md>
```

Chế độ `--full` bắt thêm các mục ở quy tắc 2 làm **lỗi** (mã thoát 1). Không có `--full` thì chỉ kiểm khung tối thiểu (tác nhân, use case hoặc user story, sơ đồ, NFR, kiểm thử, câu hỏi mở).

Liên quan: `agents/protocols/srs-workflow.md`, `agents/knowledge/srs/srs-fdd-writing-standard.md`, `agents/knowledge/srs/md-to-office-fidelity.md`.
