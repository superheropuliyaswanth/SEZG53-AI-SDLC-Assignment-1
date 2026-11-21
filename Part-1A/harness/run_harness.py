"""Unified Deterministic Harness Runner for Part 1A.

Coordinates:
- Gate 1: Syntax & Lint Guard (flake8)
- Gate 2: Security SAST Guard (bandit)
- Gate 3: Unit & Contract Test Guard (pytest)

Produces structured machine-readable JSON results, text reports, and feedback for self-healing.
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
    evidence_dir = os.path.join(PART1A_DIR, "evidence")
    os.makedirs(evidence_dir, exist_ok=True)
    current_time_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    # 1. Lint Guard
    lint_res = run_lint_guard("src")
    with open(os.path.join(evidence_dir, "lint_report.txt"), "w", encoding="utf-8") as f:
        f.write(f"Lint Report (flake8) - {current_time_iso}\n")
        f.write(f"Passed: {lint_res['passed']}\nExit Code: {lint_res['exit_code']}\n")
        f.write(lint_res.get("stdout", "") + "\n" + lint_res.get("stderr", ""))

    # 2. Security Guard
    sec_res = run_security_guard("src")
    with open(os.path.join(evidence_dir, "security_report.txt"), "w", encoding="utf-8") as f:
        f.write(f"Security SAST Report (bandit) - {current_time_iso}\n")
        f.write(f"Passed: {sec_res['passed']}\nExit Code: {sec_res['exit_code']}\n")
        f.write(sec_res.get("summary", "") + "\n")

    # 3. Unit & Contract Test Guard
    test_res = run_test_guard("tests")
    with open(os.path.join(evidence_dir, "test_report.txt"), "w", encoding="utf-8") as f:
        f.write(f"Test Report (pytest) - {current_time_iso}\n")
        f.write(f"Passed: {test_res['passed']}\nExit Code: {test_res['exit_code']}\n")
        f.write(test_res.get("stdout", "") + "\n" + test_res.get("stderr", ""))

    all_passed = lint_res["passed"] and sec_res["passed"] and test_res["passed"]
    decision = "ACCEPT" if all_passed else "REJECT"

    # Write harness_summary.txt
    summary_text = (
        f"Harness summary\n"
        f"===============\n"
        f"Time: {current_time_iso}\n\n"
        f"lint: {'PASS' if lint_res['passed'] else 'FAIL'} (exit code {lint_res['exit_code']})\n"
        f"security: {'PASS' if sec_res['passed'] else 'FAIL'} (exit code {sec_res['exit_code']})\n"
        f"tests: {'PASS' if test_res['passed'] else 'FAIL'} (exit code {test_res['exit_code']})\n\n"
        f"RESULT: {'PASS' if all_passed else 'FAIL'}\n"
    )
    with open(os.path.join(evidence_dir, "harness_summary.txt"), "w", encoding="utf-8") as f:
        f.write(summary_text)

    # Print summary to terminal matching colleague's output
    print(summary_text)

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

    if evidence_output_path:
        os.makedirs(os.path.dirname(evidence_output_path), exist_ok=True)
        with open(evidence_output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

    return report


if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PART1A_DIR, "evidence", "harness-results", "harness_run.json")
    res = execute_harness(out_file)
    sys.exit(0 if res["overall_status"] == "PASS" else 1)
