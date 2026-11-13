"""Unit & Contract Test Guard: Derives exact assertions from approved requirements."""
import subprocess
import sys
import json
import os


def run_test_guard(test_dir: str = "tests") -> dict:
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        test_dir,
        "-v",
        "--json-report",
        "--json-report-file=.harness_test_report.json"
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    
    passed = (proc.returncode == 0)
    summary = {}
    failed_tests = []

    if os.path.exists(".harness_test_report.json"):
        try:
            with open(".harness_test_report.json", "r", encoding="utf-8") as f:
                report = json.load(f)
                summary = report.get("summary", {})
                for test in report.get("tests", []):
                    if test.get("outcome") == "failed":
                        failed_tests.append({
                            "nodeid": test.get("nodeid"),
                            "message": test.get("call", {}).get("crash", {}).get("message", "Test failed")
                        })
            os.remove(".harness_test_report.json")
        except Exception:
            pass

    return {
        "gate": "Unit & Contract Test Guard",
        "tool": "pytest",
        "target": test_dir,
        "passed": passed,
        "exit_code": proc.returncode,
        "summary": summary,
        "failed_tests": failed_tests,
        "stdout": proc.stdout[-1500:] if proc.stdout else "",
        "stderr": proc.stderr[-1000:] if proc.stderr else ""
    }


if __name__ == "__main__":
    result = run_test_guard("tests")
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["passed"] else 1)
