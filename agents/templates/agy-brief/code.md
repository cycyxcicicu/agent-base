Loại việc: code · Model gợi ý: gemini-3.8-flash-medium
Xem luật chung tại [delegation-prompt.md](file:///Users/ducnvh/Documents/agent-base/agents/protocols/delegation-prompt.md). Cấm git commit/push/reset.

## 1. Mục tiêu và Tiêu chí xong
- Mục tiêu: <Cài đặt hoặc sửa lỗi cho tính năng/bug X trong tối đa 2 file>.
- Tiêu chí xong: Viết test trước (Red) rồi sửa code (Green); đạt <AC-xx>; 0 lỗi hồi quy.
- Tên giao thức, đường dẫn, cờ, mã thoát: chép nguyên văn từ `--help` hoặc mã nguồn, không diễn đạt lại; chưa chắc thì ghi chưa kiểm chứng.

## 2. Phạm vi
- File được sửa (tối đa 2 file): `<path/to/source_file>`, `<path/to/test_file>`. Cấm dùng glob.
- File cấm chạm: Mọi file ngoài 2 file trên, file cấu hình, DB migration, package lockfile.

## 3. Định vị
- Điểm can thiệp: Tên hàm `<function_name>`, lớp `<ClassName>`, interface `<InterfaceName>`. Cấm dùng số dòng.

## 4. Lệnh bằng chứng
- Lệnh test có lọc (python3): `python3 -m unittest <test_target> -k <test_name>` (Cảnh báo: không chạy test không lọc).
- Lệnh test có lọc (mvnw): `./mvnw test -Dtest=<TestClass>#<testMethod>` (Cảnh báo: không chạy test không lọc).
- Gọi bridge với: --allow-write <path/to/source_file> <path/to/test_file> --allow-cmd <python3|./mvnw>

## 5. Báo cáo
- Chi tiết ghi vào: `docs/notes/inbox/<Task>/<Task>-agy.md` kèm output test thật và mục "CHƯA kiểm chứng".
- Chat chỉ 3 dòng: (1) Đã sửa, (2) Kết quả test Red/Green, (3) Đường dẫn báo cáo.
