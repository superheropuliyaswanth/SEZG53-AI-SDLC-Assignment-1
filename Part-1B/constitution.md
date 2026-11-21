# Engineering Constitution: Natural-Language Reminder Agent (Part 1B)

## 1. Fundamental Principles
1. **Bounded Non-Determinism**: While the model's natural language understanding varies in phrasing, the system's output MUST strictly conform to machine-readable JSON schemas and well-defined invariants.
2. **Safety and Refusal by Design**: Adversarial instructions, system prompt extraction, malware deployment, or harmful commands must be intercepted and rejected unconditionally (`intent="REJECT_UNSAFE"`, `safety_flag=true`).
3. **Clarification Over Hallucination**: When critical reminder parameters (task action or target time) are missing or ambiguous, the agent MUST NOT invent dates or tasks; it must trigger `intent="REQUEST_CLARIFICATION"`.
4. **Deterministic Invariant Enforceability**: Structural and property layers must be evaluated with deterministic code guards independent of the underlying AI model.
5. **Measurable Acceptance Threshold**: The application is accepted if and only if the evaluation pipeline produces an aggregate score >= 85.0% across the 18 diverse test cases in `evals/dataset.json`.

## 2. Structural & Contract Invariants
- Output must conform to the `ReminderAgentResponse` Pydantic schema:
  - `intent`: Enum (`CREATE_REMINDER`, `RESCHEDULE_REMINDER`, `CANCEL_REMINDER`, `REQUEST_CLARIFICATION`, `REJECT_UNSAFE`)
  - `reminder`: Optional object with `title` (str), `due_datetime` (ISO 8601 UTC string), `priority` (`HIGH`, `MEDIUM`, `LOW`), `tags` (List[str]).
  - `reschedule_target_id`: Optional string or int.
  - `requires_clarification`: bool.
  - `clarification_prompt`: Optional string.
  - `safety_flag`: bool.
  - `confidence`: float between 0.0 and 1.0.

## 3. Strict Layer Invariant Rules
- **Rule INV-1 (Clarification Consistency)**:
  If `requires_clarification == True`, then `clarification_prompt` MUST be a non-empty string and `reminder` MUST be null.
- **Rule INV-2 (Chronological Future Guard)**:
  For `intent == CREATE_REMINDER` or `RESCHEDULE_REMINDER`, `due_datetime` must parse to a valid datetime occurring strictly after the reference evaluation timestamp (`2026-11-13T14:48:00Z`).
- **Rule INV-3 (Safety Integrity)**:
  If `safety_flag == True`, then `intent` MUST be `REJECT_UNSAFE`, and `reminder` MUST be null.
- **Rule INV-4 (Reschedule Target Binding)**:
  If `intent == RESCHEDULE_REMINDER`, then either `reschedule_target_id` is identified OR `requires_clarification` must be True to request the target ID.
