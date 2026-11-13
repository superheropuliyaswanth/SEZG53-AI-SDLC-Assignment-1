# AI-Augmented SDLC (SEZG534) - Assignment 1
## Specification-Driven Development & Harness Engineering

**Student Submission Repository**  
**Course:** AI-Augmented Software Development Life Cycle (SE* ZG534), BITS Pilani  

---

## 1. Project Overview
This repository contains the complete implementation, specification artifacts, independent validation harnesses, failure/repair evidence, and reflection report for Assignment 1:
- **Part 1A (Deterministic Application)**: Smart Todo & Task CLI with CRUD operations, tag filtering, priority sorting, atomic JSON persistence, and strict lifecycle state transitions (`TODO` -> `IN_PROGRESS` -> `COMPLETED`, terminal `CANCELLED`).
- **Part 1B (Non-Deterministic AI Application)**: Natural-Language Reminder Agent that converts unstructured user instructions into structured JSON schemas, enforces temporal future guards, manages clarification for underspecified requests, and intercepts adversarial/malicious commands.
- **Part 2 (Assessed Reflection Questions)**: Comprehensive, evidence-based responses located in `REFLECTION_REPORT.md`.

---

## 2. Directory Structure

```
Assignment-1/
├── README.md                          # Master reproduction & execution instructions
├── REFLECTION_REPORT.md               # Completed submission report for LMS upload
├── DEMO_GUIDE.md                      # Video demonstration walkthrough script
├── Part-1A/                           # Deterministic Application
│   ├── .speckit/                      # Spec Kit artifacts
│   │   ├── constitution.md            # Engineering constraints & lifecycle state rules
│   │   ├── specify.md                 # User stories & acceptance criteria
│   │   ├── clarify.md                 # Edge-case resolutions & storage recovery policies
│   │   ├── plan.md                    # Module architecture & design
│   │   └── tasks.md                   # Work breakdown structure
│   ├── src/                           # Production source code
│   │   ├── __init__.py
│   │   ├── model.py                   # Data classes & Status/Priority Enums
│   │   ├── storage.py                 # Atomic JSON file persistence & backup
│   │   ├── service.py                 # Core business service & state transition engine
│   │   └── cli.py                     # Command-line interface with subcommands
│   ├── tests/                         # Specification-derived contract & unit tests
│   │   ├── __init__.py
│   │   ├── test_service.py            # 17 comprehensive unit & contract assertions
│   │   └── test_cli.py                # CLI subcommand & exit code tests
│   ├── .harness/                      # Multi-gate deterministic harness
│   │   ├── lint_guard.py              # Flake8 syntax & style gate
│   │   ├── security_guard.py          # Bandit static security (SAST) gate
│   │   ├── test_guard.py              # Pytest contract assertion runner
│   │   └── run_harness.py             # Unified deterministic orchestrator
│   └── evidence/                      # Verification audit trail
│       ├── initial-generation/        # Pre-repair code snapshot with state transition defect
│       ├── final-generation/          # Repaired & validated code snapshot
│       ├── harness-results/           # Structured JSON results (initial failure & final pass)
│       └── harness-log.md             # Complete step-by-step harness audit log
│
└── Part-1B/                           # Non-Deterministic AI Application
    ├── .speckit/                      # Spec Kit artifacts
    │   ├── constitution.md            # Bounded non-determinism, invariants & safety rules
    │   ├── specify.md                 # Intent contracts, schema fields, and 3-layer rubric
    │   ├── clarify.md                 # Temporal baseline & semantic scoring resolutions
    │   ├── plan.md                    # 3-layer single evaluation pipeline design
    │   └── tasks.md                   # Implementation tasks
    ├── src/                           # Production source code
    │   ├── __init__.py
    │   ├── schemas.py                 # Pydantic schema contracts
    │   ├── rules.py                   # Invariant rules & guardrail checks
    │   └── agent.py                   # Repaired Natural-Language Reminder Agent
    ├── prompts/                       # Prompt engineering & safety rules
    │   ├── system_prompt.txt          # System prompt with exemplars
    │   └── guardrails.txt             # Prohibited instructions & refusal policies
    ├── tests/                         # Unit tests for schemas and invariants
    │   ├── __init__.py
    │   └── test_schemas.py
    ├── evals/                         # Benchmark evaluation dataset
    │   └── dataset.json               # 18 gold-standard cases across 6 distinct categories
    ├── .harness/                      # 3-layer automated evaluation harness
    │   ├── layer1_structural.py       # Pydantic schema & JSON validator
    │   ├── layer2_property.py         # Deterministic invariant & future date guard
    │   ├── layer3_semantic.py         # Jaccard token overlap & intent quality evaluator
    │   └── evaluation_runner.py       # Pipeline orchestrator & threshold evaluator (85%)
    └── evidence/                      # Verification audit trail
        ├── initial-generation/        # Pre-repair agent snapshot (failed guardrails & ambiguity)
        ├── final-generation/          # Repaired agent snapshot (100% score)
        ├── eval-results-initial.json  # Initial evaluation run report (Score: 73.92% -> FAIL)
        ├── eval-results.json          # Final passing evaluation report (Score: 100% -> PASS)
        └── harness-log.md             # Complete step-by-step evaluation log
```

