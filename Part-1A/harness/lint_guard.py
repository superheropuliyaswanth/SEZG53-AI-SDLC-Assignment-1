"""Lint Guard: Checks syntax and code style standards using flake8."""
import subprocess
import sys
import json
import os


def run_lint_guard(target_dir: str = "src") -> dict:
    cmd = [sys.executable, "-m", "flake8", target_dir, "--max-line-length=120", "--count"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    passed = (proc.returncode == 0)
    return {
        "gate": "Syntax & Lint Guard",
        "tool": "flake8",
        "target": target_dir,
        "passed": passed,
        "exit_code": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip()
    }


if __name__ == "__main__":
    result = run_lint_guard("src")
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["passed"] else 1)
