#!/usr/bin/env python3
"""
scripts/hard-check.py
Luật cứng khai báo bằng JSON: biến một nhận xét review lặp lại thành kiểm tra tự động, không cần viết linter riêng.
Giao thức: agents/protocols/hard-rules.md. Luật của dự án nằm ở docs/HARD-RULES.json (mẫu: examples/hard-rules/).

Cách dùng:
  python scripts/hard-check.py                              # quét mọi file theo dõi trong git (hoặc mọi file nếu không phải repo git)
  python scripts/hard-check.py --changed-against origin/develop   # chỉ file đổi so với nhánh gốc (dùng cho PR, không bị đỏ vì code cũ)
  python scripts/hard-check.py --rules path/to/rules.json

Thoát: 0 đạt (hoặc chưa có file luật), 1 có vi phạm mức error, 2 file luật sai.

Loại luật:
  forbid_regex    {id, include:[glob], exclude:[glob], pattern, message, severity}   cấm một mẫu (dòng nào khớp thì vi phạm)
  max_file_lines  {id, include:[glob], exclude:[glob], max, message, severity}        file không dài quá `max` dòng
  path_must_match {id, include:[glob], exclude:[glob], allow:[glob], message, severity}  file thuộc `include` phải nằm đúng chỗ `allow`
                  (cấu trúc quy ước: ví dụ mã tính năng mới chỉ được đặt trong src/features/<tên>/)
Cấm import chéo ranh giới module là forbid_regex với include là thư mục nguồn và pattern là câu import cấm.

Bỏ qua có lý do: thêm vào CÙNG dòng hoặc dòng ngay trước  `hard-ignore: <id> <lý do>`  (bắt buộc có lý do, kết quả đếm số lần bỏ qua).
"""

import argparse
import json
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
DEFAULT_RULES = 'docs/HARD-RULES.json'
MAX_FILE_BYTES = 1_000_000
SKIP_DIRS = {'.git', 'node_modules', 'build', 'dist', '__pycache__', 'graphify-out', '.venv', 'venv', '.next', 'coverage'}
RULE_TYPES = {'forbid_regex', 'max_file_lines', 'path_must_match'}
SEVERITIES = {'error', 'warn'}


def glob_to_regex(glob_str: str) -> str:
    g = glob_str.replace('\\', '/')
    out, i, n = [], 0, len(g)
    while i < n:
        c = g[i]
        if c == '*':
            if i + 1 < n and g[i + 1] == '*':
                if i + 2 < n and g[i + 2] == '/':
                    out.append('(?:.*/)?')
                    i += 3
                    continue
                out.append('.*')
                i += 2
                continue
            out.append('[^/]*')
        elif c == '?':
            out.append('[^/]')
        else:
            out.append(re.escape(c))
        i += 1
    return '^' + ''.join(out) + '$'


def matches(path: str, globs) -> bool:
    return any(re.match(glob_to_regex(g), path) for g in globs)


def load_rules(path: Path):
    """Đọc và kiểm tra file luật. Trả về danh sách luật đã chuẩn hóa; ném ValueError nếu sai."""
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: JSON sai ({exc})")
    rules = data.get('rules') if isinstance(data, dict) else None
    if not isinstance(rules, list):
        raise ValueError(f"{path}: cần khóa \"rules\" là một danh sách")
    seen, out = set(), []
    for idx, r in enumerate(rules, 1):
        where = f"{path}: luật #{idx}"
        rid = r.get('id')
        if not rid or not re.match(r'^[a-z0-9][a-z0-9-]*$', str(rid)):
            raise ValueError(f"{where}: id phải là chữ thường, số, dấu gạch ngang")
        if rid in seen:
            raise ValueError(f"{where}: id '{rid}' bị trùng")
        seen.add(rid)
        if r.get('type') not in RULE_TYPES:
            raise ValueError(f"{where} ({rid}): type phải là một trong {sorted(RULE_TYPES)}")
        if not r.get('include') or not isinstance(r['include'], list):
            raise ValueError(f"{where} ({rid}): cần include là danh sách glob")
        sev = r.get('severity', 'error')
        if sev not in SEVERITIES:
            raise ValueError(f"{where} ({rid}): severity phải là error hoặc warn")
        rule = {'id': rid, 'type': r['type'], 'include': r['include'], 'exclude': r.get('exclude', []),
                'message': r.get('message') or r.get('description') or rid, 'severity': sev}
        if rule['type'] == 'forbid_regex':
            try:
                rule['regex'] = re.compile(r['pattern'])
            except (KeyError, re.error) as exc:
                raise ValueError(f"{where} ({rid}): pattern thiếu hoặc không biên dịch được ({exc})")
        elif rule['type'] == 'path_must_match':
            allow = r.get('allow')
            if not isinstance(allow, list) or not allow or not all(isinstance(a, str) and a for a in allow):
                raise ValueError(f"{where} ({rid}): path_must_match cần allow là danh sách glob không rỗng")
            rule['allow'] = allow
        else:
            if not isinstance(r.get('max'), int) or r['max'] < 1:
                raise ValueError(f"{where} ({rid}): max phải là số nguyên >= 1")
            rule['max'] = r['max']
        out.append(rule)
    return out


