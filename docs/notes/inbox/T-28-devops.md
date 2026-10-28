# Ghi chú bàn giao: T-28

> summary: Hoàn thành chuẩn hóa phân phối manifest, tích hợp CI check.yml và nâng cấp bảo toàn tùy chỉnh dự án.

- **Từ**: devops
- **Đến**: lead, qa, reviewer
- **Loại**: bàn giao task
- **Task**: T-28 (Phân phối, CI và seed tri thức — gom file dùng chung vào một chủ)
- **Skill đã chọn & áp dụng**: ship
- **Checklist đã tuân thủ**:
  - `agents/manifest.txt` khai báo `template agents/knowledge/knowledge-manifest.json` trước `copy agents/`
  - `.github/workflows/check.yml` tích hợp các bước kiểm chuẩn CI tự động
  - `scripts/bootstrap-project.py` và `scripts/agent-base-diff.py` bảo toàn tùy chỉnh khi nâng cấp
  - Seed tri thức sạch, 0 lỗi qua validator, 5/5 test T-28 đạt 100% PASS

## Bẫy và hành vi bất ngờ
- File `agent-base-diff.py` cần nhận biết `PROJECT = Path.cwd()` để phân biệt khi chạy kiểm thử đối soát trong fixture dự án con.

## Khu vực dễ vỡ
- Không có.

## Việc dở dang
- Chuyển sang T-29: Nghiệm thu kỹ thuật toàn diện Epic E2.
