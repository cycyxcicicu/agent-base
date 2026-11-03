#!/usr/bin/env python3
"""
scripts/bootstrap-project.py
Cài agent-base vào một dự án khác theo agents/manifest.txt.

  --mode git     agent-base nằm trong git của dự án (copy cả phần gitonly).
  --mode hidden  agent-base chỉ nằm trên máy: không copy phần gitonly, ghi các đường dẫn
                 đã copy vào <target>/.git/info/exclude. Cần `git init` ở dự án trước.

Không bao giờ ghi đè file đã có ở dự án đích: file trùng được bỏ qua và liệt kê ra.
Ghi <target>/.agent-base.json (nguồn, commit agent-base, băm từng file) để
scripts/agent-base-diff.py biết phía nào đã sửa về sau.

Usage:
  python scripts/bootstrap-project.py --target D:/du-an-moi --mode hidden
  python scripts/bootstrap-project.py --target D:/du-an-moi --mode git --dry-run
"""

import argparse
import datetime
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE = Path(__file__).resolve().parent.parent
SKIP_DIRS = {'__pycache__', '.pytest_cache'}

FRESH = {
    'tasks/quick-log.md': (
        '# Nhật ký việc nhỏ\n\n'
        'Mỗi việc cỡ "nhỏ" (fix bug, sửa chữ, 1–2 file) ghi một dòng. Việc từ cỡ "vừa" trở lên dùng task card riêng.\n\n'
        '| Ngày | Task ID | Agent | Mô tả | File | Commit |\n|---|---|---|---|---|---|\n'
    ),
    'docs/PROJECT-NOTES.md': (
        '# Sổ tay dự án (PROJECT-NOTES)\n\n'
        'Bộ nhớ chung của dự án cho mọi agent. **Đọc file này (và `docs/notes/inbox/`) trước khi bắt đầu việc.**\n\n'
        '- Chỉ **Tech Writer** sửa file này, bằng cách gộp các ghi chú từ `docs/notes/inbox/` sau mỗi lần merge.\n'
        '- Mỗi mục có ID (N-001...), ngày, nguồn (T-xxx và agent), và phạm vi ảnh hưởng.\n\n'
        '## Trạng thái hiện tại\n\nMới cài agent-base, chưa có task nào.\n\n'
        '## Lưu ý và bẫy đã gặp\n\n| ID | Ngày | Nguồn | Phạm vi | Lưu ý |\n|---|---|---|---|---|\n\n'
        '## Quyết định quan trọng\n\n| ID | Ngày | Quyết định | ADR |\n|---|---|---|---|\n'
    ),
    'docs/DEBT.md': (
        '# Sổ Cái Nợ Kỹ Thuật (Technical Debt Ledger)\n\n'
        '> Tổng số khoản nợ được ghi nhận: **0**\n\n'
        '| Vị trí (File:Dòng) | Đi Tắt (Shortcut) | Trần Chịu Đựng (Ceiling) | Lộ Trình Nâng Cấp (Upgrade) |\n'
        '| :--- | :--- | :--- | :--- |\n'
    ),
}


def read_manifest() -> list:
    entries = []
    for raw in (BASE / 'agents' / 'manifest.txt').read_text(encoding='utf-8').splitlines():
        line = raw.split('#', 1)[0].strip()
        if not line:
            continue
        kind, path = line.split(None, 1)
        entries.append((kind, path.strip()))
    return entries


def expand(root: Path, path: str) -> list:
    """Danh sách file (đường dẫn tương đối, dạng /) mà một mục manifest trỏ tới dưới root."""
    p = root / path
    if path.endswith('/'):
        if not p.is_dir():
            return []
        return sorted(
            f.relative_to(root).as_posix() for f in p.rglob('*')
            if f.is_file() and not (set(f.relative_to(root).parts) & SKIP_DIRS)
        )
    return [path] if p.is_file() else []


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def base_commit() -> str:
    try:
        return subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=BASE, capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        return ''


