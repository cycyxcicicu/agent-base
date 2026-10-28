#!/usr/bin/env python3
"""
scripts/task-branch.py
Agent tự tạo nhánh cho mỗi card và tự gộp về nhánh chính khi kiểm tra đạt.
Người dùng đã cho phép (chat, 2026-09-30). Đây là CÁCH DUY NHẤT agent được dùng để
tạo/chuyển nhánh và merge (agents/protocols/task-branch.md).
KHÔNG BAO GIỜ đẩy lên remote (việc đó chỉ qua scripts/deploy.py khi người dùng báo "deploy").

  start   tạo nhánh <type>/<ticket>-<slug> từ nhánh chính trong thư mục hiện tại
  finish  kiểm tra rồi gộp nhánh card vào nhánh chính (--no-ff), chỉ khi TẤT CẢ đạt:
            1. đang đứng trên nhánh của card
            2. card-audit --card <id> --need-done đạt (card done, có bằng chứng bằng mắt nếu là card giao diện)
            3. không có file staged ngoài paths; không có nghi bí mật
            4. lệnh build (và test nếu khai) trong .deploy.json chạy thành công
            5. commit trên nhánh card (danh tính trong .deploy.json), rồi merge vào nhánh chính
          Merge lỗi thì tự hủy merge, quay lại nhánh card, không để repo nửa vời.
Không dùng --force, reset, không đụng git config.

Usage:
  python scripts/task-branch.py start  --ticket 26 --slug app-router [--type feat]
  python scripts/task-branch.py finish --ticket 26 -m "feat(app): route theo vai và phân quyền" [--dry-run]
"""

import argparse
import importlib.util
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
import deploy  # dùng lại kiểm tra an toàn của deploy.py

ROOT = deploy.ROOT
# Tên nhánh phải khớp hook pre-commit: <feature|bugfix|hotfix|fix|chore|refactor|docs|test|devops>/<số>-<mô-tả>.
# "feat" vẫn nhận nhưng được đổi thành "feature" cho hợp hook.
VALID_TYPES = {'feat', 'feature', 'bugfix', 'hotfix', 'fix', 'chore', 'refactor', 'docs', 'test', 'devops'}
git, fail = deploy.git, deploy.fail


