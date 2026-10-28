> Task: E2 · Epic: E2 · Vai: lead · Kế hoạch commit cho epic E2 (T-12..T-29). **Người dùng chạy**, agent không chạy. Danh sách file lấy từ mốc thời gian sửa file và các card (git bị chặn lúc soạn), nên **kiểm lại bằng `git status -s` và `git diff --cached --stat` sau mỗi `git add`**.

## Chế độ "chỉ commit phần lõi" (khuyến nghị nếu không muốn đưa hồ sơ làm việc)

Phần **lõi** = công cụ và quy tắc dùng lại được. Phần **hồ sơ làm việc** = card, ghi chú bàn giao, prompt, báo cáo phân tích; có thể giữ ở máy.

| Commit | Làm gì |
|---|---|
| 1 | **Làm** nhưng chỉ `tasks/EPICS.md`, `tasks/E2-tri-thuc-quy-trinh/`, `docs/approvals/E2-batch-approval.md` (xem lý do dưới); bỏ `tasks/BOARD.md` nếu muốn |
| 2, 4, 5, 6, 7, 8, 9 | **Làm hết** |
| 3 | **Làm một phần**: `PROJECT.md`, `docs/CODEMAP.md`, `docs/design/feature-map.md`, `docs/runbooks/verification-cli.md`, `docs/requirements/`. **Bỏ**: `docs/analysis/`, `docs/research/`, `docs/proposals/`; `docs/spec/` và `docs/adr/` tùy bạn |
| 10 | **Bỏ** (ghi chú bàn giao, `docs/notes/INDEX.md`, `docs/prompts/`) |

**Vì sao vẫn cần vài file hồ sơ nếu chỉ commit lõi** (đã kiểm bằng grep):
- `.github/workflows/check.yml` (commit 9) có bước `task-claim-check.py --card tasks/E2-tri-thuc-quy-trinh/T-12.md` và bước `rtm.py --check`. Không có card T-12 hay thư mục `docs/requirements/` thì hai bước này có thể làm CI đỏ. Chưa chạy thử trường hợp đó.
- `PROJECT.md` dòng 48 trỏ tới `docs/approvals/E2-batch-approval.md`.
- `agents/protocols/spec-writing.md` trỏ tới `docs/requirements/glossary.md`.

Muốn **không** commit card và requirements thì phải sửa `check.yml` bỏ hai bước đó, mà `check.yml` thuộc phiếu RK-3 nên sửa xong phải duyệt lại phiếu.

## Trước khi commit

1. Working tree còn rất nhiều thay đổi **có từ trước E2** (T-03..T-07 và các file M khác). **Không đưa chúng vào.** Không dùng `git add -A` hay `git add .`.
2. `main` là nhánh dùng chung, hook chặn commit thẳng. Tạo nhánh trước (thay thay đổi chưa commit theo sang nhánh mới):

```bash
git switch -c feature/12-e2-knowledge-process
```

3. Chạy kiểm một lần cho cả cụm:

```bash
python -m unittest discover -s tests -q
```

```bash
python scripts/sync-adapters.py --check
```

## Không commit (bỏ ra ngoài)

- `.agents/teamwork/ORIGINAL_REQUEST.md`: file do công cụ của Gemini tự tạo, ngoài mọi card.
- `build/`: thư mục sinh, đã ignore.
- Mọi file đã sửa từ trước E2 (T-03..T-07...).

## Commit 1: epic và 18 card

```bash
git add tasks/EPICS.md tasks/E2-tri-thuc-quy-trinh/ tasks/E1-nen-tang/T-08.md tasks/E1-nen-tang/T-09.md tasks/E1-nen-tang/T-10.md tasks/E1-nen-tang/T-11.md tasks/BOARD.md docs/approvals/E2-batch-approval.md
```

```bash
git commit -m "docs(tasks): epic E2 va 18 card T-12..T-29"
```

## Commit 2: protocol mới và sửa protocol

```bash
git add agents/protocols/approval.md agents/protocols/task-loop.md agents/protocols/test-cases.md agents/protocols/delegation-prompt.md agents/protocols/spec-writing.md agents/protocols/source-precedence.md agents/protocols/bug-repro.md agents/protocols/handoff-note.md agents/protocols/definition-of-done.md agents/protocols/task-card.md agents/protocols/commit-plan.md agents/protocols/git-rules.md
```

```bash
git commit -m "docs(protocols): duyet bang file, vong 13 buoc, test case, giao viec"
```

