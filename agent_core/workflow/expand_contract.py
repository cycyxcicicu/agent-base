"""
Expand-Contract Migration Tracker.
Học hỏi từ: pocock-skills (Zero-Downtime Wide Refactors & Database Migrations).
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


class MigrationPhase(str, Enum):
    EXPAND = "EXPAND"      # Tạo song song cấu trúc mới, giữ nguyên cấu trúc cũ
    MIGRATE = "MIGRATE"    # Chuyển đổi dần các callers sang cấu trúc mới
    CONTRACT = "CONTRACT"  # Xóa bỏ hoàn toàn cấu trúc cũ sau khi không còn ai dùng


@dataclass
class MigrationTask:
    name: str
    phase: MigrationPhase
    old_target: str
    new_target: str
    callers_remaining: int
    is_safe_to_contract: bool = False


class MigrationTracker:
    """Quản lý tiến trình tái cấu trúc diện rộng không làm đỏ CI."""

    def __init__(self):
        self.tasks: Dict[str, MigrationTask] = {}

    def register_migration(self, name: str, old_target: str, new_target: str, initial_callers: int) -> MigrationTask:
        task = MigrationTask(
            name=name,
            phase=MigrationPhase.EXPAND,
            old_target=old_target,
            new_target=new_target,
            callers_remaining=initial_callers,
            is_safe_to_contract=False
        )
        self.tasks[name] = task
        return task

    def advance_phase(self, name: str, remaining_callers: int) -> MigrationTask:
        task = self.tasks[name]
        task.callers_remaining = remaining_callers

        if remaining_callers > 0:
            task.phase = MigrationPhase.MIGRATE
            task.is_safe_to_contract = False
        else:
            task.phase = MigrationPhase.CONTRACT
            task.is_safe_to_contract = True

        return task