def git_lines(root: Path, *args):
    return subprocess.check_output(['git', '-C', str(root), '-c', 'core.quotepath=false', *args],
                                   text=True, encoding='utf-8', stderr=subprocess.DEVNULL).splitlines()


def list_files(root: Path, changed_against):
    """Danh sách đường dẫn (POSIX, tương đối gốc) cần quét."""
    try:
        if changed_against:
            names = git_lines(root, 'diff', '--name-only', '--diff-filter=ACMR', '--no-renames', f'{changed_against}...HEAD')
        else:
            names = git_lines(root, 'ls-files', '-co', '--exclude-standard')
        return sorted({n.strip().replace('\\', '/') for n in names if n.strip()})
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        if changed_against:
            raise ValueError(f"không lấy được danh sách file đổi so với {changed_against} (không phải repo git hoặc sai tên nhánh)")
        found = []
        for p in root.rglob('*'):
            if p.is_file() and not (set(p.relative_to(root).parts) & SKIP_DIRS):
                found.append(p.relative_to(root).as_posix())
        return sorted(found)


def check(root: Path, rules, files):
    """Trả về (vi phạm, số lần bỏ qua có lý do). Mỗi vi phạm: (đường dẫn, dòng, id, mức, thông điệp)."""
    violations, ignored = [], 0
    for rel in files:
        applicable = [r for r in rules if matches(rel, r['include']) and not matches(rel, r['exclude'])]
        if not applicable:
            continue
        # Luật vị trí file (cấu trúc quy ước) chỉ xét đường dẫn, không cần đọc nội dung
        for rule in applicable:
            if rule['type'] == 'path_must_match' and not matches(rel, rule['allow']):
                violations.append((rel, 1, rule['id'], rule['severity'],
                                   f"{rule['message']} (file này phải nằm trong: {', '.join(rule['allow'])})"))
        applicable = [r for r in applicable if r['type'] != 'path_must_match']
        if not applicable:
            continue
        path = root / rel
        try:
            if not path.is_file() or path.stat().st_size > MAX_FILE_BYTES:
                continue
            lines = path.read_text(encoding='utf-8', errors='ignore').splitlines()
        except OSError:
            continue

        def is_ignored(rule_id, idx):
            marker = re.compile(r'hard-ignore:\s*' + re.escape(rule_id) + r'\s+\S{3,}')
            return bool(marker.search(lines[idx]) or (idx > 0 and marker.search(lines[idx - 1])))

        for rule in applicable:
            if rule['type'] == 'forbid_regex':
                for i, line in enumerate(lines):
                    if rule['regex'].search(line):
                        if is_ignored(rule['id'], i):
                            ignored += 1
                        else:
                            violations.append((rel, i + 1, rule['id'], rule['severity'], rule['message']))
            elif len(lines) > rule['max']:
                violations.append((rel, rule['max'] + 1, rule['id'], rule['severity'],
                                   f"{rule['message']} (file dài {len(lines)} dòng, tối đa {rule['max']})"))
    return violations, ignored


def main() -> int:
    ap = argparse.ArgumentParser(description="Kiểm tra luật cứng khai báo bằng JSON.")
    ap.add_argument('--rules', default=DEFAULT_RULES, help=f"file luật (mặc định {DEFAULT_RULES})")
    ap.add_argument('--changed-against', metavar='REF', help="chỉ quét file đổi so với REF (ví dụ origin/develop)")
    ap.add_argument('--root', default=str(ROOT), help="gốc dự án cần quét (mặc định: dự án chứa script này)")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    rules_path = Path(args.rules)
    if not rules_path.is_absolute():
        rules_path = root / rules_path
    if not rules_path.exists():
        print(f"Chưa có {rules_path.relative_to(root) if rules_path.is_relative_to(root) else rules_path}: không có luật cứng nào để kiểm. "
              "Cách thêm luật: agents/protocols/hard-rules.md")
        return 0
    try:
        rules = load_rules(rules_path)
        files = list_files(root, args.changed_against)
    except ValueError as exc:
        print(f"LỖI: {exc}")
        return 2

    violations, ignored = check(root, rules, files)
    for rel, line, rid, sev, msg in violations:
        print(f"{rel}:{line}: [{rid}] {'LỖI' if sev == 'error' else 'cảnh báo'}: {msg}")
    errors = sum(1 for v in violations if v[3] == 'error')
    scope = f"file đổi so với {args.changed_against}" if args.changed_against else "toàn bộ file"
    print(f"Luật cứng: {len(rules)} luật, quét {len(files)} {scope}; {errors} lỗi, {len(violations) - errors} cảnh báo, "
          f"{ignored} lần bỏ qua có lý do.")
    if errors:
        print("FAIL: sửa chỗ vi phạm, hoặc nếu có lý do chính đáng thì thêm `hard-ignore: <id> <lý do>` (Reviewer sẽ xem lý do).")
        return 1
    print("PASS")
    return 0


if __name__ == '__main__':
    sys.exit(main())
