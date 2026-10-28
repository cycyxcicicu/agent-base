> summary: T-08 mới là kế hoạch cấu trúc; giữ launcher, không chuyển cookie thật, cần kiểm kê trước RK.

Task: T-08        Agent: lead        Ngày: 2026-10-27

## Đã làm
Lập card kế hoạch T-08, phân vai, phụ thuộc, nghiệm thu và cổng triển khai; gửi reviewer thẩm định. Sinh Board/dashboard bằng script chính thức.

## Lưu ý cho agent sau
- Working tree đã có nhiều thay đổi trước lượt này tại main/HEAD f12b1a2; không gom hoặc coi là thay đổi của T-08.
- Giữ launcher root có chủ đích vì manifest và wrapper đang tham chiếu vị trí này. Không di chuyển chỉ để gốc ít file.
- Manifest đã loại công cụ cookie khỏi phân phối; chưa chứng minh domain leakage bằng import. Không đọc bí mật để lập inventory.
- T-08.5 có thể cần chia nhỏ sau spec. Phạm vi code trong bảng chỉ là dự kiến, chưa cấp quyền sửa.

## Việc dở dang
Review kế hoạch; người dùng chọn phương án; kiểm kê, spec, baseline mới, card con và RK trước khi chuyển hàng loạt/sinh lại. Chưa triển khai code, chưa chạy suite.

## Ảnh hưởng đến task khác
T-07 sở hữu thay đổi adapter/CI chưa hoàn tất; phải bàn giao trước T-08.7.

## Đề xuất cập nhật quy ước hoặc tài liệu
Chốt quy tắc tasks chỉ chứa tài liệu và kiểm tra tự động trong thiết kế, không sửa AGENTS.md.

## Thay đổi dùng chung cho agent-base
Không có thay đổi code/nguồn framework trong lượt lập kế hoạch.

Skill đã chọn & áp dụng: codebase-design — giữ interface launcher và tách trách nhiệm tại module hiện có.
Checklist đã tuân thủ: đọc hiện trạng; không git ghi; không di chuyển/xóa; phân scope và phụ thuộc; không tự nhận kết quả test cũ.
