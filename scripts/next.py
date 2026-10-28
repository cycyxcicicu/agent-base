#!/usr/bin/env python3
"""
scripts/next.py   (chạy bằng:  python scripts/next.py)
Cho người dùng biết NGAY việc kế tiếp, không cần hỏi ai: đọc card, không dùng AI, không tốn token.

In ra 3 phần:
  1. CẦN NGHIỆM THU: card đang ở `review` (ai nghiệm thu, câu dán), kèm file kết quả có thật chưa.
  2. LÀM TIẾP: card đã đủ điều kiện (mọi blocked_by đã done), nhóm theo đường (tài liệu / giao diện / backend),
     có vai, model, câu dán.
  3. CỔNG đang chờ bạn duyệt (tasks/GATES.json) và card bị chặn bởi cổng đó.

tasks/GATES.json (người dùng sửa true khi đã duyệt):
  {"G1": {"approved": false, "blocks": ["T-4", "T-36", "T-37"], "note": "duyệt quyết định công nghệ (ADR-005..010)"}}

Usage:
  python scripts/next.py            # tất cả
  python scripts/next.py --all      # hiện thêm card bị chặn và lý do
"""

import argparse
import importlib.util
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


def load_audit():
    spec = importlib.util.spec_from_file_location('card_audit', Path(__file__).resolve().parent / 'card-audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_models() -> dict:
    out = {}
    f = ROOT / 'agents' / 'models.txt'
    if f.is_file():
        for line in f.read_text(encoding='utf-8').splitlines():
            m = re.match(r'^([a-z-]+)=(\S+)', line.strip())
            if m:
                out[m.group(1)] = m.group(2).replace('9router/', '')
    return out


def role_model(role: str, models: dict, tiers: dict) -> str:
    if role == 'reviewer':
        return 'gemini (khác họ model với tác giả, chọn ở khung chat)'
    if role in models:
        return models[role]
    return models.get(tiers.get(role, 'standard'), '?')


def role_tiers() -> dict:
    out = {}
    for p in (ROOT / 'agents' / 'roles').glob('*.md'):
        t = p.read_text(encoding='utf-8')
        n, tier = re.search(r'^name:\s*(\S+)', t, re.M), re.search(r'^model_tier:\s*(\S+)', t, re.M)
        if n and tier:
            out[n.group(1)] = tier.group(1)
    return out


def card_id_key(cid: str):
    m = re.match(r'T-(\d+)$', cid)
    return (0, int(m.group(1))) if m else (1, cid)


def rel_folder(card) -> str:
    return card['_path'].parent.relative_to(ROOT).as_posix()


def paste_line(card) -> str:
    return f"Đọc {rel_folder(card)}/{card['id']}.md và làm đúng card này. Phải GHI FILE bằng công cụ ghi file."


def is_ui(card) -> bool:
    return any('frontend' in s for s in (card.get('scope_edit') or []))


def is_backend(card) -> bool:
    return any(s.startswith('backend') for s in (card.get('scope_edit') or []))


def outputs_status(card) -> str:
    outs = card.get('outputs') or []
    if not outs:
        return '(card không khai file kết quả)'
    have = [o for o in outs if (ROOT / o).exists()]
    miss = [o for o in outs if o not in have]
    if not miss:
        return f'đủ {len(outs)}/{len(outs)} file kết quả có thật'
    return f'THIẾU {len(miss)}/{len(outs)} file: ' + ', '.join(miss[:3]) + ('...' if len(miss) > 3 else '')


def main():
    ap = argparse.ArgumentParser(description='Việc kế tiếp là gì?')
    ap.add_argument('--all', action='store_true', help='hiện thêm card bị chặn')
    args = ap.parse_args()

    audit = load_audit()
    cards = audit.find_cards()
    by_id = {c['id']: c for c in cards}
    models, tiers = read_models(), role_tiers()

    gates = {}
    gf = ROOT / 'tasks' / 'GATES.json'
    if gf.is_file():
        try:
            gates = json.loads(gf.read_text(encoding='utf-8'))
        except Exception as e:
            print(f'CẢNH BÁO: tasks/GATES.json lỗi ({e})')
    gate_of = {}
    for g, v in gates.items():
        if not v.get('approved'):
            for cid in v.get('blocks', []):
                gate_of[cid] = g

    def deps_done(c):
        return all(by_id.get(b, {}).get('status') == 'done' for b in (c.get('blocked_by') or []))

    # 1. cần nghiệm thu
    review = sorted([c for c in cards if c.get('status') == 'review'], key=lambda c: card_id_key(c['id']))
    print('=' * 70)
    print('1. CẦN NGHIỆM THU (card đang ở "review")')
    print('=' * 70)
    if not review:
        print('   (không có)')
    for c in review:
        cid = c['id']
        print(f"\n   {cid}  [{c.get('owner', '?')}]  {c['title'][:80]}")
        print(f"   file: {outputs_status(c)}")
        if is_ui(c):
            print('   AI nghiệm thu: QA (mở phiên QA, model ' + role_model('qa', models, tiers) + '). Dán:')
            print(f'     Kiểm bằng mắt card {cid} theo agents/protocols/ui-fidelity.md mục 3: chạy ứng dụng, đi từng màn hình ở 375/768/1440px, '
                  f'ghi docs/qa/{cid}-visual.md, nếu đạt đặt tasks/.../{cid}.md sang status: done. Phải GHI FILE bằng công cụ ghi file.')
        else:
            print('   AI nghiệm thu: LEAD (gửi vào phiên Lead). Dán:')
            print(f'     {cid} đã có file thật. Nghiệm thu theo mục 4 của tasks/PROMPT-quan-ly-tuan-tu.md; nếu đạt đặt {cid} sang done, '
                  'cập nhật RUNBOOK, rồi báo tôi câu dán card kế tiếp.')

    # 2. làm tiếp
    ready = [c for c in cards if c.get('status') in ('todo', 'blocked') and deps_done(c) and c['id'] not in gate_of]
    groups = {'TÀI LIỆU / THIẾT KẾ (đường B)': [], 'GIAO DIỆN (frontend)': [], 'BACKEND (code)': [], 'KHÁC': []}
    for c in sorted(ready, key=lambda c: card_id_key(c['id'])):
        if is_backend(c):
            groups['BACKEND (code)'].append(c)
        elif is_ui(c):
            groups['GIAO DIỆN (frontend)'].append(c)
        elif c.get('epic') == 'E0':
            groups['TÀI LIỆU / THIẾT KẾ (đường B)'].append(c)
        else:
            groups['KHÁC'].append(c)
    print('\n' + '=' * 70)
    print('2. LÀM TIẾP (đã đủ điều kiện, mỗi nhóm nên chạy tuần tự, tối đa 2-3 phiên cùng lúc)')
    print('=' * 70)
    shown = False
    for name, lst in groups.items():
        if not lst:
            continue
        shown = True
        print(f'\n   -- {name} --')
        for c in lst[:6]:
            role = c.get('owner', '?')
            print(f"   {c['id']:6} vai {role:10} model {role_model(role, models, tiers)}")
            print(f"          {c['title'][:90]}")
            print(f'          Dán: {paste_line(c)}')
            if is_ui(c) or is_backend(c):
                num = c['id'].replace('T-', '')
                print(f'          Song song (worktree riêng): python scripts/task-branch.py start --ticket {num} --slug <mo-ta> --worktree')
        if len(lst) > 6:
            print(f'          (+{len(lst) - 6} card khác cùng nhóm)')
    if not shown:
        print('   (không có card nào đủ điều kiện: xem mục 3 hoặc nghiệm thu mục 1)')

    # 3. cổng
    print('\n' + '=' * 70)
    print('3. CỔNG CHỜ BẠN DUYỆT')
    print('=' * 70)
    pending = {g: v for g, v in gates.items() if not v.get('approved')}
    if not pending:
        print('   (không có cổng nào đang chờ)')
    for g, v in pending.items():
        blocked = [b for b in v.get('blocks', []) if by_id.get(b, {}).get('status') in ('todo', 'blocked')]
        print(f"\n   {g}: {v.get('note', '')}")
        shown_b = ', '.join(blocked[:8]) + (f' ... (+{len(blocked) - 8} card)' if len(blocked) > 8 else '')
        print(f"   đang chặn: {shown_b or '(không còn)'}")
        print(f'   Sau khi bạn duyệt: mở tasks/GATES.json, đổi "{g}": {{"approved": false → true}} rồi chạy lại: python scripts/next.py')

    if args.all:
        print('\n--- Card đang bị chặn (không làm được) ---')
        for c in sorted(cards, key=lambda c: card_id_key(c['id'])):
            if c.get('status') in ('todo', 'blocked') and c not in ready:
                waiting = [b for b in (c.get('blocked_by') or []) if by_id.get(b, {}).get('status') != 'done']
                why = f'cổng {gate_of[c["id"]]}' if c['id'] in gate_of else ('chờ ' + ', '.join(waiting[:4]))
                print(f"   {c['id']:6} {why}")


if __name__ == '__main__':
    main()
