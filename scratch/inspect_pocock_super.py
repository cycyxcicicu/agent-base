import os
from pathlib import Path

base = Path("D:/skills-quarantine")
for r in ["pocock-skills", "superpowers", "ponytail"]:
    p = base / r
    print(f"\n*** REPO: {r} ***")
    for smd in sorted(p.rglob("SKILL.md")):
        rel = smd.relative_to(p)
        content = smd.read_text(encoding="utf-8", errors="replace")
        name = ""
        for line in content.splitlines()[:10]:
            if line.startswith("name:"):
                name = line.split("name:", 1)[1].strip()
        # Also check other md files in that same skill folder
        skill_folder = smd.parent
        other_mds = [f.name for f in skill_folder.glob("*.md") if f.name != "SKILL.md"]
        print(f"  Skill: {name:<25} Path: {str(rel):<50} Extra MDs: {other_mds}")
