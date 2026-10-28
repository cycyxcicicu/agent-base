# Đánh dấu nguồn gốc AI, quản lý prompt và `.aiignore`

Nguồn: quy trình công ty "AI in SDLC" (`quy-trinh-cong-ty.md` mục 6). Mục đích: truy vết phần nào do AI viết, kiểm soát prompt tái dùng, và chặn AI đọc dữ liệu nhạy cảm.

## 1. Đánh dấu file do AI sinh

Với file mới do AI viết gần như toàn bộ (code, test, tài liệu), ghi một dòng đầu file hoặc trong ghi chú bàn giao:

```
AI_Generated: <Prompt_ID hoặc tên vai> | Contribution_Level: Lvl 1|2|3
```

| Mức | AI đóng góp | Ví dụ |
|---|---|---|
| Lvl 1 | khoảng 80–90% | khung code lặp, dữ liệu giả |
| Lvl 2 | khoảng 50% | hàm nhỏ, unit test |
| Lvl 3 | khoảng 10–20% | thuật toán, tra cứu |

Reviewer xác nhận trong verdict: `Checked AI-Code Quality: Passed` (đọc hiểu 100%, không chỉ chạy test). Không dùng số dòng code để đo đóng góp. Test do AI sinh phải ghi prompt đã dùng; AI bỏ sót lỗi người tìm ra thì cập nhật prompt.

## 2. Sổ prompt tái dùng

Prompt dùng lặp lại (giao việc cho agent, sinh test, review) ghi vào `docs/prompts/registry.md`, mỗi prompt một mục:

| Trường | Nội dung |
|---|---|
| ID | `PRM-<nhóm>-<số>`, ví dụ `PRM-BACKEND-001` |
| Phiên bản | số, tăng khi sửa |
| Người tạo, model | ai viết, chạy tốt trên model nào |
| Mục tiêu và template | biến dạng `{tên}` |
| Bộ kiểm thử | vài input và output mong đợi |

Chỉ prompt đã có bộ kiểm thử mới được coi là "golden"; người dùng duyệt trước khi ban hành.

## 3. `.aiignore`

Dự án có dữ liệu nhạy cảm đặt `.aiignore` ở gốc, liệt kê file agent không được đọc: `.env*`, khóa, cấu hình mật khẩu, dữ liệu khách hàng. Khóa chỉ truyền qua biến môi trường. Cái này **bổ sung** cho quy tắc 9 và 11 trong `AGENTS.md`, không thay thế; công cụ có thực thi `.aiignore` hay không thì kiểm tra theo từng công cụ.
