"""scripts/safety_guard.py

Bộ kiểm soát an toàn PreToolUse Hook cho Antigravity:
Chặn đứng các câu lệnh hủy diệt trước khi được thực thi trong môi trường shell.
"""

import json
import os
import re
import sys

DANGEROUS_PATTERNS = [
    r"\brm\s+-[rf]{1,2}\s+[/\\]",          # rm -rf /
    r"\bDROP\s+DATABASE\b",                # DROP DATABASE
    r"\bDROP\s+TABLE\b",                   # DROP TABLE
    r"\bgit\s+reset\s+--hard\b",           # git reset --hard
    r"\bgit\s+clean\s+-[fdx]{1,3}\b",      # git clean -fd
    r"\bgit\s+push\s+.*--force\s+.*(main|develop|prod)",  # force push to main
    r"\bformat\s+[c-z]:\b",                # format drive
]

def check_safety():
    # Hook truyền payload JSON qua stdin hoặc đối số
    raw_input = sys.stdin.read().strip()
    if not raw_input:
        sys.exit(0)

    try:
        data = json.loads(raw_input)
        command = data.get("args", {}).get("CommandLine", "") or data.get("toolArgs", {}).get("CommandLine", "")
    except Exception:
        command = raw_input

    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            print(f"[SECURITY BLOCK] Lệnh bị chặn do nguy hiểm tiềm ẩn vi phạm Cổng rủi ro (§11 AGENTS.md): {pattern}", file=sys.stderr)
            sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    check_safety()

