#!/usr/bin/env python3
"""
scripts/notes-index.py
Sinh docs/notes/INDEX.md từ hộp thư docs/notes/inbox/*.md.
Mỗi note một dòng: đường dẫn — task — summary. Summary lấy từ frontmatter
`summary:` hoặc dòng `> summary:` đầu tiên; thiếu thì ghi "(không có summary)".

  python scripts/notes-index.py            # ghi INDEX.md
  python scripts/notes-index.py --check    # exit 1 nếu INDEX lệch hoặc note thiếu summary

Rule cho agent ghi note: xem agents/protocols/handoff-note.md.
"""
import re
import sys
from pathlib import Path

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
for _a in sys.argv[1:]:
    if _a.startswith('--root='):
        ROOT = Path(_a.split('=', 1)[1]).resolve()
INBOX = ROOT / 'docs' / 'notes' / 'inbox'
INDEX = ROOT / 'docs' / 'notes' / 'INDEX.md'
NO_SUMMARY = '(không có summary)'


def read_summary(path: Path) -> str:
    text = path.read_text(encoding='utf-8', errors='replace')
    m = re.search(r'^---\s*\n(.*?)\n---', text, re.S)
    if m:
        s = re.search(r'^summary:\s*(.+)$', m.group(1), re.M)
        if s:
            return s.group(1).strip()
    s = re.search(r'^>\s*summary:\s*(.+)$', text, re.M | re.I)
    return s.group(1).strip() if s else NO_SUMMARY


def task_of(name: str) -> str:
    m = re.match(r'^(T-\d+(?:\.\d+)?)', name)
    return m.group(1) if m else '—'


def build_rows():
    rows = []
    for p in sorted(INBOX.glob('*.md'), key=lambda x: x.name) if INBOX.exists() else []:
        rows.append((p.name, task_of(p.name), read_summary(p)))
    return rows


def render(rows) -> str:
    lines = ['> Task: T-07 · Epic: E1 · Vai: dev',
             '',
             '# Hộp thư ghi chú — INDEX',
             '',
             'Sinh tự động bởi `scripts/notes-index.py`. Không sửa tay.',
             'Agent chỉ mở note khớp task/module (tối đa 3), không đọc cả hộp.',
             '',
             '| Note | Task | Summary |',
             '|---|---|---|']
    lines += [f'| `docs/notes/inbox/{n}` | {t} | {s} |' for n, t, s in rows]
    if not rows:
        lines.append('| — | — | (hộp thư trống) |')
    return '\n'.join(lines) + '\n'


def main() -> int:
    check = '--check' in sys.argv
    rows = build_rows()
    new = render(rows)
    if check:
        cur = INDEX.read_text(encoding='utf-8') if INDEX.exists() else ''
        if cur != new:
            print('SAI: docs/notes/INDEX.md lệch so với hộp thư — chạy lại scripts/notes-index.py')
            return 1
        missing = [n for n, _, s in rows if s == NO_SUMMARY]
        if missing:
            print('SAI: note thiếu summary: ' + ', '.join(missing))
            return 1
        print(f'OK: INDEX khớp, {len(rows)} note đều có summary.')
        return 0
    INDEX.parent.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(new, encoding='utf-8')
    print(f'wrote   {INDEX.relative_to(ROOT)} ({len(rows)} note)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
