# Stack: Python

Lệnh dưới đây là mặc định phổ biến. Nếu `PROJECT.md` ghi lệnh khác thì theo `PROJECT.md`.

## Lệnh mặc định

| Việc | Lệnh |
|---|---|
| Tạo môi trường ảo | `python -m venv .venv` |
| Kích hoạt (PowerShell) | `.venv\Scripts\Activate.ps1` |
| Cài phụ thuộc | `pip install -r requirements.txt` (hoặc theo `pyproject.toml`) |
| Test | `pytest` |
| Lint | `ruff check .` (nếu dự án dùng ruff) |
| Format | `ruff format .` hoặc `black .` (theo dự án) |

## Cấu trúc thường dùng

`src/<package>/`, `tests/`, `pyproject.toml` hoặc `requirements.txt`.

## Quy ước code

- Đặt tên: `snake_case` cho hàm và biến, `PascalCase` cho lớp.
- Có type hint cho hàm công khai.
- Bắt lỗi cụ thể, không dùng `except:` trần.
- Theo formatter và linter mà dự án đã cấu hình, không đổi cấu hình khi không được giao.

## File dùng chung (chỉ task được chỉ định mới sửa)

`pyproject.toml`, `requirements*.txt`, lockfile (`poetry.lock`, `uv.lock`...), `setup.cfg`.

## Không sửa tay

`.venv/`, `__pycache__/`, `*.egg-info/`, `dist/`, `build/`.

## Bẫy thường gặp trên Windows

- Kích hoạt môi trường ảo bằng PowerShell có thể bị chặn bởi chính sách chạy script.
- Đường dẫn dài và khoảng trắng trong đường dẫn: dùng dấu nháy khi gọi lệnh.
- Không đặt `.venv` trong thư mục OneDrive.
