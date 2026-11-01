---
id: T-09
size: medium
status: done
owner: lead
epic: E03
phase: GĐ3
outputs:
  - docs/reports/FINAL-VERIFICATION-REPORT.md
branch: feature/09-final-verification
requirements: [REQ-KG-08]
scope_edit:
  - docs/reports/FINAL-VERIFICATION-REPORT.md
scope_deny:
  - AGENTS.md
---

# T-09: Đóng Gói, Kiểm Định Tự Động Toàn Diện & Nghiệm Thu Hệ Thống

## Mục tiêu
Chạy toàn bộ chu trình kiểm thử tự động của framework `agent-base` trên máy tính: từ kiểm định Catalog Tri thức, kiểm tra cổng Merge-gate, chạy chẩn đoán `doctor.py`, kiểm tra các bài test `pytest`, và đo đạc lại toàn bộ hiệu năng token context để nghiệm thu và bàn giao cho Người dùng.

## Bộ Công Cụ Kiểm Định Bắt Buộc:
1. `python scripts/refresh.py --check` (Kiểm định toàn vẹn adapter và catalog).
2. `python scripts/doctor.py` (Chẩn đoán onboarding và môi trường runtime).
3. `python scripts/harness-runner.py --status` (Kiểm định động cơ Harness²).
4. `python scripts/knowledge.py validate --root .` (Kiểm tra 11 tầng an toàn V00-V10 của Knowledge Graph).
5. `pytest -q` (Chạy toàn bộ test suite nội bộ).

## Phân Rã Subtasks Kiểu Scrum & Phê Duyệt Kế Hoạch
- [x] **T-09.1** [Chạy Kiểm Định Tự Động]: Kích hoạt toàn bộ 5 lệnh kiểm thử ở trên và ghi nhận log nguyên văn · Assigned: `runner`.
- [x] **T-09.2** [Hội Đồng Gate 2 Nghiệm Thu]: Bộ ba `architect + reviewer + qa` ký biên bản xác nhận: Tri thức mới đã nạp đủ, kho RBAC hoạt động chuẩn, context đã giảm >90% · Assigned: `reviewer`.
- [x] **T-09.3** [Lập Báo Cáo Nghiệm Thu]: Hoàn thiện tài liệu `docs/reports/FINAL-VERIFICATION-REPORT.md` trình Người dùng · Assigned: `lead`.

## Tiêu chí xong
- [x] 100% các lệnh kiểm tra tự động đều đạt kết quả PASS (0 lỗi).
- [x] Báo cáo nghiệm thu hoàn chỉnh trình Người dùng.
