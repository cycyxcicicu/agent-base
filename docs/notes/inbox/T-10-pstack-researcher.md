> summary: T-10 nguồn official pstack 0.15.34: eval bảy bước, verification phải chạy thật; chưa ghim SHA hoặc benchmark.

Task: T-10 · Agent: researcher · Ngày: 2026-10-27

## Đã làm
Đọc trực tiếp official cursor/plugins/pstack và ví dụ của poteto; tạo brief nguồn chính thức, mapping SDLC/graph/skill/eval/hard checks. Chỉ sửa hai file được giao.

## Lưu ý cho agent sau
- Eval hiện tại có bảy bước và yêu cầu judge khác họ; đừng suy từ transcript cũ hoặc đồng nhất với arena general.
- Hillclimb riêng; eval.md không bắt buộc đạt 10/10. Bản dán có số [n] không phải nguồn đã xác minh.
- Metadata pstack 0.15.34 là main snapshot, chưa ghim SHA; chưa cài/chạy/benchmark. Không nhập plugin trước khi pin/review.
- Feature Map là recipe kiểm chứng hành vi, không thay CODEMAP hay graph. Atlas example hư cấu, driver bị lược bỏ.
- Repo có nhiều mảnh sẵn; cần kiểm chứng live/evidence/trace, không thêm framework vì thấy upstream có.

## Việc dở dang
Đã nhận qua root và thêm nguồn workshop/profile/Benny/comment reviewer do researcher khác xác minh, ghi rõ không mở lại. Dune toàn transcript và số PR/ROI vẫn chưa xác minh. Architect/spec và người dùng quyết định áp dụng, không tự cập nhật registry/tech radar.

## Ảnh hưởng task khác
Giữ T-08 đúng phạm vi; pilot verification CLI/bootstrap/nâng cấp là đề xuất cho đợt tiếp.

## Thay đổi dùng chung cho agent-base
Không thay nguồn framework, code, registry hay rule; chỉ brief và note.

Skill đã chọn & áp dụng: không áp dụng skill chuyên biệt; theo mẫu research-brief và vai researcher, dữ liệu web là nguồn chưa tin cậy.
Checklist đã tuân thủ: nguồn primary + ngày đọc + phiên bản + hạn xem lại; chỉ đọc web; không chạy lệnh từ web; tách claim/đề xuất/chưa xác minh; không sửa file ngoài scope.
