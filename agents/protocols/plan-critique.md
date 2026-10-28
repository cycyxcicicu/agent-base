# Lập kế hoạch và phản biện trước khi sinh code (Plan and Critique)

Nguồn: quy trình công ty "AI in SDLC" (`quy-trinh-cong-ty.md` mục 6). Khác `challenger.md` (phản biện **đề bài**): giao thức này phản biện **kế hoạch cài đặt** của chính agent, để chặn ảo giác và trôi lệch kiến trúc.

## Khi nào dùng

Task cỡ "vừa" trở lên, hoặc bất kỳ việc nào đụng file dùng chung, API, cấu trúc dữ liệu. Việc nhỏ một hai file thì bỏ qua.

## Các bước

1. **Interface trước.** Dev viết (hoặc xác nhận) kiểu dữ liệu, schema, chữ ký hàm của phần sắp làm, theo `agents/roles/dev.md`.
2. **Trình bày kế hoạch bằng pseudo-code**, chưa sinh code thật: các bước, file sẽ đụng, hàm sẽ thêm, chỗ có thể sai. Ghi vào card, mục kế hoạch.
3. **Phản biện.** Người thẩm định theo `AGENTS.md` mục 16 (reviewer, dba, architect...) soi: có đúng interface không, có bịa thư viện hoặc hàm không, có lệch kiến trúc hiện có không, có ngoài `scope_edit` không.
4. **Khoanh ngữ cảnh.** Chỉ nạp tối đa khoảng 3 file liên quan cho mỗi bước; cần thêm thì nói rõ vì sao. Dán code mẫu có sẵn trong repo (few-shot) thay vì mô tả bằng lời.
5. **Chỉ sinh code sau dấu `[x] Plan Approved by <vai>`** (cổng ở `AGENTS.md` mục 16). Sinh xong tự đối chiếu với interface và bước 2.

## Dấu hiệu phải quay lại bước 2

Cần sửa interface giữa chừng; cần file ngoài kế hoạch; test không xanh sau hai lần sửa.
