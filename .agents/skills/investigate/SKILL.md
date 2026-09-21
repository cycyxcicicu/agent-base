---
name: investigate
description: Systematic root cause debugging. Reproduces issues with minimal tests, isolates single variables, and traces execution paths.
triggers:
  - debug this
  - fix this bug
  - why is this broken
  - root cause analysis
  - investigate error
---

# /investigate — Systematic Root Cause Investigation

Use this skill when facing subtle, intermittent, or complex bugs that resist quick fixes. Forbids guessing or symptom masking.

## 1. Investigation Protocol (4 Phases)

### Phase 1: Minimal Deterministic Reproduction
- Create a standalone reproducing script or test case that reliably triggers the failure.
- If it cannot be reproduced deterministically, collect real-world inputs, environment flags, and stack traces.

### Phase 2: Single-Variable Isolation
- Change exactly ONE variable at a time.
- If testing whether a database query is slow, isolate network latency from query execution time.
- Use binary search (`git bisect`) if the defect was introduced by a recent commit.

### Phase 3: The 5 Whys (Root Cause Analysis)
- Ask "Why did this fail?" repeatedly until reaching the architectural root cause (e.g. unhandled concurrency, missing null check, race condition).
- Do not stop at surface symptoms (e.g. adding a `try/except: pass` is prohibited).

### Phase 4: Verification & Regression Proof
- Run the minimal test case to prove the defect is resolved.
- Run the entire project test suite to confirm zero regressions.
