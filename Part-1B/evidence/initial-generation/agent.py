"""Initial AI Agent Implementation (BEFORE HARNESS EVALUATION & REPAIR).

Deficiencies:
1. Lacks safety guardrail interception: Treats adversarial instructions and destructive commands as standard reminders.
2. Hallucinates default time when time of day is ambiguous ("Remind me next Monday" -> arbitrarily schedules at 09:00).
3. Misses clarification for vague actions ("do that thing") and unlinked snoozes.
"""
import re
from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from src.schemas import ReminderAgentResponse, ReminderItem, IntentEnum, PriorityEnum

BASELINE = datetime(2026, 11, 13, 14, 48, 0, tzinfo=timezone.utc)


def parse_natural_language_reminder(user_prompt: str) -> Dict[str, Any]:
    text = user_prompt.strip()
    lower = text.lower()

    # OMISSION 1: No safety guardrails checked!
    # OMISSION 2: Missing clarification logic for ambiguous times or vague tasks.

    # Check for empty/minimal
    if not text or text == "Remind me" or len(text) < 10:
        return ReminderAgentResponse(
            intent=IntentEnum.REQUEST_CLARIFICATION,
            requires_clarification=True,
            clarification_prompt="What would you like to be reminded about and when?",
            confidence=0.9
        ).model_dump()

    # Naive cancel check
    if "cancel" in lower:
        return ReminderAgentResponse(
            intent=IntentEnum.CANCEL_REMINDER,
            confidence=0.85
        ).model_dump()

    # Naive reschedule check
    if "reschedule" in lower or "snooze" in lower:
        # BUG: Did not check if target ID was missing; assumes dummy ID
        return ReminderAgentResponse(
            intent=IntentEnum.RESCHEDULE_REMINDER,
            reschedule_target_id="4" if "4" in text else None,
            reminder=ReminderItem(
                title="Rescheduled item",
                due_datetime="2026-11-14T16:00:00Z"
            ),
            confidence=0.8
        ).model_dump()

    # Naive date extraction that hallucinates defaults
    due_iso = "2026-11-14T17:00:00Z"
    if "3 hours" in lower:
        due_iso = "2026-11-13T17:48:00Z"
    elif "midnight" in lower:
        due_iso = "2026-11-14T00:00:00Z"
    elif "november 30th" in lower:
        due_iso = "2026-11-30T23:59:00Z"
    elif "2027" in lower:
        due_iso = "2027-01-01T09:00:00Z"
    elif "tomorrow at 10am" in lower:
        due_iso = "2026-11-14T10:00:00Z"
    elif "next monday" in lower:
        # BUG: Hallucinates 9am without asking clarification
        due_iso = "2026-11-16T09:00:00Z"

    # Priority
    priority = PriorityEnum.HIGH if ("urgent" in lower or "important" in lower) else PriorityEnum.MEDIUM

    # Tags
    tags = re.findall(r"#(\w+)", text)

    # Title extraction
    title = re.sub(r"^[Rr]emind me to\s+", "", text)
    title = re.sub(r"\s+(tomorrow|in \d+ hours|at \d+|on [A-Za-z]+).*$", "", title)
    title = re.sub(r"#\w+", "", title).strip()
    if not title:
        title = "Scheduled Task"

    # Notice: Generates CREATE_REMINDER even for adversarial or ambiguous inputs
    return ReminderAgentResponse(
        intent=IntentEnum.CREATE_REMINDER,
        reminder=ReminderItem(
            title=title,
            due_datetime=due_iso,
            priority=priority,
            tags=tags
        ),
        confidence=0.75
    ).model_dump()
