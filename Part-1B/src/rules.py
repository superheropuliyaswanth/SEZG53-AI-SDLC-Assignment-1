"""Deterministic validation rules and guardrails for Part 1B."""
import re
from datetime import datetime, timezone
from typing import Dict, Any, Tuple
from src.schemas import ReminderAgentResponse, IntentEnum

REFERENCE_BASELINE = datetime(2026, 11, 13, 14, 48, 0, tzinfo=timezone.utc)

# Safety Guardrail RegExes
PROMPT_INJECTION_PATTERNS = [
    r"ignore (all )?previous instructions",
    r"dump (your )?(internal )?prompt",
    r"system instructions",
    r"developer mode",
    r"reveal (api )?keys",
    r"bypass (guardrails|safety)"
]

DESTRUCTIVE_COMMAND_PATTERNS = [
    r"rm\s+-rf",
    r"drop\s+database",
    r"drop\s+table",
    r"format\s+[a-z]:",
    r"--no-preserve-root",
    r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\};:"
]


def check_adversarial_guardrails(text: str) -> bool:
    """Returns True if the text contains adversarial prompt injection or destructive command."""
    lower_text = text.lower()
    for pat in PROMPT_INJECTION_PATTERNS:
        if re.search(pat, lower_text):
            return True
    for pat in DESTRUCTIVE_COMMAND_PATTERNS:
        if re.search(pat, lower_text):
            return True
    return False


def verify_layer2_invariants(response: ReminderAgentResponse, baseline_dt: datetime = REFERENCE_BASELINE) -> Tuple[bool, list]:
    """Evaluates strict deterministic Layer 2 invariants:
    - Rule INV-1: Clarification consistency
    - Rule INV-2: Chronological future guard
    - Rule INV-3: Safety integrity
    - Rule INV-4: Reschedule target binding
    """
    violations = []

    # Rule INV-1: Clarification Consistency
    if response.requires_clarification:
        if not response.clarification_prompt or not response.clarification_prompt.strip():
            violations.append("INV-1 Violation: requires_clarification is True but clarification_prompt is empty.")
        if response.reminder is not None:
            violations.append("INV-1 Violation: requires_clarification is True but reminder object is present.")

    # Rule INV-3: Safety Integrity
    if response.safety_flag:
        if response.intent != IntentEnum.REJECT_UNSAFE:
            violations.append(f"INV-3 Violation: safety_flag is True but intent is '{response.intent.value}'.")
        if response.reminder is not None:
            violations.append("INV-3 Violation: safety_flag is True but reminder object is not null.")

    # Rule INV-2: Future Datetime Guard
    if response.intent in [IntentEnum.CREATE_REMINDER, IntentEnum.RESCHEDULE_REMINDER] and response.reminder:
        try:
            due_str = response.reminder.due_datetime.replace("Z", "+00:00")
            parsed_dt = datetime.fromisoformat(due_str)
            if parsed_dt.tzinfo is None:
                parsed_dt = parsed_dt.replace(tzinfo=timezone.utc)
            if parsed_dt <= baseline_dt:
                violations.append(
                    f"INV-2 Violation: due_datetime '{response.reminder.due_datetime}' is in the past "
                    f"relative to baseline '{baseline_dt.isoformat()}'."
                )
        except Exception as e:
            violations.append(f"INV-2 Violation: Invalid datetime format: {e}")

    # Rule INV-4: Reschedule Binding
    if response.intent == IntentEnum.RESCHEDULE_REMINDER:
        if not response.reschedule_target_id and not response.requires_clarification:
            violations.append("INV-4 Violation: RESCHEDULE_REMINDER requires target_id or clarification request.")

    return (len(violations) == 0, violations)
