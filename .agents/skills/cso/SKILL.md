---
name: cso
description: Chief Security Officer audit. Enforces evidence before assurance, finds exploitable vulnerabilities, OWASP flaws, and credential leaks.
triggers:
  - security audit
  - check for vulnerabilities
  - owasp review
  - cso review
---

# CSO (Chief Security Officer) Audit

Find exploitable security defects, verify threat models, and enforce evidence before assurance. 

## 1. Core Principle: Evidence Before Assurance
Do not assume code is secure because it compiles or passes functional tests. Security assurance requires active testing and verification against concrete exploit vectors.

## 2. Threat Modeling Dimensions
- **Attacker Profile**: Who can reach this code? (Unauthenticated public web, authenticated user, internal worker, AI prompt injection).
- **Trust Boundary**: Where does untrusted input cross into trusted execution? (HTTP params, webhooks, LLM generation, file uploads).
- **Impact Analysis**: What is the worst-case blast radius? (Remote code execution, credential exfiltration, data destruction, unauthorized privilege escalation).

## 3. Automated Static Verification
Run the project's security scanner or audit command (e.g. `python scripts/cso.py` if present, or ecosystem tools like `bandit`, `npm audit`, `trivy`):
```bash
# In agent-base or repos with cso.py:
python scripts/cso.py --strict
# In other projects: run the security audit configured in PROJECT.md
```

## 4. Key Vulnerability Vectors Audited
1. **Secrets & Credentials**: No hardcoded API keys, private keys, or passwords.
2. **Command Injection**: Disallow `shell=True` with dynamic strings or unescaped variables.
3. **SQL Injection**: Enforce parameterized queries; forbid f-strings in `execute()`.
4. **Path Traversal**: Validate file paths with base directory containment checks.
5. **Insecure Deserialization**: Forbid unsafe `pickle.loads()` or `yaml.load()` without SafeLoader.
6. **Prompt Injection & SSRF**: Validate URL destinations against internal IP allowlists.

## 5. Security Gate Criteria
- **CRITICAL / HIGH Findings**: Automatic block. Merge or commit is prohibited until remediated.
- **MEDIUM Findings**: Must be triaged and tracked in `docs/DEBT.md` with an explicit ceiling and remediation trigger.
