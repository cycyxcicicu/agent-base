"""Trọng tài giả cho ví dụ Eval (chấm bằng quy tắc, không gọi model).
Dùng: demo_judge.py <rubric_file> <task_file> <output_file>   (in JSON {"scores": {...}} ra stdout)"""
import json
import re
import sys

rubric = json.load(open(sys.argv[1], encoding="utf-8"))
output = open(sys.argv[3], encoding="utf-8").read()

checks = {
    "doc-file": lambda t: 10 if re.search(r"đã đọc\s+\S+\.\w+", t, re.I) else 3,
    "evidence": lambda t: 10 if re.search(r"\b[\w/.-]+\.\w+:\d+", t) else 2,
}
scores = {item["id"]: checks.get(item["id"], lambda t: 5)(output) for item in rubric["items"]}
print(json.dumps({"scores": scores}))
