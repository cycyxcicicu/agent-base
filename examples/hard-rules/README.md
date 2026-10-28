# Ví dụ luật cứng (`docs/HARD-RULES.json`)

Luật cứng biến một nhận xét review lặp lại thành kiểm tra tự động: máy chặn, không ai phải nhớ. Giao thức: `agents/protocols/hard-rules.md`. Công cụ: `scripts/hard-check.py`.

## Dùng

1. Chép `hard-rules.example.json` thành `docs/HARD-RULES.json`, **xóa luật không hợp dự án**, sửa `include` cho đúng thư mục của bạn. Mọi luật trong file mẫu là ví dụ, không có luật nào bắt buộc.
2. Chạy thử trên toàn dự án để xem có bao nhiêu vi phạm cũ:

```
python scripts/hard-check.py
```

3. Trong PR chỉ kiểm file đổi (code cũ không làm đỏ PR):

```
python scripts/hard-check.py --changed-against origin/develop
```

CI của bộ khung (`.github/workflows/check.yml`) tự chạy lệnh này cho mỗi Pull Request nếu dự án có `docs/HARD-RULES.json`.

## Loại luật

| `type` | Ý nghĩa | Trường |
|---|---|---|
| `forbid_regex` | cấm một mẫu, dòng nào khớp là vi phạm | `pattern`, `include`, `exclude`, `message`, `severity` |
| `max_file_lines` | file không dài quá `max` dòng | `max`, `include`, `exclude`, `message`, `severity` |
| `path_must_match` | file thuộc `include` phải nằm đúng chỗ `allow` (cấu trúc quy ước, gom mã theo tính năng) | `allow`, `include`, `exclude`, `message`, `severity` |

- `include`, `exclude`: glob theo đường dẫn từ gốc dự án (`**` cho mọi cấp thư mục).
- `severity`: `error` (mặc định, làm CI đỏ) hoặc `warn` (chỉ báo).
- Cấm import chéo ranh giới module là `forbid_regex` với `include` là thư mục nguồn và `pattern` là câu import cấm.

## Bỏ qua có lý do

Cùng dòng hoặc dòng ngay trước: `hard-ignore: <id luật> <lý do>`. Thiếu lý do thì không có tác dụng. Reviewer xem mọi dòng `hard-ignore:` khi duyệt, và báo cáo cuối của script đếm số lần bỏ qua.

## Khi thêm luật mới

- Có **một ca vi phạm bị chặn** và **một ca hợp lệ đi qua** (viết thành test hoặc thử tay), để chắc luật không chặn nhầm.
- Luật chỉ đúng với một stack hay một dự án thì để ở dự án, **không đưa vào khung dùng chung**.
- Ghi lý do và card nguồn vào trường `description` hoặc `docs/HARD-RULES.md`.
