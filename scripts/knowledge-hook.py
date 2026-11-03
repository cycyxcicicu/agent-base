#!/usr/bin/env python3
"""scripts/knowledge-hook.py

Hook tùy chọn cho Claude Code (sự kiện UserPromptSubmit): đọc lời người dùng từ stdin (JSON có khóa "prompt"), nếu có kiến thức
khớp rõ ràng thì in 1 đến 3 dòng gợi ý (id, tóm tắt, đường dẫn) để thêm vào ngữ cảnh. Không khớp rõ thì im lặng.

Mặc định KHÔNG bật (không có trong .claude/settings.json sinh ra). Lý do: điểm khớp từ khóa không tách sạch lời thường khỏi lời có chủ đề,
nên cổng đặt chặt để không chèn nhiễu: điểm >= 200 và ít nhất 2 từ khóa khớp ở id, tiêu đề hoặc từ khóa của nút. Đo trên 15 lời thường
và 46 lời có chủ đề: 0 lời thường lọt, bắt được khoảng 43% lời có chủ đề. Phần còn lại agent tự tra bằng `knowledge.py query`.

Bật thủ công: thêm vào .claude/settings.local.json (không commit):
  {"hooks": {"UserPromptSubmit": [{"hooks": [{"type": "command", "command": "python3 scripts/knowledge-hook.py"}]}]}}
Tắt tạm: đặt biến môi trường AGENT_BASE_NO_HOOK=1.

Luôn thoát với mã 0 và không bao giờ làm hỏng phiên.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

MIN_SCORE = 200
MIN_STRONG = 2
MAX_HITS = 3


def suggest(prompt, root=ROOT):
    """Trả về (danh sách gợi ý, nút đầu) hoặc ([], None). Mỗi gợi ý: (id, tiêu đề, tóm tắt, đường dẫn)."""
    from agent_core.knowledge.catalog import load_catalog
    from agent_core.knowledge import search as S

    prompt = (prompt or "").strip()
    if len(prompt) < 12 or prompt.startswith("/"):
        return []
    local = Path(root) / ".local" / "knowledge-manifest.json"
    manifest = ".local/knowledge-manifest.json" if local.is_file() else "agents/knowledge/knowledge-manifest.json"
    catalog = load_catalog(str(root), filename=manifest)
    ranked = S.rank(catalog, str(root), prompt)
    if not ranked:
        return []
    top_score, top = ranked[0]
    sets, _ = S._field_sets(top, str(root))
    strong = sum(1 for t in S.tokens_of(prompt) if any(S._has(t, sets[f]) for f in ("id", "title", "keywords")))
    if top_score < MIN_SCORE or strong < MIN_STRONG:
        return []
    out = []
    for score, node in ranked[:MAX_HITS]:
        if score < 0.5 * top_score:
            break
        path = Path(root) / node.content_ref
        summary = ""
        if path.is_file():
            summary = S._outline(path.read_text(encoding="utf-8", errors="ignore"))[0][:120]
        out.append((node.id, node.title, summary, node.content_ref))
    return out


def main():
    if os.environ.get("AGENT_BASE_NO_HOOK") == "1":
        return
    try:
        raw = sys.stdin.read()
        prompt = json.loads(raw).get("prompt", "") if raw.strip() else ""
        hits = suggest(prompt)
        if not hits:
            return
        lines = ['Gợi ý tri thức (tra thêm: python scripts/knowledge.py query -q "<từ khóa>"):']
        lines += [f"- {i}: {t}. {s} [{f}]" for i, t, s, f in hits]
        print("\n".join(lines))
        log_dir = ROOT / ".local"
        log_dir.mkdir(exist_ok=True)
        with open(log_dir / "knowledge-usage.jsonl", "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), "source": "hook",
                                 "q": prompt[:200], "hits": [h[0] for h in hits]}, ensure_ascii=False) + "\n")
    except Exception:
        return


if __name__ == "__main__":
    main()
    sys.exit(0)
