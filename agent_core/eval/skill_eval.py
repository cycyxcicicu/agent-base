"""
Eval cho Skill (kiểm thử đơn vị cho một file SKILL.md).

Quy trình (agents/protocols/skill-eval.md):
  1. Rubric: bảng tiêu chí có trọng số, chấm 0..10 cho mỗi tiêu chí.
  2. Môi trường cách ly: mỗi lần chạy dùng một thư mục tạm tên ngẫu nhiên (agent không nên đoán ra mình đang bị eval).
  3. Ma trận model: cùng một bộ tác vụ chạy trên nhiều model để skill không phụ thuộc một model.
  4. Trọng tài: model KHÁC họ với mọi model được thử chấm điểm theo rubric.
  5. Leo núi (hill climbing): sửa skill, chạy lại, chỉ giữ bản tốt hơn, dừng khi đạt mục tiêu hoặc hết vòng.

Module không gọi model nào. `runner`, `judge` và `improver` là hàm do người gọi truyền vào (ví dụ bọc một lệnh CLI,
xem scripts/skill-eval.py), nên kiểm thử được bằng hàm giả và không tốn token.
"""

import json
import math
import re
import secrets
import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from statistics import mean
from typing import Any, Callable, Dict, List, Optional, Union

# runner(model, skill_text, task_prompt, sandbox_dir) -> đầu ra của agent (văn bản)
Runner = Callable[[str, str, str, Path], str]
# judge(judge_model, rubric, task, output) -> {mã_tiêu_chí: điểm 0..10}
Judge = Callable[[str, "Rubric", "EvalTask", str], Dict[str, float]]
# improver(skill_text, report_markdown) -> nội dung skill mới
Improver = Callable[[str, str], str]


@dataclass
class RubricItem:
    id: str
    description: str
    weight: float = 1.0


@dataclass
class Rubric:
    skill: str
    items: List[RubricItem]

    def validate(self):
        ids = [i.id for i in self.items]
        if not ids:
            raise ValueError("rubric không có tiêu chí nào")
        if len(set(ids)) != len(ids):
            raise ValueError("mã tiêu chí bị trùng")
        if any(i.weight <= 0 for i in self.items):
            raise ValueError("trọng số phải > 0")

    @classmethod
    def from_json(cls, text: str) -> "Rubric":
        data = json.loads(text)
        rub = cls(skill=data["skill"], items=[RubricItem(i["id"], i["description"], float(i.get("weight", 1.0))) for i in data["items"]])
        rub.validate()
        return rub


@dataclass
class EvalTask:
    name: str
    prompt: str


@dataclass
class CellResult:
    model: str
    task: str
    score: float
    item_scores: Dict[str, float]
    output_preview: str
    critical_fail: bool = False
    critical_reason: str = ""
    is_inconclusive: bool = False
    inconclusive_reason: str = ""


@dataclass
class MatrixResult:
    cells: List[CellResult] = field(default_factory=list)
    critical_fails: int = 0
    inconclusive_count: int = 0

    def per_model(self) -> Dict[str, float]:
        out: Dict[str, List[float]] = {}
        for c in self.cells:
            out.setdefault(c.model, []).append(c.score)
        return {m: round(mean(v), 2) for m, v in out.items()}

    def min_model_score(self) -> float:
        pm = self.per_model()
        return min(pm.values()) if pm else 0.0

    def spread(self) -> float:
        """Chênh lệch giữa model cao điểm nhất và thấp điểm nhất: lớn nghĩa là skill không ổn định giữa các model."""
        pm = self.per_model()
        return round(max(pm.values()) - min(pm.values()), 2) if pm else 0.0

    def weakest_model(self) -> str:
        pm = self.per_model()
        return min(pm, key=pm.get) if pm else ""

    def passed(self, target: float) -> bool:
        return bool(self.cells) and self.min_model_score() >= target

    def passed_v2(self, target: float, case_min_score: float = 0.0) -> bool:
        if not self.cells:
            return False
        if self.critical_fails > 0 or self.inconclusive_count > 0:
            return False
        if any(math.isnan(c.score) for c in self.cells):
            return False
        if any(c.critical_fail or c.is_inconclusive for c in self.cells):
            return False
        if any(c.score < case_min_score for c in self.cells):
            return False
        return self.min_model_score() >= target


