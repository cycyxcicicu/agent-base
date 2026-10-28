"""Kiểm thử bảng điều khiển tools/viewer: site tách nhiều file nhẹ, nội dung nạp theo yêu cầu, máy chủ chỉ phục vụ thư mục an toàn.
Viết bằng unittest (CI chạy `python -m unittest discover -s tests`, không cài pytest)."""
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _generate(project: Path, out: Path):
    env = dict(os.environ, VIEWER_ROOT=str(project), VIEWER_OUT=str(out), PYTHONIOENCODING='utf-8')
    return subprocess.run([sys.executable, str(ROOT / 'scripts' / 'generate-dashboard.py')],
                          env=env, capture_output=True, text=True, encoding='utf-8', timeout=120)


def _make_project(base: Path) -> Path:
    proj = base / 'proj'
    (proj / 'docs' / 'spec').mkdir(parents=True)
    (proj / 'tasks').mkdir()
    (proj / 'PROJECT.md').write_text('# Demo\n\n| Tên dự án | Demo |\n|---|---|\n', encoding='utf-8')
    (proj / 'docs' / 'spec' / 'a.md').write_text('# Đặc tả A\n\nNội dung </script><b>x</b> thử.\n', encoding='utf-8')
    return proj


class TestViewerSite(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix='viewer-test-')
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name)
        self.proj = _make_project(self.base)
        self.out = self.base / 'out'
        res = _generate(self.proj, self.out)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_generate_splits_into_light_files(self):
        for name in ('index.html', 'dashboard.css', 'dashboard.js', 'data.js', 'monitor.html'):
            self.assertTrue((self.out / name).is_file(), name)
        self.assertTrue((self.out / 'cards' / '_search.js').is_file())
        self.assertTrue(list((self.out / 'docs').glob('*.js')), 'mỗi tài liệu phải có file riêng')
        index = (self.out / 'index.html').read_text(encoding='utf-8')
        self.assertNotIn('@@', index, 'còn thẻ @@TOKEN@@ chưa thay')
        for needle in ('dashboard.css', 'data.js', 'dashboard.js'):
            self.assertIn(needle, index)
        self.assertLess(len(index), 100_000, 'khung trang phải nhẹ')

    def test_doc_body_not_in_index_and_script_close_is_escaped(self):
        data = (self.out / 'data.js').read_text(encoding='utf-8')
        self.assertNotIn('html_body', data)
        self.assertNotIn('raw_md', data)
        body_js = ''.join(p.read_text(encoding='utf-8') for p in (self.out / 'docs').glob('*.js'))
        self.assertNotIn('</script>', body_js, 'phải escape "</" để không đóng thẻ script sớm')
        self.assertIn('window.__setDoc(', body_js)


class TestMonitorStatic(unittest.TestCase):
    def test_static_whitelist_blocks_secrets_and_traversal(self):
        spec = importlib.util.spec_from_file_location('watch_swarm_under_test', ROOT / 'scripts' / 'watch-swarm.py')
        ws = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ws)
        for url in ('/.env', '/AGENTS.md', '/scripts/watch-swarm.py', '/viewer/../../.env',
                    '/viewer/%2e%2e/%2e%2e/AGENTS.md', '/docs/../.env', '/docs/../AGENTS.md'):
            self.assertIsNone(ws.resolve_static(url), url)


if __name__ == '__main__':
    unittest.main()
