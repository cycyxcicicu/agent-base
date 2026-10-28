"""Agent giả cho ví dụ Eval: không gọi model nào.
Dùng: demo_runner.py <model> <skill_file> <prompt_file>   (in câu trả lời ra stdout)"""
import sys

model, skill_file, prompt_file = sys.argv[1:4]
skill = open(skill_file, encoding="utf-8").read()
prompt = open(prompt_file, encoding="utf-8").read().strip()

if "file:dòng" in skill:
    print(f"[{model}] Đã đọc src/settings/save.ts và tests/save.test.ts. Nguyên nhân: src/settings/save.ts:42 "
          f"trả về null khi chưa có cấu hình, giao diện không xử lý. Việc: {prompt}")
else:
    print(f"[{model}] Chắc là do biến bị null ở đâu đó. Việc: {prompt}")
