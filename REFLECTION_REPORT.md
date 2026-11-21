# Assignment Submission: Specification-Driven Development & Harness Engineering
**Course:** AI-Augmented Software Development Life Cycle (SE* ZG534)  
**Institution:** BITS Pilani  

---

## Student Details
| Field | Details |
|---|---|
| **Name** | Yaswanth Pulikonda |
| **Student ID** | 2026NS93064 |
| **Email ID** | 2026NS93064@wilp.bits-pilani.ac.in |
| **GitHub Repository Link** | https://github.com/superheropuliyaswanth/SEZG53-AI-SDLC-Assignment-1 |
| **Video Link** | https://drive.google.com/file/d/your-video-link-here/view?usp=sharing |

---

## Problem Statements

### Part 1A: Problem Statement
**Concise Description:**  
Part 1A addresses the problem of deterministic task management through a reliable Command-Line Interface (CLI) application named **Smart Todo & Task CLI**. The intended users are software developers and technical operators requiring deterministic, local task tracking with atomic file persistence. Key requirements include full CRUD operations (`add`, `list`, `get`, `start`, `complete`, `cancel`, `reopen`, `delete`), tag filtering, multi-level priority sorting (`HIGH` > `MEDIUM` > `LOW`), atomic JSON file persistence with corruption backup, and strict enforcement of a lifecycle state machine (`TODO` -> `IN_PROGRESS` -> `COMPLETED`, terminal `CANCELLED`). The expected outcome is a completely deterministic software system whose behavior, status transitions, and data integrity are independently verified by a multi-gate harness (Flake8 linting, Bandit SAST security, and Pytest contract assertions).

### Part 1B: Problem Statement
**Concise Description:**  
Part 1B addresses the extraction and orchestration of unstructured natural-language reminder requests through a **Natural-Language Reminder Agent**. The non-deterministic behavior arises from linguistic variability, differing date/time expressions ("tomorrow at 5pm", "in 3 hours", "at midnight"), ambiguous user inputs ("Remind me to visit dentist next Monday" without time), and adversarial prompt injections or destructive OS instructions ("rm -rf /"). The expected output is a strictly typed JSON response adhering to a Pydantic schema contract with validated intent, normalized ISO 8601 UTC timestamps, priority, and safety flags. The evaluation approach consists of a 3-layer automated harness pipeline—**Layer 1 (Structural Pydantic schema validation)**, **Layer 2 (Deterministic property & invariant rules)**, and **Layer 3 (Semantic & quality token-overlap heuristics)**—benchmarked against an 18-case dataset with an aggregate acceptance threshold of >= 85.0%.

---

## Assessed Reflection Questions

### 1. Specification Influence (1 mark)
**Question:** Identify one concrete decision in your implementation that was directly shaped by a Spec Kit artifact (constitution, specification, clarification, plan, or tasks). Explain the traceability from the artifact to the implemented decision.

**Response:**  
In **Part 1A**, the implementation of the state transition engine in `src/service.py` was directly governed by **`.speckit/constitution.md` (Section 4: Lifecycle State Machine)** and **`.speckit/clarify.md` (Q4)**. The constitution explicitly mandated that:
1. `TODO` cannot jump directly to `COMPLETED` without entering `IN_PROGRESS`.
2. `CANCELLED` is a strictly terminal state that cannot be reopened or started.
3. Violations must immediately abort with specific Exit Code `3` (`IllegalStateTransitionError`).

This upstream specification directly shaped the implementation of the `VALID_TRANSITIONS` lookup dictionary in `src/service.py`:
```python
VALID_TRANSITIONS: Dict[Status, Set[Status]] = {
    Status.TODO: {Status.IN_PROGRESS, Status.CANCELLED},
    Status.IN_PROGRESS: {Status.COMPLETED, Status.CANCELLED},
    Status.COMPLETED: {Status.TODO},  # Explicit reopen only
    Status.CANCELLED: set()            # Strictly terminal
}
```
Without this constitutional rule, an unconstrained coding agent would have implemented naive status reassignment (`task.status = target_status`), permitting illegal workflow skips. Traceability is established from `constitution.md#L30` to `specify.md#US-4`, then to contract test `tests/test_service.py::test_illegal_status_transition_todo_to_completed`, and finally to the enforced guard in `service.py#L93`.

---

### 2. Harness Value in Part 1A (1 mark)
**Question:** Describe one issue detected by the deterministic harness that would have been missed or less reliably detected by simply asking the coding agent to review its own output. State the relevant harness gate/evidence and how the issue was resolved.

**Response:**  
During the initial generation of Part 1A (`evidence/initial-generation/service.py`), the coding agent implemented the `complete_task` method simply as `self._transition(task_id, Status.COMPLETED)` without verifying that the task's current status was `IN_PROGRESS`. When self-reviewing, LLM coding agents suffer from confirmation bias—they inspect code syntax and happy-path execution, falsely assuming that calling `complete_task` succeeds because the task status is successfully changed to `COMPLETED`.

The deterministic harness independently caught this violation through **Gate 3 (Unit & Contract Test Guard / Pytest)**, recorded in `evidence/harness-results/initial_failure.json`:
- **Failed Assertion:** `tests/test_service.py::test_illegal_status_transition_todo_to_completed`
- **Observed Behavior:** Task moved directly from `TODO` to `COMPLETED` with exit code 0.
- **Expected Behavior:** Raise `IllegalStateTransitionError` with exit code 3.

The harness also caught an unused import (`F401 'os'`) via **Gate 1 (Flake8)**. The issue was resolved by replacing ad-hoc status assignment with the validated transition check against `VALID_TRANSITIONS` in `src/service.py`. On re-running the harness runner (`.harness/run_harness.py`), all 17 contract tests passed cleanly with zero lint or security defects (`evidence/harness-results/final_pass.json`).