@dataclass
class SanitizedBundle:
    blind_id: str
    output: str
    artifacts: Dict[str, Path] = field(default_factory=dict)
    trace: List[dict] = field(default_factory=list)


@dataclass
class EvidenceCollector:
    allowlist: Optional[List[str]] = None

    def collect(self, sandbox: Path, dest_dir: Path) -> Dict[str, Path]:
        dest_dir.mkdir(parents=True, exist_ok=True)
        collected: Dict[str, Path] = {}
        if not sandbox.exists():
            return collected
        for item in sandbox.rglob("*"):
            if item.is_file():
                rel = item.relative_to(sandbox).as_posix()
                if self.allowlist is not None and rel not in self.allowlist and item.name not in self.allowlist:
                    continue
                target = dest_dir / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target)
                collected[rel] = target
        return collected


@dataclass
class EvidenceRequest:
    skill_text: str
    tasks: List[EvalTask]
    models: List[str]
    judge_model: str
    rubric: Rubric
    sandbox_base: Optional[Path] = None
    allow_same_family: bool = False
    evidence_root: Optional[Path] = None
    case_min_score: float = 0.0
    target: float = 10.0
    required_criteria: Optional[List[str]] = None
    required_traces: Optional[List[str]] = None
    holdout_tasks: Optional[List[EvalTask]] = None


def extract_json(text: str):
    """Lấy khối JSON đầu tiên trong đầu ra của model (model hay bọc trong rào ``` hoặc thêm lời dẫn)."""
    start, end = text.find('{'), text.rfind('}')
    if start < 0 or end <= start:
        raise ValueError("đầu ra không có JSON")
    return json.loads(text[start:end + 1])


def draft_rubric(skill_name: str, raw_output: str) -> "Rubric":
    """Dựng Rubric từ đầu ra của agent điều phối. Đặt tên skill đúng theo thư mục (không tin tên model tự ghi) và kiểm hợp lệ."""
    data = extract_json(raw_output)
    items = [RubricItem(str(i["id"]).strip(), str(i["description"]).strip(), float(i.get("weight", 1.0))) for i in data["items"]]
    rubric = Rubric(skill=skill_name, items=items)
    rubric.validate()
    if not 3 <= len(items) <= 8:
        raise ValueError(f"rubric nên có 3 đến 8 tiêu chí, nhận được {len(items)}")
    return rubric


def model_family(model: str) -> str:
    """Họ model, lấy từ phần đầu tên: 'anthropic/claude-x' -> 'claude', 'gpt-5' -> 'gpt', 'gemini-2' -> 'gemini'."""
    name = model.lower().split('/')[-1]
    return re.split(r'[-_:.\s]', name, maxsplit=1)[0]


def check_judge_independent(models: List[str], judge_model: str, allow_same_family: bool = False):
    if judge_model in models:
        raise ValueError(f"trọng tài '{judge_model}' trùng với model đang được thử")
    if not allow_same_family:
        fams = {model_family(m) for m in models}
        if model_family(judge_model) in fams:
            raise ValueError(f"trọng tài '{judge_model}' cùng họ với model được thử ({sorted(fams)}); "
                             "dùng model họ khác để tránh thiên vị, hoặc đặt allow_same_family=True và ghi rõ trong báo cáo")


def make_sandbox(base: Optional[Path] = None) -> Path:
    """Thư mục tạm tên ngẫu nhiên, không chứa chữ 'eval' hay 'test'."""
    root = Path(base) if base else Path(tempfile.gettempdir())
    root.mkdir(parents=True, exist_ok=True)
    path = root / secrets.token_hex(8)
    path.mkdir()
    return path


def weighted_score(rubric: Rubric, item_scores: Dict[str, float]) -> float:
    total_w = sum(i.weight for i in rubric.items)
    acc = 0.0
    for item in rubric.items:
        s = item_scores.get(item.id)
        if s is None:
            raise ValueError(f"trọng tài không chấm tiêu chí '{item.id}'")
        acc += max(0.0, min(10.0, float(s))) * item.weight
    return round(acc / total_w, 2)


