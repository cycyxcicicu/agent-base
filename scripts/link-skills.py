#!/usr/bin/env python3
"""
scripts/link-skills.py
Tạo cầu nối để Claude Code (`.claude/skills/`) và Qoder (`.qoder/skills/`) nhìn thấy
bộ skill chuẩn trong `.agents/skills/` mà không nhân bản nội dung.

Thứ tự tạo (đúng thứ tự, không nhảy bước):
  - Windows: junction bằng `cmd /c mklink /J` với đường dẫn tuyệt đối (không cần admin).
  - Windows nếu junction lỗi: `os.symlink(..., target_is_directory=True)`.
  - Nếu vẫn lỗi và có `--copy`: `shutil.copytree` (bản sao dễ lệch khi nguồn đổi).
  - POSIX: symlink trước, `--copy` là dự phòng.

An toàn (ràng buộc cứng, xem mục "Chấp thuận rủi ro" của card T-06):
  - Không xóa, không ghi đè: gặp thư mục thật hoặc link trỏ sai thì báo lỗi rồi dừng.
  - Không có `shutil.rmtree`, `rm -rf`, `Remove-Item -Recurse` ở bất kỳ đâu trong file này.
  - Gỡ cầu nối thủ công: junction/symlink thư mục thì dùng `os.rmdir`, symlink file thì `os.unlink`.
  - Idempotent: chạy lại khi cầu nối đã đúng thì bỏ qua, không tạo link lồng.

Dùng:
  python scripts/link-skills.py            # tạo cầu nối
  python scripts/link-skills.py --check    # chỉ đọc: báo chế độ + kiểm hash nội dung
  python scripts/link-skills.py --copy     # cho phép copy khi cả hai cách link đều lỗi
  python scripts/link-skills.py --root <thư-mục-gốc> --source <thư-mục-skill-nguồn>

Mã thoát: 0 ok · 1 có vấn đề · 2 lỗi tham số hoặc nguồn không tồn tại.
"""

import argparse
import hashlib
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

# Ép UTF-8 cho console Windows (giống các script khác trong repo).
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent

# Đích cần cầu nối, tính từ thư mục gốc.
TARGETS = (
    Path('.claude') / 'skills',
    Path('.qoder') / 'skills',
)

# Bỏ qua khi băm nội dung: rác sinh tự động, không phải nội dung skill.
SKIP_PARTS = {'__pycache__', '.git'}
SKIP_SUFFIXES = {'.pyc', '.pyo'}

EXIT_OK = 0
EXIT_PROBLEM = 1
EXIT_USAGE = 2


# --------------------------------------------------------------------------- #
# Nhận diện chế độ ở đích
# --------------------------------------------------------------------------- #

def _reparse_tag(path: Path) -> int:
    """Trả về tag reparse của đường dẫn (Windows), 0 nếu không có/không đọc được."""
    try:
        st = path.lstat()
    except OSError:
        return 0
    return int(getattr(st, 'st_reparse_tag', 0) or 0)


def detect_mode(path: Path) -> str:
    """'junction' | 'symlink' | 'copy' | 'other' | 'missing'."""
    if path.is_symlink():
        return 'symlink'
    if os.name == 'nt' and _reparse_tag(path) == stat.IO_REPARSE_TAG_MOUNT_POINT:
        # Junction trên Windows: is_symlink() trả False, phải xem reparse tag.
        return 'junction'
    if path.is_dir():
        return 'copy'
    if path.exists():
        return 'other'
    return 'missing'


def same_target(dst: Path, src: Path) -> bool:
    """So sánh đích đã trỏ đúng nguồn chưa (theo đường dẫn thật, không phân biệt hoa thường)."""
    return _norm(os.path.realpath(dst)) == _norm(os.path.realpath(src))


def _norm(raw) -> str:
    return os.path.normcase(os.path.normpath(str(raw)))


# --------------------------------------------------------------------------- #
# Băm nội dung
# --------------------------------------------------------------------------- #

def _skipped(rel: Path) -> bool:
    if any(part in SKIP_PARTS for part in rel.parts):
        return True
    return rel.suffix.lower() in SKIP_SUFFIXES


def fingerprint(skills_dir: Path) -> dict:
    """Trả về {tên_skill: sha256 của toàn bộ file trong skill}. Rỗng nếu không phải thư mục."""
    result = {}
    if not skills_dir.is_dir():
        return result
    try:
        entries = sorted((p for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith('.')),
                         key=lambda p: p.name)
    except OSError:
        return result
    for skill in entries:
        digest = hashlib.sha256()
        try:
            files = [p for p in skill.rglob('*') if p.is_file()]
        except OSError:
            files = []
        for f in sorted(files, key=lambda p: p.as_posix()):
            rel = f.relative_to(skill)
            if _skipped(rel):
                continue
            digest.update(rel.as_posix().encode('utf-8'))
            digest.update(b'\0')
            try:
                with open(f, 'rb') as fh:
                    for chunk in iter(lambda: fh.read(65536), b''):
                        digest.update(chunk)
            except OSError:
                digest.update(b'<unreadable>')
            digest.update(b'\0')
        result[skill.name] = digest.hexdigest()
    return result


