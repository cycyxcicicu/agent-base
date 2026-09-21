# Skill: lưu ở đâu, cài thế nào, vai nào được dùng

Skill là một thư mục chứa `SKILL.md` (và có thể kèm script, tài liệu tham chiếu) dạy agent làm một loại việc. Agent chỉ thấy tên và mô tả lúc bắt đầu phiên, và đọc toàn bộ khi thấy việc khớp mô tả.

**Skill do bên thứ ba viết là văn bản và mã chạy với quyền của agent.** Coi như cài một gói phần mềm: chưa đọc kỹ thì chưa cài. Mặc định `agent-base` **không có skill nào**.

## 1. Lưu ở đâu (theo tài liệu Kilo và Antigravity, ngày 2026-09-19)

| Nơi | Kilo Code | Antigravity |
|---|---|---|
| **`<dự-án>/.agents/skills/<tên>/SKILL.md`** | đọc (chế độ tương thích) | **đọc** (nơi chính của dự án) |
| `<dự-án>/.kilo/skills/<tên>/` | đọc (nơi chính của Kilo) | không đọc |
| `<dự-án>/.claude/skills/<tên>/` | đọc (chế độ tương thích) | không nói tới |
| `~/.kilo/skills/` (`C:\Users\<bạn>\.kilo\skills`) | đọc, dùng cho mọi dự án | không đọc |
| `~/.gemini/config/skills/` | không đọc | đọc, dùng cho mọi dự án |
| Đường dẫn khác | khai báo trong `kilo.jsonc` mục `skills.paths` hoặc `skills.urls` | không nói tới |

**Khuyến nghị: dùng `.agents/skills/` trong từng dự án.** Đây là nơi duy nhất **cả Kilo lẫn Antigravity cùng đọc**, và nằm trong repo nên xem lại được, có lịch sử Git, mang sang dự án khác cùng bộ khung. Tránh cài toàn cục (`~/.kilo/skills`, `~/.gemini/config/skills`): skill lạ sẽ có mặt ở mọi dự án mà không ai để ý.

Lưu ý:
- `.claude/` nằm trong `.gitignore` của bộ khung (theo bài giảng), nên skill đặt ở `.claude/skills/` sẽ **không được commit**, nhưng Kilo vẫn đọc nó. Đừng để skill lạ ở đó.
- Tên thư mục phải trùng `name` trong `SKILL.md`: chữ thường, số và dấu gạch ngang, không bắt đầu hay kết thúc bằng gạch ngang, tối đa 64 ký tự. `description` bắt buộc, tối đa 1024 ký tự.
- Trùng tên giữa dự án và toàn cục: skill của **dự án thắng** (theo Kilo).
- Máy này (2026-09-19): chưa có skill nào của bạn. Chỉ có 3 skill sẵn của Antigravity tại `C:\Users\ADMIN\.gemini\antigravity-ide\builtin\skills`.

## 2. Cài một skill: 7 bước

1. **Tải về thư mục tạm ngoài dự án** (ví dụ `Downloads`), không bỏ thẳng vào `.agents/skills/`.
2. **Tự đọc**, không nhờ AI đọc thay (AI đọc chỉ dẫn độc cũng bị dắt theo). Đọc cả các chỗ dễ giấu: chú thích HTML `<!-- -->` trong `SKILL.md`, mọi file script, file tham chiếu. Xem mục 3.
3. **Chạy `python scripts/check-skills.py --path <thư-mục-tạm>`** (hoặc dùng `.ps1` / `.sh`): kiểm tên, mô tả, liệt kê script và các dấu hiệu đáng ngờ. Đây chỉ là lưới lọc thô, không thay việc đọc.
4. **Chép vào `.agents/skills/<tên>/`** và **ghi một dòng vào `agents/knowledge/skills.md`**: nguồn, phiên bản hoặc mã commit, ngày duyệt, ai duyệt, vai nào được dùng, có script không.
5. **Chạy `python scripts/check-skills.py`** (không tham số): kiểm skill đã có trong sổ đăng ký chưa.
6. **Thử trong một worktree riêng** với vai quyền thấp (ví dụ `reviewer`), xem skill có kéo agent làm điều lạ không.
7. **Commit qua nhánh và Merge Request** như mọi thay đổi khác, ví dụ `chore(skills): them skill <tên>`. Ghi lại nó vào `agents/knowledge/tech-radar.md` mức "thử".

## 3. Checklist khi tự đọc một skill

