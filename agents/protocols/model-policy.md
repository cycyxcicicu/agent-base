# Chính sách model: khi nào dùng model nào

Mỗi vai có một **tầng** (`model_tier` trong `agents/roles/*.md`). Tầng được ánh xạ sang model cụ thể ở **một chỗ duy nhất**: `agents/models.txt`. Nhờ vậy đổi model cho cả dự án là sửa một file, và mang bộ khung sang dự án khác không phải sửa từng vai.

Kilo cho ghim model riêng cho từng agent (`model: nhà-cung-cấp/model-id` trong file agent). `scripts/sync-adapters.ps1` sinh dòng đó khi tầng có giá trị. Tầng để trống thì vai dùng model bạn chọn trong giao diện.

## 1. Ba tầng

| Tầng | Dùng cho việc | Vai mặc định |
|---|---|---|
| **strong** | Suy luận sâu, sai một lần rất đắt hoặc khó thấy: chia việc, kiến trúc, bảo mật, duyệt code, đối chiếu tài liệu với code | lead, architect, security, reviewer, analyst |
| **standard** | Làm việc chính: viết code, migration, pipeline, nghiên cứu, nhập tài liệu, thiết kế, test, gộp ghi chú | dev, dba, devops, researcher, ba, designer, qa, writer |
| **fast** | Việc cơ học, đầu ra kiểm chứng được: chạy lệnh và báo kết quả | runner |

## 2. Khi nào nâng hoặc hạ tầng cho một việc

**Nâng lên strong** (đổi model trong giao diện, hoặc nhờ Lead giao cho vai tầng strong) khi:
- Việc cỡ **lớn**, hoặc đổi kiến trúc, đổi API, đổi cấu trúc dữ liệu.
- Đụng **bảo mật** (xác thực, phân quyền, khóa bí mật, đầu vào không tin cậy).
- Có **migration dữ liệu** hoặc deploy (khó hoàn tác).
- Agent **thất bại 2 lần liên tiếp** trên cùng một lỗi (dừng thử tiếp, nâng model hoặc đổi cách làm).
- Lỗi khó tái hiện, đa luồng, hiệu năng.

**Hạ xuống fast** khi việc cơ học và có cách kiểm chứng đầu ra: chạy test, format, đổi tên hàng loạt, tóm tắt kết quả chạy.

**Không hạ** cho: Reviewer, Security, Architect, Lead. Tiết kiệm ở đây thường tốn hơn về sau.

## 3. Quy tắc riêng

1. **Reviewer không yếu hơn Dev** của cùng task. Nên khác nhà cung cấp nếu có thể, để tránh cùng điểm mù (đây là khuyến nghị thực hành, tôi chưa đo được hiệu quả).
2. **Việc có tài liệu dài** (BA, Analyst): chọn model có ngữ cảnh đủ dài, kiểm tra trước khi giao. Ngữ cảnh không đủ thì tài liệu bị cắt mà không báo.
3. **Model miễn phí** (đuôi `:free` trong `kilo models`): không dùng cho mã hoặc tài liệu riêng tư, có khóa bí mật, hoặc dữ liệu khách hàng. Chưa xác minh chính sách dữ liệu của từng model miễn phí.
4. **Không đổi model giữa chừng một phiên** nếu tránh được: đổi xong agent mất một phần ngữ cảnh. Đổi ở ranh giới task.
5. **Ghi model đã dùng** vào "Nhật ký phiên" của task card khi việc quan trọng, để truy vết được khi kết quả có vấn đề.
6. **Xem lại định kỳ**: model đổi rất nhanh. `researcher` cập nhật `agents/knowledge/tech-radar.md` và đề xuất đổi ánh xạ ở `agents/models.txt` (người dùng duyệt).
7. **Nguồn chân lý duy nhất `agents/models.txt`**: Mọi Agent khi gọi subagent (công cụ `task`) **BẮT BUỘC** chỉ được sử dụng model đã được khai báo và ánh xạ trong `agents/models.txt` (hoặc trường `model:` trong file vai trò `.kilo/agents/<vai>.md` tương ứng). **Tuyệt đối cấm** tự ý bịa tên model, gọi model trần của hãng, hoặc dùng tool `agent_manager_models` để probe các model nằm ngoài danh mục đã cấu hình trong `agents/models.txt`. Khi muốn thay đổi model cho bất kỳ vai nào, chỉ cần sửa tại `agents/models.txt` và chạy `scripts/sync-adapters.py` để đồng bộ tự động.
8. **Chống kẹt `Compaction exhausted`**: Khi một subagent gặp lỗi tràn dung lượng ngữ cảnh (context limit/compaction exhausted sau 30-40 bước), **CẤM resume session cũ**. Lead coi việc đã hoàn thành nếu có note bàn giao và test pass, và phải mở phiên làm việc mới tinh (Fresh session) cho vai tiếp theo (Reviewer, Security), hoặc Lead trực tiếp đọc diff và chạy lệnh nghiệm thu.

## 4. Cài đặt

1. Xem model dùng được: `kilo models` (đường dẫn lệnh nằm trong thư mục extension Kilo cài trong Antigravity).
2. Điền `agents/models.txt` bằng id đúng như lệnh in ra.
3. Sinh lại: `powershell -File scripts/sync-adapters.ps1`.
4. Kiểm tra Kilo đọc đúng: `kilo agent list` (mỗi vai có trường model).

Antigravity **không** đọc trường này: model của các agent trong Antigravity chọn trong giao diện của nó. Chính sách này chỉ được ép ở Kilo.

## 5. Điều chưa xác minh

- Quyền dùng và chi phí của từng model trên tài khoản của bạn (Kilo CLI trên máy chưa lưu thông tin đăng nhập nào, tiện ích trong Antigravity có thể lưu riêng).
- Ghim model có được Kilo giữ nguyên khi agent được gọi làm subagent (`task`) hay không: cần thử trong giao diện.
- Chất lượng thực tế của từng model cho từng vai: cần đo trong giai đoạn 2 trước khi chốt ánh xạ.
