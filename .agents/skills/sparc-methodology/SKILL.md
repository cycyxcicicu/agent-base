---
name: sparc-methodology
description: Systematic SPARC development cycle: Specification, Pseudocode, Architecture, Refinement, and Completion for robust software engineering.
triggers:
  - sparc
  - sparc methodology
  - structured dev cycle
  - systematic development
---

# SPARC Methodology

Execute software engineering tasks through the 5 rigorous phases of SPARC to eliminate guesswork and prevent costly architectural rollbacks.

## Phase 1: S — Specification
- Extract exact functional requirements, boundary limits, and inputs/outputs.
- Identify non-functional requirements (latency ceilings, memory bounds, concurrent users).
- Document edge cases and failure modes upfront in `docs/spec/`.

## Phase 2: P — Pseudocode
- Write human-readable, language-agnostic logic flows before touching production code.
- Validate the control flow, state transitions, and error handling branches on paper.
- Ensure the algorithm has optimal time and space complexity ($O(N)$ vs $O(N^2)$).

## Phase 3: A — Architecture
- Define clear module seams, data contracts, and dependency graphs.
- Establish clean interfaces (Deep Modules: simple interface, deep capability).
- Check for zero-downtime database migrations (Expand-Contract pattern).

## Phase 4: R — Refinement (TDD Loop)
- Write the minimal failing test case first (Red).
- Implement the simplest code that passes the test (Green).
- Refactor and clean up while keeping all tests passing.
- Replace any hardcoded `sleep()` with condition-based waiting.

## Phase 5: C — Completion
- Run the full project test suite, linters, and static type checkers defined in `PROJECT.md`.
- Execute project security audits and quality verification checks.
- Produce concrete verification proof logs with Exit Code 0 before declaring task completion.
