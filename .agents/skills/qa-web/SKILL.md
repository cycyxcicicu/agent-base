---
name: qa-web
description: Systematically QA test a web application, discover bugs, and verify fixes. Produces health scores, visual evidence, and ship-readiness summaries.
triggers:
  - qa test this
  - find bugs on site
  - test the site
  - web quality check
  - qa web
---

# /qa-web — Systematic Web Quality Assurance

Use this skill when verifying web applications, testing user flows, checking visual regressions, or evaluating ship-readiness.

## 1. QA Tiers
- **Quick Tier**: Critical and High severity bugs only (broken authentication, 500 server crashes, blocked checkout, broken primary navigation).
- **Standard Tier** *(Default)*: Quick tier + medium UX regressions, broken form validations, layout overflows, and missing loading states.
- **Exhaustive Tier**: Standard tier + cosmetic imperfections, micro-alignment issues, contrast warnings, and edge-case responsive breakpoints.

## 2. The 4-Step QA Cycle
1. **Reconnaissance & Surface Mapping**:
   - Map primary navigation routes, form flows, modals, and dynamic components.
   - Catalog core state variants: Empty state, Loading state, Error state, and Success state.
2. **Execution & Bug Hunting**:
   - Drive real user flows across desktop and mobile breakpoints (375px, 768px, 1280px).
   - Test edge cases: rapid double-clicks, empty submissions, boundary strings, network disconnection.
3. **Defect Isolation & Evidence Capture**:
   - For every defect found, capture browser console traces, network failure codes, and DOM screenshots.
   - Classify root failure layer: Frontend UI, API/HTTP, or Database state.
4. **Defect Reporting & Re-Verification**:
   - Document exact reproduction steps and expected vs actual behavior in a task card or bug report.
   - Hand off to `dev` for code repair (QA roles must never edit source code directly).
   - Once `dev` delivers the fix, re-run the exact flow to confirm resolution.
