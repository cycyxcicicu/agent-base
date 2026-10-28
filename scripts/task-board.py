#!/usr/bin/env python3
"""
scripts/task-board.py
Gom mọi task card trong tasks/ theo phase -> epic và sinh tasks/BOARD.md.

Đọc phần front matter của tasks/T-*.md (id, title, status, owner, epic, phase,
blocked_by, outputs) và bảng epic trong tasks/EPICS.md. Không sửa card nào.

Usage:
  python scripts/task-board.py            # ghi tasks/BOARD.md
  python scripts/task-board.py --check    # chỉ báo lỗi card, không ghi
"""

import argparse
import re
import sys
from pathlib import Path

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
TASKS = ROOT / 'tasks'
PHASE_ORDER = ['PT', 'GĐ1', 'GĐ2']
STATUS_ICON = {'done': '✅', 'review': '👀', 'doing': '🔄', 'todo': '⬜', 'blocked': '⛔', 'cancelled': '🚫'}


def parse_front(text: str) -> dict:
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.S)
    if not m:
        return {}
    meta, cur = {}, None
    for line in m.group(1).splitlines():
        item = re.match(r'^\s+-\s+(.+)$', line)
        if item and cur:
            meta.setdefault(cur, [])
            if not isinstance(meta[cur], list):
                meta[cur] = []
            meta[cur].append(item.group(1).strip().strip('"\''))
            continue
        kv = re.match(r'^([a-z_]+):\s*(.*)$', line)
        if kv:
            cur, val = kv.group(1), kv.group(2).strip()
            if val.startswith('[') and val.endswith(']'):
                meta[cur] = [v.strip().strip('"\'') for v in val[1:-1].split(',') if v.strip()]
            else:
                meta[cur] = [] if val == '' else val.strip('"\'')
    return meta


def as_list(v) -> list:
    if isinstance(v, list):
        return v
    return [v] if v else []


def load_epics() -> dict:
    epics = {}
    f = TASKS / 'EPICS.md'
    if not f.exists():
        return epics
    # | Epic | Thư mục | Tên | Mã yêu cầu | Phase |
    for line in f.read_text(encoding='utf-8').splitlines():
        m = re.match(r'^\|\s*(E\d+)\s*\|\s*`?([^|`]+?)`?\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$', line)
        if m:
            epics[m.group(1)] = {'folder': m.group(2).strip().rstrip('/'), 'name': m.group(3),
                                 'codes': m.group(4), 'phase': m.group(5)}
    return epics


def load_cards() -> list:
    from agent_core.workflow.task_discovery import discover_tasks
    raw_cards = discover_tasks(TASKS)
    cards = []
    for c in raw_cards:
        cards.append({
            'file': (TASKS / c['file']).relative_to(ROOT).as_posix(),
            'folder': c['folder'],
            'id': c['id'],
            'title': c['title'],
            'slug': c.get('slug', ''),
            'status': c['status'],
            'owner': c.get('owner', '?'),
            'epic': c.get('epic', ''),
            'phase': c.get('phase', ''),
            'blocked_by': as_list(c.get('blocked_by')),
            'outputs': as_list(c.get('outputs')),
            'is_example': str(c.get('is_example', '')).lower() == 'true',
        })
    return cards


NAME_OK = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
# Từ đầu của slug là loại việc, cùng bộ với loại nhánh/commit: feat (nhánh feature), fix (nhánh fix, bugfix), hotfix...
TASK_TYPES = {'feat', 'fix', 'hotfix', 'refactor', 'docs', 'test', 'chore', 'devops', 'perf'}


def name_warnings(cards: list) -> list:
    """Cảnh báo (không chặn) khi tên task không cho biết nó làm gì: file phải là T-<số>-<slug>.md, có tiêu đề thật."""
    out = []
    for c in cards:
        if c.get('is_example'):
            continue
        fname = Path(c['file']).name
        if not c['slug']:
            out.append(f"{c['id']}: tên file '{fname}' chỉ có mã, nên đặt T-<số>-<slug>.md (động từ + đối tượng, ví dụ T-12-docs-chuan-hoa-ten-task.md)")
        elif not NAME_OK.match(c['slug']) or len(c['slug']) > 40:
            out.append(f"{c['id']}: slug '{c['slug']}' phải là chữ thường, số, gạch ngang, tối đa 40 ký tự")
        elif c['slug'].split('-')[0] not in TASK_TYPES:
            out.append(f"{c['id']}: slug '{c['slug']}' nên bắt đầu bằng loại việc ({', '.join(sorted(TASK_TYPES))}), ví dụ T-12-fix-loi-xuat-excel")
        title = (c['title'] or '').strip()
        if not title or re.match(r'^T-\d', title):
            out.append(f"{c['id']}: thiếu tiêu đề nói rõ việc làm gì (dòng '# {c['id']}: <tiêu đề>')")
    return out


