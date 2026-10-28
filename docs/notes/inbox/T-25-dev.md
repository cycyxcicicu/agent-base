> summary: Hoàn thành T-25 kiểm chứng chạy thật trên fixture bootstrap và nâng cấp (proof), xuất proof bundle chuẩn.
# Handoff Note: T-25 — Kiểm chứng chạy thật trên fixture (Bootstrap & Upgrade Proof)

- **Task**: T-25
- **Agent**: dev
- **Ngày**: 2026-10-28

## 1. Việc đã làm
- Tạo `schemas/proof.schema.json` quy chuẩn envelope theo JSON Schema draft 2020-12, `additionalProperties: false`.
- Cài đặt `agent_core/verification/proof.py` với bộ kiểm chuẩn hợp đồng bằng Python stdlib cho enum, timestamp, SHA256 hex và chống path escape.
- Cài đặt CLI `scripts/proof-check.py` kiểm chuẩn độc lập tính toàn vẹn của proof và các tệp artifacts trên đĩa.
- Cài đặt `agent_core/verification/bootstrap.py`: Recipe cài đặt framework vào fixture cô lập, kiểm tra exit code 0, sự hiện diện của `.agent-base.json` và các template fresh.
- Cài đặt `agent_core/verification/upgrade.py`: Recipe nâng cấp kiểm chứng 4 kịch bản (giữ tùy chỉnh dự án, phát hiện xung đột qua `agent-base-diff.py`, an toàn dry-run không đổi byte, chạy lại idempotent).
- Cài đặt CLI `scripts/verify.py` hỗ trợ hai lệnh con `bootstrap` và `upgrade`.
- Xây dựng 3 bộ test tự động: `tests/test_proof.py`, `tests/test_verify_bootstrap.py`, `tests/test_verify_upgrade.py`.

## 2. Ghi chú cho agent sau
- T-26 sẽ mở rộng `scripts/verify.py` để bổ sung recipe tái hiện lỗi 2 lần có reset (`bug-harness`) và xây dựng `docs/design/feature-map.md`.
- T-27 sẽ sử dụng khung proof bundle để xây dựng chế độ eval chấm mù có bằng chứng.

Skill đã chọn & áp dụng: sparc-methodology
Checklist đã tuân thủ:
- TDD chặt chẽ qua từng subtask.
- 100% Python stdlib, không thêm dependency.
