---
name: careful
description: Safety guardrails for destructive commands. Warns and halts before rm -rf, DROP TABLE, force push, hard reset, and dangerous system alterations.
triggers:
  - be careful
  - safety mode
  - warn before destructive
  - check destructive commands
---

# /careful — Destructive Command Guardrails

> [!NOTE]
> **Bản chất thực thi**: Kỹ năng này đóng vai trò là cẩm nang checklist an toàn kết hợp với danh sách chặn lệnh cứng (`danger_deny`) trong `.kilo` và `.claude/settings.json`. Hệ thống không cài đặt hook can thiệp ngầm vào terminal của người dùng.

Use this skill when performing sensitive refactoring, touching live data, or running batch system commands to prevent irreversible data loss.

## 1. Protected Destructive Patterns
Every command proposing any of the following patterns MUST trigger an explicit human confirmation gate:

| Danger Pattern | Example | Concrete Risk |
|---|---|---|
| `rm -rf` / `rmdir /s` / `del /s` | `rm -rf /var/data` | Recursive file deletion |
| `DROP TABLE` / `DROP DATABASE` | `DROP TABLE users;` | Irreversible database loss |
| `TRUNCATE` | `TRUNCATE orders;` | Bulk record wipeout |
| `git push --force` / `-f` | `git push -f origin main` | Remote history overwrite |
| `git reset --hard` | `git reset --hard HEAD~3` | Loss of uncommitted work |
| `git checkout .` / `git restore .` | `git checkout .` | Discarding uncommitted edits |
| `docker system prune` / `rm -f` | `docker system prune -a` | Bulk container/image purge |

## 2. Cache Cleanup Policy & Gate Alignment
> [!IMPORTANT]
> To prevent catastrophic file loss, **all recursive deletion commands** (`rm -rf *`, `rmdir /s`, `del /q /s`) are strictly blocked by repository deny gates (`danger_deny` in `.claude/settings.json` and Kilo agent roles).
> 
> When temporary build/cache artifacts (`node_modules`, `.next`, `dist`, `__pycache__`, `.cache`, `build`, `.turbo`, `coverage`) need cleanup:
> 1. Use dedicated project clean scripts (e.g. `npm run clean`, language-specific build tools).
> 2. Always ask the human operator to confirm before removing build or cache directories.
> 3. Never attempt raw shell wildcards `rm -rf *` or unconstrained recursive deletions.

## 3. Human Confirmation Gate
When a destructive pattern is required:
1. STOP immediately before proposing the command.
2. Clearly state the exact destructive command and the irreversible consequence.
3. Require explicit typed user confirmation before proceeding. Never auto-approve.
