> summary: T-07 lead: chiến lược junction đã bác vì .qoder/agents là bản sinh; cải tạo thật nằm ở nguồn AGENTS.md + sync-adapters

Task: T-07        Agent: lead        Ngày: 2026-10-27

## Đã làm
- Cắt AGENTS.md 178 → 154 dòng: §§15–17 thành cổng tóm tắt, §3 bảng vai thành trích gọn; toàn văn sang `agents/protocols/full-workflow.md`. Luật §§1–4, 11–13 giữ nguyên từng chữ.
- Loader Qoder: `trigger: always_on` → `model_decision`, thân rút còn 5 dòng trỏ đường (sửa tại `scripts/sync-adapters.py` `QODER_LOADER_RULE`).
- `scripts/notes-index.py` sinh `docs/notes/INDEX.md` (14 note, mỗi note 1 dòng summary); backfill `> summary:` vào 14 note cũ.
- CI thêm step "Generated adapters and notes index are fresh" (sync --check + notes-index --check).
- RK-1 APPROVED (người dùng: "Duyệt RK-1").

## Lưu ý cho agent sau
- Bẫy / quyết định: **đừng đề xuất junction cho `.qoder/agents`** — đó là bản sinh với frontmatter riêng (`name/description/tools`) từ `agents/roles/*.md`; junction sẽ mất mapping tools và model tier. Chỉ sửa nguồn rồi chạy `sync-adapters.py`.
- **Chưa xác minh**: Qoder Desktop có thật sự tôn trọng `trigger: model_decision` không. Phải mở 1 phiên mới kiểm tra; nếu nó vẫn nạp đều thì chấp nhận (thân loader chỉ 5 dòng), nếu nó *không* nạp bao giờ thì đổi về `always_on` bản 5 dòng này (vẫn lời so với 14 dòng cũ).
- Khu vực dễ vỡ: `scripts/sync-adapters.py` có logic "quét file mồ côi" — chạy write mode sẽ **xóa** bản sinh của vai đã bị xóa trong nguồn. Lần chạy này xóa `.agents/rules/role-orchestrator.md` + `.kilo/agents/orchestrator.md` vì `agents/roles/orchestrator.md` đã bị xóa từ trước (không phải do T-07).
- Working tree repo này **đã dirty trước khi T-07 bắt đầu** (94 M / 116 ??). Không dùng `git add -A` bao giờ ở repo này — thêm từng file theo kế hoạch commit trong card.
- AGENTS.md không xuống ≤100 dòng như card ghi ban đầu: trần thực tế là 154 vì §§1–4 + 11–13 (39 dòng, trong đó rule git 4 dài ~10 dòng) phải giữ nguyên chữ theo RK-1. Muốn thấp hơn phải cắt luật cứng = cần phiếu RK mới.

## Việc dở dang
- Card phải chuyển `review` + chờ `Plan Approved by reviewer` (§16 gates) và người dùng commit.
- Downstream (Humana-Handover) chưa nhận bản AGENTS.md mới — sync theo `agents/protocols/agent-base-sync.md` sau merge.

## Skill đã chọn & áp dụng: codebase-design, careful
## Checklist đã tuân thủ: (1) sửa tại nguồn thay vì nhân bản bản sinh; (2) không dùng lệnh phá hủy — xóa duy nhất do script sync tự quản; (3) RK-1 APPROVED trước khi sửa AGENTS.md.
