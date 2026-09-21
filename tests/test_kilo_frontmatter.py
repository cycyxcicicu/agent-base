"""
tests/test_kilo_frontmatter.py
Bảo đảm các file .kilo/agents/*.md do sync-adapters sinh ra luôn có YAML frontmatter HỢP LỆ.

Lỗi từng xảy ra: mẫu chặn chứa ký tự xuống dòng thật (`*\\ngit push*`) hoặc dấu `\\` (`.\\mvnw.cmd*`) được ghi thô vào
chuỗi YAML, làm cả 20 file không đọc được; và khoá lặp (`*drop table*` xuất hiện hai lần) bị trình đọc YAML nghiêm ngặt
(js-yaml của Kilo) từ chối. `sync-adapters --check` không bắt được vì nó chỉ so file sinh ra với chính nó.
"""

import glob
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location("sync_adapters", str(ROOT / "scripts" / "sync-adapters.py"))
_argv = sys.argv
try:
    sys.argv = [str(ROOT / "scripts" / "sync-adapters.py"), "--check"]  # tránh ghi file khi nạp module
    sync_adapters = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(sync_adapters)
finally:
    sys.argv = _argv

try:
    import yaml  # PyYAML: có sẵn trên máy dev, có thể không có trên CI
except ImportError:  # pragma: no cover
    yaml = None


def _frontmatter(path: str) -> str:
    text = Path(path).read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, f"{path}: thiếu frontmatter"
    return m.group(1)


class TestKiloFrontmatterStructure(unittest.TestCase):
    """Kiểm tra cấu trúc bằng bộ kiểm tra riêng của sync-adapters (không cần PyYAML)."""

    def test_all_role_files_have_valid_structure(self):
        files = sorted(glob.glob(str(ROOT / ".kilo" / "agents" / "*.md")))
        self.assertGreaterEqual(len(files), 20)
        for f in files:
            text = Path(f).read_text(encoding="utf-8").replace("\r\n", "\n")
            problems = sync_adapters.validate_kilo_frontmatter(text, Path(f).name)
            self.assertEqual(problems, [], f"{Path(f).name}: {problems[:3]}")

    def test_no_raw_control_characters_in_frontmatter(self):
        for f in sorted(glob.glob(str(ROOT / ".kilo" / "agents" / "*.md"))):
            fm = _frontmatter(f)
            self.assertIsNone(re.search(r"[\x00-\x08\x0b-\x1f]", fm.replace("\t", "")), f"{Path(f).name}: ký tự điều khiển thô")
            self.assertNotIn("\t", fm, f"{Path(f).name}: tab thô trong frontmatter")

    def test_every_rule_line_is_one_line(self):
        for f in sorted(glob.glob(str(ROOT / ".kilo" / "agents" / "*.md"))):
            for n, line in enumerate(_frontmatter(f).split("\n"), 2):
                if line.startswith("    "):
                    self.assertRegex(line, r'^    "(?:[^"\\]|\\.)*": (?:allow|deny|ask)$', f"{Path(f).name}:{n}")


@unittest.skipIf(yaml is None, "PyYAML không có: bỏ qua kiểm tra bằng trình đọc YAML thật")
class TestKiloFrontmatterWithYamlParser(unittest.TestCase):
    """Kiểm tra bằng trình đọc YAML thật, từ chối khoá lặp như js-yaml."""

    @staticmethod
    def _strict_load(text: str):
        class StrictLoader(yaml.SafeLoader):
            pass

        def construct_mapping(loader, node, deep=False):
            seen = set()
            for key_node, _ in node.value:
                key = loader.construct_object(key_node, deep=deep)
                if key in seen:
                    raise ValueError(f"duplicated mapping key: {key!r}")
                seen.add(key)
            return yaml.SafeLoader.construct_mapping(loader, node, deep)

        StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
        return yaml.load(text, Loader=StrictLoader)

    def test_all_role_files_parse_without_duplicate_keys(self):
        for f in sorted(glob.glob(str(ROOT / ".kilo" / "agents" / "*.md"))):
            data = self._strict_load(_frontmatter(f))
            self.assertIn("permission", data, Path(f).name)

    def test_newline_tab_and_backslash_patterns_survive_round_trip(self):
        data = self._strict_load(_frontmatter(str(ROOT / ".kilo" / "agents" / "dev.md")))
        bash = data["permission"]["bash"]
        self.assertIn("*\ngit reset*", bash)  # xuống dòng thật
        self.assertIn("git\t*", bash)         # tab thật
        self.assertEqual(bash["*\ngit reset*"], "deny")
        runner = self._strict_load(_frontmatter(str(ROOT / ".kilo" / "agents" / "runner.md")))
        self.assertTrue(any("\\mvnw.cmd" in k for k in runner["permission"]["bash"]))  # dấu \ thật

    def test_last_match_wins_order_is_preserved(self):
        """*drop table* ban đầu 'ask' rồi bị vai sre 'deny': sau khi khử trùng phải còn đúng một khoá và là 'deny'."""
        data = self._strict_load(_frontmatter(str(ROOT / ".kilo" / "agents" / "sre.md")))
        self.assertEqual(data["permission"]["bash"]["*drop table*"], "deny")


class TestYamlQuoting(unittest.TestCase):
    def test_yq_round_trips_through_json(self):
        for s in ["plain", 'a"b', "back\\slash", "*\ngit push*", "git\t*", ".\\mvnw.cmd*", "tiếng Việt ✓", "a\r\nb"]:
            self.assertEqual(json.loads(sync_adapters.yq(s)), s)

    def test_yq_output_is_single_line(self):
        for s in ["*\ngit push*", "git\t*", "a\r\nb"]:
            self.assertNotRegex(sync_adapters.yq(s), r"[\n\r\t]")

    def test_dedupe_keeps_last_occurrence_at_its_position(self):
        lines = ["  bash:", '    "a": ask', '    "b": allow', '    "a": deny', '    "c": allow', "  webfetch: deny"]
        out = sync_adapters.dedupe_rule_lines(lines)
        self.assertEqual(out, ["  bash:", '    "b": allow', '    "a": deny', '    "c": allow', "  webfetch: deny"])

    def test_validator_rejects_bad_front_matter(self):
        good = '---\npermission:\n  bash:\n    "*": allow\n---\nbody\n'
        self.assertEqual(sync_adapters.validate_kilo_frontmatter(good, "x.md"), [])
        raw_newline = '---\npermission:\n  bash:\n    "*\ngit push*": deny\n---\nbody\n'
        self.assertTrue(sync_adapters.validate_kilo_frontmatter(raw_newline, "x.md"))
        dup = '---\npermission:\n  bash:\n    "a": ask\n    "a": deny\n---\nbody\n'
        self.assertTrue(any("duplicate" in p for p in sync_adapters.validate_kilo_frontmatter(dup, "x.md")))


if __name__ == "__main__":
    unittest.main()
