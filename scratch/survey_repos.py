import os
import glob
from pathlib import Path

base = Path("D:/skills-quarantine")
for d in sorted(os.listdir(base)):
    p = base / d
    if p.is_dir():
        md_files = list(p.rglob("*.md"))
        skills = list(p.rglob("SKILL.md"))
        all_files = [f for f in p.rglob("*") if f.is_file()]
        print(f"{d:<22}: Total Files: {len(all_files):<5} | MD Files: {len(md_files):<4} | SKILL.md: {len(skills)}")
