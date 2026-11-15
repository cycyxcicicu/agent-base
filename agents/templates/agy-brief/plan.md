Loại việc: plan · Model gợi ý: gemini-3.8-flash-medium
Xem luật chung tại [delegation-prompt.md](file:///Users/ducnvh/Documents/agent-base/agents/protocols/delegation-prompt.md). Chỉ lập kế hoạch, KHÔNG sửa code.

## 1. Mục tiêu và Tiêu chí xong
- Mục tiêu: <Lập kế hoạch thực thi chi tiết cho tính năng/nâng cấp hệ thống X>.
- Tiêu chí xong: Kế hoạch có các pha, phụ thuộc, tiêu chí nghiệm thu (AC), rủi ro, 3 phương án + 1 khuyến nghị.
- Tên giao thức, đường dẫn, cờ, mã thoát: chép nguyên văn từ `--help` hoặc mã nguồn, không diễn đạt lại; chưa chắc thì ghi chưa kiểm chứng.

## 2. Phạm vi
- File được tạo: `tasks/<Task>-plan.md` (hoặc `doc/features/<UC>/tasks/<Task>.md`). Đường dẫn chính xác, cấm glob.
- File cấm chạm: Tuyệt đối KHÔNG sửa bất kỳ file mã nguồn `src/` hay file cấu hình nào.

## 3. Định vị
- Điểm can thiệp: Heading `## Ke_Hoach_Thuc_Hien`, mục `### 3_Phuong_An`, bảng `Ma_Tran_Rui_Ro`. Cấm dùng số dòng.

## 4. Lệnh bằng chứng
- Lệnh kiểm tra file kế hoạch (python3): `python3 -c "import os; assert os.path.exists('tasks/<Task>-plan.md')"`
- Gọi bridge với: --allow-write tasks/<Task>-plan.md --allow-cmd python3

## 5. Báo cáo
- Chi tiết ghi vào: `docs/notes/inbox/<Task>/<Task>-agy.md` kèm tóm tắt kế hoạch và mục "CHƯA kiểm chứng".
- Chat chỉ 3 dòng: (1) Phương án khuyến nghị, (2) Số pha & rủi ro chính, (3) Đường dẫn báo cáo.
