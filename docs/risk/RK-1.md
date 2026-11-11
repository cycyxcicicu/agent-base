# RK-1: Dọn 12 template UML đặt sai loại ở 6 thư mục sang `assets/uml/_template-cu-sai/`

Status: APPROVED
Ngày lập: 2026-11-11        Người lập: lead
Mốc kiểm tra: nhánh feature/01-hard-gates-and-worktree-sync, HEAD 665b673db01a4f60f446208c9a7eb3e6717f195b
Yêu cầu nguyên văn của người dùng: "còn 1 đống template công commit à" / "thực hiện tất đi"

## Đã xác minh (kèm lệnh đã dùng)
- Liệt kê file thay đổi còn lại: `git -C /Users/ducnvh/Documents/agent-base status --short -- assets/uml`
- Kết quả cho thấy đúng **12 file xóa (`D`)** ở 6 thư mục chưa có công cụ vẽ và **29 file** trong `assets/uml/_template-cu-sai/` (`README.md` + 14 cặp `template.drawio` & `template.json` cũ đặt sai `diagramType: activity`).
- Đã kiểm tra tham chiếu bằng `scripts/safe-search.py`: không có script/test/mã nguồn nào trỏ tới 12 đường dẫn bị xóa; [`agents/knowledge/srs/uml-diagrams-mastery.md`](../../agents/knowledge/srs/uml-diagrams-mastery.md#L96) và 6 file `README-template.md` đã ghi nhận việc chuyển vào `assets/uml/_template-cu-sai/`.

## Sẽ mất hoặc bị đổi
Xóa khỏi vị trí gốc 12 file (đều là bản sao trùng lặp của mẫu sơ đồ hoạt động cũ đặt nhầm thư mục, tổng `172K` cả bộ 14 cặp trong `_template-cu-sai/`):
- `assets/uml/communication-diagram/template.drawio`, `template.json`
- `assets/uml/composite-structure-diagram/template.drawio`, `template.json`
- `assets/uml/interaction-overview-diagram/template.drawio`, `template.json`
- `assets/uml/profile-diagram/template.drawio`, `template.json`
- `assets/uml/timing-diagram/template.drawio`, `template.json`
- `assets/uml/uml-examples/template.drawio`, `template.json`

Đổi lại sẽ đưa toàn bộ `assets/uml/_template-cu-sai/` (`29` file) lên nhánh cùng `docs/risk/RK-1.md`.

## Bị ảnh hưởng
- Không có script, unit test hay tài liệu tri thức nào bị lỗi khi gỡ 12 file này (bộ `453` unit test và `refresh.py --check` chạy trên trạng thái đĩa hiện tại sau khi dọn đều đạt).
- Chỉ cache local `graphify-out/` (đã nằm trong `.gitignore`) còn ghi tên đường dẫn cũ cho tới lần index lại kế tiếp.

## Ngoài git (không hoàn tác được bằng git)
Không có (chỉ là file mẫu tĩnh trong Git repo).

## Xung đột dự kiến
Không có (trên nhánh cá nhân `feature/01-hard-gates-and-worktree-sync`).

## Mức rủi ro: thấp
Toàn bộ 12 file bị xóa ở vị trí cũ thực chất đều là bản sao giống hệt nhau của mẫu sai cũ, vừa được lưu đối chiếu tại `assets/uml/_template-cu-sai/` vừa có đầy đủ trong lịch sử commit nền `6540bda`.

## Cách giảm rủi ro
- Đã commit & tách riêng phần thêm/sửa hợp lệ (`66` file trong commit `665b673`) trước khi xử lý 12 file xóa.
- Có thể khôi phục bất kỳ lúc nào bằng `git checkout 6540bda -- assets/uml/<thư-mục>/template.drawio assets/uml/<thư-mục>/template.json`.

## Phương án khác
- Khôi phục lại 12 file sai ở 6 thư mục để né ngưỡng `>= 10` file xóa (không khuyến nghị vì bẫy agent dùng sai loại và mâu thuẫn với `README-template.md`).
- Xóa luôn cả `assets/uml/_template-cu-sai/` để repo gọn hơn, sửa lại `uml-diagrams-mastery.md`.

## Chưa xác minh
- Không có mục nào chưa xác minh đối với `assets/uml/`. (`docs/source/dwh_integration/` được giữ riêng ngoài commit vì chứa file nhị phân `9.8M` PDF và `9.3M` ZIP vượt giới hạn `5242880` bytes của `.githooks/pre-commit`).

## Câu hỏi cần bạn trả lời
1. Bạn có đồng ý xóa 12 file `template.{drawio,json}` sai cũ ở 6 thư mục trên và đưa cùng `assets/uml/_template-cu-sai/` vào commit tiếp theo không? (Nhắn rõ **"Chấp thuận RK-1"** để thực hiện).

## Chấp thuận
- [x] **Người dùng duyệt phiếu rủi ro RK-1**: ducnvh (xác nhận qua chat, AI ghi hộ) · 2026-11-11 · "chập thuân rk-1"

