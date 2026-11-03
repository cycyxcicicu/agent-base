#!/usr/bin/env python3
"""
scripts/toggle-permissions.py
Bật / tắt các quyền hạn chế (deny) của các Agent trong Kilo Code.

Chế độ:
  --relax   : Comment lại các dòng cấm (deny) để Agent tự do phát triển phần mềm.
  --strict  : Mở lại các dòng cấm (deny) để áp dụng quy tắc bảo mật doanh nghiệp nghiêm ngặt.
"""

import sys
import glob
from pathlib import Path

def process_file(file_path: Path, mode: str):
    text = file_path.read_text(encoding='utf-8')
    parts = text.split('---', 2)
    if len(parts) < 3:
        return False, "Not valid frontmatter"
    
    front = parts[1]
    lines = front.splitlines()
    new_lines = []
    in_perm = False
    modified = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('permission:'):
            in_perm = True
            new_lines.append(line)
            continue
        
        if in_perm:
            # Check if left the permission section
            if stripped and not line.startswith(' ') and not line.startswith('\t'):
                in_perm = False
            elif mode == 'relax':
                if stripped.startswith('# [DENY_RESTRICTED]'):
                    # Already relaxed
                    new_lines.append(line)
                    continue
                if stripped == 'edit: deny':
                    indent = len(line) - len(line.lstrip())
                    sp = ' ' * indent
                    new_lines.append(f"{sp}# [DENY_RESTRICTED] edit: deny")
                    new_lines.append(f"{sp}edit: allow")
                    modified = True
                    continue
                if stripped == 'bash: deny':
                    indent = len(line) - len(line.lstrip())
                    sp = ' ' * indent
                    new_lines.append(f"{sp}# [DENY_RESTRICTED] bash: deny")
                    new_lines.append(f"{sp}bash: allow")
                    modified = True
                    continue
                if stripped == '"*": deny':
                    indent = len(line) - len(line.lstrip())
                    sp = ' ' * indent
                    new_lines.append(f"{sp}# [DENY_RESTRICTED] \"*\": deny")
                    new_lines.append(f"{sp}\"*\": allow")
                    modified = True
                    continue
                if stripped.endswith(': deny'):
                    indent = len(line) - len(line.lstrip())
                    sp = ' ' * indent
                    new_lines.append(f"{sp}# [DENY_RESTRICTED] {stripped}")
                    modified = True
                    continue
            elif mode == 'strict':
                # Restore original
                if '# [DENY_RESTRICTED]' in line:
                    indent = len(line) - len(line.lstrip())
                    sp = ' ' * indent
                    orig = stripped.replace('# [DENY_RESTRICTED] ', '').replace('# [DENY_RESTRICTED]', '')
                    new_lines.append(f"{sp}{orig}")
                    modified = True
                    continue
                if stripped in ('edit: allow', 'bash: allow', '"*": allow'):
                    # If this was added during relax, skip it if preceding was restored
                    # We will check if the line above had [DENY_RESTRICTED]
                    continue

        new_lines.append(line)

    if modified:
        new_text = '---' + '\n'.join(new_lines) + '\n---' + parts[2]
        file_path.write_text(new_text, encoding='utf-8')
        return True, "Updated"
    return False, "No changes"

def main():
    # Mặc định là STRICT (bảo vệ): chỉ nới quyền khi được yêu cầu rõ bằng --relax.
    mode = 'strict'
    if len(sys.argv) > 1 and sys.argv[1] in ('--relax', 'relax'):
        mode = 'relax'
    elif len(sys.argv) > 1 and sys.argv[1] in ('--strict', 'strict'):
        mode = 'strict'

    print(f"=== Running toggle-permissions in [{mode.upper()}] mode ===")

    # Suy ra đường dẫn từ vị trí script để base copy sang máy/dự án khác vẫn chạy đúng.
    base_root = Path(__file__).resolve().parent.parent  # .../agent-base
    candidate_roots = [
        base_root / ".kilo" / "agents",          # .kilo của chính base
        base_root.parent / ".kilo" / "agents",   # .kilo ở thư mục cha (workspace)
    ]
    seen = set()
    roots = []
    for r in candidate_roots:
        rp = r.resolve()
        if rp not in seen:
            seen.add(rp)
            roots.append(rp)

    total_processed = 0
    for r in roots:
        if not r.exists():
            continue
        for f in r.glob("*.md"):
            changed, status = process_file(f, mode)
            if changed:
                total_processed += 1
                print(f"  [{mode}] {f.parent.parent.name}/{f.name} -> {status}")

    print(f"\nDone! Modified {total_processed} agent files.")
    if mode == 'relax':
        print(">> To revert back to strict permissions later, run: python scripts/toggle-permissions.py --strict")
    else:
        print(">> To relax permissions again later, run: python scripts/toggle-permissions.py --relax")

if __name__ == '__main__':
    main()
