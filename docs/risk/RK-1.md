# RK-1: Cải tạo context economy cho T-07 (sửa AGENTS.md + ghi đè bản sinh hàng loạt)

Status: APPROVED
Ngày lập: 2026-10-27        Người lập: lead
Mốc kiểm tra: nhánh main, HEAD f12b1a2
Yêu cầu nguyên văn của người dùng: "dự án đang làm đến cái gì" → "bây giờ cần build sao cho context nó giảm đi nhưng cái thông tin nó vẫn lấy được đủ" → "thực hiện sao cho nó chuẩn chỉ đi nhỉ"

## Đã xác minh (kèm lệnh đã dùng)
- `AGENTS.md` = 178 dòng, là nguồn duy nhất sinh `GEMINI.md`, `CODEX.md`, `.github/copilot-instructions.md`, `.agents/rules/agents-core.md` (đọc header `scripts/sync-adapters.py:10`).
- `python scripts/sync-adapters.py --check` → "OK: generated files are up to date" — bản sinh đang khớp nguồn, không có nội dung sửa tay cần giữ.
- `.qoder/agents/`, `.qoder/rules/` KHÔNG nằm trong git (`git ls-files` trả 0) — là artifact cục bộ, regenerate không rủi ro mất mát.
- `docs/notes/inbox/` có 14 note / 501 dòng; `docs/notes/INDEX.md` chưa tồn tại.
- §§15–17 AGENTS.md (dài ~30 dòng) sẽ được dời nguyên văn sang `agents/protocols/full-workflow.md` — nội dung không mất, chỉ đổi chỗ nạp.

## Sẽ mất hoặc bị đổi
- `AGENTS.md`: §§15–17 bản đầy đủ bị thay bằng bản rút gọn 2–3 dòng trỏ protocol (toàn văn vẫn còn trong protocol mới + lịch sử git).
- Các file sinh bị ghi đè khi chạy sync: `GEMINI.md`, `CODEX.md`, `.github/copilot-instructions.md`, `.agents/rules/agents-core.md` (182 dòng) — nội dung mới phản ánh AGENTS.md mới.
- `scripts/sync-adapters.py`: hằng `QODER_LOADER_RULE` đổi `trigger: always_on` → `model_decision` và rút gọn.

## Bị ảnh hưởng
- Mọi phiên agent từ nay: §§15–17 không còn nạp tự động — agent phải đọc protocol khi nhận việc vừa (đúng thiết kế, nhưng là đổi hành vi).
- Worktree Humana-Handover: nhận bản AGENTS.md mới khi sync downstream (quy trình upstream→downstream hiện hữu).
- Card T-03..T-06 đang review: không đụng file chồng phạm vi, nhưng diff review của T-05 (adapter Qoder) có thể cần đối chiếu lại sau khi loader đổi.

## Ngoài git (không hoàn tác được bằng git)
- Artifact cục bộ `.qoder/*` (gitignore) — hoàn tác bằng cách chạy lại `sync-adapters.py` sau revert, đã ghi trong kịch bản.

## Xung đột dự kiến
- Không với task đang review (scope khác nhau). Với chính nó: nếu ai sửa `agents/roles/*.md` trong lúc chờ duyệt, bản sinh lệch — xử lý bằng chạy lại sync trước commit.

## Mức rủi ro: vừa
AGENTS.md là nguồn quy tắc của mọi agent; sai sót ở đây nhân bản ra mọi IDE. Bù lại: thay đổi thuần tài liệu + script, hoàn tác đúng bằng git revert, và đã verify bản sinh sạch.

## Cách giảm rủi ro
- Giữ nguyên văn §§1–4, 11–13 (luật cấm) — chỉ cắt §§15–17; QA đối chiếu từng câu trước/sau (T-07.5).
- Trước khi commit: `git diff AGENTS.md` cho người dùng xem trực tiếp; commit mang `Risk-Approved: RK-1`.
- Chạy `sync-adapters.py --check` + toàn bộ test sau mỗi subtask.

## Phương án khác
- Junction `.qoder/agents/` → `agents/roles/` (đã loại: `.qoder/agents` là bản sinh với frontmatter riêng cho Qoder, junction sẽ mất mapping tools/model).
- Không cắt §§15–17, chỉ đổi loader (tiết kiệm ít hơn, còn ~200 dòng nạp màn).

## Chưa xác minh
- Qoder Desktop có tôn trọng `trigger: model_decision` trong rule sinh hay không — cần实测 một phiên mới sau khi regenerate (ghi vào handoff note).
- Giới hạn 16 KB của Antigravity sau khi AGENTS.md slim (nhỏ hơn nên an toàn, chưa đo lại).

## Câu hỏi cần bạn trả lời
1. Chấp thuận RK-1 để cắt §§15–17 khỏi AGENTS.md (toàn văn chuyển protocol)?
2. Loader `model_decision` nếu Qoder bỏ qua trigger (chưa xác minh) — bạn chấp nhận rủi ro nó vẫn nạp, hay giữ `always_on` bản ≤8 dòng?

## Chấp thuận
- Nguyên văn: "Duyệt RK-1" — 2026-10-27, người dùng. Hướng mặc định câu 2: loader `model_decision` (chấp nhận rủi ro phải实测; fallback always_on ≤8 dòng nếu Qoder bỏ qua trigger).
