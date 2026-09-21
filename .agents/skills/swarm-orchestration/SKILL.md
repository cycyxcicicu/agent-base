---
name: swarm-orchestration
description: Coordinate multi-agent swarms using hierarchical topologies, clean context isolation, atomic task delegation, and resilient handoff protocols.
triggers:
  - swarm orchestration
  - multi-agent coordination
  - dispatch swarm
  - agent swarm
---

# Swarm Orchestration (Multi-Agent Swarm Coordinator)

Coordinate complex projects across specialized agent swarms while preventing context pollution, race conditions, and duplicated labor.

## 1. Swarm Topologies
1. **Hierarchical (Queen / Specialist / Worker)**: Default architecture. A lead orchestrator plans, decomposes work into independent tickets, dispatches to domain specialists (e.g. `dev`, `designer`, `security`), and evaluates results.
2. **Consensus (Independent Reviewers)**: High-stakes decisions (security, schema migrations, financial logic) require independent sign-off from 2+ agents without shared bias.
3. **Pipeline (Assembly Line)**: Linear data processing or staged workflows (`intake` $\rightarrow$ `eval` $\rightarrow$ `transform` $\rightarrow$ `render`).

## 2. Context-Clean Delegation
- Never dump an entire monolithic chat history into a worker subagent.
- Provide only:
  1. The atomic task definition (`tasks/T-xxx.md`).
  2. Targeted file paths and explicit lines of code.
  3. Strict acceptance criteria and expected test command.
- Retrieve only:
  1. Diffs made.
  2. Test execution proof log with exit code.
  3. Identified edge cases or unresolved risks.

## 3. Handoff Protocol
When transferring work between agent roles (e.g., `dev` $\rightarrow$ `reviewer` $\rightarrow$ `qa`):
1. Write a structured handoff note in `docs/notes/inbox/` summarizing state, changed files, and test commands.
2. Clear worker scratch files to avoid state bleed.
3. Verify the receiving agent confirms receipt and runs independent verification.
