"""Người cải thiện giả cho ví dụ Eval: thêm chỉ dẫn còn thiếu vào skill rồi in skill mới ra stdout.
Dùng: demo_improver.py <skill_file> <report_file>"""
import sys

skill = open(sys.argv[1], encoding="utf-8").read()
report = open(sys.argv[2], encoding="utf-8").read()  # báo cáo vòng trước; bản thật sẽ đọc để quyết định sửa gì

if "file:dòng" not in skill:
    skill = skill.rstrip("\n") + (
        "\n\n## Quy tắc dẫn chứng\n"
        "- Trước khi kết luận nguyên nhân, đọc thật các file liên quan và ghi rõ đã đọc file nào.\n"
        "- Mỗi nguyên nhân nêu kèm `file:dòng` cụ thể.\n")
print(skill)
