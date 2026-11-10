#!/usr/bin/env python3
"""
scripts/card-audit.py
Kiểm tra card có nói thật không, bắt các lỗi mà "build qua" không bắt được.
Quy tắc: agents/protocols/ui-fidelity.md.

Card giao diện = scope_edit có đường dẫn chứa "frontend" hoặc "mobile".

LỖI (exit 1):
  - card giao diện thiếu mục "Mẫu tham chiếu" hoặc "Kiểm tra bằng mắt"
  - card giao diện `done` mà thiếu docs/qa/<id>-visual.md có dòng "KẾT QUẢ: ĐẠT",
    hoặc thiếu ảnh trong docs/qa/screens/<id>/
  - card `done` mà file trong outputs không tồn tại
CẢNH BÁO (exit 0):
  - card nhắc tới gói `@scope/tên` trong dấu huyền mà không có ở package.json nào (vd dnd-kit)
  - epic đã xong hết mà thiếu docs/notes/inbox/retro-<epic>*.md

Usage:
  python scripts/card-audit.py                 # kiểm tất cả card, in báo cáo
  python scripts/card-audit.py --card T-26     # kiểm một card; dùng thêm --need-done để bắt buộc status done
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
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
IMG_EXT = {'.png', '.jpg', '.jpeg', '.webp'}
SKIP_DIRS = {'node_modules', '.next', '.git', 'dist', 'build'}


def parse_card(path: Path) -> dict:
    text = path.read_text(encoding='utf-8')
    m = re.match(r'^---\r?\n(.*?)\r?\n---', text, re.S)
    meta = {'_text': text, '_path': path, 'title': ''}
    if not m:
        return meta
    key = None
    for line in m.group(1).splitlines():
        if re.match(r'^\s+-\s+', line) and key:
            meta.setdefault(key, []).append(re.sub(r'^\s+-\s+', '', line).strip().strip('"\''))
            continue

        kv = re.match(r'^([A-Za-z_]+):\s*(.*)$', line)
        if kv:
            key, val = kv.group(1), kv.group(2).strip()
            if val == '' or val == '[]':
                meta[key] = []
            elif val.startswith('['):
                meta[key] = [x.strip().strip('"\'') for x in val.strip('[]').split(',') if x.strip()]
            else:
                meta[key] = val.strip('"\'')
    t = re.search(r'^#\s+(.+)$', text, re.M)
    meta['title'] = t.group(1).strip() if t else ''
    return meta


def find_cards() -> list:
    from agent_core.workflow.task_discovery import discover_tasks
    return discover_tasks(ROOT / 'tasks')









def is_ui(card: dict) -> bool:
    return any(('frontend' in s or 'mobile' in s) for s in (card.get('scope_edit') or []))


def package_deps() -> set:
    deps = set()
    for p in ROOT.rglob('package.json'):
        if any(part in SKIP_DIRS for part in p.parts):
            continue

        try:
            data = json.loads(p.read_text(encoding='utf-8'))
        except Exception:
            continue

        for k in ('dependencies', 'devDependencies', 'peerDependencies'):
            val = data.get(k)
            if isinstance(val, dict):
                deps.update(str(x) for x in val.keys())
            elif isinstance(val, (list, set)):
                for item in val:
                    if isinstance(item, str):
                        deps.add(item)
                    elif isinstance(item, dict) and 'name' in item:
                        deps.add(str(item['name']))
    return deps


def audit_card(card: dict, need_done: bool, deps: set, out_base=None):
    errors, warns = [], []
    cid, status, text = card['id'], card.get('status', ''), card['_text']
    if status == 'cancelled':
        return errors, warns
    ui = is_ui(card)
    if ui:
        if not re.search(r'Mẫu tham chiếu', text):
            errors.append(f'{cid}: card giao diện thiếu mục "Mẫu tham chiếu"')
        if not re.search(r'Kiểm tra bằng mắt', text):
            errors.append(f'{cid}: card giao diện thiếu mục "Kiểm tra bằng mắt"')
    if need_done and status != 'done':
        errors.append(f'{cid}: status là "{status}", cần "done" (do QA/Reviewer/Lead đặt sau khi kiểm bằng mắt)')
    if status == 'done':
        for out in card.get('outputs') or []:
            # Có ở thư mục chính HOẶC ở worktree (code nằm trong worktree, bằng chứng QA ở thư mục chính) đều tính là có.
            if not (((out_base or ROOT) / out).exists() or (ROOT / out).exists()):
                errors.append(f'{cid}: outputs ghi "{out}" nhưng file không tồn tại')
        if ui:
            vis = ROOT / 'docs' / 'qa' / f'{cid}-visual.md'
            if not vis.is_file():
                errors.append(f'{cid}: thiếu docs/qa/{cid}-visual.md (bằng chứng kiểm bằng mắt)')
            elif not re.search(r'KẾT QUẢ:\s*ĐẠT', vis.read_text(encoding='utf-8')):
                errors.append(f'{cid}: docs/qa/{cid}-visual.md chưa có dòng "KẾT QUẢ: ĐẠT"')
            shots = ROOT / 'docs' / 'qa' / 'screens' / cid
            if not (shots.is_dir() and any(f.suffix.lower() in IMG_EXT for f in shots.iterdir())):
                errors.append(f'{cid}: thiếu ảnh chụp trong docs/qa/screens/{cid}/')
    for pkg in sorted(set(re.findall(r'`(@[a-z0-9-]+/[a-z0-9._-]+)`', text))):
        if pkg not in deps and '/' in pkg and not (ROOT / pkg).exists():
            warns.append(f'{cid}: card nhắc gói `{pkg}` nhưng không có trong package.json nào')
    for m in re.finditer(r'(?<![\w@/-])(dnd-kit)(?![\w-])', text):
        if not any('dnd-kit' in d for d in deps):
            warns.append(f'{cid}: card nhắc dnd-kit nhưng không có gói @dnd-kit trong package.json nào')
        break
    return errors, warns


def epic_retro_warns(cards: list) -> list:
    warns, by_epic = [], {}
    for c in cards:
        by_epic.setdefault(c.get('epic', '?'), []).append(c)
    inbox = ROOT / 'doc' / 'notes' / 'inbox' if (ROOT / 'doc' / 'notes' / 'inbox').is_dir() else ROOT / 'docs' / 'notes' / 'inbox'
    for epic, cs in by_epic.items():
        if all(c.get('status') == 'done' for c in cs):
            if not (inbox.is_dir() and any(inbox.glob(f'retro-{epic}*.md'))):
                warns.append(f'epic {epic}: đã xong hết nhưng thiếu docs/notes/inbox/retro-{epic}*.md')
    return warns


def run(card_id: str = '', need_done: bool = False, quiet: bool = False, out_base=None):
    cards = find_cards()
    deps = package_deps()
    if card_id:
        cards_sel = [c for c in cards if c['id'] == card_id]
        if not cards_sel:
            return [f'không thấy card {card_id} trong tasks/'], []
    else:
        cards_sel = cards
    errors, warns = [], []
    for c in cards_sel:
        e, w = audit_card(c, need_done, deps, out_base)
        errors += e
        warns += w
    if not card_id:
        warns += epic_retro_warns(cards)
    if not quiet:
        for w in warns:
            print(f'CẢNH BÁO  {w}')
        for e in errors:
            print(f'LỖI       {e}')
        print(f'Đã kiểm {len(cards_sel)} card: {len(errors)} lỗi, {len(warns)} cảnh báo.')
    return errors, warns


def main():
    ap = argparse.ArgumentParser(description='Kiểm card có nói thật không.')
    ap.add_argument('--card', default='', help='chỉ kiểm một card, ví dụ T-26')
    ap.add_argument('--need-done', action='store_true', help='bắt buộc card ở trạng thái done')
    args = ap.parse_args()
    errors, _ = run(args.card, args.need_done)
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
