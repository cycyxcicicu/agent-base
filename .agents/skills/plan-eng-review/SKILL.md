---
name: plan-eng-review
description: Engineering manager plan review. Evaluates 10x scale, database table locks, race conditions, module seams, and edge cases before coding begins.
triggers:
  - review architecture
  - eng plan review
  - check the implementation plan
  - tech review
---

# Plan Engineering Review (Eng Manager Mode)

Use this skill to lock in the technical execution plan before writing code. Enforces deep module design, concurrency safety, scale stress-testing, and rigorous edge case analysis.

## 1. Scope Gate (Hard Stop)
Ensure an active implementation plan, architecture specification, or diff is designated. Do not write or modify source code during the review phase.

## 2. The 10x Scale Stress Test
For every design or architectural proposal, evaluate:
- **10x Data Volume**: Does this query or parser load the entire dataset into memory? Will it OOM when tables grow from 1,000 to 100,000 records?
- **10x Concurrency**: Will multiple concurrent agents or workers cause race conditions, deadlocks, or duplicate writes?
- **10x Latency / Degradation**: Does the system fail fast with graceful fallbacks (Circuit Breaker, Exponential Backoff with Jitter) when external APIs degrade?

## 3. Database & Concurrency Checks
- **Lock Contention**: Does an `ALTER TABLE` or migration require an exclusive lock that blocks reads/writes?
- **Zero-Downtime Migration**: Does the change use the Expand-Contract pattern? (Add column nullable $\rightarrow$ dual write $\rightarrow$ backfill $\rightarrow$ contract old column).
- **Idempotency**: Can every write operation be safely retried without creating duplicate records or billing errors?

## 4. Module Seams & Interface Depth
- **Deep Modules**: Is the interface simple while the internal implementation is rich? (Avoid shallow pass-through wrappers).
- **Clean Seams**: Can the module be tested in complete isolation without mocking 10 external dependencies?
- **Information Hiding**: Are internal state machines and caching strategies hidden behind the interface?

## 5. Test Coverage & Edge Case Matrix
Verify that the plan includes:
- Minimum reproducing test case for any bug fix.
- Edge case handling: Empty inputs, malformed JSON, network disconnects, token limits.
- Condition-based waiting instead of hardcoded `sleep()`.
