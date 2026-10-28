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
- **Chú thích & Docstrings**: Bắt buộc viết bằng **Tiếng Việt có dấu** rõ ràng, súc tích để phục vụ bảo trì dự án lâu dài.
- Theo formatter và linter mà dự án đã cấu hình, không đổi cấu hình khi không được giao.

## Quy chuẩn kiểm thử (Testing & TDD)

- **Framework**: `pytest` (kết hợp `pytest-mock`, `pytest-asyncio` cho pipeline async).
- **Chế độ kiểm thử im lặng (Quiet Mode)**: Bắt buộc dùng `python -m pytest -q` khi chạy kiểm thử tự động. Khi test pass, terminal chỉ in 1 dòng tóm tắt nhằm tránh phình bộ nhớ ngữ cảnh của Agent. Khi test fail, pytest vẫn hiển thị đầy đủ 100% stack trace và file/dòng lỗi để Dev phân tích và sửa mã nguồn.
- **Dữ liệu mẫu (Mock Data)**: Lưu các payload mẫu vào `tests/mock_data/*.json` để chạy kiểm thử offline siêu tốc, không phụ thuộc mạng hay API ngoài.
- **Quy trình**: Viết test Happy Path trước trong `tests/`, sau đó hoàn thiện logic hàm trong `src/` để `pytest` chuyển từ FAIL sang PASS.

## File dùng chung (chỉ task được chỉ định mới sửa)

`pyproject.toml`, `requirements*.txt`, lockfile (`poetry.lock`, `uv.lock`...), `setup.cfg`.

## Không sửa tay

`.venv/`, `__pycache__/`, `*.egg-info/`, `dist/`, `build/`.

## Bẫy thường gặp trên Windows

- Kích hoạt môi trường ảo bằng PowerShell có thể bị chặn bởi chính sách chạy script.
- Đường dẫn dài và khoảng trắng trong đường dẫn: dùng dấu nháy khi gọi lệnh.
- Không đặt `.venv` trong thư mục OneDrive.
