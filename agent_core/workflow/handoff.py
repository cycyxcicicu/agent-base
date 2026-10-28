"""
Agent Role Handoff & Swarm State Machine.
Học hỏi từ: ruflo & claude-flow (Structured Handoff Note & Role Transitions).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import time


@dataclass
class HandoffNote:
    from_role: str
    to_role: str
    task_id: str
    summary: str
    files_changed: List[str]
    proof_of_done: str
    open_questions: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)


class HandoffRouter:
    """Bộ định tuyến bàn giao nhiệm vụ giữa các vai trò trong Swarm."""

    VALID_TRANSITIONS = {
        "analyst": ["architect", "product", "ba", "researcher"],
        "product": ["architect", "ba", "designer", "writer"],
        "ba": ["architect", "dev", "product", "designer"],
        "architect": ["dev", "mobile", "dba", "security", "designer", "devops", "reviewer"],
        "designer": ["dev", "mobile", "qa", "product"],
        "dev": ["qa", "reviewer", "devops", "security", "writer"],
        "mobile": ["qa", "reviewer", "devops", "security", "writer"],
        "qa": ["dev", "mobile", "devops", "sre", "reviewer"],
        "reviewer": ["dev", "mobile", "devops", "writer", "lead"],
        "security": ["dev", "mobile", "devops", "sre", "architect", "reviewer"],
        "devops": ["sre", "dev", "mobile", "security"],
        "sre": ["devops", "dev", "security"],
        "dba": ["dev", "architect", "devops"],
        "researcher": ["analyst", "architect", "ai-eng", "product"],
        "ai-eng": ["dev", "architect", "researcher", "qa"],
        "debt-hunter": ["dev", "architect", "reviewer"],
        "writer": ["reviewer", "product", "lead"],
        "lead": [
            "analyst", "product", "ba", "architect", "designer", "dev", "mobile",
            "qa", "reviewer", "security", "devops", "sre", "dba", "researcher",
            "ai-eng", "debt-hunter", "writer"
        ]
    }

    @classmethod
    def can_transition(cls, from_role: str, to_role: str) -> bool:
        allowed = cls.VALID_TRANSITIONS.get(from_role.lower(), [])
        return to_role.lower() in allowed or from_role.lower() == "lead"

    @classmethod
    def create_note(
        cls,
        from_role: str,
        to_role: str,
        task_id: str,
        summary: str,
        files_changed: List[str],
        proof_of_done: str,
        open_questions: Optional[List[str]] = None
    ) -> HandoffNote:
        if not cls.can_transition(from_role, to_role):
            print(f"⚠️ Cảnh báo chuyển giao phi tiêu chuẩn từ '{from_role}' sang '{to_role}'")

        return HandoffNote(
            from_role=from_role,
            to_role=to_role,
            task_id=task_id,
            summary=summary,
            files_changed=files_changed,
            proof_of_done=proof_of_done,
            open_questions=open_questions or []
        )