def run_matrix(skill_text: str, tasks: List[EvalTask], models: List[str], judge_model: str, rubric: Rubric,
               runner: Runner, judge: Judge, sandbox_base: Optional[Path] = None,
               allow_same_family: bool = False) -> MatrixResult:
    rubric.validate()
    check_judge_independent(models, judge_model, allow_same_family)
    result = MatrixResult()
    for model in models:
        for task in tasks:
            sandbox = make_sandbox(sandbox_base)
            try:
                output = runner(model, skill_text, task.prompt, sandbox)
            finally:
                shutil.rmtree(sandbox, ignore_errors=True)
            scores = judge(judge_model, rubric, task, output)
            result.cells.append(CellResult(model, task.name, weighted_score(rubric, scores), scores,
                                           output[:160] + ('...' if len(output) > 160 else '')))
    return result


def render_report(result: MatrixResult, rubric: Rubric, target: float, judge_model: str, round_no: int = 1) -> str:
    lines = [f"# Eval skill `{rubric.skill}` (vòng {round_no})", "",
             f"Trọng tài: `{judge_model}`. Mục tiêu: mọi model đạt trung bình >= {target}.", "",
             "| Model | Điểm TB |", "|---|---|"]
    for m, s in result.per_model().items():
        lines.append(f"| {m} | {s} {'✅' if s >= target else '❌'} |")
    if len(result.per_model()) > 1:
        lines += ["", f"Model yếu nhất: `{result.weakest_model()}` ({result.min_model_score()}). "
                      f"Chênh lệch giữa các model: {result.spread()}"
                  + (" ⚠️ skill chưa ổn định giữa các model (chênh > 1.5), xem lại chỗ chỉ dẫn mơ hồ hoặc quá hợp một model." if result.spread() > 1.5 else ".")]
    lines += ["", "| Model | Tác vụ | Điểm | " + " | ".join(i.id for i in rubric.items) + " |",
              "|---|---|---|" + "---|" * len(rubric.items)]
    for c in result.cells:
        lines.append(f"| {c.model} | {c.task} | {c.score} | " + " | ".join(str(c.item_scores.get(i.id, '')) for i in rubric.items) + " |")
    return "\n".join(lines) + "\n"


@dataclass
class ClimbOutcome:
    best_text: str
    best_score: float
    rounds: int
    reached_target: bool
    history: List[float]


def hill_climb(skill_text: str, evaluate: Callable[[str], MatrixResult], improver: Improver, rubric: Rubric,
               target: float = 10.0, max_rounds: int = 5, patience: int = 2, judge_model: str = "") -> ClimbOutcome:
    """Chấm bản hiện tại; chưa đạt thì nhờ improver sửa, chấm lại, giữ bản TỐT HƠN. Dừng khi đạt mục tiêu,
    hết `max_rounds`, hoặc `patience` vòng liền không cải thiện. Không bao giờ ghi đè file: người gọi tự quyết dùng best_text."""
    best_text = skill_text
    best = evaluate(best_text)
    best_score = best.min_model_score()
    history = [best_score]
    stale = 0
    rounds = 1
    while not best.passed(target) and rounds < max_rounds and stale < patience:
        report = render_report(best, rubric, target, judge_model, rounds)
        candidate = improver(best_text, report)
        rounds += 1
        if not candidate or candidate == best_text:
            stale += 1
            history.append(best_score)
            continue
        res = evaluate(candidate)
        score = res.min_model_score()
        history.append(score)
        if score > best_score:
            best_text, best, best_score, stale = candidate, res, score, 0
        else:
            stale += 1
    return ClimbOutcome(best_text, best_score, rounds, best.passed(target), history)


