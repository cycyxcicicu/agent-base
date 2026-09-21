# Hệ Thống Ví Dụ Thực Chiến (Executable Working Examples)

Thư mục này chứa toàn bộ các bộ ví dụ thực chiến, có thể chạy và kiểm thử trực tiếp trên terminal, được chắt lọc và học hỏi từ 18 repositories tinh hoa:

```
examples/
├── ui-ux-design/              # [ui-ux-pro-max-skill] Tokens 3 tầng, SaaS landing, Healthcare dashboard
│   ├── tokens.json            # Design token schema 3 tầng (Primitive, Semantic, Component)
│   ├── tokens.css             # CSS Variables tự động sinh bởi generate-tokens.cjs
│   ├── saas-landing.html      # Landing Page SaaS hoàn chỉnh (Dark mode, glow badges)
│   ├── healthcare-dashboard.html # Dashboard Y tế điện tử (Vitals, telemetry charts)
│   └── README.md
│
├── tracer-bullet-tickets/     # [pocock-skills] Phân rã lát cắt dọc & Expand-Contract wide refactor
│   ├── 01-auth-session-cookie.md
│   ├── 02-auth-protected-dashboard.md
│   ├── 03-auth-rbac-admin-panel.md
│   ├── wide-refactor-expand-contract.md # Kỹ thuật Expand-Contract cho refactor lớn
│   ├── validate-tickets.js    # Kiểm tra DAG, chu trình phụ thuộc và tính toán Frontier
│   └── README.md
│
├── systematic-debugging/      # [pocock-skills] Quy trình gỡ lỗi 5 pha (Feedback Loop -> Fix)
│   ├── rate_limiter.py        # Token Bucket Rate Limiter (bản lỗi & bản đã sửa)
│   ├── test_repro.py          # Feedback loop chặt chẽ (Pha 1 ĐỎ ➔ Pha 5 XANH)
│   └── README.md
│
├── llm-eval-redteam/          # [promptfoo] Đánh giá an toàn & Red-Teaming cho Coding Agent
│   ├── promptfooconfig.yaml   # Cấu hình Promptfoo chính thức (Plugins, Rubric, Canary)
│   ├── eval-runner.js         # Bộ chạy test bảo mật (Canary leak, Human commit gate, Shell guard)
│   └── README.md
│
└── plan-reviews/              # [gstack] Phản biện kế hoạch & Cổng duyệt chất lượng
    ├── ceo-eng-rubric.md      # Bộ câu hỏi thẩm vấn CEO & Kỹ sư trưởng
    ├── review_gate.py         # Kiểm định tự động chất lượng Task Card & Implementation Plan
    └── README.md
```

## Bảng Lệnh Thực Thi Kiểm Thử Nhanh (One-Liner Execution Suite)

| Bộ ví dụ | Lệnh thực thi trực tiếp trên Terminal | Kết quả mong đợi |
|---|---|---|
| **UI/UX Tokens** | `node .agents/skills/ui-ux-pro-max/scripts/generate-tokens.cjs --config examples/ui-ux-design/tokens.json -o examples/ui-ux-design/tokens.css` | Sinh file `tokens.css` chuẩn W3C DTCG |
| **Token Linter** | `node .agents/skills/ui-ux-pro-max/scripts/validate-tokens.cjs -d examples/ui-ux-design` | Quét 0 vi phạm hardcoded tokens |
| **Ticket DAG** | `node examples/tracer-bullet-tickets/validate-tickets.js examples/tracer-bullet-tickets` | Tính toán Frontier, 0 chu trình lỗi |
| **Debug RED** | `python examples/systematic-debugging/test_repro.py --mode buggy` | Tái hiện lỗi chuẩn xác (Tín hiệu ĐỎ, Exit 1) |
| **Debug GREEN** | `python examples/systematic-debugging/test_repro.py --mode fixed` | Xác nhận dập tắt lỗi 100% (Tín hiệu XANH, Exit 0) |
| **Red-Team Guard** | `node examples/llm-eval-redteam/eval-runner.js` | 4/4 rào chắn bảo vệ Agent vượt qua (Exit 0) |
| **Plan Gate** | `python examples/plan-reviews/review_gate.py tasks/T-01.md` | Điểm chất lượng kế hoạch 100/100 (Exit 0) |
