"""Harness Self-Check / Mutation Suite for Part 1A.

Demonstrates that each deterministic gate independently catches problems and fails:
1. Gate 1 (Lint): Tested with deliberate unused import & whitespace error -> Expect FAIL
2. Gate 2 (Security): Tested with deliberate dangerous eval() usage -> Expect FAIL
3. Gate 3 (Unit/Contract Tests): Tested against initial buggy service -> Expect FAIL
4. Clean Run: Tested against production src/ -> Expect PASS
"""
import os
import sys
import tempfile
import json
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PART1A_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PART1A_DIR not in sys.path:
    sys.path.insert(0, PART1A_DIR)

from lint_guard import run_lint_guard
from security_guard import run_security_guard
from test_guard import run_test_guard


def run_self_check():
    os.chdir(PART1A_DIR)
    print("=" * 75)
    print("HARNESS SELF-CHECK: Verifying that all gates can independently FAIL on defect")
    print("=" * 75)
    results = []

    # 1. Test Gate 1 with synthetic lint defect
    with tempfile.TemporaryDirectory() as tmpdir:
        bad_file = os.path.join(tmpdir, "bad_syntax.py")
        with open(bad_file, "w") as f:
            f.write("import os\nimport sys\n\ndef foo( ):\n  pass\n")
        res = run_lint_guard(tmpdir)
        passed = (res["passed"] is False)
        results.append(("Gate 1 (Lint Guard)", "Synthetic unused import & bad spacing", "FAIL", "FAIL" if not res["passed"] else "PASS", passed))

    # 2. Test Gate 2 with synthetic security defect (Bandit)
    with tempfile.TemporaryDirectory() as tmpdir:
        insecure_file = os.path.join(tmpdir, "insecure.py")
        with open(insecure_file, "w") as f:
            f.write("import sys\n\ndef unsafe(user_input):\n    return eval(user_input)\n")
        res = run_security_guard(tmpdir)
        passed = (res["passed"] is False)
        results.append(("Gate 2 (Security Guard)", "Synthetic dangerous eval() usage", "FAIL", "FAIL" if not res["passed"] else "PASS", passed))

    # 3. Test Gate 3 with initial buggy implementation
    init_service = os.path.join(PART1A_DIR, "evidence", "initial-generation", "service.py")
    src_service = os.path.join(PART1A_DIR, "src", "service.py")
    backup_file = os.path.join(PART1A_DIR, "src", "service.py.selfcheck.bak")
    
    shutil.copyfile(src_service, backup_file)
    try:
        shutil.copyfile(init_service, src_service)
        res = run_test_guard("tests")
        passed = (res["passed"] is False)
        results.append(("Gate 3 (Test Guard)", "Buggy state transitions (initial gen)", "FAIL", "FAIL" if not res["passed"] else "PASS", passed))
    finally:
        shutil.copyfile(backup_file, src_service)
        os.remove(backup_file)

    # 4. Test all gates against clean production src/
    res_lint = run_lint_guard("src")
    res_sec = run_security_guard("src")
    res_test = run_test_guard("tests")
    all_clean = res_lint["passed"] and res_sec["passed"] and res_test["passed"]
    results.append(("All Gates Combined", "Clean production code (final gen)", "PASS", "PASS" if all_clean else "FAIL", all_clean))

    # Print summary table
    print(f"{'Gate / Target':<25} | {'Tested Input Scenario':<35} | {'Expected':<8} | {'Observed':<8} | {'Status'}")
    print("-" * 95)
    for gate, scenario, exp, obs, ok in results:
        status_str = "VERIFIED" if ok else "FAILED"
        print(f"{gate:<25} | {scenario:<35} | {exp:<8} | {obs:<8} | {status_str}")
    print("=" * 95)

    all_verified = all(r[4] for r in results)
    print(f"SELF-CHECK OVERALL RESULT: {'ALL GATES INDEPENDENTLY PROVEN SENSITIVE TO FAULTS' if all_verified else 'SELF-CHECK FAILED'}\n")
    return all_verified


if __name__ == "__main__":
    ok = run_self_check()
    sys.exit(0 if ok else 1)
