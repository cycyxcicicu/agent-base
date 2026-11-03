#!/usr/bin/env python3
"""
scripts/skill-eval.py
Chạy Eval cho một skill: ma trận model, trọng tài khác họ, vòng leo núi tùy chọn. Chi tiết: agents/protocols/skill-eval.md

Mỗi bước gọi model được bọc bằng một LỆNH NGOÀI do bạn khai báo (CLI của công cụ bạn dùng), nên script không giữ khóa API nào
và không phụ thuộc nhà cung cấp. Lệnh được tách bằng shlex (KHÔNG chạy qua shell), dùng dấu / trong đường dẫn.

  --runner-cmd   chạy agent với skill, in đầu ra ra stdout.
                 Chỗ giữ: {model} {skill_file} {prompt_file} {sandbox}   (thư mục làm việc = sandbox tạm ngẫu nhiên)
  --judge-cmd    trọng tài chấm, in JSON {"scores": {"<mã tiêu chí>": 0..10}} ra stdout.
                 Chỗ giữ: {judge_model} {rubric_file} {task_file} {output_file}
  --improver-cmd (tùy chọn, bật leo núi) in NỘI DUNG SKILL MỚI ra stdout.
                 Chỗ giữ: {skill_file} {report_file}

Ví dụ rubric.json: {"skill": "investigate", "items": [{"id": "doc-file", "description": "Đã đọc file trước khi kết luận", "weight": 2}]}
Ví dụ tasks.json:  [{"name": "bug-null", "prompt": "Trang X trắng sau khi bấm Lưu, tìm nguyên nhân"}]

Cách dùng:
  python scripts/skill-eval.py rubric --skill .agents/skills/investigate/SKILL.md --rubric-cmd "<lệnh>" --out r.json   # agent điều phối soạn NHÁP tiêu chí, người duyệt
  python scripts/skill-eval.py plan --skill .agents/skills/investigate/SKILL.md --rubric r.json --tasks t.json --models a,b --judge c
  python scripts/skill-eval.py run  ... --runner-cmd "..." --judge-cmd "..." [--improver-cmd "..."] [--out report.md]
Script không tự ghi đè SKILL.md. Có leo núi thì bản tốt nhất ghi ra <skill>.best.md để người dùng xem diff rồi tự quyết.
"""

import argparse
import json
import os
import re
import secrets
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agent_core.eval.skill_eval import (  # noqa: E402
    EvalTask, Rubric, check_judge_independent, draft_rubric, hill_climb, render_report, run_matrix,
    EvidenceRequest, EvidenceCollector, SanitizedBundle, run_matrix_with_evidence,
)


def _absolutize(tok: str, base: Path) -> str:
    """Đường dẫn tương đối tới một file có thật (ví dụ examples/skill-eval/demo_runner.py) đổi thành tuyệt đối theo thư mục
    đang đứng khi chạy script, vì lệnh runner chạy trong thư mục tạm khác."""
    p = Path(tok)
    if not p.is_absolute() and ('/' in tok or '\\' in tok) and (base / p).exists():
        return str((base / p).resolve())
    return tok


def _fill(tok: str, values: dict) -> str:
    """Thay đúng các placeholder đã biết ({model}, {prompt_file}...). Không dùng str.format: dấu {} nằm trong
    đường dẫn (ví dụ TEMP dạng sandbox.{UUID}) sẽ bị hiểu nhầm là placeholder và gây KeyError."""
    return re.sub(r'\{(\w+)\}', lambda m: str(values[m.group(1)]) if m.group(1) in values else m.group(0), tok)


def call(template: str, values: dict, cwd=None, timeout: int = 900) -> str:
    argv = [_fill(tok, values) for tok in shlex.split(template)]
    if cwd is not None:
        base = Path.cwd()
        argv = [argv[0]] + [_absolutize(t, base) for t in argv[1:]]
    env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')  # lệnh Python con in tiếng Việt không vỡ trên Windows
    proc = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, encoding='utf-8', timeout=timeout, env=env)
    if proc.returncode != 0:
        raise RuntimeError(f"lệnh lỗi (mã {proc.returncode}): {argv[0]}\n{proc.stderr[-500:]}")
    return proc.stdout


