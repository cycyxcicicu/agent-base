#!/usr/bin/env python3
"""tests/test_task_checkpoint.py

Unit test cho công cụ scripts/task-checkpoint.py (Git Checkpoint & Auto-Rollback).
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location("task_checkpoint", str(ROOT / "scripts" / "task-checkpoint.py"))
task_checkpoint = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(task_checkpoint)


class TestTaskCheckpoint(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.repo = Path(self.temp_dir)
        # Khởi tạo git repo giả lập
        subprocess.run(["git", "init"], cwd=self.repo, capture_output=True, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo, check=True)

        # Tạo initial commit
        f = self.repo / "main.py"
        f.write_text("print('version 1')\n", encoding="utf-8")
        subprocess.run(["git", "add", "main.py"], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-m", "init commit"], cwd=self.repo, check=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_and_list_checkpoint(self):
        meta = task_checkpoint.create_checkpoint(
            task="T-99.1", desc="Initial clean state", root=self.repo
        )
        self.assertEqual(meta["task"], "T-99.1")
        self.assertEqual(meta["desc"], "Initial clean state")
        self.assertTrue(len(meta["head_sha"]) >= 7)

        # Kiểm tra danh sách checkpoint
        cps = task_checkpoint.list_checkpoints(root=self.repo, task="T-99.1")
        self.assertEqual(len(cps), 1)
        self.assertEqual(cps[0]["task"], "T-99.1")

    def test_rollback_discards_bad_edits_and_untracked_files(self):
        # 1. Tạo checkpoint tại version 1
        task_checkpoint.create_checkpoint(task="T-99.2", desc="Pre-edit", root=self.repo)

        # 2. Sửa code hỏng (chưa commit) và thêm 1 file rác
        main_py = self.repo / "main.py"
        main_py.write_text("print('corrupted version 2')\n", encoding="utf-8")
        trash_file = self.repo / "bad_scratch.py"
        trash_file.write_text("import broken\n", encoding="utf-8")

        self.assertIn("corrupted", main_py.read_text())
        self.assertTrue(trash_file.exists())

        # 3. Rollback
        meta = task_checkpoint.rollback_checkpoint(task="T-99.2", root=self.repo, clean_untracked=True)

        # 4. Kiểm tra code đã được phục hồi về version 1 và file rác bị dọn sạch
        self.assertEqual(main_py.read_text(), "print('version 1')\n")
        self.assertFalse(trash_file.exists())

    def test_drop_checkpoint(self):
        task_checkpoint.create_checkpoint(task="T-99.3", root=self.repo)
        self.assertEqual(len(task_checkpoint.list_checkpoints(root=self.repo)), 1)

        task_checkpoint.drop_checkpoints(task="T-99.3", root=self.repo)
        self.assertEqual(len(task_checkpoint.list_checkpoints(root=self.repo)), 0)


if __name__ == "__main__":
    unittest.main()
