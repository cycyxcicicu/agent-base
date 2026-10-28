# Sổ luật cứng của agent-base

Mỗi luật nằm trong `docs/HARD-RULES.json` và chạy bằng `python scripts/hard-check.py` (CI chạy trên file đổi của mỗi Pull Request). Giao thức: `agents/protocols/hard-rules.md`.

| Ngày | Luật | Nơi thực thi | Nguồn (lỗi đã lặp) |
|---|---|---|---|
| 2026-10-19 | `tests-unittest-only` | `hard-check` (CI, PR) | Ngày 2026-10-18 viết 2 file test kiểu pytest (`test_viewer.py`, `test_skill_eval.py`); CI chỉ chạy `unittest` nên bỏ qua 12 test. Phát hiện nhờ số test lệch (167 so với 179). Lỗi lặp lần 2 trong cùng ngày. |
| 2026-10-19 | `tests-no-bare-test-functions` | `hard-check` (CI, PR) | Cùng sự cố: hàm `def test_` ở cấp module không được `unittest discover` thu thập. |

## Lỗi đã sửa nhưng chưa có luật cứng (để không quên)
- `merge-gate.py` dùng biến `ROOT` chưa định nghĩa, bị `except` nuốt nên bước cập nhật bảng điều khiển luôn im lặng lỗi. Một bộ kiểm tên chưa định nghĩa (ví dụ pyflakes) sẽ bắt được; chưa thêm vì chưa chốt công cụ cho CI. Nếu lỗi kiểu này lặp lại lần nữa thì thêm.
- `doctor.py` thoát mã 1 trên máy CI vì thiếu thư mục kiểm dịch skill: đã sửa bằng nhánh `CI`, chưa có luật cứng chung.
