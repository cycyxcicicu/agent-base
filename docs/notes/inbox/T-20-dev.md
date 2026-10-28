> summary: Hoàn thành T-20 danh mục tri thức và validator 11 quy tắc V00-V10 với 12 test mới xanh.
# Handoff Note: T-20 — Danh mục tri thức (Catalog) và Validator

- **Task**: T-20
- **Agent**: dev
- **Ngày**: 2026-10-28

## 1. Việc đã làm
- Tạo `schemas/knowledge.schema.json` quy định schema JSON cho node tri thức và quan hệ có kiểu.
- Cài đặt `agent_core/knowledge/__init__.py` và `agent_core/knowledge/catalog.py` cung cấp `load_catalog` và `validate_catalog`.
- Hỗ trợ đầy đủ 11 mã chẩn đoán V00–V10 theo đặc tả T-11 §2 và R-01, R-02:
  - V00: Sai schema / malformed.
  - V01: Trùng lặp ID node.
  - V02: Sai định dạng TYPE:slug hoặc lệch prefix so với kind.
  - V03: Path escape hoặc đường dẫn tuyệt đối.
  - V04: Thiếu tệp nội dung trên đĩa.
  - V05: Không khớp băm SHA256 byte tệp.
  - V06: Quan hệ trỏ tới node không tồn tại (dangling).
  - V07: Sai kiểu điểm đầu / điểm cuối quan hệ.
  - V08: Self-edge (quan hệ tự trỏ).
  - V09: Chu trình vòng lặp (DFS cycle detection).
  - V10: Quá hạn xem xét (stale) so với `as_of` UTC.
- Tạo bộ kiểm thử `tests/test_knowledge_catalog.py` (12 tests) phủ toàn bộ các kịch bản lỗi và trường hợp hợp lệ (happy path).

## 2. Ghi chú cho agent sau
- Task T-21 sẽ sử dụng `load_catalog` và `validate_catalog` để xây dựng CLI `scripts/knowledge.py` và module trích xuất ngữ cảnh `agent_core/knowledge/context.py`.

Skill đã chọn & áp dụng: sparc-methodology
Checklist đã tuân thủ:
- TDD đúng chuẩn (test đỏ trước, cài đặt xanh sau).
- 100% Python stdlib, không thêm dependency.