---

### 3. Evaluating Non-Determinism in Part 1B (1 mark)
**Question:** Choose one evaluation case where exact string matching would be inappropriate. Explain which schema constraint, invariant/property, and semantic/quality criterion you used instead, and why these checks were suitable.

**Response:**  
In **Part 1B**, test case **`TC-01`** ("*Remind me to submit the quarterly tax report tomorrow at 5pm*") illustrates why exact string matching is fundamentally flawed: different LLM generations or prompting styles may extract the title as `"submit the quarterly tax report"`, `"submit quarterly tax report"`, `"tax report submission"`, or `"file quarterly taxes"`. Exact string equality (`title == "submit the quarterly tax report"`) would cause brittle false negatives on valid semantic variations.

Instead, the 3-layer harness evaluated TC-01 using three robust criteria:
1. **Schema Constraint (Layer 1):** Validated that output conforms to `ReminderAgentResponse`, where `reminder.title` is a non-empty string between 1 and 200 characters, and `reminder.due_datetime` parses into a valid ISO 8601 UTC timestamp string.
2. **Invariant / Property Constraint (Layer 2):** Evaluated **Rule INV-2** ensuring `due_datetime` (`2026-11-14T17:00:00Z`) is chronologically strictly in the future relative to the reference evaluation baseline (`2026-11-13T14:48:00Z`), and verified that `safety_flag == False` and `requires_clarification == False`.
3. **Semantic / Quality Criterion (Layer 3):** Evaluated intent classification (`intent == "CREATE_REMINDER"` for 50% weight) and computed **Jaccard token similarity** between the extracted title tokens and the gold-standard key token set `{"submit", "quarterly", "tax", "report"}` (35% weight). A token overlap threshold >= 0.30 rewarded full credit.

These checks are suitable because they verify structural validity, temporal correctness, and semantic intent without over-fitting to surface-level wording.

---

### 4. Feedback and Self-Healing (1 mark)
**Question:** Using one actual repair cycle from either part, explain what failure evidence was fed back to the coding agent, what changed in the next attempt, and whether the repair solved the root cause without weakening the specification or harness.

**Response:**  
In **Part 1B**, the initial generation of `agent.py` scored only **73.92%** against `evals/dataset.json` in the harness run (`evidence/eval-results-initial.json`), failing the required 85.0% threshold.

**Failure Evidence Fed Back:**  
The structured evaluation report highlighted two critical failures:
1. `TC-17` & `TC-18` (Adversarial Guardrails): Prompt injection and destructive commands (`"rm -rf /"`) resulted in `CREATE_REMINDER` instead of being intercepted with `intent="REJECT_UNSAFE"` and `safety_flag=True`.
2. `TC-14` (Ambiguous Reschedule): For input `"Snooze my meeting by 30 minutes"`, the regex pattern `re.search(r"#?(\d+)")` misidentified the duration `"30"` as the target reminder ID, setting `reschedule_target_id="30"` instead of requesting clarification.

**What Changed in the Next Attempt:**  
The coding agent modified `src/agent.py` by:
1. Inserting a pre-execution guardrail scanner (`check_adversarial_guardrails`) that intercepts prompt injection patterns and destructive commands before intent routing.
2. Refining reschedule identifier matching to require explicit identifier tokens (`(?:reminder|task|id|\#)\s*(\d+)`), ensuring durations followed by `"minutes"` or `"hours"` do not falsely trigger target ID extraction.

**Root Cause Verification:**  
The re-execution of `.harness/evaluation_runner.py` produced an aggregate composite score of **100.00%** across all 18 cases (`evidence/eval-results.json`). The repair resolved the root cause programmatically without weakening acceptance criteria, altering test cases, or modifying the 85.0% threshold.

---

### 5. Human Accountability (1 mark)
**Question:** Identify one limitation or residual risk that remained even after the harness reported PASS. Explain the final human ACCEPT/REJECT decision and what additional control you would introduce before using the application in a higher-risk or production setting.

**Response:**  
**Residual Risk Identified:**  
Despite achieving a 100% automated harness PASS on both applications, a significant residual risk in **Part 1B** is **statelessness and multi-turn conversational ambiguity**. In production, users rarely speak in isolated single-turn prompts; when the agent returns `intent="REQUEST_CLARIFICATION"` (e.g. asking *"What time on Monday would you like to receive the reminder?"*), the agent currently has no conversation memory or session state to bind the user's subsequent reply (*"at 3pm"*) back to the original task (*"visit the dentist"*). Additionally, semantic token-overlap (Jaccard similarity) can be fooled by negation boundary cases (e.g., *"Do not remind me to call John"* shares 100% tokens with *"Remind me to call John"*).

**Final Human ACCEPT/REJECT Decision:**  
The decision was **ACCEPT for bounded scope deployment**, justified because the applications strictly satisfied all constitutional constraints, passed 100% of deterministic unit/contract tests, and demonstrated reliable refusal of prompt injections and destructive shell commands.

**Additional Control for Production:**  
Before production release in a mission-critical environment, I would introduce:
1. **Stateful Session Context:** A session cache (e.g., Redis) to track clarification state across conversational turns.
2. **Dual-Model LLM-as-a-Judge with Polarity Guard:** An independent small evaluator model specifically checking semantic negation and sentiment polarity to prevent unintended task scheduling from negated requests.
3. **Deterministic Human-in-the-Loop Confirmation:** For tasks classified as high impact or involving calendar mutations, requiring explicit one-click confirmation before scheduling.