def new_work_dir() -> Path:
    """Thư mục làm việc tạm tên ngẫu nhiên trung tính (không chứa chữ gợi ý đang bị đánh giá)."""
    d = Path(tempfile.gettempdir()) / secrets.token_hex(8)
    d.mkdir()
    return d


def load_tasks(path: Path):
    return [EvalTask(t["name"], t["prompt"]) for t in json.loads(path.read_text(encoding='utf-8'))]


def main() -> int:
    ap = argparse.ArgumentParser(description="Eval cho skill (ma trận model + trọng tài + leo núi).")
    ap.add_argument("action", choices=["rubric", "plan", "run"])
    ap.add_argument("--skill", required=True)
    ap.add_argument("--rubric", help="file rubric.json (plan, run)")
    ap.add_argument("--tasks", help="file tasks.json (plan, run)")
    ap.add_argument("--models", help="danh sách model cách nhau dấu phẩy (plan, run)")
    ap.add_argument("--judge", help="model trọng tài (plan, run)")
    ap.add_argument("--rubric-cmd", help="(lệnh rubric) lệnh để agent điều phối soạn tiêu chí, in JSON ra stdout; chỗ giữ: {skill_file}")
    ap.add_argument("--runner-cmd")
    ap.add_argument("--judge-cmd")
    ap.add_argument("--improver-cmd")
    ap.add_argument("--target", type=float, default=10.0, help="điểm trung bình tối thiểu cho MỌI model (mặc định 10)")
    ap.add_argument("--rounds", type=int, default=5)
    ap.add_argument("--allow-same-family", action="store_true")
    ap.add_argument("--evidence-mode", action="store_true", help="chế độ v2: thu thập bằng chứng trước khi xóa sandbox, chấm mù, bắt critical fail")
    ap.add_argument("--evidence-root", help="thư mục lưu trữ bằng chứng (evidence-mode)")
    ap.add_argument("--case-min-score", type=float, default=0.0, help="điểm tối thiểu cho từng case (evidence-mode)")
    ap.add_argument("--out")
    args = ap.parse_args()

    skill_path = Path(args.skill)
    skill_text = skill_path.read_text(encoding='utf-8')

    if args.action == "rubric":
        if not args.rubric_cmd or not args.out:
            print("LỖI: lệnh `rubric` cần --rubric-cmd và --out")
            return 2
        work = new_work_dir()
        sk = work / "guide.md"
        sk.write_text(skill_text, encoding='utf-8')
        # Tên skill lấy theo thư mục chứa SKILL.md, không tin tên do model tự ghi
        name = skill_path.resolve().parent.name
        rub = draft_rubric(name, call(args.rubric_cmd, {"skill_file": sk.as_posix()}))
        Path(args.out).write_text(json.dumps({"skill": rub.skill, "items": [vars(i) for i in rub.items]},
                                             ensure_ascii=False, indent=2) + "\n", encoding='utf-8')
        shutil.rmtree(work, ignore_errors=True)
        print(f"Đã ghi BẢN NHÁP rubric ({len(rub.items)} tiêu chí) vào {args.out}.")
        print("Người dùng hoặc Lead phải đọc và sửa trước khi dùng cho `plan`/`run`: tiêu chí phải đo được, không viết kiểu 'làm tốt'.")
        return 0

    missing = [n for n in ("rubric", "tasks", "models", "judge") if not getattr(args, n)]
    if missing:
        print("LỖI: thiếu " + ", ".join("--" + m for m in missing))
        return 2
    rubric = Rubric.from_json(Path(args.rubric).read_text(encoding='utf-8'))
    tasks = load_tasks(Path(args.tasks))
    models = [m.strip() for m in args.models.split(',') if m.strip()]
    try:
        check_judge_independent(models, args.judge, args.allow_same_family)
    except ValueError as e:
        print(f"LỖI: {e}")
        return 2

    if args.action == "plan":
        print(f"Skill: {skill_path} | tiêu chí: {len(rubric.items)} | tác vụ: {len(tasks)} | model: {', '.join(models)}")
        print(f"Trọng tài: {args.judge} (khác họ) | số lượt chạy mỗi vòng: {len(models) * len(tasks)} + {len(models) * len(tasks)} lượt chấm")
        print(f"Mục tiêu: mọi model >= {args.target} | tối đa {args.rounds} vòng" + (" | có leo núi" if args.improver_cmd else ""))
        return 0

    if not args.runner_cmd or not args.judge_cmd:
        print("LỖI: lệnh `run` cần --runner-cmd và --judge-cmd")
        return 2

    # Agent được thử nhìn thấy đường dẫn này trong lệnh, nên tên thư mục và file không được lộ "eval", "skill-eval", "test"
    work = new_work_dir()

    def runner(model, text, prompt, sandbox):
        sk, pr = work / "guide.md", work / "ask.txt"
        sk.write_text(text, encoding='utf-8')
        pr.write_text(prompt, encoding='utf-8')
        return call(args.runner_cmd, {"model": model, "skill_file": sk.as_posix(), "prompt_file": pr.as_posix(),
                                      "sandbox": sandbox.as_posix()}, cwd=sandbox)

    def judge(judge_model, rub, task, output_or_bundle):
        rf, tf, of = work / "rubric.json", work / "task.json", work / "output.txt"
        rf.write_text(json.dumps({"skill": rub.skill, "items": [vars(i) for i in rub.items]}, ensure_ascii=False), encoding='utf-8')
        tf.write_text(json.dumps({"name": task.name, "prompt": task.prompt}, ensure_ascii=False), encoding='utf-8')
        out_str = output_or_bundle.output if isinstance(output_or_bundle, SanitizedBundle) else str(output_or_bundle)
        of.write_text(out_str, encoding='utf-8')
        raw = call(args.judge_cmd, {"judge_model": judge_model, "rubric_file": rf.as_posix(),
                                    "task_file": tf.as_posix(), "output_file": of.as_posix()})
        return json.loads(raw)["scores"]

    def evaluate(text):
        return run_matrix(text, tasks, models, args.judge, rubric, runner, judge, allow_same_family=args.allow_same_family)

    if args.evidence_mode:
        req = EvidenceRequest(
            skill_text=skill_text,
            tasks=tasks,
            models=models,
            judge_model=args.judge,
            rubric=rubric,
            allow_same_family=args.allow_same_family,
            evidence_root=Path(args.evidence_root) if args.evidence_root else None,
            case_min_score=args.case_min_score,
            target=args.target,
        )
        collector = EvidenceCollector()
        result = run_matrix_with_evidence(req, runner, judge, collector)
        report = render_report(result, rubric, args.target, args.judge)
        passed = result.passed_v2(args.target, args.case_min_score)
        valid_scores = [c.score for c in result.cells if not (isinstance(c.score, float) and (c.score != c.score))]
        lowest_score = min(valid_scores) if valid_scores else 0.0
        report += (
            f"\n[Evidence Mode v2]\n"
            f"- Critical Fails: {result.critical_fails}\n"
            f"- Inconclusive Cases: {result.inconclusive_count}\n"
            f"- Lowest Case Score: {lowest_score:.2f}\n"
            f"- Đạt mục tiêu v2: {'có' if passed else 'chưa'}.\n"
        )
    elif args.improver_cmd:
        def improver(text, report):
            sk, rp = work / "skill_cur.md", work / "report.md"
            sk.write_text(text, encoding='utf-8')
            rp.write_text(report, encoding='utf-8')
            return call(args.improver_cmd, {"skill_file": sk.as_posix(), "report_file": rp.as_posix()})
        outcome = hill_climb(skill_text, evaluate, improver, rubric, args.target, args.rounds, judge_model=args.judge)
        best = outcome.best_text
        report = render_report(evaluate(best), rubric, args.target, args.judge, outcome.rounds)
        report += f"\nLịch sử điểm thấp nhất theo vòng: {outcome.history}. Đạt mục tiêu: {'có' if outcome.reached_target else 'chưa'}.\n"
        if best != skill_text:
            best_path = skill_path.with_suffix('.best.md')
            best_path.write_text(best, encoding='utf-8')
            report += f"Bản tốt nhất ghi ở `{best_path}`; xem diff rồi tự quyết định thay SKILL.md.\n"
    else:
        result = evaluate(skill_text)
        report = render_report(result, rubric, args.target, args.judge)
        report += f"\nĐạt mục tiêu: {'có' if result.passed(args.target) else 'chưa'}.\n"

    shutil.rmtree(work, ignore_errors=True)
    if args.out:
        Path(args.out).write_text(report, encoding='utf-8')
    print(report)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (RuntimeError, ValueError, KeyError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
        print(f"LỖI: {exc}")
        sys.exit(1)