def compare_content(src_fp: dict, dst_fp: dict) -> list:
    """Mô tả các điểm lệch giữa nguồn và đích. Rỗng nghĩa là khớp."""
    issues = []
    missing = sorted(set(src_fp) - set(dst_fp))
    extra = sorted(set(dst_fp) - set(src_fp))
    differ = sorted(n for n in set(src_fp) & set(dst_fp) if src_fp[n] != dst_fp[n])
    if missing:
        issues.append(f"thiếu {len(missing)} skill: {', '.join(missing)}")
    if extra:
        issues.append(f"thừa {len(extra)} skill: {', '.join(extra)}")
    if differ:
        issues.append(f"lệch nội dung {len(differ)} skill: {', '.join(differ)}")
    return issues


# --------------------------------------------------------------------------- #
# Tạo cầu nối
# --------------------------------------------------------------------------- #

def create_link(src: Path, dst: Path) -> str:
    """Tạo junction (Windows) hoặc symlink. Trả về chế độ đã tạo; ném RuntimeError nếu thất bại."""
    dst.parent.mkdir(parents=True, exist_ok=True)

    if os.name == 'nt':
        proc = subprocess.run(
            ['cmd', '/c', 'mklink', '/J', str(dst), str(src)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        raw = proc.stdout or b''
        try:
            msg = raw.decode('utf-8', errors='replace').strip()
        except Exception:
            msg = ''
        if proc.returncode == 0 and detect_mode(dst) == 'junction':
            return 'junction'
        junction_err = msg or f"mklink trả mã {proc.returncode}"
        try:
            os.symlink(src, dst, target_is_directory=True)
        except OSError as exc:
            raise RuntimeError(f"mklink /J lỗi ({junction_err}); symlink lỗi ({exc})")
        return 'symlink'

    try:
        try:
            target_path = os.path.relpath(src, dst.parent)
        except ValueError:
            target_path = src
        os.symlink(target_path, dst, target_is_directory=True)
    except OSError as exc:
        raise RuntimeError(f"symlink lỗi ({exc})")
    return 'symlink'


# --------------------------------------------------------------------------- #
# In ấn
# --------------------------------------------------------------------------- #

def _disp(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _banner(src: Path, src_fp: dict, check_only: bool) -> None:
    mode = 'KIỂM TRA (chỉ đọc)' if check_only else 'TẠO CẦU NỐI'
    print(f"== Cầu nối skill: {mode} ==")
    print(f"Nguồn: {src}  ({len(src_fp)} skill)")


# --------------------------------------------------------------------------- #
# Luồng chính
# --------------------------------------------------------------------------- #

def run_link(root: Path, src: Path, allow_copy: bool, relink: bool = False) -> int:
    src_fp = fingerprint(src)
    _banner(src, src_fp, check_only=False)
    targets = [root / t for t in TARGETS]
    problems = 0

    for dst in targets:
        label = _disp(dst, root)
        mode = detect_mode(dst)

        if mode in ('junction', 'symlink'):
            if same_target(dst, src):
                print(f"[BỎ QUA] {label}: đã là {mode} trỏ đúng nguồn.")
                continue
            elif relink:
                print(f"[RE-LINK] {label}: đang trỏ sai hoặc đứt link ({os.path.realpath(dst)}). Gỡ và tạo lại...")
                try:
                    if mode == 'junction' and os.name == 'nt':
                        os.rmdir(dst)
                    else:
                        dst.unlink()
                except OSError as exc:
                    print(f"[LỖI]   {label}: không gỡ được link cũ: {exc}")
                    problems += 1
                    continue
                mode = 'missing'
            else:
                print(f"[LỖI]   {label}: đang là {mode} nhưng trỏ tới {os.path.realpath(dst)}, "
                      f"không phải {src}. Không xóa, không ghi đè.")
                print("        Chạy lại với --relink hoặc gỡ thủ công bằng os.rmdir/os.unlink.")
                problems += 1
                continue

        if mode == 'copy':
            if allow_copy and fingerprint(dst) == src_fp:
                print(f"[BỎ QUA] {label}: bản copy đã khớp nội dung nguồn.")
            else:
                print(f"[LỖI]   {label}: là thư mục thật (không phải cầu nối). "
                      f"Không xóa, không ghi đè.")
                print("        Đổi tên/chuyển thư mục đó đi bằng tay rồi chạy lại.")
                problems += 1
            continue

        if mode == 'other':
            print(f"[LỖI]   {label}: đã có file cùng tên. Không ghi đè.")
            problems += 1
            continue

        # mode == 'missing'
        try:
            created = create_link(src, dst)
        except RuntimeError as exc:
            if not allow_copy:
                print(f"[LỖI]   {label}: không tạo được cầu nối. {exc}")
                print("        Chạy lại với --copy nếu chấp nhận bản sao (dễ lệch khi nguồn đổi).")
                problems += 1
                continue
            try:
                shutil.copytree(src, dst)
            except (OSError, shutil.Error) as copy_exc:
                print(f"[LỖI]   {label}: link và copy đều thất bại. {exc} / {copy_exc}")
                problems += 1
                continue
            created = 'copy'

        if created != 'copy' and not same_target(dst, src):
            print(f"[LỖI]   {label}: vừa tạo {created} nhưng không trỏ đúng nguồn "
                  f"({os.path.realpath(dst)}).")
            problems += 1
            continue

        print(f"[TẠO]    {label}: {created} -> {src}")

    if problems:
        print(f"\nTổng kết: {problems} vấn đề. Không xóa gì; xem hướng dẫn ở trên.")
        return EXIT_PROBLEM
    print("\nTổng kết: mọi cầu nối skill đã sẵn sàng.")
    return EXIT_OK


def run_check(root: Path, src: Path) -> int:
    src_fp = fingerprint(src)
    _banner(src, src_fp, check_only=True)
    targets = [root / t for t in TARGETS]
    problems = 0

    for dst in targets:
        label = _disp(dst, root)
        mode = detect_mode(dst)

        if mode == 'missing':
            print(f"[LỖI]   {label}: chưa có cầu nối (missing). "
                  f"Chạy: python scripts/link-skills.py")
            problems += 1
            continue
        if mode == 'other':
            print(f"[LỖI]   {label}: có file cùng tên, không phải thư mục skill.")
            problems += 1
            continue
        if mode in ('junction', 'symlink') and not same_target(dst, src):
            print(f"[LỖI]   {label}: là {mode} nhưng trỏ tới {os.path.realpath(dst)}, "
                  f"không phải {src}.")
            problems += 1
            continue
        if mode == 'copy':
            print(f"[CẢNH BÁO] {label}: là thư mục thật (bản copy), không phải cầu nối — "
                  f"phải chạy lại khi nguồn đổi.")

        dst_fp = fingerprint(dst)
        issues = compare_content(src_fp, dst_fp)
        if issues:
            print(f"[LỖI]   {label}: chế độ {mode}, {len(dst_fp)}/{len(src_fp)} skill, "
                  f"{'; '.join(issues)}")
            problems += 1
        else:
            print(f"[OK]    {label}: chế độ {mode}, {len(dst_fp)}/{len(src_fp)} skill, "
                  f"nội dung khớp.")

    if problems:
        print(f"\nTổng kết: {problems} vấn đề (chỉ đọc, không sửa gì).")
        return EXIT_PROBLEM
    print("\nTổng kết: cầu nối skill đạt.")
    return EXIT_OK


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Tạo/kiểm cầu nối .claude/skills và .qoder/skills trỏ tới bộ skill chuẩn.")
    parser.add_argument('--check', action='store_true',
                        help='Chỉ đọc: báo chế độ cầu nối và kiểm hash nội dung từng skill.')
    parser.add_argument('--copy', action='store_true',
                        help='Cho phép copy thư mục khi cả junction và symlink đều thất bại.')
    parser.add_argument('--relink', action='store_true',
                        help='Gỡ và tạo lại cầu nối nếu đích đang là symlink/junction trỏ sai hoặc đứt link.')
    parser.add_argument('--root', default='',
                        help=f'Thư mục gốc của repo (mặc định: {ROOT}).')
    parser.add_argument('--source', default='',
                        help='Thư mục skill nguồn (mặc định: <root>/.agents/skills).')
    args = parser.parse_args(argv)

    root = Path(args.root).resolve() if args.root else ROOT
    src = Path(args.source).resolve() if args.source else root / '.agents' / 'skills'

    if not root.is_dir():
        print(f"LỖI: thư mục gốc không tồn tại: {root}")
        return EXIT_USAGE
    if not src.is_dir():
        print(f"LỖI: thư mục nguồn không tồn tại: {src}")
        return EXIT_USAGE
    if not fingerprint(src):
        print(f"LỖI: {src} không có thư mục skill nào.")
        return EXIT_USAGE

    if args.check:
        return run_check(root, src)
    return run_link(root, src, args.copy, getattr(args, 'relink', False))


if __name__ == '__main__':
    sys.exit(main())