## Commit 3: tài liệu dự án

```bash
git add PROJECT.md docs/CODEMAP.md docs/design/feature-map.md docs/runbooks/verification-cli.md docs/requirements/ docs/spec/T-11-knowledge-verification-eval.md docs/adr/ADR-13-file-approval.md docs/adr/ADR-19-t11-rescope.md docs/proposals/roles-and-rules-2026-10-28.md docs/analysis/ docs/research/2026-10-27-lauren-tan-primary-sources.md
```

```bash
git commit -m "docs(project): PROJECT, CODEMAP, yeu cau pilot, ADR, de xuat vai tro"
```

## Commit 4: tri thức (catalog, context, seed)

```bash
git add agent_core/knowledge/ schemas/knowledge.schema.json scripts/knowledge.py tests/test_knowledge_catalog.py tests/test_knowledge_context.py tests/test_knowledge_seed.py agents/knowledge/knowledge-manifest.json examples/knowledge/
```

```bash
git commit -m "feat(knowledge): catalog, validator, context CLI, seed"
```

## Commit 5: tìm card chung

```bash
git add agent_core/workflow/task_discovery.py agent_core/workflow/tracer_bullet.py agent_core/cli.py scripts/task-board.py scripts/card-audit.py tests/test_task_discovery.py tests/test_frontier_discovery.py tests/test_task_board_discovery.py tests/test_audit_discovery.py
```

```bash
git commit -m "refactor(workflow): task discovery chung cho CLI, board, audit"
```

## Commit 6: claim check và RTM

```bash
git add agent_core/workflow/claim_check.py agent_core/workflow/rtm.py scripts/task-claim-check.py scripts/rtm.py tests/test_claim_check.py tests/test_rtm.py
```

```bash
git commit -m "feat(workflow): claim check co van va RTM sinh tu card"
```

## Commit 7: kiểm chứng và tái hiện lỗi

```bash
git add agent_core/verification/ schemas/proof.schema.json scripts/proof-check.py scripts/verify.py tests/test_proof.py tests/test_verify_bootstrap.py tests/test_verify_upgrade.py tests/test_verify_repro.py
```

```bash
git commit -m "feat(verify): proof, bootstrap, upgrade va repro tren fixture"
```

## Commit 8: eval có bằng chứng (gồm bản sửa lỗi dấu {})

`scripts/skill-eval.py` chứa cả bản sửa `{}` lẫn cờ `--evidence-mode`, nên đi chung một commit.

```bash
git add agent_core/eval/skill_eval.py scripts/skill-eval.py tests/test_skill_eval.py tests/test_skill_eval_evidence.py tests/test_skill_eval_cli_evidence.py
```

```bash
git commit -m "feat(eval): eval co bang chung va sua dau ngoac trong lenh"
```

## Commit 9: phân phối và CI (có phiếu RK-3)

**Điều kiện:** RK-3 đã duyệt lại ngày 2026-10-28 (`Status: APPROVED`, gồm cả bước claim check có điều kiện trong `check.yml`). Nếu trước khi commit có commit mới chạm các file này hoặc HEAD đổi khỏi `f12b1a23169da79ec8490b64d51a90c685b8f76f` thì phiếu `EXPIRED` và phải duyệt lại.

Commit này sửa file dùng chung, **bắt buộc** có dòng `Risk-Approved: RK-3` (RK-3 đã APPROVED).

```bash
git add agents/manifest.txt .github/workflows/check.yml scripts/agent-base-diff.py tests/test_t11_distribution.py tests/test_t11_upgrade_compatibility.py docs/risk/RK-3.md
```

```bash
git commit -m "ci(distribution): manifest va buoc kiem moi" -m "Risk-Approved: RK-3"
```

## Commit 10: ghi chú bàn giao

```bash
git add docs/notes/inbox/ docs/notes/INDEX.md docs/prompts/
```

```bash
git commit -m "docs(notes): ghi chu ban giao va prompt E2"
```

## Sau khi commit

- `git status -s` còn file nào của E2 chưa vào commit nào thì xem lại; file khác E2 thuộc thay đổi cũ.
- Điền "Mã merge commit" vào card khi merge, và đổi `status` các card sang `done` chỉ khi bạn nghiệm thu.
- `notes-index --check` vẫn báo lỗi `RK-2-lead.md` thiếu summary. Lỗi có sẵn, ngoài E2.
