import os
from pathlib import Path

base = Path("D:/skills-quarantine")

def list_skills_in_repo(repo_name):
    p = base / repo_name
    skills = []
    for smd in p.rglob("SKILL.md"):
        rel = smd.relative_to(p)
        # đọc name từ frontmatter
        name = ""
        desc = ""
        try:
            content = smd.read_text(encoding="utf-8", errors="replace")
            for line in content.splitlines()[:15]:
                if line.startswith("name:"):
                    name = line.split("name:", 1)[1].strip()
                if line.startswith("description:"):
                    desc = line.split("description:", 1)[1].strip()
        except Exception:
            pass
        skills.append((str(rel), name, desc[:80]))
    return skills

repos = ["pocock-skills", "superpowers", "ponytail", "gstack", "i-have-adhd", "diagram-design", "ui-ux-pro-max-skill"]
for r in repos:
    sks = list_skills_in_repo(r)
    print(f"\n=================== {r.upper()} ({len(sks)} skills) ===================")
    for path, name, desc in sks:
        print(f"  - [{name or 'no-name'}] ({path}): {desc}")
