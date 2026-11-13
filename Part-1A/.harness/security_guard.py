"""Security / SAST Guard: Runs static security analysis using Bandit."""
import subprocess
import sys
import json


def run_security_guard(target_dir: str = "src") -> dict:
    cmd = [sys.executable, "-m", "bandit", "-r", target_dir, "-f", "json", "-q"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    
    passed = True
    issues = []
    try:
        report = json.loads(proc.stdout)
        results = report.get("results", [])
        # Flag if any medium or high severity issues exist
        for r in results:
            if r.get("issue_severity") in ["MEDIUM", "HIGH"]:
                passed = False
                issues.append({
                    "test_id": r.get("test_id"),
                    "issue_text": r.get("issue_text"),
                    "severity": r.get("issue_severity"),
                    "line_number": r.get("line_number"),
                    "filename": r.get("filename")
                })
    except json.JSONDecodeError:
        # If output was empty or non-json
        if proc.returncode != 0:
            passed = False

    return {
        "gate": "Security / SAST Guard",
        "tool": "bandit",
        "target": target_dir,
        "passed": passed,
        "exit_code": proc.returncode,
        "high_medium_issues": issues,
        "summary": f"{len(issues)} critical security issues found."
    }


if __name__ == "__main__":
    result = run_security_guard("src")
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["passed"] else 1)
