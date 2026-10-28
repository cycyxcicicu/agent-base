# Eval cho skill: kiểm thử đơn vị cho `SKILL.md`

Lý do: skill là chỉ dẫn nạp vào ngữ cảnh agent. Skill viết mơ hồ, lỗi thời hoặc chỉ hợp với một model sẽ làm agent làm sai mà không ai biết. Eval cho skill đo xem skill có thực sự làm agent làm đúng không, trên nhiều model, bằng một trọng tài độc lập.

Công cụ: `agent_core/eval/skill_eval.py` (logic, kiểm thử được không cần model) và `scripts/skill-eval.py` (chạy thật, bọc lệnh CLI của công cụ bạn dùng). Dùng khi: thêm skill mới (`skills-policy.md`), sửa skill lớn, hoặc nghi một skill đang gây lỗi lặp lại. Không bắt buộc cho mọi thay đổi nhỏ vì mỗi vòng tốn token.

**Bắt đầu ở máy nội bộ.** Viết và chạy Eval trước trên máy bạn để đọc được đầu ra thật của agent và rubric có hợp lý không; chỉ khi ổn định mới tính chạy hàng loạt hay chạy ngầm.

## 1. Quy trình

1. **Có rubric** (`rubric.json`): 3 đến 8 tiêu chí đo được, mỗi tiêu chí có trọng số. Tiêu chí viết kiểu "đã đọc file trước khi kết luận", không viết kiểu "làm tốt". **Agent điều phối soạn nháp** bằng `python scripts/skill-eval.py rubric --skill ... --rubric-cmd "<lệnh>" --out rubric.json` (tên skill lấy theo thư mục, không tin tên model tự ghi; ngoài khoảng 3 đến 8 tiêu chí thì bị từ chối), rồi **người dùng hoặc Lead đọc và sửa** trước khi chạy. Rubric là thước đo, để model tự đặt rồi tự chấm thì vô nghĩa.
2. **Viết bộ tác vụ** (`tasks.json`): 3 đến 6 việc thật, trong đó có ít nhất một việc dễ bị đoán mò và một việc mà skill nên *không* kích hoạt.
3. **Chạy ma trận** nhiều model (ít nhất 2 họ khác nhau). Mỗi lượt chạy trong thư mục tạm **tên ngẫu nhiên** và được dọn ngay sau đó; skill và việc được đưa cho agent qua file tên trung tính (`guide.md`, `ask.txt`) trong thư mục tạm cũng tên ngẫu nhiên, **không có chữ `eval`, `test` hay `skill` trong đường dẫn agent nhìn thấy**, để nó không đoán ra mình đang bị đánh giá và đổi hành vi (có test giữ điều này). Báo cáo ghi **model yếu nhất và chênh lệch giữa các model**; chênh lệch lớn (> 1.5) nghĩa là skill chỉ hợp một vài model.
4. **Trọng tài khác họ** với mọi model được thử chấm theo rubric (điểm 0..10 từng tiêu chí). Script từ chối khi trọng tài trùng hoặc cùng họ (đặt `--allow-same-family` chỉ khi buộc phải, và ghi rõ trong báo cáo).
5. **Leo núi** (tùy chọn, `--improver-cmd`): sửa skill theo báo cáo, chạy lại, **chỉ giữ bản điểm cao hơn**, dừng khi mọi model đạt mục tiêu, hết số vòng, hoặc 2 vòng liền không cải thiện.

## 2. Chạy

**Thử trước, không tốn token:** `examples/skill-eval/README.md` có đủ bộ rubric, tác vụ, runner/trọng tài/người cải thiện giả để chạy trọn một vòng leo núi ngay trên máy (ra 10/10 sau một lần sửa). Sau đó mới thay bằng lệnh model thật.

```
python scripts/skill-eval.py plan --skill .agents/skills/<tên>/SKILL.md --rubric rubric.json --tasks tasks.json --models <m1>,<m2> --judge <m3>
python scripts/skill-eval.py run  <như trên> --runner-cmd "<lệnh>" --judge-cmd "<lệnh>" [--improver-cmd "<lệnh>"] --out docs/qa/skill-eval/<tên>.md
```

Luôn chạy `plan` trước để thấy số lượt gọi model. Lệnh ngoài (`--runner-cmd`, `--judge-cmd`, `--improver-cmd`) là CLI của công cụ bạn dùng; chỗ giữ chỗ và định dạng JSON của trọng tài ghi ở đầu `scripts/skill-eval.py`. Lệnh không chạy qua shell, dùng dấu `/` trong đường dẫn, và **đường dẫn có dấu cách phải đặt trong dấu nháy kép** (ví dụ `"D:/OneDrive - x/skill.py"`), vì lệnh được tách bằng shlex. Chỗ giữ chỗ như `{skill_file}` thì không cần nháy.

## 3. Quy tắc an toàn

- **Script không tự ghi đè `SKILL.md`.** Có leo núi thì bản tốt nhất ghi ra `SKILL.best.md`; người dùng xem diff rồi tự quyết. Skill sửa xong vẫn qua checklist duyệt của `skills-policy.md` (nguồn, script, quyền).
- Chạy trong worktree hoặc thư mục tạm với vai quyền thấp; không đưa khóa bí mật vào tác vụ hay lệnh.
- Tác vụ eval dùng **dữ liệu giả**, không dùng dữ liệu thật của dự án.
- Mục tiêu 10/10 trên mọi model là rất chặt; đặt `--target` thấp hơn (ví dụ 8.5) nếu phần còn lại chỉ là khác biệt phong cách.
- Điểm của trọng tài là **ý kiến của một model**, không phải sự thật. Đọc vài đầu ra thật trước khi tin điểm.

## 4. Kết quả

Báo cáo (bảng điểm theo model và tác vụ, lịch sử các vòng) lưu ở `docs/qa/skill-eval/<skill>.md`. Ghi tóm tắt điểm vào dòng của skill trong `agents/knowledge/skills.md` hoặc `tech-radar.md` khi kết quả đáng nhớ.
