#!/usr/bin/env python3
"""
scripts/notes-index.py
Sinh và tra cứu INDEX.md từ hộp thư docs/notes/inbox/ hoặc doc/notes/inbox/.
Hỗ trợ cả note phẳng và note phân cấp theo thư mục Task (inbox/<Task>/<Subtask>-<agent>.md).

Cách dùng:
  python scripts/notes-index.py                  # ghi INDEX.md
  python scripts/notes-index.py --check          # exit 1 nếu INDEX lệch hoặc note thiếu summary
  python scripts/notes-index.py --task T-12      # lọc các note thuộc task T-12 (hoặc UC-04)
  python scripts/notes-index.py --role dev       # lọc các note theo vai trò dev
  python scripts/notes-index.py --tag db         # lọc theo tag
  python scripts/notes-index.py --query "auth"   # tìm kiếm từ khóa
  python scripts/notes-index.py --json           # xuất danh sách ra JSON (cho agents/scripts)

Rule cho agent ghi note: xem agents/protocols/handoff-note.md.
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
NO_SUMMARY = '(không có summary)'


def get_paths(root_dir: Path):
    """
    Hỗ trợ cả 2 cấu trúc:
    - doc/notes/ (chuẩn Enterprise Global của gdt-workspace)
    - docs/notes/ (chuẩn mặc định của agent-base)
    """
    if (root_dir / 'doc' / 'notes').exists() or (root_dir / 'doc' / 'notes' / 'inbox').exists():
        inbox = root_dir / 'doc' / 'notes' / 'inbox'
        index = root_dir / 'doc' / 'notes' / 'INDEX.md'
    else:
        inbox = root_dir / 'docs' / 'notes' / 'inbox'
        index = root_dir / 'docs' / 'notes' / 'INDEX.md'
    return inbox, index


def parse_metadata(path: Path, inbox_root: Path, root_dir: Path):
    """
    Trích xuất metadata từ frontmatter (YAML) hoặc fallback regex.
    Trả về dict: {path, rel_path, full_path, task, role, status, tags, summary}
    """
    text = path.read_text(encoding='utf-8', errors='replace')
    rel_path = path.relative_to(inbox_root).as_posix()
    inbox_rel = inbox_root.relative_to(root_dir).as_posix()
    full_path = f"{inbox_rel}/{rel_path}"

    fm_dict = {}
    m = re.search(r'^---\s*\n(.*?)\n---', text, re.S)
    if m:
        fm_content = m.group(1)
        for line in fm_content.splitlines():
            line = line.strip()
            if ':' in line:
                k, v = line.split(':', 1)
                k = k.strip().lower()
                v = v.strip()
                if v.startswith('[') and v.endswith(']'):
                    items = [x.strip().strip("'\"") for x in v[1:-1].split(',') if x.strip()]
                    fm_dict[k] = items
                else:
                    fm_dict[k] = v.strip("'\"")

    # Summary
    summary = fm_dict.get('summary')
    if not summary:
        s_m = re.search(r'^>\s*summary:\s*(.+)$', text, re.M | re.I)
        summary = s_m.group(1).strip() if s_m else NO_SUMMARY

    # Task (hỗ trợ T-xxx, UC-xxx, T-xxx.y)
    task = fm_dict.get('task')
    if not task:
        m_task = re.search(r'((?:T|UC)-\d+(?:\.\d+)?)', path.name, re.I)
        if not m_task and path.parent != inbox_root:
            m_task = re.search(r'((?:T|UC)-\d+(?:\.\d+)?)', path.parent.name, re.I)
        if not m_task:
            m_task = re.search(r'(?:Task|Tính năng):\s*`?((?:T|UC)-\d+(?:\.\d+)?)`?', text, re.I)
        task = m_task.group(1).upper() if m_task else '—'

    # Role
    role = fm_dict.get('role')
    if not role:
        m_role = re.search(r'-(lead|dev|qa|ba|architect|writer|dba|sre|security|reviewer|runner)(?:\.md|-|$)', path.name.lower())
        if m_role:
            role = m_role.group(1)
        else:
            role = '—'

    # Status
    status = fm_dict.get('status', 'done' if summary != NO_SUMMARY else 'draft')

    # Tags
    raw_tags = fm_dict.get('tags', [])
    if isinstance(raw_tags, str):
        tags = [x.strip() for x in raw_tags.split(',') if x.strip()]
    elif isinstance(raw_tags, list):
        tags = raw_tags
    else:
        tags = []

    return {
        'rel_path': rel_path,
        'full_path': full_path,
        'task': task,
        'role': role,
        'status': status,
        'tags': tags,
        'summary': summary
    }


def build_notes(inbox_dir: Path, root_dir: Path):
    if not inbox_dir.exists():
        return []
    files = sorted([p for p in inbox_dir.rglob('*.md') if p.is_file()], key=lambda x: x.relative_to(inbox_dir).as_posix())
    notes = [parse_metadata(p, inbox_dir, root_dir) for p in files]
    return notes


def render(notes) -> str:
    lines = [
        '> Task: T-07 · Epic: E1 · Vai: dev',
        '',
        '# Hộp thư ghi chú — INDEX',
        '',
        'Sinh tự động bởi `scripts/notes-index.py`. Không sửa tay.',
        'Agent chỉ mở note khớp task/module (tối đa 3), không đọc cả hộp.',
        '',
        '| Note | Task | Summary |',
        '|---|---|---|'
    ]
    for n in notes:
        summary_text = n['summary']
        if n['tags']:
            summary_text = f"[{', '.join(n['tags'])}] {summary_text}"
        lines.append(f"| `{n['full_path']}` | {n['task']} | {summary_text} |")

    if not notes:
        lines.append('| — | — | (hộp thư trống) |')
    return '\n'.join(lines) + '\n'


def filter_notes(notes, task_filter=None, role_filter=None, tag_filter=None, query_filter=None):
    res = notes
    if task_filter:
        tf = task_filter.strip().upper()
        res = [n for n in res if tf in n['task'].upper()]
    if role_filter:
        rf = role_filter.strip().lower()
        res = [n for n in res if rf in n['role'].lower()]
    if tag_filter:
        tg = tag_filter.strip().lower()
        res = [n for n in res if any(tg in t.lower() for t in n['tags'])]
    if query_filter:
        q = query_filter.strip().lower()
        res = [
            n for n in res if q in n['summary'].lower()
            or q in n['rel_path'].lower()
            or q in n['task'].lower()
            or any(q in t.lower() for t in n['tags'])
        ]
    return res


def main() -> int:
    parser = argparse.ArgumentParser(description="Chỉ mục và tra cứu hộp thư ghi chú inbox/")
    parser.add_argument('--root', help="Thư mục gốc của repo (mặc định: repo root)")
    parser.add_argument('--check', action='store_true', help="Kiểm tra tính toàn vẹn của INDEX.md (CI mode)")
    parser.add_argument('--task', help="Lọc các note thuộc Task ID (vd: T-12 hoặc UC-04)")
    parser.add_argument('--role', help="Lọc các note theo vai trò (vd: dev, qa, lead)")
    parser.add_argument('--tag', help="Lọc các note theo tag (vd: auth, db)")
    parser.add_argument('--query', '-q', help="Tìm kiếm từ khóa trong summary, tag, tên file")
    parser.add_argument('--json', action='store_true', help="Xuất danh sách ra định dạng JSON")

    args = parser.parse_args()

    root_dir = Path(args.root).resolve() if args.root else ROOT
    inbox_dir, index_file = get_paths(root_dir)

    all_notes = build_notes(inbox_dir, root_dir)

    # Nếu có cờ lọc hoặc JSON
    has_filter = any([args.task, args.role, args.tag, args.query])
    if has_filter or args.json:
        matched = filter_notes(all_notes, args.task, args.role, args.tag, args.query)
        if args.json:
            print(json.dumps(matched, ensure_ascii=False, indent=2))
        else:
            print(f"=== KẾT QUẢ TÌM KIẾM HỘP THƯ GHI CHÚ ({len(matched)}/{len(all_notes)} notes) ===")
            for n in matched:
                tag_str = f" [{', '.join(n['tags'])}]" if n['tags'] else ""
                print(f"• [{n['task']}] ({n['role']}) {n['full_path']}{tag_str}\n  └─ {n['summary']}")
        return 0

    if args.check:
        new_content = render(all_notes)
        cur_content = index_file.read_text(encoding='utf-8') if index_file.exists() else ''
        if cur_content != new_content:
            print(f'SAI: {index_file.relative_to(root_dir)} lệch so với hộp thư — chạy lại scripts/notes-index.py')
            return 1
        missing = [n['rel_path'] for n in all_notes if n['summary'] == NO_SUMMARY]
        if missing:
            print('SAI: note thiếu summary: ' + ', '.join(missing))
            return 1
        print(f'OK: INDEX khớp, {len(all_notes)} note đều có summary.')
        return 0

    # Mặc định: Ghi file INDEX.md
    new_content = render(all_notes)
    index_file.parent.mkdir(parents=True, exist_ok=True)
    index_file.write_text(new_content, encoding='utf-8')
    print(f'wrote   {index_file.relative_to(root_dir)} ({len(all_notes)} note)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
