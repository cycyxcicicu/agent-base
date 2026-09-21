---
name: plan-ceo-review
description: CEO & Founder-mode plan review. Challenges premises, uncovers 10-star product potential, inverts hidden assumptions, and enforces strict scope gating.
triggers:
  - think bigger
  - expand scope
  - strategy review
  - rethink this plan
  - ceo review
---

# Plan CEO Review (Founder Mode)

Use this skill when asked to "think bigger", "rethink this plan", "CEO review", or when a technical plan risks building the wrong product or suffering from scope creep.

## 1. Scope Gate (Mandatory First Step)
Before doing any deep analysis or editing files, confirm the review target:
1. **Target Identification**: Check if an implementation plan (`implementation_plan.md`), ticket, or PR diff was explicitly provided.
2. If ambiguous, stop and ask the user to clarify what to review.

## 2. The 10-Star Product Exercise
Ask the breakthrough questions to escape incremental thinking:
- **1-Star Product**: What is broken, clunky, or frustrating about the current status quo?
- **5-Star Product**: What meets expectations cleanly and solves the immediate friction?
- **10-Star Product**: What would make users feel like they are using magic? What is the boldest, most ambitious version?
- **The Sweet Spot**: Which high-leverage elements from the 7-star to 10-star vision can be delivered with minimal extra code today?

## 3. Assumptions Inversion
Identify the hidden, unstated assumptions in the plan:
- Why does this require multiple manual steps or screens? Can it be zero-click?
- Why do we assume users will configure this? Can sensible defaults remove the configuration entirely?
- Why are we building a custom solution instead of leveraging an existing primitive?

## 4. The Four Scope Modes
Explicitly classify the recommendation into one of four scope modes:
1. **SCOPE EXPANSION (Dream Big)**: When the opportunity is massive and the current plan is too conservative. Propose the higher-impact architecture.
2. **SELECTIVE EXPANSION (High ROI)**: Keep the core timeline/scope intact, but cherry-pick 1 or 2 transformative enhancements.
3. **HOLD SCOPE (Maximum Rigor)**: The scope is well-sized; focus 100% on execution excellence, robustness, and speed.
4. **SCOPE REDUCTION (Strip to MVP)**: The plan is over-engineered. Slash unnecessary features to ship 5x faster.

## 5. Structured Decision Brief
For any proposed change, present a structured decision brief:
- **ELI10**: Plain language explanation of the decision and why it matters.
- **Stakes**: What breaks or is lost if we choose incorrectly.
- **Recommendation**: Explicit opinionated recommendation labeled `(recommended)`.
- **Options**: A/B choices with concrete pros (>=40 chars) and honest cons (>=40 chars).
