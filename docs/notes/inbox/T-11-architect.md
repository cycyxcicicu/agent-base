> summary: T-11 spec balanced còn PROPOSED; giữ legacy eval, proof trước cleanup và approval ngoài quyền AI.

Task: T-11.2 · Agent: architect · Ngày: 2026-10-27

## Đã làm
Soạn `docs/spec/T-11-knowledge-verification-eval.md`: domain, graph/context, RACI/gates, proof, verification fixture, eval migration và ownership 16 lát cắt đề xuất. Chưa triển khai hoặc chạy test runtime.

## Lưu ý cho agent sau
- `docs/CODEMAP.md` chưa tồn tại lúc đọc. Archify/CODEMAP/ADR cần Lead cấp scope riêng; hai file của phiên này không cấp quyền sửa chúng.
- `run_matrix` hiện có callers Runner/Judge string và CellResult positional; chuyển sang bundle phải opt-in, không âm thầm phá contract.
- Hash/JSON approval là metadata, không xác minh human identity; thiếu verifier ngoài quyền AI phải báo unverified.
- Subprocess cwd không là filesystem isolation; blind eval có giới hạn khi candidate cùng OS user.
- Không làm lại RK-2 cleanup, không gom dirty changes trước T-11; I15 một owner shared files và có thể cần chia phiên.
- Task-branch thiếu .deploy.json và chỉ hỗ trợ ticket số nguyên: hardblock trước code; không sửa config/script để né. Lead chốt leaf số nguyên liên kết parent thay ID chấm cho nhánh.
- I3 thêm parser tracer_bullet.py; I5b migrate audit/next; I11 chứa regression literal braces TEMP đã được QA cô lập. Các failure full baseline khác chưa chốt nguyên nhân.

## Việc dở dang và ảnh hưởng
Lead chuyển hàng thành card có scope/blocked_by; reviewer thẩm định và người dùng duyệt spec; runner lấy baseline mới. Danh sách R mới chưa được duyệt nên chưa có mapping R-xxx thật. Không claim shipped. Diagram, ADR, map còn là deliverable sau cổng duyệt.

## Đề xuất và thay đổi dùng chung
Không sửa framework hoặc file dùng chung. PROJECT.md còn placeholder; dùng unittest discovery từ CI làm contract tương thích, không tự chọn stack/dependency.

Skill đã chọn & áp dụng: codebase-design, domain-modeling, codebase-map (đã đọc và có registry cho architect); ghi glossary trong spec vì scope không cho CONTEXT.md.
Checklist đã tuân thủ: đúng hai file sở hữu; đọc nguồn nội bộ và code; không web/plugin/git ghi; phân biệt proposed/observed; không auth giả; handoff và dependencies rõ.
