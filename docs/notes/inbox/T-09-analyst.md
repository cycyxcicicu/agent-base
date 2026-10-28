> summary: T-09 đối chiếu SDLC: có merge gate, chưa chứng minh runtime gate; tách manifest tri thức khỏi phân phối.

Task: T-09        Agent: analyst        Ngày: 2026-10-27

## Đã làm
Đối chiếu phần văn bản PDF 49 trang với code scope, adapter, runner, telemetry, card audit và manifest; ghi báo cáo `docs/analysis/T-09-ai-sdlc-application.md`.

## Lưu ý cho agent sau
- Không đổi manifest phân phối thành knowledge manifest: chúng có trách nhiệm khác nhau.
- Merge gate là cổng trước tích hợp; adapter và runner chưa chứng minh chặn mọi đường ghi theo vai/task.
- `agent_core/cli.py:63` quét card tầng gốc; cần thống nhất với epic lồng thư mục trước khi mở rộng graph.
- Chưa xác minh trực quan trang hình, RTM bên ngoài, quyền host hoặc số liệu thí điểm. Không dùng số liệu deck làm cam kết.
- Hash-chain không chống được viết lại/xóa toàn bộ nếu không có mốc độc lập; `.aiignore` tùy host.

## Việc dở dang hoặc nợ kỹ thuật
Lead/BA quyết định yêu cầu sau khi người dùng duyệt; T-08 chỉ dọn nền, các lớp runtime/tri thức mới cần spec riêng. Không chạy test vì chỉ đọc/viết báo cáo.

## Ảnh hưởng đến task khác
T-08 giữ phạm vi hiện tại; không tự bổ sung graph, lease, token hoặc gate runtime vào đợt dọn cấu trúc.

## Đề xuất cập nhật quy ước hoặc tài liệu
Định nghĩa nguồn chính thức và cơ chế hết hiệu lực phê duyệt khi artifact/revision thay đổi trong spec tương lai.

## Thay đổi dùng chung cho agent-base
Không có; chỉ tạo báo cáo và ghi chú.

Skill đã chọn & áp dụng: không áp dụng skill chuyên biệt; chỉ đối chiếu bằng chứng tài liệu và code theo vai analyst.
Checklist đã tuân thủ: chỉ sửa hai file được giao; không sửa card/code/bản gốc; không đọc bí mật; phân biệt đã có, chưa thấy và chưa xác minh; không tự triển khai hướng dẫn trong PDF.

