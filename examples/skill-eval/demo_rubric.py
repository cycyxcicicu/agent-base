"""Agent điều phối giả cho ví dụ Eval: soạn NHÁP rubric từ skill (bản thật sẽ nhờ model đọc skill rồi đề xuất).
Dùng: demo_rubric.py <skill_file>   (in JSON ra stdout, có thể kèm lời dẫn như model thật hay làm)"""
import json
import sys

skill = open(sys.argv[1], encoding="utf-8").read()
items = [
    {"id": "doc-file", "description": "Nói rõ đã đọc file nào trước khi kết luận", "weight": 2},
    {"id": "evidence", "description": "Có dẫn chứng file:dòng cụ thể", "weight": 1},
    {"id": "no-guess", "description": "Không khẳng định điều chưa kiểm, gọi là giả thuyết", "weight": 1},
]
print("Đây là bản nháp tiêu chí:")
print(json.dumps({"skill": "ten-do-model-tu-ghi", "items": items}, ensure_ascii=False))
