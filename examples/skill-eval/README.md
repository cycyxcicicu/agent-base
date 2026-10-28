# Ví dụ Eval cho skill (chạy được ngay, không cần model thật)

Bộ ví dụ này dùng **runner, trọng tài và người cải thiện giả** (script Python nhỏ) để bạn thấy trọn vòng của `scripts/skill-eval.py` trước khi nối với model thật. Giao thức đầy đủ: `agents/protocols/skill-eval.md`.

| File | Vai trò |
|---|---|
| `SKILL.example.md` | skill mẫu, cố ý thiếu một chỉ dẫn |
| `rubric.example.json` | 2 tiêu chí có trọng số |
| `tasks.example.json` | 2 tác vụ (một tác vụ dễ bị đoán mò) |
| `demo_runner.py` | "agent" giả: có chỉ dẫn `file:dòng` trong skill thì trả lời có dẫn chứng, không thì đoán |
| `demo_judge.py` | trọng tài giả, chấm theo từng tiêu chí |
| `demo_improver.py` | "người cải thiện" giả: thêm chỉ dẫn còn thiếu vào skill |
| `demo_rubric.py` | "agent điều phối" giả: soạn nháp rubric |

Lưu ý: lệnh được tách bằng shlex; nếu đường dẫn thư mục dự án của bạn có dấu cách, đặt các đường dẫn trong lệnh vào dấu nháy kép.

## Thử nhanh (từ thư mục gốc dự án)

```
python scripts/skill-eval.py plan --skill examples/skill-eval/SKILL.example.md --rubric examples/skill-eval/rubric.example.json --tasks examples/skill-eval/tasks.example.json --models claude-a,gpt-b --judge gemini-c

python scripts/skill-eval.py run --skill examples/skill-eval/SKILL.example.md --rubric examples/skill-eval/rubric.example.json --tasks examples/skill-eval/tasks.example.json --models claude-a,gpt-b --judge gemini-c --runner-cmd "python examples/skill-eval/demo_runner.py {model} {skill_file} {prompt_file}" --judge-cmd "python examples/skill-eval/demo_judge.py {rubric_file} {task_file} {output_file}" --improver-cmd "python examples/skill-eval/demo_improver.py {skill_file} {report_file}" --target 10
```

Kết quả mong đợi: vòng 1 điểm thấp, vòng 2 đạt 10/10, bản tốt nhất ghi ở `examples/skill-eval/SKILL.example.best.md` (file `SKILL.example.md` **không bị sửa**). Xóa file `.best.md` sau khi xem.

Soạn nháp rubric bằng agent điều phối:

```
python scripts/skill-eval.py rubric --skill examples/skill-eval/SKILL.example.md --rubric-cmd "python examples/skill-eval/demo_rubric.py {skill_file}" --out rubric.draft.json
```

## Nối với model thật

Thay ba lệnh giả bằng CLI của công cụ bạn dùng, theo chỗ giữ chỗ ở đầu `scripts/skill-eval.py`:
- `--runner-cmd`: chạy agent với skill ({skill_file}) và việc ({prompt_file}), **in câu trả lời ra stdout**.
- `--judge-cmd`: cho model **khác họ** chấm theo rubric, **in JSON** `{"scores": {"<mã tiêu chí>": 0..10}}`.
- `--improver-cmd` (tùy chọn): in nội dung skill mới ra stdout.

Kiểm cờ dòng lệnh của công cụ bạn bằng `--help` của chính công cụ đó; ví dụ này không đoán hộ cờ nào. Luôn chạy `plan` trước để biết số lượt gọi model (mỗi lượt tốn token).
