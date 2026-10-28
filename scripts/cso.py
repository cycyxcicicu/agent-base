#!/usr/bin/env python3
"""
scripts/cso.py
CLI interface for CSO (Chief Security Officer) Static Security Audit.
Usage:
  python scripts/cso.py
  python scripts/cso.py --path src/
  python scripts/cso.py --strict
"""

import sys
import argparse
from pathlib import Path

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

# Add root directory to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from agent_core.eval.cso_scanner import CsoScanner

def main():
    parser = argparse.ArgumentParser(description="CSO Static Security Audit Runner")
    parser.add_argument("--path", type=str, default="", help="Directory or file to audit (defaults to repo root)")
    parser.add_argument("--strict", action="store_true", help="Fail with exit code 1 if any finding is found")
    args = parser.parse_args()

    target = Path(args.path) if args.path else root_dir
    scanner = CsoScanner(root_dir=root_dir)

    print(f"🛡️ Running CSO Security Audit on: {target}")
    if target.is_file():
        findings = scanner.scan_file(target)
    else:
        findings = scanner.scan_directory(target)

    gate = scanner.evaluate_gate(findings)

    print("\n" + "=" * 60)
    print(f"CSO Security Audit Report - Verdict: {gate['verdict']}")
    print(f"Critical: {gate['critical']} | High: {gate['high']} | Medium: {gate['medium']}")
    print(f"Miễn trừ có lý do (# cso: allow): {getattr(scanner, 'suppressed_count', 0)}")
    for finding, reason in getattr(scanner, "suppressed", []):
        print(f"  - {finding.file_path}:{finding.line_number} {finding.rule_id} — {reason}")
    print("=" * 60)

    if findings:
        for f in findings:
            print(f"\n[{f.severity}] {f.rule_id} in {f.file_path}:{f.line_number}")
            print(f"  Snippet: {f.snippet}")
            print(f"  Issue:   {f.message}")
            print(f"  Fix:     {f.recommendation}")
    else:
        print("✅ No exploitable security defects or hardcoded credentials detected.")

    if not gate["passed"] or (args.strict and findings):
        print("\n❌ CSO Gate: BLOCKED by security violations.")
        sys.exit(1)
    else:
        print("\n✅ CSO Gate: PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    main()
