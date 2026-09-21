---
name: archify-review
description: Review issues, PRs, and architectural changes through Value, Cost, and Impact to support evidence-based maintenance and triage decisions.
triggers:
  - triage issue
  - archify review
  - architecture review
  - assess change
---

# Archify Review (Value, Cost, and Impact Assessment)

Judge whether a technical problem is worth solving and an architectural approach is worth maintaining over time using three objective dimensions:

## 1. The Three Review Dimensions
1. **Value (Is it worth solving?)**:
   - What is the real underlying problem, and who specifically benefits from fixing it?
   - How frequently does this problem occur, and what are its concrete business/system consequences?
   - Is it worth addressing right now, or should it be deferred?

2. **Cost (What is the true burden?)**:
   - Implementation and verification effort required.
   - Cognitive load: How much harder will it be for future engineers or agents to understand, modify, and debug this code?
   - Prefer leveraging existing codebase primitives over introducing new external dependencies. Keep the solution proportional to the problem.

3. **Impact (What is the blast radius?)**:
   - Which components, public APIs, and user behaviors are affected?
   - Does this change improve long-term maintainability or add tight coupling and brittle constraints?
   - Are there hidden ripple effects on performance, latency, or concurrency?

## 2. Evidence-Based Judgments
- Ground all judgments in tangible evidence from the codebase, benchmark results, or test logs.
- Clearly distinguish verified facts from assumptions and unproven claims.
- Conclude with an actionable recommendation: **Proceed**, **Revise Approach**, or **Reject/Close**, with explicit rationale.
