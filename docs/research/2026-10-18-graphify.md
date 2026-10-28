# Brief: Graphify (đồ thị tri thức mã nguồn)

Đọc ngày 2026-10-18. Hạn xem lại: 2027-01-16 (90 ngày).

## Câu hỏi
Có dùng được Graphify để agent đỡ lạc đường trong codebase lạ, và cài thế nào cho an toàn với agent-base?

## Đã xác minh (đọc mã thật trong kho kiểm dịch)
- Kho: `https://github.com/Graphify-Labs/graphify`, nhánh `v8`, commit `86c57be8204673c2a1b9849a3292a7dd3ab373d8`, đã clone nông vào `D:\skills-quarantine\graphify` (qua `scripts/fetch-skills.py --clone-all`, không chạy mã).
- Gói PyPI `graphifyy` (hai chữ y), phiên bản `0.9.92` trong `pyproject.toml`, giấy phép Apache-2.0 và MIT (có `LICENSE`, `LICENSE-MIT`, `NOTICE`), Python >= 3.10.
- Skill gốc là `graphify/skill.md` (44 KB, không phải `SKILL.md`). Nó: tự cài gói bằng `uv tool install` hoặc `pip install graphifyy` kể cả `--break-system-packages`; chạy rất nhiều khối `python -c`; ép dùng subagent ("MANDATORY"); ghi `graphify-out/`. Với agent-base: `python -c` bị cấm theo `sync-adapters.py`, và agent không được tự cài gói, nên **không dùng nguyên văn**.
- README nói: mã phân tích cục bộ bằng tree-sitter; `graphify extract` chạy offline với mã; `--code-only` bỏ tài liệu/ảnh (phần cần LLM); mọi lệnh `query/path/explain` được ghi vào `~/.cache/graphify-queries.log` (tắt bằng `GRAPHIFY_QUERY_LOG_DISABLE=1`); `graphify install` ghi vào hồ sơ người dùng (`--project` giữ trong thư mục dự án); `graphify hook install` cài hook; cạnh có nhãn `EXTRACTED`/`INFERRED`.

## Chưa xác minh
- Con số 128 nghìn sao, 80% giảm token, "không có telemetry": lấy từ trang GitHub/README, chưa kiểm độc lập. Chưa chạy công cụ, chưa đọc toàn bộ mã Python.
- Tên người bảo trì và lịch phát hành.
- Hành vi thật của `graphify extract --code-only` (chưa chạy).

## Quyết định
Mức **Thử**. Áp dụng ý tưởng qua skill tự viết `codebase-map` (cấp 0 bản đồ thư mục, cấp 1 chỉ đọc đồ thị do người dùng cài). Agent-base không cài, không đặt hook, không chạy công cụ.
