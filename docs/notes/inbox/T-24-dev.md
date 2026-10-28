> summary: Hoàn thành T-24 sinh ma trận truy vết Function_RTM từ card và requirements, 14 yêu cầu liên kết đầy đủ.
# Handoff Note: T-24 — Ma trận truy vết yêu cầu (Function_RTM)

- **Task**: T-24
- **Agent**: dev
- **Ngày**: 2026-10-28

## 1. Việc đã làm
- Cài đặt `agent_core/workflow/rtm.py`:
  - `parse_requirements`: Quét bóc tách các yêu cầu R-xxx từ `docs/requirements/`.
  - `build_rtm_data`: Liên kết yêu cầu -> task card -> tệp mã nguồn -> tệp kiểm thử -> bằng chứng.
  - `render_rtm_markdown`: Sinh bảng `build/rtm/RTM.md`, cột Xác nhận giữ nguyên `[ ] Chờ duyệt (người)`.
  - Phát hiện các lỗ hổng truy vết: `MISSING_TASK`, `MISSING_CARD_FILE`, `MISSING_TEST`, `MISSING_PROOF`.
- Cài đặt CLI `scripts/rtm.py` với cờ `--check` và định dạng text/json.
- Tạo bộ kiểm thử `tests/test_rtm.py` (4 tests) kiểm thử sinh bảng, phát hiện thiếu sót, tính tất định và gọi CLI.

## 2. Ghi chú cho agent sau
- Đã hoàn tất toàn bộ các task trong Lượt 4:
  - T-20 (Knowledge Catalog & Validator)
  - T-22 (Task Discovery & Nested Folders)
  - T-21 (Context CLI & Token Budget)
  - T-23 (Task Claim Check Advisory)
  - T-24 (Function_RTM Generator)
- Sẵn sàng chuyển tiếp sang Lượt 5 (T-25: Kiểm chứng thật fixture bootstrap/upgrade; T-26: Bug harness & Feature Map; T-27: Eval v2).

Skill đã chọn & áp dụng: sparc-methodology
Checklist đã tuân thủ:
- TDD đúng chuẩn.
- 100% Python stdlib, không thêm dependency.
