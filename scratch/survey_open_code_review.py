import os
from pathlib import Path

p = Path("D:/skills-quarantine/open-code-review")

print("=== Top level directories and files ===")
for item in sorted(p.iterdir()):
    if item.is_dir():
        print(f"  [DIR]  {item.name}")
    else:
        print(f"  [FILE] {item.name}")

print("\n=== SKILL.md files in open-code-review ===")
for smd in p.rglob("SKILL.md"):
    rel = smd.relative_to(p)
    print(f"  {rel}")
