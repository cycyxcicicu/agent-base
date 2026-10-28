# Ghi chú bàn giao: T-26

> summary: Hoàn tất harness tái hiện lỗi 2 lần có reset, verify mode bản gốc/vá, Feature Map và runbook CLI verification.

- **Từ**: dev
- **Đến**: lead, qa, reviewer
- **Loại**: bàn giao task
- **Task**: T-26 (Harness tái hiện lỗi hai lần, so bản gốc và bản vá, Feature Map)
- **Skill đã chọn & áp dụng**: sparc-methodology
- **Checklist đã tuân thủ**:
  - Tái hiện độc lập 2 lần có quan sát trạng thái reset sạch sẽ, không giả lập
  - Chế độ verify đối soát bản gốc (lỗi x2) và bản vá (sạch x2), proof gắn revision
  - Cả 2 file đầu ra docs có header định danh chuẩn, runbook dán output thật đã kiểm chứng

## Bẫy và hành vi bất ngờ
- Trạng thái reset phải được đo đạc qua sentinel file hoặc clean state callback; nếu callback reset không dọn sạch artifact thì harness coi là state pollution và trả `inconclusive`.
- Chế độ verify yêu cầu cả 4 lượt chạy đều thành công theo kỳ vọng (2/2 fail ở baseline, 2/2 pass ở candidate), nếu thiếu 1 lượt sẽ rơi vào `inconclusive`.

## Quyết định và lý do
- Cung cấp cờ CLI `verify.py repro --recipe <file>` với recipe declarative JSON, ngăn ngừa việc thực thi chuỗi lệnh shell tùy tiện từ nguồn không tin cậy.
- Feature Map được biên soạn độc lập theo 4 mục chuẩn của hệ thống, tương thích với protocol tại `agents/protocols/feature-map.md`.

## Khu vực dễ vỡ
- Khi mở rộng recipe cho các công cụ ngoài Python stdlib, cần đảm bảo executable nằm trong allowlist của môi trường host.

## Việc dở dang
- Không có. 4 test cases trong `tests/test_verify_repro.py` đạt 100% PASS.
