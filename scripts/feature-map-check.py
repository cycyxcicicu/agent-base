#!/usr/bin/env python3
"""
scripts/feature-map-check.py
Kiểm Feature Map (docs/design/feature-map.md) có còn khớp mã nguồn không. Giao thức: agents/protocols/feature-map.md,
skill: .agents/skills/feature-map/SKILL.md. Chỉ ĐỌC, không sửa gì.

Kiểm:
  - mỗi mục `## F-xx <tên>` có đủ: Khu vực, Đường vào, Định vị, File nguồn, Kiểm tra nhanh;
  - mọi đường dẫn trong `File nguồn` (đặt trong dấu `) có thật;
  - mọi `data-testid` trong `Định vị` còn xuất hiện trong mã (trước hết trong file nguồn của mục, sau đó cả dự án);
  - (tùy chọn --changed-against REF) file giao diện đổi nhưng không thuộc mục nào: cảnh báo, gợi ý cập nhật bản đồ.
Đếm số mục còn đánh dấu `(chưa kiểm)`.

Thoát: 0 khớp (hoặc dự án chưa có Feature Map), 1 có lỗi lệch, 2 lỗi dùng.

Cách dùng:
  python scripts/feature-map-check.py
  python scripts/feature-map-check.py --changed-against origin/develop
  python scripts/feature-map-check.py --map docs/design/feature-map.md
"""

import argparse
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
DEFAULT_MAP = 'docs/design/feature-map.md'
REQUIRED = ['Khu vực', 'Đường vào', 'Định vị', 'File nguồn', 'Kiểm tra nhanh']
FIELDS = REQUIRED + ['Điều kiện', 'Thao tác', 'Tính năng phụ']
SRC_EXT = {'.js', '.jsx', '.ts', '.tsx', '.vue', '.svelte', '.html', '.htm', '.dart', '.kt', '.java', '.swift', '.xml',
           '.cshtml', '.razor', '.py', '.php', '.erb', '.astro', '.mdx'}
UI_EXT = {'.js', '.jsx', '.ts', '.tsx', '.vue', '.svelte', '.html', '.htm', '.dart', '.kt', '.swift', '.xml', '.cshtml',
          '.razor', '.astro', '.css', '.scss'}
SKIP_DIRS = {'.git', 'node_modules', 'build', 'dist', '__pycache__', 'graphify-out', '.venv', 'venv', '.next', 'coverage'}
TEST_HINTS = ('.test.', '.spec.', '/__tests__/', '/tests/', '/test/', '/e2e/')


def parse_map(text: str):
    """Trả về danh sách mục: {id, title, line, fields:{tên: nội dung}}."""
    entries, cur = [], None
    for lineno, line in enumerate(text.splitlines(), 1):
        m = re.match(r'^##\s+(F-\d+)\b\s*(.*)$', line)
        if m:
            cur = {'id': m.group(1), 'title': m.group(2).strip(), 'line': lineno, 'fields': {}}
            entries.append(cur)
            continue
        if cur is None:
            continue
        m = re.match(r'^[-*]\s+(' + '|'.join(FIELDS) + r')\s*:\s*(.*)$', line)
        if m:
            cur['fields'][m.group(1)] = m.group(2).strip()
    return entries


def backticked(s: str):
    return [t.strip() for t in re.findall(r'`([^`]+)`', s) if t.strip()]


def testids(s: str):
    return sorted(set(re.findall(r'data-testid\s*=\s*["\']?([\w.:\-/]+)', s)))


def repo_files(root: Path):
    try:
        names = subprocess.check_output(['git', '-C', str(root), '-c', 'core.quotepath=false', 'ls-files', '-co', '--exclude-standard'],
                                        text=True, encoding='utf-8', stderr=subprocess.DEVNULL).splitlines()
        return sorted({n.strip().replace('\\', '/') for n in names if n.strip()})
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return sorted(p.relative_to(root).as_posix() for p in root.rglob('*')
                      if p.is_file() and not (set(p.relative_to(root).parts) & SKIP_DIRS))


def changed_files(root: Path, ref: str):
    try:
        names = subprocess.check_output(
            ['git', '-C', str(root), '-c', 'core.quotepath=false', 'diff', '--name-only', '--diff-filter=ACMR', '--no-renames', f'{ref}...HEAD'],
            text=True, encoding='utf-8', stderr=subprocess.DEVNULL).splitlines()
        return sorted({n.strip().replace('\\', '/') for n in names if n.strip()})
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        raise ValueError(f"không lấy được file đổi so với {ref} (không phải repo git hoặc sai tên nhánh)")


