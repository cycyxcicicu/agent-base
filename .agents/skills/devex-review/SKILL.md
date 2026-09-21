---
name: devex-review
description: Developer experience audit. Tests onboarding ergonomics, times time-to-hello-world (TTHW), evaluates error messages, and tests CLI clarity.
triggers:
  - dx audit
  - devex review
  - test developer experience
  - developer experience audit
---

# /devex-review — Developer Experience (DX) Audit

Use this skill after building libraries, CLIs, APIs, or developer-facing modules to measure and optimize developer ergonomics.

## 1. Key Ergonomic Metrics
1. **Time to Hello World (TTHW)**: How many minutes does it take a new developer to clone, install, configure, and run a working example? (Target: $\le 3$ minutes).
2. **Error Message Clarity**:
   - Does an error message tell the developer what went wrong?
   - Does it explain WHY it happened?
   - Does it provide an actionable command or fix to resolve it?
3. **Configuration Friction**: Are there required `.env` variables that could have sensible defaults?
4. **CLI Helpfulness**: Are `--help` flags complete, clear, and accompanied by concrete usage examples?

## 2. Audit Rubrics
- **Zero Ambiguity**: No undocumented magic strings or silent failures.
- **Fail Fast**: Catch bad configurations at startup, not 10 minutes into execution.
- **Self-Healing Diagnostics**: Provide health scripts (e.g. `python scripts/doctor.py`) that guide the user step-by-step.
