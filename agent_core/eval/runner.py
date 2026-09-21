"""
Eval Test Harness Runner.
Học hỏi từ: promptfoo (Test suite evaluation, pass/fail aggregation, summary scoring).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from .assertions import AssertionEngine, AssertionResult
from .redteam import RedTeamScanner, SecurityIssue


@dataclass
class TestCase:
    name: str
    prompt: str
    response: str
    expected_contains: Optional[List[str]] = None
    forbidden_contains: Optional[List[str]] = None
    expected_regex: Optional[str] = None
    must_be_json: bool = False
    required_json_keys: Optional[List[str]] = None
    scan_security: bool = True


@dataclass
class EvalReport:
    total_tests: int
    passed_tests: int
    failed_tests: int
    pass_rate: float
    security_violations: int
    details: List[Dict[str, Any]] = field(default_factory=list)


class EvalRunner:
    """Hệ thống thực thi và chấm điểm chất lượng câu trả lời AI."""

    @classmethod
    def run_case(cls, test: TestCase) -> Dict[str, Any]:
        assertion_results: List[AssertionResult] = []
        security_issues: List[SecurityIssue] = []

        # 1. Chạy các Assertions
        if test.expected_contains:
            for substring in test.expected_contains:
                assertion_results.append(AssertionEngine.assert_contains(test.response, substring))

        if test.forbidden_contains:
            for substring in test.forbidden_contains:
                assertion_results.append(AssertionEngine.assert_not_contains(test.response, substring))

        if test.expected_regex:
            assertion_results.append(AssertionEngine.assert_regex(test.response, test.expected_regex))

        if test.must_be_json:
            assertion_results.append(AssertionEngine.assert_json_valid(test.response, test.required_json_keys))

        # 2. Quét bảo mật Red-team
        if test.scan_security:
            security_issues = RedTeamScanner.scan_text(test.response)

        all_passed = all(a.passed for a in assertion_results) and len(security_issues) == 0

        return {
            "test_name": test.name,
            "passed": all_passed,
            "assertions": assertion_results,
            "security_issues": security_issues,
            "response_preview": test.response[:120] + "..." if len(test.response) > 120 else test.response
        }

    @classmethod
    def run_suite(cls, test_cases: List[TestCase]) -> EvalReport:
        results = [cls.run_case(tc) for tc in test_cases]
        passed_count = sum(1 for r in results if r["passed"])
        failed_count = len(results) - passed_count
        security_count = sum(len(r["security_issues"]) for r in results)
        rate = round((passed_count / len(results) * 100), 2) if test_cases else 0.0

        return EvalReport(
            total_tests=len(test_cases),
            passed_tests=passed_count,
            failed_tests=failed_count,
            pass_rate=rate,
            security_violations=security_count,
            details=results
        )