class Source:
    """Đọc nội dung file nguồn khi cần, có nhớ tạm."""

    def __init__(self, root: Path, files):
        self.root, self.files, self.cache = root, files, {}

    def text(self, rel):
        if rel not in self.cache:
            try:
                p = self.root / rel
                self.cache[rel] = p.read_text(encoding='utf-8', errors='ignore') if p.stat().st_size < 1_000_000 else ''
            except OSError:
                self.cache[rel] = ''
        return self.cache[rel]

    def expand(self, token: str):
        """File hoặc thư mục trong `File nguồn` thành danh sách file nguồn thật."""
        t = token.strip().strip('/').replace('\\', '/')
        if (self.root / t).is_file():
            return [t]
        return [f for f in self.files if f.startswith(t + '/') and Path(f).suffix.lower() in SRC_EXT]

    def contains(self, needle: str, rels):
        return any(needle in self.text(r) for r in rels)


def check(root: Path, map_path: Path, changed_ref=None):
    errors, warnings, info = [], [], []
    entries = parse_map(map_path.read_text(encoding='utf-8', errors='ignore'))
    if not entries:
        return [f"{map_path.name}: không có mục `## F-xx` nào"], warnings, info, 0
    files = repo_files(root)
    src = Source(root, files)
    owned = set()
    unverified = 0
    ids_seen = set()

    for e in entries:
        where = f"{e['id']} ({map_path.name}:{e['line']})"
        if e['id'] in ids_seen:
            errors.append(f"{where}: mã F-xx bị trùng")
        ids_seen.add(e['id'])
        for name in REQUIRED:
            if not e['fields'].get(name):
                errors.append(f"{where}: thiếu mục \"{name}\"")
        if any('(chưa kiểm)' in v for v in e['fields'].values()) or '(chưa kiểm)' in e['title']:
            unverified += 1

        entry_files = []
        for tok in backticked(e['fields'].get('File nguồn', '')):
            found = src.expand(tok)
            if not found:
                errors.append(f"{where}: File nguồn `{tok}` không còn tồn tại")
            entry_files += found
        owned.update(entry_files)

        for tid in testids(e['fields'].get('Định vị', '')):
            if src.contains(tid, entry_files):
                continue
            if src.contains(tid, [f for f in files if Path(f).suffix.lower() in SRC_EXT]):
                warnings.append(f"{where}: data-testid \"{tid}\" có trong dự án nhưng không nằm trong File nguồn của mục này")
            else:
                errors.append(f"{where}: data-testid \"{tid}\" không còn xuất hiện trong mã (selector lệch)")

    if changed_ref:
        for f in changed_files(root, changed_ref):
            low = '/' + f.lower()
            if Path(f).suffix.lower() in UI_EXT and not any(h in low for h in TEST_HINTS) and f not in owned:
                warnings.append(f"file giao diện đổi nhưng không thuộc mục nào trong Feature Map: {f}")
    return errors, warnings, info, unverified


def main() -> int:
    ap = argparse.ArgumentParser(description="Kiểm Feature Map có còn khớp mã nguồn không.")
    ap.add_argument('--map', default=DEFAULT_MAP)
    ap.add_argument('--changed-against', metavar='REF')
    ap.add_argument('--root', default=str(ROOT))
    args = ap.parse_args()

    root = Path(args.root).resolve()
    map_path = Path(args.map)
    if not map_path.is_absolute():
        map_path = root / map_path
    if not map_path.exists():
        print(f"Chưa có {args.map}: dự án chưa có Feature Map (bỏ qua nếu không có giao diện). Cách tạo: agents/protocols/feature-map.md")
        return 0
    try:
        errors, warnings, _info, unverified = check(root, map_path, args.changed_against)
    except ValueError as exc:
        print(f"LỖI: {exc}")
        return 2

    for w in warnings:
        print(f"cảnh báo: {w}")
    for e in errors:
        print(f"LỆCH: {e}")
    print(f"Feature Map: {len(errors)} lỗi lệch, {len(warnings)} cảnh báo, {unverified} mục còn `(chưa kiểm)`.")
    if errors:
        print("FAIL: cập nhật Feature Map cho khớp mã (skill feature-map, chế độ maintain), kiểm lại trên ứng dụng thật rồi chạy lại.")
        return 1
    print("PASS")
    return 0


if __name__ == '__main__':
    sys.exit(main())
