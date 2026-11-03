#!/usr/bin/env python3
"""
scripts/deploy.py
Commit và đẩy code lên các remote khai báo trong .deploy.json để hệ thống tự build (vd Vercel).
Đây là CÁCH DUY NHẤT agent được dùng để commit/push khi người dùng báo "deploy"
(agents/protocols/deploy.md). Script tự kiểm tra an toàn rồi mới ghi git.

Kiểm tra trước khi ghi git (sai thì dừng, không ghi gì):
  1. đang ở đúng nhánh khai báo (branch)
  2. chỉ có file nằm trong danh sách paths được thêm vào commit; không có file nào đã staged ngoài paths
  3. không có file giống khóa bí mật (.env, *.pem, *.key...) hoặc dòng giống khóa/mật khẩu
  4. lệnh build (nếu có) chạy thành công
  5. thông điệp commit đúng dạng <type>(scope): <tóm tắt> (tối đa 72 ký tự)
Không bao giờ dùng --force, không đụng git config (danh tính truyền qua git -c cho đúng một lần commit).

.deploy.json (đặt ở gốc dự án, không commit):
  {
    "branch": "main",
    "paths": ["frontend"],
    "remotes": ["origin", "vercel"],
    "identity": {"name": "...", "email": "..."},
    "build": "pnpm --dir frontend build"
  }

Usage:
  python scripts/deploy.py -m "feat(frontend): thêm trang ứng viên"
  python scripts/deploy.py -m "chore: sync" --dry-run        # chỉ in ra sẽ làm gì
  python scripts/deploy.py -m "chore: trigger build" --allow-empty
  python scripts/deploy.py -m "fix(ui): ..." --skip-build    # không khuyến khích
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / '.deploy.json'

COMMIT_RE = re.compile(r'^(feat|fix|chore|docs|refactor|test|style|perf|build|ci|revert)(\([\w./-]+\))?: .{1,72}$')
SECRET_NAME_RE = re.compile(
    r'(^|/)(\.env(\..+)?|[^/]*\.(pem|key|p12|pfx)|id_rsa[^/]*|credentials[^/]*\.json)$', re.I)
SECRET_CONTENT_RE = re.compile(
    r'(AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|'
    r'(api[_-]?key|secret|token|password)\s*[:=]\s*["\'][^"\'\s]{12,}["\'])', re.I)


def fail(msg: str, code: int = 2):
    print(f'DỪNG  {msg}')
    sys.exit(code)


def git(*args, check=True):
    p = subprocess.run(['git', '-C', str(ROOT), *args], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and p.returncode != 0:
        fail(f"git {' '.join(args)} lỗi: {(p.stderr or p.stdout).strip()}", 3)
    return p


def load_config() -> dict:
    if not CONFIG.is_file():
        fail('Thiếu .deploy.json ở gốc dự án (xem đầu file scripts/deploy.py).')
    cfg = json.loads(CONFIG.read_text(encoding='utf-8'))
    for key in ('branch', 'paths', 'remotes', 'identity'):
        if not cfg.get(key):
            fail(f'.deploy.json thiếu khóa "{key}".')
    ident = cfg['identity']
    if not ident.get('name') or not ident.get('email'):
        fail('.deploy.json: identity cần name và email.')
    return cfg


def under(path: str, roots: list) -> bool:
    path = path.replace('\\', '/')
    return any(path == r.rstrip('/') or path.startswith(r.rstrip('/') + '/') for r in roots)


def changed_files(paths: list) -> list:
    out = git('status', '--porcelain=v1', '-uall', '--', *paths).stdout
    files = []
    for line in out.splitlines():
        entry = line[3:]
        if ' -> ' in entry:
            entry = entry.split(' -> ', 1)[1]
        files.append(entry.strip().strip('"').replace('\\', '/'))
    return files


def scan_secrets(files: list) -> list:
    problems = []
    for f in files:
        if f.endswith('.example') or f.endswith('.sample') or f.endswith('.template'):
            continue
        if SECRET_NAME_RE.search(f):
            problems.append(f'{f}: tên file giống khóa bí mật')
            continue
        p = ROOT / f
        if p.is_file() and p.stat().st_size < 1_000_000:
            try:
                text = p.read_text(encoding='utf-8')
            except (UnicodeDecodeError, OSError):
                continue
            m = SECRET_CONTENT_RE.search(text)
            if m:
                problems.append(f'{f}: có chuỗi giống khóa/mật khẩu ({m.group(0)[:12]}...)')
    return problems


def git_env(args, env, check=True):
    p = subprocess.run(['git', '-C', str(ROOT), *args], capture_output=True, text=True,
                       encoding='utf-8', errors='replace', env={**os.environ, **env})
    if check and p.returncode != 0:
        fail(f"git {' '.join(args)} lỗi: {(p.stderr or p.stdout).strip()}", 3)
    return p


def allowed_roots(cfg: dict) -> set:
    """Tên thư mục/tệp ở gốc được phép có trong commit đẩy lên remote."""
    roots = {p.replace('\\', '/').split('/')[0] for p in cfg['paths']}
    roots.update(cfg.get('allow_root', []))
    return roots


def check_tree(commit: str, cfg: dict):
    """Dừng nếu cây thư mục của commit có thứ nằm ngoài phần được phép (chống lọt tasks/, docs/, agents/...)."""
    top = {n.split('/')[0] for n in git('ls-tree', '--name-only', commit).stdout.splitlines() if n.strip()}
    leak = sorted(top - allowed_roots(cfg))
    if leak:
        fail(f'CHẶN: commit {commit[:8]} chứa thứ không được đẩy lên remote ở gốc: {", ".join(leak)}. '
             'Chỉ đẩy qua scripts/deploy.py ở chế độ "filtered".', 6)
    print(f'Kiểm tra cây thư mục commit {commit[:8]}: sạch (chỉ có {", ".join(sorted(top))}).')


def build_filtered_tree(paths: list) -> str:
    """Dựng cây chỉ gồm các paths, lấy từ HEAD (không đụng chỉ mục thật)."""
    idx = git('rev-parse', '--git-path', 'deploy.index').stdout.strip()
    idx = idx if os.path.isabs(idx) else str(ROOT / idx)
    if os.path.exists(idx):
        os.remove(idx)
    env = {'GIT_INDEX_FILE': idx}
    try:
        for p in paths:
            r = git_env(['read-tree', f'--prefix={p}/', f'HEAD:{p}'], env, check=False)
            if r.returncode != 0:
                fail(f'Thư mục "{p}" chưa có trong HEAD (chưa commit?): {(r.stderr or r.stdout).strip()}', 3)
        return git_env(['write-tree'], env).stdout.strip()
    finally:
        if os.path.exists(idx):
            os.remove(idx)


def push_filtered(cfg: dict, paths: list, message: str, co_authors: list, dry_run: bool, allow_empty: bool, remotes: list = None) -> list:
    """Dựng commit lọc (chỉ paths), cha là commit đã đẩy trước đó, rồi đẩy. Trả về danh sách remote lỗi."""
    branch, ident = cfg['branch'], cfg['identity']
    tree = build_filtered_tree(paths)
    names = git('ls-tree', '-r', '--name-only', tree).stdout.splitlines()
    outside = [n for n in names if n.split('/')[0] not in allowed_roots(cfg)]
    if outside:
        fail('Cây lọc có file ngoài paths (không nên xảy ra): ' + ', '.join(outside[:5]), 6)
    print(f'Cây lọc: {len(names)} file, chỉ thuộc: {", ".join(sorted({n.split("/")[0] for n in names}))}.')
    msg_args = ['-m', message] + [x for c in co_authors for x in ('-m', f'Co-Authored-By: {c}')]
    cenv = {'GIT_AUTHOR_NAME': ident['name'], 'GIT_AUTHOR_EMAIL': ident['email'],
            'GIT_COMMITTER_NAME': ident['name'], 'GIT_COMMITTER_EMAIL': ident['email'],
            'ALLOW_PROTECTED_PUSH': '1'}
    failed = []
    remotes_to_push = remotes if remotes is not None else cfg['remotes']
    for remote in remotes_to_push:
        parent = ''
        for ref in (f'refs/deploy/{remote}', f'refs/remotes/{remote}/{branch}'):
            r = git('rev-parse', '--verify', '--quiet', ref, check=False)
            if r.returncode == 0:
                parent = r.stdout.strip()
                break
        ptree = git('rev-parse', f'{parent}^{{tree}}', check=False).stdout.strip() if parent else ''
        if ptree == tree and not allow_empty:
            print(f'{remote}: nội dung lọc không đổi so với bản đã đẩy, không tạo commit mới.')
            continue
        if dry_run:
            print(f'[dry-run] {remote}: sẽ tạo commit lọc (cha {parent[:8] or "không có"}) và đẩy {branch}. '
                  f'File sẽ lên remote (tối đa 40 tên): {", ".join(names[:40])}')
            continue
        args = ['commit-tree', tree] + (['-p', parent] if parent else []) + msg_args
        sha = git_env(args, cenv).stdout.strip()
        check_tree(sha, cfg)
        p = git_env(['push', remote, f'{sha}:refs/heads/{branch}'], cenv, check=False)
        if p.returncode == 0:
            git('update-ref', f'refs/deploy/{remote}', sha)
            print(f'Đã đẩy {remote}/{branch} (commit lọc {sha[:8]}).')
        else:
            failed.append(remote)
            print(f'LỖI đẩy {remote}: {(p.stderr or p.stdout).strip()[-400:]}')
    return failed


def main():
    ap = argparse.ArgumentParser(description='Commit và đẩy code để hệ thống tự build.')
    ap.add_argument('--check-tree', metavar='COMMIT', help='chỉ kiểm cây thư mục của commit có lọt file ngoài paths không (dùng cho hook pre-push)')
    ap.add_argument('-m', '--message', help='thông điệp commit: <type>(scope): <tóm tắt>')
    ap.add_argument('--dry-run', action='store_true', help='chỉ kiểm tra và in kế hoạch, không ghi git')
    ap.add_argument('--allow-empty', action='store_true', help='cho phép commit rỗng (chỉ để kích hoạt build)')
    ap.add_argument('--skip-build', action='store_true', help='bỏ qua lệnh build (không khuyến khích)')
    ap.add_argument('--co-author', action='append', default=[], metavar='"Tên <email>"', help='thêm dòng Co-Authored-By')
    ap.add_argument('--allow-branch', action='store_true', help='cho phép deploy từ nhánh hiện tại lên target branch của remote')
    ap.add_argument('--remote', help='chỉ đẩy lên remote được chỉ định (ví dụ: vercel)')
    args = ap.parse_args()

    cfg = load_config()
    if args.check_tree:
        check_tree(args.check_tree, cfg)
        return
    if not args.message:
        ap.error('thiếu -m/--message')
    paths = [p.replace('\\', '/').rstrip('/') for p in cfg['paths']]
    for p in paths:
        if not (ROOT / p).exists():
            fail(f'Thư mục trong paths không tồn tại: {p}')

    if not COMMIT_RE.match(args.message):
        fail('Thông điệp commit sai dạng. Cần: <type>(scope): <tóm tắt> tối đa 72 ký tự. '
             'type: feat, fix, chore, docs, refactor, test, style, perf, build, ci, revert.')

    curr_branch = git('rev-parse', '--abbrev-ref', 'HEAD').stdout.strip()
    if curr_branch != cfg['branch'] and not args.allow_branch:
        fail(f'Đang ở nhánh "{curr_branch}", .deploy.json chỉ cho deploy từ "{cfg["branch"]}". Dùng --allow-branch nếu muốn deploy từ nhánh hiện tại.')
    branch = curr_branch

    staged = [f.replace('\\', '/') for f in git('diff', '--cached', '--name-only').stdout.splitlines() if f.strip()]
    outside = [f for f in staged if not under(f, paths)]
    if outside:
        fail('Có file đã staged nằm ngoài paths, không commit: ' + ', '.join(outside[:5]))

    files = changed_files(paths)
    print(f'Nhánh: {branch} | paths: {", ".join(paths)} | remote: {", ".join(cfg["remotes"])}')
    print(f'File thay đổi trong paths: {len(files)}')

    problems = scan_secrets(files)
    if problems:
        fail('Phát hiện nghi bí mật, dừng:\n  ' + '\n  '.join(problems))

    if not files and not args.allow_empty:
        print('Không có thay đổi mới để commit; chỉ đẩy các commit chưa đẩy (nếu có).')

    build = cfg.get('build')
    if build and not args.skip_build and files:
        print(f'Chạy build: {build}')
        if args.dry_run:
            print('[dry-run] bỏ qua build thật.')
        else:
            rc = subprocess.run(build, shell=True, cwd=ROOT).returncode  # cso: allow INJ-02 build từ PROJECT.md, không phải input runtime
            if rc != 0:
                fail(f'Build lỗi (mã {rc}). Sửa lỗi build rồi deploy lại, chưa commit gì.', 4)

    target_remotes = [args.remote] if args.remote else cfg['remotes']

    if args.dry_run:
        print('[dry-run] sẽ: git add, commit với danh tính '
              f'{cfg["identity"]["name"]} <{cfg["identity"]["email"]}>, rồi đẩy: {", ".join(target_remotes)}.')
        if cfg.get('mode') == 'filtered':
            print('[dry-run] chế độ filtered: danh sách file bên dưới lấy từ HEAD hiện tại '
                  '(thay đổi chưa commit sẽ được commit trước rồi mới đưa vào cây lọc).')
            push_filtered(cfg, paths, args.message, args.co_author, True, args.allow_empty, target_remotes)
        return

    committed = False
    if files or args.allow_empty:
        git('add', '--', *paths)
        msg_args = ['-m', args.message] + [x for c in args.co_author for x in ('-m', f'Co-Authored-By: {c}')]
        cmd = ['-c', f'user.name={cfg["identity"]["name"]}', '-c', f'user.email={cfg["identity"]["email"]}',
               'commit', *msg_args]
        if args.allow_empty and not files:
            cmd.append('--allow-empty')
        # deploy.py là đường được phép commit ở nhánh chính (hook pre-commit chặn commit thẳng vào main)
        git_env(cmd, {'ALLOW_PROTECTED_COMMIT': '1'})
        committed = True
    head = git('rev-parse', '--short', 'HEAD').stdout.strip()
    print(f'Commit: {head}' + ('' if committed else ' (không tạo commit mới)'))

    if cfg.get('mode') == 'filtered':
        failed = push_filtered(cfg, paths, args.message, args.co_author, False, args.allow_empty, target_remotes)
        if failed:
            print(f'Chưa đẩy được: {", ".join(failed)}. Không dùng --force; báo người dùng.')
            sys.exit(5)
        print('Xong. Hệ thống build sẽ tự chạy sau khi nhận commit.')
        return

    failed = []
    for remote in target_remotes:
        p = git('push', remote, cfg['branch'], check=False)
        if p.returncode == 0:
            print(f'Đã đẩy {remote}/{cfg["branch"]}')
        else:
            failed.append(remote)
            print(f'LỖI đẩy {remote}: {(p.stderr or p.stdout).strip()[-400:]}')

    if failed:
        print(f'Chưa đẩy được: {", ".join(failed)}. Không dùng --force; báo người dùng.')
        sys.exit(5)
    print('Xong. Hệ thống build sẽ tự chạy sau khi nhận commit.')


if __name__ == '__main__':
    main()