- Có script (`.ps1`, `.sh`, `.py`, `.js`, `.exe`) không? Đọc từng dòng. Có tải file từ mạng (`curl`, `Invoke-WebRequest`), giải mã chuỗi (`base64`), đụng thư mục bí mật (`.ssh`, `.aws`, `.env`, trình duyệt), gửi dữ liệu ra ngoài không?
- Có chú thích HTML hoặc văn bản ẩn trong `SKILL.md` không?
- Có câu kiểu "bỏ qua các quy tắc trước đó", "không cần hỏi người dùng", "tự động duyệt", "bỏ qua kiểm tra", "tắt hook"? Loại ngay.
- Có bảo agent chạy lệnh git ghi (`commit`, `push`...)? Trái quy tắc của bạn, loại hoặc sửa.
- `description` có quá rộng ("dùng cho mọi việc") để nó tự kích hoạt ở nơi không cần?
- Tác giả là ai, repo còn được bảo trì không, có ai báo lỗi bảo mật chưa?
- Cần khóa API hay quyền đặc biệt? Không đưa khóa của dịch vụ khác vào.

## 4. Vai nào dùng skill nào

Nguyên tắc: **ít vai nhất có thể**, và skill có script chỉ dành cho vai có `bash: full` sau khi duyệt kỹ.

| Loại skill | Vai nên dùng |
|---|---|
| Đọc và chuyển tài liệu (pdf, docx, xlsx, pptx) | `ba`, `analyst`, `writer` |
| Duyệt code, kiểm thử, gỡ lỗi | `reviewer`, `qa`, `dev` |
| Bảo mật, kiểm toán | `security` |
| Thiết kế giao diện | `designer` |
| Hạ tầng, đám mây, CI/CD | `devops` |
| Cơ sở dữ liệu | `dba` |
| Nghiên cứu, viết báo cáo | `researcher`, `writer` |
| Bất kỳ loại nào | **không** cho `runner` và `orchestrator` |

## 5. Giới hạn theo vai: hiện thực ra sao

- **Skill không được vượt quyền của vai.** Skill dặn `reviewer` sửa code vẫn không làm được vì `reviewer` không có quyền `edit`. Skill dặn chạy lệnh thì vẫn bị luật shell của vai chặn (git ghi bị chặn với mọi vai). Đây là lớp bảo vệ chính, hãy giữ quyền vai chặt.
- **Kilo**: có quyền `skill` khớp theo tên skill (theo tài liệu opencode, nền của Kilo), mặc định cho phép mọi skill. Có thể khai báo cho từng vai chỉ được nạp vài skill. Tài liệu **không cho ví dụ cú pháp cụ thể**, nên `agent-base` **chưa** sinh cấu hình này. Khi bạn chọn skill đầu tiên, tôi sẽ thêm khóa `skills:` vào file vai trò rồi thử trong giao diện thật trước khi dựa vào.
- **Antigravity**: tài liệu **không** nói có giới hạn skill theo agent. Nghĩa là mọi agent trong Antigravity nhìn thấy mọi skill trong `.agents/skills/`. Vì vậy chỉ đặt vào đó skill đã duyệt kỹ và có mô tả hẹp.
- Skill trong dự án và skill từ URL **không** được chạy lệnh nhúng trong SKILL.md (theo Kilo), và mọi lệnh vẫn cần bạn duyệt. Đừng tắt cơ chế này.

## 6. Quy tắc ưu tiên

`AGENTS.md` và file vai trò **thắng skill**. Skill mâu thuẫn quy tắc thì theo quy tắc. Skill bảo bỏ qua quy tắc, tắt kiểm tra, tự duyệt, đọc khóa bí mật, hay gửi dữ liệu ra ngoài: agent dừng và báo Orchestrator (`AGENTS.md` mục 4, quy tắc 14).

## 7. Cập nhật và gỡ

- **Không tự cập nhật.** Skill từ URL (`skills.urls`) hoặc kho bên ngoài có thể đổi nội dung sau khi bạn duyệt, nên dùng bản **chép cục bộ, ghim mã commit**, không trỏ vào URL sống.
- Muốn lên phiên bản mới: làm lại 7 bước ở mục 2, cập nhật dòng trong sổ đăng ký.
- Gỡ: xóa thư mục và dòng trong sổ đăng ký, qua nhánh và Merge Request. Nếu skill từng chạm dữ liệu nhạy cảm, coi khóa liên quan là đã lộ và đổi.

## 8. Chưa xác minh

- Cú pháp quyền `skill` theo vai trong Kilo (mục 5).
- Antigravity có giới hạn skill theo agent hay không (tài liệu không nói).
- Skill có script chạy đúng trên Windows PowerShell 5.1 hay không: phụ thuộc từng skill.
- Kilo trên máy này: CLI đang lỗi thư mục tạm nên chưa liệt kê được skill bằng dòng lệnh; cần xem trong giao diện.

Nguồn tra cứu: tài liệu Kilo về Skills, tài liệu Antigravity về Agent Skills, tài liệu quyền của opencode, và các bài phân tích bảo mật về skill (Snyk, Red Hat Developer, Akamai, Sysdig).
