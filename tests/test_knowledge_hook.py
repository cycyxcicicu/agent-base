"""Kiểm thử hook gợi ý tri thức: chỉ lên tiếng khi khớp rõ, im lặng với lời thường, không bao giờ làm hỏng phiên."""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run_hook(payload, env_extra=None):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", **(env_extra or {}))
    stdin = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
    return subprocess.run([sys.executable, "scripts/knowledge-hook.py"], cwd=ROOT, input=stdin, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", env=env)


class TestKnowledgeHook(unittest.TestCase):
    def test_topic_prompt_gets_suggestions(self):
        r = run_hook({"prompt": "tối ưu câu sql chậm và lỗi jpa n+1 trên postgres"})
        self.assertEqual(r.returncode, 0)
        self.assertIn("Gợi ý tri thức", r.stdout)
        self.assertIn("sql-postgresql-and-jpa-hibernate", r.stdout)
        self.assertLess(len(r.stdout), 1500)

    def test_ordinary_prompts_stay_silent(self):
        for p in ("xin chào bạn nhé hôm nay", "chạy lệnh git status giúp tôi", "sửa lỗi chính tả trong file này", "tiếp tục làm đi nhé"):
            r = run_hook({"prompt": p})
            self.assertEqual((r.returncode, r.stdout), (0, ""), p)

    def test_never_breaks_the_session(self):
        for bad in ("", "không phải json", "{}", json.dumps({"prompt": None})):
            r = run_hook(bad)
            self.assertEqual((r.returncode, r.stdout), (0, ""), bad)

    def test_can_be_disabled(self):
        r = run_hook({"prompt": "tối ưu câu sql chậm và lỗi jpa n+1 trên postgres"}, {"AGENT_BASE_NO_HOOK": "1"})
        self.assertEqual((r.returncode, r.stdout), (0, ""))

    def test_hook_is_not_enabled_by_default(self):
        settings = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
        self.assertNotIn("hooks", settings)


if __name__ == "__main__":
    unittest.main()
