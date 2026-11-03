#!/usr/bin/env python3
"""
scripts/agent-base-diff.py
Chạy trong một dự án đã cài agent-base: so phần khung (theo agents/manifest.txt) của
dự án với agent-base để biết cái gì cần đưa ngược về agent-base, cái gì cần kéo về dự án.

Dùng <dự án>/.agent-base.json (do bootstrap-project.py ghi) làm mốc để biết phía nào đã sửa.
Không có mốc thì chỉ báo "khác nhau".

Usage:
  python scripts/agent-base-diff.py                       # liệt kê
  python scripts/agent-base-diff.py --base D:/agent-base  # khi không có .agent-base.json
  python scripts/agent-base-diff.py --push scripts/x.py   # copy dự án -> agent-base (từng file nêu tên)
  python scripts/agent-base-diff.py --pull scripts/x.py   # copy agent-base -> dự án
  python scripts/agent-base-diff.py --mark-synced         # cập nhật mốc sau khi đã đồng bộ xong
"""

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

PROJECT = Path.cwd() if (Path.cwd() / '.agent-base.json').is_file() else Path(__file__).resolve().parent.parent
SKIP_DIRS = {'__pycache__', '.pytest_cache'}


def read_manifest(root: Path) -> list:
    entries = []
    for raw in (root / 'agents' / 'manifest.txt').read_text(encoding='utf-8').splitlines():
        line = raw.split('#', 1)[0].strip()
        if line:
            kind, path = line.split(None, 1)
            entries.append((kind, path.strip()))
    return entries


def expand(root: Path, path: str) -> set:
    p = root / path
    if path.endswith('/'):
        if not p.is_dir():
            return set()
        return {f.relative_to(root).as_posix() for f in p.rglob('*')
                if f.is_file() and not (set(f.relative_to(root).parts) & SKIP_DIRS)}
    return {path} if p.is_file() else set()


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def main():
    ap = argparse.ArgumentParser(description='So phần khung của dự án với agent-base.')
    ap.add_argument('--base', help='đường dẫn agent-base (mặc định lấy từ .agent-base.json)')
    ap.add_argument('--push', nargs='+', metavar='FILE', help='copy các file nêu tên từ dự án sang agent-base')
    ap.add_argument('--pull', nargs='+', metavar='FILE', help='copy các file nêu tên từ agent-base sang dự án')
    ap.add_argument('--mark-synced', action='store_true', help='ghi mốc mới vào .agent-base.json')
    args = ap.parse_args()

    meta_file = PROJECT / '.agent-base.json'
    meta = json.loads(meta_file.read_text(encoding='utf-8')) if meta_file.exists() else {}
    base = Path(args.base or meta.get('source', '')).resolve() if (args.base or meta.get('source')) else None
    if not base or not (base / 'agents' / 'manifest.txt').is_file():
        sys.exit('LỖI  không tìm thấy agent-base. Dùng --base <đường dẫn agent-base>')
    if base == PROJECT:
        sys.exit('LỖI  đang chạy trong chính agent-base; chạy script này ở dự án đã cài agent-base')
    baseline = meta.get('files', {})

    tracked, templates = set(), set()
    for kind, path in read_manifest(base):
        norm_path = path.replace('\\', '/')
        if kind == 'template':
            templates.add(norm_path)
        elif kind == 'copy' or (kind == 'gitonly' and meta.get('mode') != 'hidden'):
            tracked |= expand(base, norm_path) | expand(PROJECT, norm_path)
    tracked -= templates

    for flag, src_root, dst_root, label in ((args.push, PROJECT, base, 'agent-base'),
                                            (args.pull, base, PROJECT, 'dự án')):
        if not flag:
            continue
        for rel in flag:
            rel = rel.replace('\\', '/')
            if rel not in tracked:
                print(f'BỎ QUA  {rel}: không thuộc phần khung trong manifest')
                continue
            if not (src_root / rel).is_file():
                print(f'BỎ QUA  {rel}: không có ở nguồn')
                continue
            (dst_root / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_root / rel, dst_root / rel)
            print(f'đã copy {rel} -> {label}')
        print('\nNhớ chạy python scripts/sync-adapters.py ở phía vừa nhận, rồi --mark-synced khi hai bên đã khớp.')
        return

    if args.mark_synced:
        meta.setdefault('source', str(base))
        meta['files'] = {rel: h for rel in sorted(tracked)
                         if (h := sha(PROJECT / rel)) and h == sha(base / rel)}
        meta_file.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'đã ghi mốc: {len(meta["files"])} file khớp giữa dự án và agent-base')
        return

    groups = {'up': [], 'down': [], 'both': [], 'new_here': [], 'new_base': [], 'diff': []}
    for rel in sorted(tracked):
        p, b, o = sha(PROJECT / rel), sha(base / rel), baseline.get(rel)
        if p == b:
            continue
        if p and not b:
            groups['new_here'].append(rel)
        elif b and not p:
            groups['new_base'].append(rel)
        elif not o:
            groups['diff'].append(rel)
        elif p != o and b == o:
            groups['up'].append(rel)
        elif b != o and p == o:
            groups['down'].append(rel)
        else:
            groups['both'].append(rel)

    titles = {
        'up': 'Dự án đã sửa, agent-base chưa có → ĐƯA NGƯỢC VỀ agent-base (--push) nếu là thay đổi dùng chung',
        'new_here': 'File khung mới chỉ có ở dự án → đưa về agent-base (--push) nếu dùng chung',
        'down': 'agent-base đã cập nhật, dự án chưa có → kéo về (--pull)',
        'new_base': 'File mới chỉ có ở agent-base → kéo về (--pull)',
        'both': 'CẢ HAI PHÍA ĐỀU SỬA → gộp tay, không dùng --push/--pull',
        'diff': 'Khác nhau (chưa có mốc để biết phía nào sửa) → xem diff rồi quyết định',
    }
    total = 0
    for key, title in titles.items():
        if groups[key]:
            total += len(groups[key])
            print(f'\n## {title}')
            for rel in groups[key]:
                print(f'  {rel}')
    print(f'\nagent-base: {base}')
    print('Khớp hoàn toàn.' if total == 0 else f'{total} file cần xem.')


if __name__ == '__main__':
    main()
