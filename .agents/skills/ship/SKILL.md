---
name: ship
description: Production release workflow. Enforces pre-flight checks, automated test suites, version bumping, changelog updates, and pull request readiness.
triggers:
  - chuẩn bị release
  - kiểm tra trước khi ship
  - prepare release
  - pre-ship check
  - create a pr
---

# Ship Workflow (Release Readiness Gatekeeper)

Use this skill when preparing to ship code, create a pull request, or bundle a release. Enforces zero broken builds, complete verification proof, and strict human commit gates.

## 1. Pre-Flight Checks
Before proposing a release or pull request:
1. **Working Tree Cleanliness**: Inspect `git status` to ensure no stray untracked scratch files, temp artifacts, or secrets are being included.
2. **Upstream Sync**: Verify the working branch is rebased or up to date with the integration base branch.
3. **The Iron Law**: Zero unverified claims. Every test must be executed with proof logs (Exit Code 0).

## 2. Mandatory Verification Suite
Run the full verification suite defined for the target repository:
1. **Project Tests & Linter**: Execute the official test, lint, and typecheck commands specified in `PROJECT.md` or repository configuration (e.g., `pytest`, `npm test`, `cargo test`).
2. **Security & Governance Checks**: Execute the project's automated security audit and integrity checks (e.g., secret scanners, audit scripts).
3. If ANY command fails with a non-zero exit code, stopping is mandatory. Fix defects before continuing.

## 3. Version Bump & Changelog Update
For meaningful feature additions or fixes:
1. Determine bump level following SemVer: `PATCH` (bug fixes), `MINOR` (new backwards-compatible features), `MAJOR` (breaking changes).
2. Update the project changelog file (`CHANGELOG.md` or release notes) following standard conventions:
   - Added, Changed, Deprecated, Removed, Fixed, Security.

## 4. Pull Request & Human Commit Gate
- **Human Gate Enforced**: Agents must NEVER run `git push` or merge directly to protected branches (`main`, `master`, `develop`).
- Format structured conventional commit messages (`feat:`, `fix:`, `refactor:`, `test:`, `chore:`).
- Prepare a comprehensive PR description detailing test proof logs, affected scope, and verification steps for human review.
