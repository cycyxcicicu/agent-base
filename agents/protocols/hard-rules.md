# Luật cứng: biến góp ý lặp lại thành kiểm tra tự động

Lý do: quy tắc viết bằng chữ (AGENTS.md, file vai trò, skill) là **luật mềm**. Agent có thể quên hoặc bỏ qua. Reviewer mà phải góp ý tay cùng một lỗi lần thứ hai là dấu hiệu quy trình thiếu một **luật cứng**: thứ máy tự chặn, không cần ai nhớ.

## 1. Cứng và mềm

| Cứng (máy chặn) | Mềm (chữ, agent có thể quên) |
|---|---|
| lint, kiểm kiểu, test trong CI | AGENTS.md, file vai trò, file `agents/stacks/*.md` |
| `scripts/merge-gate.py` (phạm vi, cỡ thay đổi, phiếu rủi ro) | skill (`.agents/skills/`) |
| hook `.githooks/*`, luật cấm lệnh của công cụ (deny) | nhận xét review viết trong card |
| `scripts/sync-adapters.py --check`, `scripts/check-skills.py` | ghi chú bàn giao |

Việc quan trọng và kiểm tra được bằng máy thì nên chuyển lên cột trái.

## 2. Quy tắc

1. **Lần thứ hai** Reviewer (hoặc QA) phải ghi cùng một loại góp ý trong cùng dự án, Reviewer **lập đề xuất luật cứng** vào card (mục "Đề xuất luật cứng", mẫu bên dưới) thay vì chỉ ghi thêm nhận xét.
2. Lead giao việc thực hiện luật cứng như một card riêng (Dev hoặc DevOps làm; luật về bảo mật thì `security` duyệt). Hook, script khung và file cấu hình CI là file dùng chung: chỉ task được chỉ định mới sửa.
3. Luật cứng mới phải **có test chứng minh nó chặn đúng** (một ca vi phạm bị chặn, một ca hợp lệ đi qua) và **không chặn nhầm** việc hợp lệ.
4. **Đường nhanh nhất: khai báo luật vào `docs/HARD-RULES.json`**, không cần viết linter. `scripts/hard-check.py` đọc file này, hỗ trợ cấm một mẫu (`forbid_regex`, kể cả cấm import chéo ranh giới module) và giới hạn độ dài file (`max_file_lines`), báo `file:dòng`. CI chạy nó trên file đổi của mỗi Pull Request. Mẫu và cách dùng: `examples/hard-rules/README.md`. Luật phức tạp hơn thì dùng linter của stack hoặc viết test.
5. Ghi mỗi luật một dòng vào `docs/HARD-RULES.md` (Writer tạo file nếu chưa có) hoặc vào trường `description` của luật: ngày, lý do, card nguồn.
6. Bỏ qua một lần có lý do bằng `hard-ignore: <id> <lý do>` (thiếu lý do thì vô hiệu); Reviewer xem lại mọi dòng này. Bỏ qua tràn lan là dấu hiệu luật sai, hãy sửa luật.
7. Chưa làm được luật cứng (cần thời gian) thì ghi `# debt:` hoặc dòng vào sổ nợ để không quên; giữa chừng vẫn giữ luật mềm.

## 2b. Ba cách biến một góp ý thành thứ không lặp lại (theo bài nói của Lauren Tan)

Khi định ghi nhận xét tay lần nữa, hỏi theo thứ tự này (từ mạnh đến yếu):
1. **Loại bỏ hẳn bằng thiết kế**: chọn công nghệ hoặc cấu trúc để lỗi **không thể xảy ra** (ví dụ ngôn ngữ có trình biên dịch chặt, tách tiến trình để mã nặng không lọt vào luồng giao diện, thiết kế sao cho đường ngắn nhất cũng là đường đúng).
2. **Cấu trúc quy ước chặt**: gom mã của một tính năng vào một thư mục, chỉ cho một cách tạo tính năng mới. Agent rất thích sao chép mẫu có sẵn nên đây là lớp ràng buộc mạnh nhất. Khai báo bằng luật `path_must_match` trong `docs/HARD-RULES.json`.
3. **Kiểm tự động**: lint, kiểm tra import giữa các lớp, test, CI (`forbid_regex`, `max_file_lines` trong `hard-check`, hoặc linter của stack).

Luật mềm (AGENTS.md, skill, hướng dẫn phong cách, bot review) chỉ nên xếp **thêm** lên trên các lớp trên, không dùng làm lớp duy nhất: chỉ là chuyện thời gian trước khi mã nguồn xuống cấp.

## 3. Không biến thành luật cứng

- Sở thích cá nhân, hoặc luật chỉ đúng với một stack hay một dự án (ví dụ cấm một API của một framework) mà đưa vào **khung dùng chung**. Luật như vậy để ở `agents/stacks/<stack>.md` hoặc cấu hình của chính dự án.
- Luật mơ hồ máy không kiểm được ("code phải sạch"): viết lại thành điều kiện đo được hoặc để làm checklist của Reviewer.

## Mẫu "Đề xuất luật cứng" trong card

```markdown
## Đề xuất luật cứng
- Lỗi lặp lại: (mô tả một câu) | Số lần: 2 | Nhận xét gốc: (card hoặc file:dòng)
- Nơi chặn đề xuất: lint / test / merge-gate / hook / CI
- Cách kiểm: (lệnh hoặc quy tắc cụ thể)
- Ca vi phạm bị chặn: ... | Ca hợp lệ đi qua: ...
- Người làm: ... | Cần duyệt thêm: ...
```
