"""Tests for scripts/link-skills.py: cầu nối .claude/skills và .qoder/skills.

Mọi ca chạy script qua subprocess với `sys.executable`, thư mục gốc là
`tempfile.TemporaryDirectory` và nguồn skill cũng nằm trong thư mục tạm đó
(mặc định `<root>/.agents/skills`), nên không bao giờ đụng `.agents/skills` thật.

Run: python -m unittest discover -s tests -p "test_link_skills.py" -v
"""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "link-skills.py"

# Tên skill của fixture: cố định để so tập tên ở đích.
SKILLS = ("demo-alpha", "demo-beta")

CLAUDE = Path(".claude") / "skills"
QODER = Path(".qoder") / "skills"

EXIT_OK = 0
EXIT_PROBLEM = 1
TIMEOUT = 120


def make_skills(base, names=SKILLS):
    """Dựng fixture skill (mỗi skill có SKILL.md + references/) và trả về thư mục gốc."""
    base = Path(base)
    base.mkdir(parents=True, exist_ok=True)
    for name in names:
        skill = base / name
        skill.mkdir()
        (skill / "references").mkdir()
        payload = "---\nname: {}\ndescription: fixture\n---\n".format(name)
        (skill / "SKILL.md").write_bytes(payload.encode("utf-8"))
        (skill / "references" / "notes.md").write_bytes(b"noi dung tham chieu\n")
    return base


def skill_names(path):
    """Tên các thư mục skill nhìn thấy ở một đích (rỗng nếu không đọc được)."""
    try:
        return sorted(p.name for p in Path(path).iterdir() if p.is_dir())
    except OSError:
        return []


def make_link(src, dst):
    """Dựng link THẬT ở đích để dựng ca 'trỏ sai nguồn'; không dựng được thì skip rõ lý do."""
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    src = Path(src)
    if os.name == "nt":
        proc = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(dst), str(src)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=TIMEOUT,
        )
        if proc.returncode == 0:
            return
        detail = (proc.stdout or b"").decode("utf-8", errors="replace").strip()
    else:
        detail = "không phải Windows"
    try:
        os.symlink(src, dst, target_is_directory=True)
    except (OSError, NotImplementedError) as exc:
        raise unittest.SkipTest(
            "không tạo được link tạm để dựng ca sai nguồn (mklink: {}; symlink: {})".format(detail, exc)
        )


def remove_link_quiet(path):
    """Gỡ cầu nối trong thư mục tạm: chỉ os.rmdir/os.unlink, không bao giờ rmtree."""
    path = Path(path)
    try:
        os.rmdir(path)
        return
    except OSError:
        pass
    try:
        os.unlink(path)
    except OSError:
        pass


class LinkSkillsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.source = make_skills(self.root / ".agents" / "skills")
        self.claude = self.root / CLAUDE
        self.qoder = self.root / QODER
        for target in (self.claude, self.qoder):
            self.addCleanup(remove_link_quiet, target)

    # ------------------------------------------------------------------ #
    # Tiện ích
    # ------------------------------------------------------------------ #

    def run_script(self, *args, source=None):
        cmd = [sys.executable, str(SCRIPT), "--root", str(self.root)]
        if source is not None:
            cmd += ["--source", str(source)]
        cmd += [str(a) for a in args]
        return subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=TIMEOUT,
        )

    def describe(self, proc):
        return "rc={}\nstdout:\n{}\nstderr:\n{}".format(proc.returncode, proc.stdout, proc.stderr)

    def assertExit(self, expected, proc):
        self.assertEqual(expected, proc.returncode, self.describe(proc))

    # ------------------------------------------------------------------ #
    # 1. Tạo cầu nối đủ hai đích rồi --check xanh
    # ------------------------------------------------------------------ #

    def test_create_builds_both_bridges_then_check_passes(self):
        self.assertExit(EXIT_OK, self.run_script())

        for target in (self.claude, self.qoder):
            self.assertTrue(target.is_dir(), "thiếu cầu nối: {}".format(target))
            self.assertEqual(sorted(SKILLS), skill_names(target))

        # Đọc xuyên cầu nối phải thấy nội dung skill.
        for name in SKILLS:
            self.assertTrue((self.claude / name / "SKILL.md").is_file())
            self.assertTrue((self.qoder / name / "references" / "notes.md").is_file())

        self.assertExit(EXIT_OK, self.run_script("--check"))

    # ------------------------------------------------------------------ #
    # 2. Idempotent: chạy lại không lỗi, không tạo link lồng
    # ------------------------------------------------------------------ #

    def test_second_run_is_idempotent(self):
        self.assertExit(EXIT_OK, self.run_script())
        before_claude = skill_names(self.claude)
        before_qoder = skill_names(self.qoder)

        self.assertExit(EXIT_OK, self.run_script())

        self.assertEqual(before_claude, skill_names(self.claude))
        self.assertEqual(before_qoder, skill_names(self.qoder))
        for target in (self.claude, self.qoder):
            # Link lồng sẽ nằm ngay trong đích: <đích>/.claude/skills, <đích>/skills ...
            self.assertFalse((target / ".claude").exists(), "sinh link lồng trong {}".format(target))
            self.assertFalse((target / ".qoder").exists(), "sinh link lồng trong {}".format(target))
            self.assertFalse((target / "skills").exists(), "sinh link lồng trong {}".format(target))

        self.assertExit(EXIT_OK, self.run_script("--check"))

    # ------------------------------------------------------------------ #
    # 3. Thiếu đích (chưa tạo) → --check rc 1, chỉ đọc
    # ------------------------------------------------------------------ #

    def test_check_reports_missing_targets(self):
        self.assertExit(EXIT_PROBLEM, self.run_script("--check"))
        self.assertFalse(os.path.exists(self.claude), "--check không được tạo đích")
        self.assertFalse(os.path.exists(self.qoder), "--check không được tạo đích")

    # ------------------------------------------------------------------ #
    # 4. Chế độ copy: sửa một file trong đích → --check rc 1
    # ------------------------------------------------------------------ #

    def test_copy_mode_detects_content_drift(self):
        for target in (self.claude, self.qoder):
            shutil.copytree(self.source, target)

        # Bản copy khớp nội dung là chế độ hợp lệ: chỉ cảnh báo, vẫn rc 0.
        self.assertExit(EXIT_OK, self.run_script("--check"))

        edited = self.claude / SKILLS[0] / "SKILL.md"
        edited.write_bytes(edited.read_bytes() + b"\nsua tay trong ban copy\n")

        self.assertExit(EXIT_PROBLEM, self.run_script("--check"))
        self.assertTrue(edited.is_file(), "--check không được xóa/sửa bản copy")

    # ------------------------------------------------------------------ #
    # 5. Thư mục thật ở đích → rc 1, không xóa, không ghi đè
    # ------------------------------------------------------------------ #

    def test_real_directory_is_never_overwritten(self):
        self.claude.mkdir(parents=True)
        keep = self.claude / "keep.txt"
        keep.write_bytes(b"noi dung cu khong duoc mat\n")

        self.assertExit(EXIT_PROBLEM, self.run_script())

        self.assertTrue(self.claude.is_dir(), "thư mục thật bị đổi")
        self.assertEqual(["keep.txt"], sorted(p.name for p in self.claude.iterdir()))
        self.assertEqual(b"noi dung cu khong duoc mat\n", keep.read_bytes())

    # ------------------------------------------------------------------ #
    # 6. Link trỏ sai nguồn → lệnh tạo rc 1, giữ nguyên link cũ
    # ------------------------------------------------------------------ #

    def test_link_to_wrong_source_is_refused(self):
        other = make_skills(self.root / "other-skills", names=("demo-other",))
        make_link(other, self.claude)
        self.assertTrue((self.claude / "demo-other").is_dir(), "fixture link sai nguồn không dựng được")

        self.assertExit(EXIT_PROBLEM, self.run_script())

        # Không ghi đè: đích vẫn trỏ nguồn cũ.
        self.assertTrue((self.claude / "demo-other").is_dir())
        for name in SKILLS:
            self.assertFalse((self.claude / name).exists(), "đã ghi đè link sai nguồn")

        self.assertExit(EXIT_PROBLEM, self.run_script("--check"))


if __name__ == "__main__":
    unittest.main()
