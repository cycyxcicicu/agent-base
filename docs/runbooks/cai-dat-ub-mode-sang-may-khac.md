# Runbook: Cài Đặt ub-mode & Companion Tools Sang Máy Mới

> **File:** `docs/runbooks/cai-dat-ub-mode-sang-may-khac.md`  
> **Áp dụng cho:** Môi trường phát triển mới (Mac, Linux, Windows/WSL)  

---

## 1. Danh Sách URL Git Clone

- **ub-mode:** `https://github.com/unclebob/ub-mode.git`
- **crapper:** `https://github.com/unclebob/crapper.git`
- **dryer:** `https://github.com/unclebob/dryer.git`
- **mutator:** `https://github.com/unclebob/mutator.git`
- **uml-viewer:** `https://github.com/unclebob/uml-viewer.git`

## 2. Lệnh Cài Đặt 1 Dòng (One-Liner Setup)

```bash
mkdir -p ~/Documents/skill/repos && cd ~/Documents/skill/repos && git clone https://github.com/unclebob/ub-mode.git && cd ~/Documents/skill && ln -sf repos/ub-mode ub-mode && mkdir -p ~/Documents/agent-base/.agents/skills/ub-mode && cp ~/Documents/skill/repos/ub-mode/SKILL.md ~/Documents/agent-base/.agents/skills/ub-mode/SKILL.md && cd ~/Documents/agent-base && python3 scripts/knowledge.py skill-graph sync && python3 scripts/link-skills.py && python3 scripts/sync-adapters.py
```

Sau khi chạy xong lệnh trên, toàn bộ hệ thống Antigravity, Claude, Codex, Qoder và các repo workspace (như `gdt-workspace`) sẽ tự động nhận diện `ub-mode`.