def load_card_audit():
    spec = importlib.util.spec_from_file_location('card_audit', Path(__file__).resolve().parent / 'card-audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def current_branch() -> str:
    return git('rev-parse', '--abbrev-ref', 'HEAD').stdout.strip()


def branches_for(ticket: str) -> list:
    out = git('branch', '--list', '--format=%(refname:short)').stdout.split()
    return [b for b in out if re.match(rf'^[a-z]+/{ticket}-', b)]


# ---------------- Chế độ WORKTREE (song song nhiều card code, mỗi card một thư mục riêng) ----------------
# Thư mục chứa worktree: .deploy.json khóa "worktree_root", mặc định <thư mục cha của thư mục cha dự án>/humana-wt.
# Phải trùng thư mục đã mở quyền "external_directory" trong cấu hình Kilo (D:/congviec/humana-wt/**).

def wt_root(cfg) -> Path:
    r = cfg.get('worktree_root')
    return Path(r) if r else ROOT.parent.parent / 'humana-wt'


def gitc(path, *args, check=True):
    p = subprocess.run(['git', '-C', str(path), *args], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and p.returncode != 0:
        fail(f"git {' '.join(args)} (trong {path}) lỗi: {(p.stderr or p.stdout).strip()}", 3)
    return p


def worktree_for(ticket: str):
    """Trả về (đường dẫn, nhánh) của worktree thuộc card này, hoặc None."""
    cur_path = None
    for line in git('worktree', 'list', '--porcelain').stdout.splitlines():
        if line.startswith('worktree '):
            cur_path = line[len('worktree '):].strip()
        elif line.startswith('branch refs/heads/') and cur_path:
            br = line[len('branch refs/heads/'):].strip()
            if re.match(rf'^[a-z]+/{ticket}-', br):
                return Path(cur_path), br
    return None


def start_worktree(args, cfg, branch):
    main_branch = cfg['branch']
    path = wt_root(cfg) / f'T-{args.ticket}'
    if path.exists():
        fail(f'Thư mục worktree đã có: {path}. Dùng lại hoặc gỡ trước.')
    if args.dry_run:
        print(f'[dry-run] sẽ tạo worktree {path} với nhánh {branch} từ {main_branch}.')
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    git('worktree', 'add', str(path), '-b', branch, main_branch)
    print(f'Đã tạo worktree: {path} (nhánh {branch} từ {main_branch}).')
    fe = path / 'frontend-v1-nextjs'
    if not args.no_install and (fe / 'package.json').is_file():
        print('Cài phụ thuộc frontend trong worktree (pnpm install --frozen-lockfile)...')
        r = subprocess.run('pnpm install --frozen-lockfile', shell=True, cwd=fe, env={**os.environ, 'CI': 'true'})  # cso: allow INJ-02 lệnh literal cố định
        print('   cài xong.' if r.returncode == 0 else f'   CẢNH BÁO: pnpm install trả mã {r.returncode}; chạy lại trong {fe}.')
    print('\nDEV LÀM VIỆC TRONG WORKTREE:')
    print(f'  - Sửa code bằng ĐƯỜNG DẪN TUYỆT ĐỐI dưới {path}; chạy lệnh bash với thư mục làm việc (workdir) = {path}.')
    print('  - CHỈ sửa file thuộc scope_edit của card trong worktree. KHÔNG sửa tasks/, docs/ ở worktree (card và tài liệu nằm ở thư mục chính).')
    print(f'  - Xong thì đặt card review (ở thư mục chính). QA kiểm; khi card done chạy: '
          f'python scripts/task-branch.py finish --ticket {args.ticket} -m "<type>(scope): <tóm tắt>"')


def finish_worktree(args, cfg, wt, branch, card_id):
    main_branch = cfg['branch']
    paths = [p.replace('\\', '/').rstrip('/') for p in cfg['paths']]
    # File kết quả của card nằm trong worktree cho tới khi gộp, nên kiểm tồn tại ở worktree (out_base=wt).
    errors, warns = load_card_audit().run(card_id, need_done=True, quiet=True, out_base=wt)
    for w in warns:
        print(f'CẢNH BÁO  {w}')
    if errors:
        fail('Card chưa đạt, không gộp:\n  ' + '\n  '.join(errors), 6)
    cur_main = current_branch()
    if cur_main != main_branch:
        fail(f'Thư mục chính đang ở nhánh "{cur_main}", cần "{main_branch}" để gộp.')

    def changed(*extra):
        out = gitc(wt, 'status', '--porcelain=v1', '-uall', *extra).stdout
        res = []
        for line in out.splitlines():
            e = line[3:]
            if ' -> ' in e:
                e = e.split(' -> ', 1)[1]
            res.append(e.strip().strip('"').replace('\\', '/'))
        return res

    all_changed = changed()
    outside = [f for f in all_changed if not deploy.under(f, paths)]
    if outside:
        fail('Trong worktree có file sửa NGOÀI paths (' + ', '.join(outside[:5]) + '). '
             'Dev chỉ được sửa code trong paths; card và tài liệu nằm ở thư mục chính. Bỏ các thay đổi đó rồi chạy lại.')
    files = [f for f in all_changed if deploy.under(f, paths)]
    problems = []
    for f in files:
        if deploy.SECRET_NAME_RE.search(f) and not f.endswith('.example'):
            problems.append(f'{f}: tên file giống khóa bí mật')
            continue
        p = wt / f
        if p.is_file() and p.stat().st_size < 1_000_000:
            try:
                m = deploy.SECRET_CONTENT_RE.search(p.read_text(encoding='utf-8'))
            except (UnicodeDecodeError, OSError):
                continue
            if m:
                problems.append(f'{f}: có chuỗi giống khóa/mật khẩu ({m.group(0)[:12]}...)')
    if problems:
        fail('Phát hiện nghi bí mật, dừng:\n  ' + '\n  '.join(problems))
    print(f'{card_id}: worktree {wt} | nhánh {branch} | file thay đổi trong paths: {len(files)}')

    for label in ('build', 'test'):
        command = cfg.get(label)
        if command:
            print(f'Chạy {label} trong worktree: {command}')
            if args.dry_run:
                print(f'[dry-run] bỏ qua {label} thật.')
            elif subprocess.run(command, shell=True, cwd=wt).returncode != 0:  # cso: allow INJ-02 command từ PROJECT.md, không phải input runtime
                fail(f'{label} lỗi trong worktree, không gộp. Sửa rồi chạy lại finish.', 4)

    ident = cfg['identity']
    idargs = ['-c', f'user.name={ident["name"]}', '-c', f'user.email={ident["email"]}']
    if args.dry_run:
        print(f'[dry-run] sẽ commit trong worktree, gộp --no-ff {branch} vào {main_branch}, rồi gỡ worktree (không đẩy remote).')
        return
    if files:
        gitc(wt, 'add', '--', *paths)
        gitc(wt, *idargs, 'commit', '-m', args.message)
    m = git(*idargs, 'merge', '--no-ff', branch, '-m', f'Merge {card_id}: {args.message}', check=False)
    if m.returncode != 0:
        git('merge', '--abort', check=False)
        fail(f'Merge vào {main_branch} lỗi (xung đột?), đã hủy merge; worktree {wt} giữ nguyên để sửa: '
             f'{(m.stderr or m.stdout).strip()[-300:]}', 7)
    head = git('rev-parse', '--short', 'HEAD').stdout.strip()
    git('worktree', 'remove', '--force', str(wt), check=False)
    if wt.exists():
        shutil.rmtree(wt, ignore_errors=True)
    print(f'Đã gộp {branch} vào {main_branch} (merge {head}) và gỡ worktree {wt}. Chưa đẩy remote; người dùng báo "deploy" thì chạy scripts/deploy.py.')
    print(f'Hoàn tác nếu cần: git revert -m 1 {head} (người dùng hoặc Lead lập phiếu rủi ro).')


def cmd_start(args, cfg):
    if not re.fullmatch(r'[0-9]+', args.ticket):
        fail('--ticket phải là số, ví dụ 26.')
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,40}', args.slug):
        fail('--slug chỉ gồm chữ thường, số, dấu gạch ngang (tối đa 41 ký tự).')
    if args.type not in VALID_TYPES:
        fail('--type phải là một trong: ' + ', '.join(sorted(VALID_TYPES)))
    main_branch = cfg['branch']
    if args.type == 'feat':
        args.type = 'feature'
    branch = f'{args.type}/{args.ticket}-{args.slug}'
    cur = current_branch()
    existing = branches_for(args.ticket)
    if existing:
        fail(f'Đã có nhánh cho T-{args.ticket}: {", ".join(existing)}. Dùng lại nhánh đó, không tạo thêm.')
    if args.worktree:
        return start_worktree(args, cfg, branch)
    if cur != main_branch:
        fail(f'Đang ở nhánh "{cur}", chỉ tạo nhánh card mới từ "{main_branch}". Xong card hiện tại trước.')
    if git('status', '--porcelain=v1', '-uno').stdout.strip():
        print('LƯU Ý: có thay đổi chưa commit, chúng sẽ đi theo sang nhánh mới.')
    if args.dry_run:
        print(f'[dry-run] sẽ tạo nhánh {branch} từ {main_branch}.')
        return
    git('switch', '-c', branch)
    print(f'Đã tạo và chuyển sang nhánh {branch}. Làm việc tại đây, xong thì: '
          f'python scripts/task-branch.py finish --ticket {args.ticket} -m "<type>(scope): <tóm tắt>"')


def cmd_finish(args, cfg):
    main_branch = cfg['branch']
    paths = [p.replace('\\', '/').rstrip('/') for p in cfg['paths']]
    card_id = f'T-{args.ticket}'
    if not deploy.COMMIT_RE.match(args.message):
        fail('Thông điệp commit sai dạng <type>(scope): <tóm tắt> (tối đa 72 ký tự).')
    wt = worktree_for(args.ticket)
    if wt:
        return finish_worktree(args, cfg, wt[0], wt[1], card_id)
    names = branches_for(args.ticket)
    cur = current_branch()
    if cur not in names:
        fail(f'Đang ở nhánh "{cur}", không phải nhánh của {card_id} ({", ".join(names) or "chưa có nhánh"}).')

    errors, warns = load_card_audit().run(card_id, need_done=True, quiet=True)
    for w in warns:
        print(f'CẢNH BÁO  {w}')
    if errors:
        fail('Card chưa đạt, không gộp:\n  ' + '\n  '.join(errors), 6)

    staged = [f.replace('\\', '/') for f in git('diff', '--cached', '--name-only').stdout.splitlines() if f.strip()]
    outside = [f for f in staged if not deploy.under(f, paths)]
    if outside:
        fail('Có file đã staged nằm ngoài paths, không commit: ' + ', '.join(outside[:5]))
    files = deploy.changed_files(paths)
    problems = deploy.scan_secrets(files)
    if problems:
        fail('Phát hiện nghi bí mật, dừng:\n  ' + '\n  '.join(problems))
    print(f'{card_id}: nhánh {cur} | file thay đổi trong paths: {len(files)}')

    for label in ('build', 'test'):
        command = cfg.get(label)
        if command:
            print(f'Chạy {label}: {command}')
            if args.dry_run:
                print(f'[dry-run] bỏ qua {label} thật.')
            elif subprocess.run(command, shell=True, cwd=ROOT).returncode != 0:  # cso: allow INJ-02 command từ PROJECT.md, không phải input runtime
                fail(f'{label} lỗi, không gộp. Sửa rồi chạy lại finish.', 4)

    ident = cfg['identity']
    idargs = ['-c', f'user.name={ident["name"]}', '-c', f'user.email={ident["email"]}']
    if args.dry_run:
        print(f'[dry-run] sẽ commit trên {cur}, rồi gộp --no-ff vào {main_branch} (không đẩy remote).')
        return
    if files:
        git('add', '--', *paths)
        git(*idargs, 'commit', '-m', args.message)
    git('switch', main_branch)
    # Tiêu đề merge bắt đầu bằng "Merge " để qua hook commit-msg.
    m = git(*idargs, 'merge', '--no-ff', cur, '-m', f'Merge {card_id}: {args.message}', check=False)
    if m.returncode != 0:
        git('merge', '--abort', check=False)
        git('switch', cur, check=False)
        fail(f'Merge vào {main_branch} lỗi (xung đột?), đã hủy merge và quay lại {cur}: '
             f'{(m.stderr or m.stdout).strip()[-300:]}', 7)
    head = git('rev-parse', '--short', 'HEAD').stdout.strip()
    print(f'Đã gộp {cur} vào {main_branch} (merge {head}). Chưa đẩy remote; người dùng báo "deploy" thì chạy scripts/deploy.py.')
    print(f'Hoàn tác nếu cần: git revert -m 1 {head} (người dùng hoặc Lead lập phiếu rủi ro).')


def main():
    ap = argparse.ArgumentParser(description='Nhánh theo card: tạo và tự gộp khi đạt.')
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('start', help='tạo nhánh cho card')
    s.add_argument('--ticket', required=True)
    s.add_argument('--slug', required=True)
    s.add_argument('--type', default='feat')
    s.add_argument('--worktree', action='store_true', help='tạo worktree riêng cho card (chạy song song nhiều card code)')
    s.add_argument('--no-install', action='store_true', help='với --worktree: không chạy pnpm install')
    s.add_argument('--dry-run', action='store_true')
    f = sub.add_parser('finish', help='kiểm tra rồi gộp nhánh card vào nhánh chính')
    f.add_argument('--ticket', required=True)
    f.add_argument('-m', '--message', required=True)
    f.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    cfg = deploy.load_config()
    (cmd_start if args.cmd == 'start' else cmd_finish)(args, cfg)


if __name__ == '__main__':
    main()