def main():
    ap = argparse.ArgumentParser(description='Cài agent-base vào dự án khác theo agents/manifest.txt.')
    ap.add_argument('--target', required=True, help='thư mục gốc của dự án đích')
    ap.add_argument('--mode', choices=['git', 'hidden'], required=True,
                    help='git: agent-base lên git của dự án; hidden: chỉ nằm trên máy (.git/info/exclude)')
    ap.add_argument('--dry-run', action='store_true', help='chỉ in ra sẽ làm gì')
    args = ap.parse_args()

    target = Path(args.target).resolve()
    if not target.is_dir():
        sys.exit(f'LỖI  không có thư mục đích: {target}')
    if target == BASE:
        sys.exit('LỖI  thư mục đích chính là agent-base')
    if args.mode == 'hidden' and not (target / '.git').is_dir():
        sys.exit('LỖI  --mode hidden cần git ở dự án đích. Chạy trước: git init -b main (trong thư mục dự án)')

    copied, skipped, created, record = [], [], [], {}
    hide = set()
    if args.mode == 'hidden':
        for d in ('docs', 'tasks'):
            if (target / d).exists():
                print(f'CẢNH BÁO  dự án đã có {d}/: chế độ hidden sẽ giấu cả {d}/ khỏi git. Kiểm tra git status sau khi chạy.')

    manifest = read_manifest()
    templates = {p for k, p in manifest if k == 'template'}
    done = set()
    for kind, path in manifest:
        if kind == 'gitonly' and args.mode != 'git':
            continue
        if kind in ('template', 'copy', 'generated', 'gitonly'):
            hide.add(path)
            for rel in expand(BASE, path):
                if rel in done:
                    continue
                done.add(rel)
                dst = target / rel
                if dst.exists():
                    skipped.append(rel)
                    continue
                if not args.dry_run:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(BASE / rel, dst)
                copied.append(rel)
                if kind not in ('generated', 'template') and rel not in templates:
                    record[rel] = sha(BASE / rel)
        elif kind == 'fresh':
            dst = target / path
            hide.add(path.split('/')[0] + '/')
            if dst.exists():
                skipped.append(path)
            else:
                if not args.dry_run:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    dst.write_text(FRESH.get(path, ''), encoding='utf-8')
                created.append(path)
        elif kind == 'mkdir':
            hide.add(path.split('/')[0] + '/')
            if not args.dry_run:
                (target / path).mkdir(parents=True, exist_ok=True)
        else:
            sys.exit(f'LỖI  manifest có loại không hợp lệ: {kind} {path}')

    if not args.dry_run:
        meta = {
            'source': str(BASE),
            'commit': base_commit(),
            'mode': args.mode,
            'installed': datetime.date.today().isoformat(),
            'files': record,
        }
        (target / '.agent-base.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    if args.mode == 'hidden':
        hide.add('.agent-base.json')
        exclude = target / '.git' / 'info' / 'exclude'
        have = exclude.read_text(encoding='utf-8').splitlines() if exclude.exists() else []
        add = [p for p in sorted(hide) if p not in have]
        if add and not args.dry_run:
            exclude.parent.mkdir(parents=True, exist_ok=True)
            with exclude.open('a', encoding='utf-8') as fh:
                fh.write('\n# agent-base (local only, not in git) - scripts/bootstrap-project.py\n' + '\n'.join(add) + '\n')
        print(f'exclude  {len(add)} đường dẫn thêm vào .git/info/exclude')

    pre = '[dry-run] ' if args.dry_run else ''
    print(f'{pre}copy     {len(copied)} file')
    print(f'{pre}fresh    {len(created)} file mẫu trống')
    if skipped:
        print(f'{pre}bỏ qua   {len(skipped)} file đã có ở dự án (không ghi đè):')
        for s in skipped:
            print(f'           {s}')
    print()
    steps = ['.\\setup.ps1 (hoặc ./setup.sh trên Mac/Linux)  # Khởi tạo toàn diện kho kỹ năng & adapter 1-click']
    if args.mode == 'git':
        steps.append('python scripts/install-hooks.py')
    else:
        steps.append('git status: chỉ còn file thật của dự án. Không dùng worktree (xem onboarding.md, Kịch bản 3)')
    steps += ['Mở đúng thư mục dự án trong editor, Developer: Reload Window, chọn vai lead',
              'Theo agents/protocols/onboarding.md: điền PROJECT.md, thay bảng tasks/EPICS.md']
    print('Bước tiếp (trong thư mục dự án):')
    for i, s in enumerate(steps, 1):
        print(f'  {i}. {s}')


if __name__ == '__main__':
    main()
