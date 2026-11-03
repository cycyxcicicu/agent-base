#!/usr/bin/env python3
"""
scripts/show-permissions.py
Print the permission matrix of every role, read straight from agents/roles/*.md.

Usage:
  python scripts/show-permissions.py
"""

import sys
import re
from pathlib import Path

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


def parse_meta(front: str) -> dict:
    meta = {}
    cur = None
    for line in front.splitlines():
        m_item = re.match(r'^\s+-\s+(.+)$', line)
        if m_item:
            if cur:
                if not isinstance(meta[cur], list):
                    meta[cur] = []
                meta[cur].append(m_item.group(1).strip().strip('"'))
            continue
        m_key = re.match(r'^([a-z_]+):\s*(.*)$', line)
        if m_key:
            cur = m_key.group(1)
            val = m_key.group(2).strip()
            meta[cur] = [] if val == '' else val
    return meta


def main():
    root = Path(__file__).resolve().parent.parent
    roles_dir = root / 'agents' / 'roles'
    role_files = sorted(list(roles_dir.glob('*.md')), key=lambda x: x.name)

    headers = ["Role", "Mode", "Tier", "Bash", "Web", "EditAllow", "EditDeny", "ExtraAsk"]
    rows = []

    for f in role_files:
        text = f.read_text(encoding='utf-8').replace('\r\n', '\n')
        m = re.match(r'(?s)^---\n(.*?)\n---', text)
        if not m:
            continue
        meta = parse_meta(m.group(1))

        allow = meta.get('edit_allow', [])
        if not isinstance(allow, list):
            allow = [allow]
        allow = [x for x in allow if x != 'docs/notes/inbox/**']

        deny = meta.get('edit_deny', [])
        if not isinstance(deny, list):
            deny = [deny]

        ask = meta.get('bash_ask', [])
        if not isinstance(ask, list):
            ask = [ask]

        rows.append([
            meta.get('name', ''),
            meta.get('mode', ''),
            meta.get('model_tier', ''),
            meta.get('bash', ''),
            meta.get('web', 'deny'),
            ', '.join(allow),
            ', '.join(deny),
            ', '.join(ask)
        ])

    # Print formatted table
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(val))

    # Format header
    header_line = "  ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    sep_line = "  ".join("-" * col_widths[i] for i in range(len(headers)))
    print(header_line)
    print(sep_line)
    for row in rows:
        print("  ".join(val.ljust(col_widths[i]) for i, val in enumerate(row)))

    print("\nEvery role may also write its own handoff note in docs/notes/inbox/.")
    print("bash: none = no shell | readonly = git status/diff/log/show only | full = any command, except ask/deny lists in sync-adapters")
    print("web:  allow | ask | deny for webfetch, websearch and codesearch (default deny)")


if __name__ == '__main__':
    main()
