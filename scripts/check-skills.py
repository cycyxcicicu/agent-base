#!/usr/bin/env python3
"""
scripts/check-skills.py
Read-only screening of agent skills (folders that contain SKILL.md).
Checks front matter, folder names, descriptions, suspicious patterns, and registry.

Usage:
  python scripts/check-skills.py
  python scripts/check-skills.py --path C:/tmp/my-skill-folder
  python scripts/check-skills.py --strict
"""

import sys
import re
import argparse
from pathlib import Path

# Force UTF-8 on Windows console if needed
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

PATTERNS = [
    ('hidden text (HTML comment)', r'<!--'),
    ('embedded shell command', r'!`'),
    ('download tool', r'(?i)\b(curl|wget|Invoke-WebRequest|iwr|Invoke-RestMethod|irm)\b'),
    ('encoded payload', r'(?i)(base64|FromBase64String|-EncodedCommand)'),
    ('touches secrets or credentials', r'(?i)(\.ssh|id_rsa|\.aws|\.env\b|credentials|api[_-]?key|password)'),
    ('tries to override the rules', r'(?i)(ignore (all |any |the )?(previous|prior|above|earlier)|disregard|override (the )?(rules|instructions)|do not tell the user|without (asking|approval|confirmation))'),
    ('auto-approve or disable checks', r'(?i)(auto-?approve|skip (the )?(review|tests|checks)|--no-verify|disable (the )?(hook|security|check))'),
    ('git write command', r'(?i)\bgit (add|commit|push|pull|rebase|reset|merge|checkout|switch|tag|stash)\b'),
    ('remote URL', r'https?://'),
    ('GitHub CLI or issue tracker', r'(?i)(\bgh (api|pr|issue|release)\b|issue tracker|linear\.app)'),
    ('keychain or code signing', r'(?i)(security (find|list|delete)-|codesign|keychain)')
]

SCRIPT_EXT = {'.ps1', '.psm1', '.sh', '.bat', '.cmd', '.py', '.js', '.mjs', '.cjs', '.ts', '.exe', '.dll', '.jar', '.vbs', '.zip', '.7z', '.gz', '.tar'}
TEXT_EXT = {'.md', '.txt', '.json', '.yaml', '.yml', '.ps1', '.psm1', '.sh', '.bat', '.cmd', '.py', '.js', '.mjs', '.cjs', '.ts', '.toml', '.xml', '.html'}


def main():
    parser = argparse.ArgumentParser(description="Check skills syntax and security patterns.")
    parser.add_argument("--path", type=str, default="", help="Path to a skill folder or parent skills directory.")
    parser.add_argument("--registry", type=str, default="", help="Path to skills.md registry file.")
    parser.add_argument("--strict", action="store_true", help="Fail with exit code 1 on suspicious patterns.")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    in_repo = (args.path == "")
    skills_path = Path(args.path) if args.path else root / ".agents" / "skills"
    reg_path = Path(args.registry) if args.registry else root / "agents" / "knowledge" / "skills.md"

    if not skills_path.exists():
        print(f"No folder at {skills_path}. Nothing to check.")
        sys.exit(0)

    skill_dirs = []
    if (skills_path / "SKILL.md").exists():
        skill_dirs.append(skills_path)
    else:
        for item in skills_path.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                skill_dirs.append(item)

    if not skill_dirs:
        print(f"No skill folders under {skills_path}.")
        sys.exit(0)

    reg_text = reg_path.read_text(encoding='utf-8') if reg_path.exists() else ""

    problems = 0
    warnings = 0

    for d in sorted(skill_dirs, key=lambda x: x.name):
        name = d.name
        print(f"\n=== skill: {name}")
        skill_md = d / "SKILL.md"
        if not skill_md.exists():
            print("  ERROR: no SKILL.md")
            problems += 1
            continue

        text = skill_md.read_text(encoding='utf-8').replace('\r\n', '\n')
        m = re.match(r'(?s)^---\n(.*?)\n---', text)
        if not m:
            print("  ERROR: SKILL.md has no front matter (--- block)")
            problems += 1
        else:
            fm = m.group(1)
            m_name = re.search(r'(?m)^name:\s*(.+?)\s*$', fm)
            m_desc = re.search(r'(?m)^description:\s*(.+?)\s*$', fm)
            n = m_name.group(1).strip().strip('"').strip("'") if m_name else ""
            desc = m_desc.group(1).strip() if m_desc else ""

            if not n:
                print("  ERROR: front matter has no name")
                problems += 1
            elif n != name:
                print(f"  ERROR: name '{n}' does not match the folder name '{name}'")
                problems += 1

            if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name) or len(name) > 64:
                print("  ERROR: folder name must be lowercase letters, digits and single dashes, max 64 chars")
                problems += 1

            if not desc:
                print("  ERROR: front matter has no description")
                problems += 1
            elif len(desc) > 1024:
                print(f"  ERROR: description is {len(desc)} chars, max 1024")
                problems += 1
            elif len(desc) > 400:
                print(f"  WARN: description is long ({len(desc)} chars); a broad description makes the skill trigger too often")
                warnings += 1

        files = [p for p in d.rglob("*") if p.is_file()]
        scripts = [p for p in files if p.suffix.lower() in SCRIPT_EXT]
        print(f"  files: {len(files)}   script or binary files: {len(scripts)}")
        for s in scripts:
            rel_s = s.relative_to(d)
            print(f"  SCRIPT/BINARY: {rel_s}   READ IT LINE BY LINE")
            warnings += 1

        hits = 0
        for f in files:
            if f.suffix.lower() not in TEXT_EXT:
                continue
            rel_f = f.relative_to(d)
            try:
                content_lines = f.read_text(encoding='utf-8', errors='replace').splitlines()
            except Exception:
                continue
            for ln, line in enumerate(content_lines, start=1):
                for label, pat in PATTERNS:
                    if re.search(pat, line):
                        hits += 1
                        snippet = line.strip()
                        if len(snippet) > 110:
                            snippet = snippet[:110] + "..."
                        print(f"  SUSPICIOUS [{label}] {rel_f}:{ln}: {snippet}")

        if hits > 0:
            warnings += 1
            print(f"  {hits} suspicious line(s). Each one needs a human decision.")

        if in_repo or args.registry:
            if not re.search(r'(?m)^\|\s*' + re.escape(name) + r'\s*\|', reg_text):
                print(f"  ERROR: '{name}' is not registered in agents/knowledge/skills.md")
                problems += 1
            else:
                print("  registered: yes")
        else:
            print("  (screening a folder outside the repo: registry not checked)")

        if hits > 0 and args.strict:
            problems += 1

    print(f"\nChecked {len(skill_dirs)} skill(s): {problems} problem(s), {warnings} warning(s).")
    if problems > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
