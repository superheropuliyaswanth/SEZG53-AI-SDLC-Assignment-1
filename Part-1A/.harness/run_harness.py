"""Unified Deterministic Harness Runner for Part 1A.

Coordinates:
- Gate 1: Syntax & Lint Guard (flake8)
- Gate 2: Security SAST Guard (bandit)
- Gate 3: Unit & Contract Test Guard (pytest)

Produces structured machine-readable JSON results and feedback for self-healing.
"""
import os
import sys
import json
from datetime import datetime, timezone

# Ensure project root is in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PART1A_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PART1A_DIR not in sys.path:
    sys.path.insert(0, PART1A_DIR)

from lint_guard import run_lint_guard
from security_guard import run_security_guard
from test_guard import run_test_guard


def execute_harness(evidence_output_path: str = None) -> dict:
    os.chdir(PART1A_DIR)
    print("=" * 70)
    print("RUNNING DETERMINISTIC HARNESS - PART 1A")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    # 1. Lint Guard
    print("[1/3] Running Syntax & Lint Guard (flake8)...")
    lint_res = run_lint_guard("src")
    print(f"      Result: {'PASS' if lint_res['passed'] else 'FAIL'}")

    # 2. Security Guard
    print("[2/3] Running Security SAST Guard (bandit)...")
    sec_res = run_security_guard("src")
    print(f"      Result: {'PASS' if sec_res['passed'] else 'FAIL'}")

    # 3. Unit & Contract Test Guard
    print("[3/3] Running Unit & Contract Test Guard (pytest)...")
    test_res = run_test_guard("tests")
    print(f"      Result: {'PASS' if test_res['passed'] else 'FAIL'}")

    all_passed = lint_res["passed"] and sec_res["passed"] and test_res["passed"]
    decision = "ACCEPT" if all_passed else "REJECT"

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "application": "Part-1A Smart Todo & Task CLI",
        "overall_status": "PASS" if all_passed else "FAIL",
        "human_decision": decision,
        "gates": {
            "lint_guard": lint_res,
            "security_guard": sec_res,
            "test_guard": test_res
        }
    }

    print("-" * 70)
    print(f"OVERALL HARNESS RESULT: {report['overall_status']} -> Decision: {decision}")
    print("-" * 70)

    if evidence_output_path:
        os.makedirs(os.path.dirname(evidence_output_path), exist_ok=True)
        with open(evidence_output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"Harness report saved to: {evidence_output_path}")

    return report


if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PART1A_DIR, "evidence", "harness-results", "harness_run.json")
    res = execute_harness(out_file)
    sys.exit(0 if res["overall_status"] == "PASS" else 1)