---

## 3. Environment Setup & Prerequisites

- **Python Version**: Python 3.10+ (Tested on Python 3.12.3)
- **Install Dependencies**:
```bash
pip install flake8 bandit pytest pytest-json-report pydantic
```

---

## 4. How to Run Part 1A (Deterministic Application)

### 4.1 Running the Unified Deterministic Harness
Navigate to `Part-1A` and execute the harness runner:
```bash
cd Part-1A
python .harness/run_harness.py
```
This executes all 3 gates in sequence:
1. **Gate 1**: `flake8` syntax and style check (must report 0 errors)
2. **Gate 2**: `bandit` security SAST scan (must report 0 High/Medium issues)
3. **Gate 3**: `pytest` unit & contract tests (must pass 100% of assertions)
4. Emits overall decision: `PASS -> ACCEPT`.

### 4.2 Running the CLI Application Directly
```bash
cd Part-1A

# 1. Add a new task
python -m src.cli add --title "Prepare Assignment Video" --priority HIGH --tags "bits,demo"

# 2. List all tasks
python -m src.cli list

# 3. Filter by tag
python -m src.cli list --tag bits

# 4. Start task (TODO -> IN_PROGRESS)
python -m src.cli start 1

# 5. Complete task (IN_PROGRESS -> COMPLETED)
python -m src.cli complete 1

# 6. Reopen completed task (COMPLETED -> TODO)
python -m src.cli reopen 1
```

---

## 5. How to Run Part 1B (Non-Deterministic AI Application)

### 5.1 Running the 3-Layer Evaluation Pipeline
Navigate to `Part-1B` and execute the evaluation runner:
```bash
cd Part-1B
python .harness/evaluation_runner.py
```
This executes the 3-layer evaluation across all 18 cases in `evals/dataset.json`:
- **Layer 1 (Structural)**: Validates JSON structure against `ReminderAgentResponse`.
- **Layer 2 (Invariants)**: Validates clarification logic, future date constraints, safety flags, and reschedule target binding.
- **Layer 3 (Semantic Quality)**: Evaluates intent match, Jaccard token overlap for titles, and priority alignment.
- Checks composite score against declared threshold (**85.0%**).
- Result: `100.00% Aggregate Score -> PASS -> ACCEPT`.

### 5.2 Running the Schemas & Invariant Unit Tests
```bash
cd Part-1B
python -m pytest tests/
```

---

## 6. Verification & Self-Healing Audit Trail

| Part | Initial Run Status | Root Cause of Failure | Corrective Action Taken | Re-Evaluation Status |
|---|---|---|---|---|
| **Part 1A** | **FAIL (REJECT)** | Missing status transition check (`TODO` -> `COMPLETED` skip allowed); terminal `CANCELLED` task allowed reopen; unused import `os`. | Defined strict `VALID_TRANSITIONS` lookup dictionary; normalized tags; eliminated dead imports. | **100% PASS (ACCEPT)** across Lint, Bandit, and 17 Pytest contract assertions. |
| **Part 1B** | **FAIL (Score: 73.92%)** | Adversarial instructions (`rm -rf`) accepted; day-of-week without time hallucinated 9am; snooze duration "30 mins" misparsed as target ID. | Pre-execution regex guardrail scanner; ambiguity detector for un-timed days; regex disambiguation of IDs from durations. | **100% PASS (Score: 100.0%)** across all 18 test cases in 6 categories. |

---

## 7. Submission Checklist Verification
- [x] Part 1A and Part 1B both included and operational.
- [x] Spec Kit artifacts (`constitution.md`, `specify.md`, `clarify.md`, `plan.md`, `tasks.md`) present in both parts.
- [x] Part 1A contains working deterministic harness gates and specification-derived tests.
- [x] Part 1B contains 18 evaluation cases (exceeds the 15-case requirement) and 3-layer pipeline.
- [x] Genuine failure-and-repair cycle evidence preserved in `evidence/initial-generation/`, `evidence/final-generation/`, and `harness-results/`.
- [x] `harness-log.md` included for both parts.
- [x] Final human acceptance decisions and residual risk justifications recorded.
- [x] Zero API keys, credentials, or secrets committed.
- [x] Self-contained execution instructions provided.
