# Part 1B — AI Reminder Agent

Autonomous Natural-Language Reminder Agent engineered using GitHub Spec Kit Spec-Driven Development (SDD) and validated with a 3-layer automated evaluation harness.

## Quick Start

### 1. Run Evaluation Harness
```powershell
python .harness/evaluation_runner.py
```
Expected Output:
```json
{
  "reference_datetime": "2026-11-21T12:00:00",
  "case_count": 22,
  "structural_score": 100.0,
  "property_score": 86.36,
  "semantic_score": 93.41,
  "aggregate_score": 92.57,
  "result": "PASS"
}
```

### 2. Run Tests
```powershell
python -m pytest tests/test_reminder_agent.py
```