def run_matrix_with_evidence(
    request: EvidenceRequest,
    runner: Any,
    judge: Any,
    collector: Optional[EvidenceCollector] = None,
) -> MatrixResult:
    request.rubric.validate()
    check_judge_independent(request.models, request.judge_model, request.allow_same_family)

    result = MatrixResult()
    root_evidence = Path(request.evidence_root) if request.evidence_root else None
    if root_evidence:
        root_evidence.mkdir(parents=True, exist_ok=True)

    for model in request.models:
        for task in request.tasks:
            sandbox = make_sandbox(request.sandbox_base)
            blind_id = f"candidate_{secrets.token_hex(4)}"
            run_id = secrets.token_hex(6)
            run_evidence_dir = root_evidence / f"{blind_id}_{run_id}" if root_evidence else None

            raw_output = ""
            critical_fail = False
            critical_reason = ""
            collected_artifacts: Dict[str, Path] = {}

            try:
                out_val = runner(model, request.skill_text, task.prompt, sandbox)
                if isinstance(out_val, dict):
                    raw_output = str(out_val.get("output", ""))
                    escapes = out_val.get("path_escapes", [])
                    forbidden = out_val.get("forbidden_writes", [])
                    fabricated = out_val.get("fabricated_proofs", [])
                    if escapes or forbidden or fabricated:
                        critical_fail = True
                        reasons = []
                        if escapes:
                            reasons.append(f"path escapes: {escapes}")
                        if forbidden:
                            reasons.append(f"forbidden writes: {forbidden}")
                        if fabricated:
                            reasons.append(f"fabricated proofs: {fabricated}")
                        critical_reason = "; ".join(reasons)
                else:
                    raw_output = str(out_val)

                # Thu thập bằng chứng trước khi dọn dẹp sandbox
                if run_evidence_dir:
                    run_evidence_dir.mkdir(parents=True, exist_ok=True)
                    if collector:
                        collected_artifacts = collector.collect(sandbox, run_evidence_dir)
                    else:
                        collected_artifacts = EvidenceCollector().collect(sandbox, run_evidence_dir)
            finally:
                # Dọn dẹp sandbox sau khi đã thu thập
                shutil.rmtree(sandbox, ignore_errors=True)

            # Khử định danh (blind sanitization)
            sanitized_output = raw_output
            sanitized_output = re.sub(re.escape(model), blind_id, sanitized_output, flags=re.IGNORECASE)

            bundle = SanitizedBundle(
                blind_id=blind_id,
                output=sanitized_output,
                artifacts=collected_artifacts,
                trace=[],
            )

            if critical_fail:
                result.critical_fails += 1
                result.cells.append(
                    CellResult(
                        model=model,
                        task=task.name,
                        score=0.0,
                        item_scores={item.id: 0.0 for item in request.rubric.items},
                        output_preview=raw_output[:160] + ('...' if len(raw_output) > 160 else ''),
                        critical_fail=True,
                        critical_reason=critical_reason,
                    )
                )
                continue

            # Gọi judge
            scores = {}
            is_inconclusive = False
            inconclusive_reason = ""
            try:
                scores = judge(request.judge_model, request.rubric, task, bundle)
                for item in request.rubric.items:
                    sc = scores.get(item.id)
                    if sc is None or (isinstance(sc, (int, float)) and math.isnan(sc)):
                        is_inconclusive = True
                        inconclusive_reason = f"thiếu hoặc NaN tiêu chí {item.id}"
                        break
                    if isinstance(sc, (int, float)) and (sc < 0.0 or sc > 10.0):
                        is_inconclusive = True
                        inconclusive_reason = f"điểm tiêu chí {item.id} ngoài [0, 10]: {sc}"
                        break
            except Exception as ex:
                is_inconclusive = True
                inconclusive_reason = f"judge ngoại lệ: {ex}"

            if is_inconclusive:
                result.inconclusive_count += 1
                result.cells.append(
                    CellResult(
                        model=model,
                        task=task.name,
                        score=float("nan"),
                        item_scores={item.id: float("nan") for item in request.rubric.items},
                        output_preview=raw_output[:160] + ('...' if len(raw_output) > 160 else ''),
                        is_inconclusive=True,
                        inconclusive_reason=inconclusive_reason,
                    )
                )
            else:
                score_val = weighted_score(request.rubric, scores)
                result.cells.append(
                    CellResult(
                        model=model,
                        task=task.name,
                        score=score_val,
                        item_scores=scores,
                        output_preview=raw_output[:160] + ('...' if len(raw_output) > 160 else ''),
                    )
                )

    return result