def check(cards: list, epics: dict) -> list:
    problems = []
    ids = [c['id'] for c in cards]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        problems.append(f"{dup}: trùng id ở nhiều file ({', '.join(c['file'] for c in cards if c['id'] == dup)})")
    ids = set(ids)
    for c in cards:
        if c['is_example']:
            continue
        if c['status'] not in STATUS_ICON:
            problems.append(f"{c['id']}: status '{c['status']}' không hợp lệ")
        if c['status'] == 'done':
            for o in c['outputs']:
                if not (ROOT / o).exists():
                    problems.append(f"{c['id']}: đã done nhưng thiếu tài liệu {o}")
            continue
        if c['status'] == 'cancelled':
            continue
        want = epics.get(c['epic'], {}).get('folder')
        if want and c['folder'] != want:
            problems.append(f"{c['id']}: card nằm ở tasks/{c['folder'] or ''} nhưng epic {c['epic']} dùng thư mục tasks/{want}/")
        if not c['epic']:
            problems.append(f"{c['id']}: thiếu 'epic'")
        elif c['epic'] not in epics:
            problems.append(f"{c['id']}: epic '{c['epic']}' không có trong tasks/EPICS.md")
        if not c['phase']:
            problems.append(f"{c['id']}: thiếu 'phase'")
        elif c['epic'] in epics and epics[c['epic']]['phase'] != c['phase']:
            problems.append(f"{c['id']}: phase '{c['phase']}' khác phase của {c['epic']} ('{epics[c['epic']]['phase']}')")
        for b in c['blocked_by']:
            if b not in ids:
                problems.append(f"{c['id']}: blocked_by '{b}' không có card")
    return problems


def render(cards: list, epics: dict, problems: list) -> str:
    cards = [c for c in cards if not c['is_example']]
    by_id = {c['id']: c for c in cards}
    out = [
        '# Bảng tổng task',
        '',
        '> SINH TỰ ĐỘNG bởi `scripts/task-board.py` từ `tasks/<thư mục epic>/T-*.md` và `tasks/EPICS.md`. Không sửa tay, sửa card rồi chạy lại script.',
        '',
        'Ký hiệu: ✅ done · 👀 review · 🔄 doing · ⬜ todo · ⛔ blocked · 🚫 cancelled (không tính vào tiến độ) · 📄 tài liệu đã có · ⭕ tài liệu chưa có',
        '',
    ]

    ready = [c for c in cards if c['status'] in ('todo', 'blocked')
             and all(by_id.get(b, {}).get('status') == 'done' for b in c['blocked_by'])]
    out.append('## Làm được ngay')
    out.append('')
    if ready:
        for c in ready:
            out.append(f"- **{c['id']}** ({c['owner']}, {c['epic'] or '?'}) {c['title']}")
    else:
        out.append('- (không có: mọi task còn lại đang chờ task khác hoặc đang làm)')
    out.append('')

    phases = PHASE_ORDER + sorted({c['phase'] for c in cards} - set(PHASE_ORDER) - {''})
    for ph in phases + ['']:
        in_phase = [c for c in cards if c['phase'] == ph]
        if not in_phase:
            continue
        active = [c for c in in_phase if c['status'] != 'cancelled']
        done = sum(1 for c in active if c['status'] == 'done')
        total = len(active) or 1
        bar = '█' * round(10 * done / total) + '░' * (10 - round(10 * done / total))
        out.append(f"## {ph or 'Chưa gán phase'}  {bar} {done}/{len(active)} xong")
        out.append('')
        epic_ids = sorted({c['epic'] for c in in_phase}, key=lambda e: (e == '', int(e[1:]) if e[1:].isdigit() else 999))
        for e in epic_ids:
            group = [c for c in in_phase if c['epic'] == e]
            gdone = sum(1 for c in group if c['status'] == 'done')
            gcount = sum(1 for c in group if c['status'] != 'cancelled')
            name = epics.get(e, {}).get('name', 'Chưa gán epic' if not e else '(epic không có trong EPICS.md)')
            folder = epics.get(e, {}).get('folder')
            where = f"  · `tasks/{folder}/`" if folder else ''
            out.append(f"### {e or '—'} {name}  ({gdone}/{gcount}){where}")
            out.append('')
            for c in group:
                wait = [b for b in c['blocked_by'] if by_id.get(b, {}).get('status') != 'done']
                extra = f" · chờ {', '.join(wait)}" if wait and c['status'] != 'done' else ''
                out.append(f"- {STATUS_ICON.get(c['status'], '?')} **{c['id']}** {c['title']} · _{c['owner']}_{extra}")
                for o in c['outputs']:
                    mark = '📄' if (ROOT / o).exists() else '⭕'
                    out.append(f"  - {mark} `{o}`")
            out.append('')

    if problems:
        out.append('## Card cần sửa')
        out.append('')
        out.extend(f'- {p}' for p in problems)
        out.append('')
    return '\n'.join(out)


def main():
    ap = argparse.ArgumentParser(description='Sinh tasks/BOARD.md từ các task card.')
    ap.add_argument('--check', action='store_true', help='chỉ kiểm tra card, không ghi BOARD.md')
    args = ap.parse_args()

    epics = load_epics()
    cards = load_cards()
    problems = check(cards, epics)

    if args.check:
        for p in problems:
            print(f'LỖI  {p}')
        for w in name_warnings(cards):
            print(f'CẢNH BÁO tên  {w}')
        print(f'{len(cards)} card, {len(problems)} lỗi')
        sys.exit(1 if problems else 0)

    (TASKS / 'BOARD.md').write_text(render(cards, epics, problems), encoding='utf-8')
    print(f'wrote    tasks/BOARD.md ({len(cards)} card, {len(problems)} lỗi)')
    for p in problems:
        print(f'LỖI  {p}')
    for w in name_warnings(cards):
        print(f'CẢNH BÁO tên  {w}')


if __name__ == '__main__':
    main()
