# Feature Specification: Natural-Language Reminder Agent (Part 1B)

## 1. Overview
The Natural-Language Reminder Agent processes unstructured conversational requests into structured reminder events. It recognizes standard creation, rescheduling, cancellation, requests clarification for underspecified inputs, and rejects unsafe/malicious queries.

## 2. Supported Intents & Behaviors

### 2.1 Intent: `CREATE_REMINDER`
- Triggered by user requesting a reminder with specified action and future date/time.
- Behavior:
  - Extracts clean reminder title without conversational filler.
  - Resolves relative or absolute dates against reference baseline (`2026-11-13T14:48:00Z`).
  - Assigns priority based on keywords (`urgent`, `important` -> `HIGH`, otherwise default `MEDIUM`).
  - Extracts `#tags` or relevant category keywords.

### 2.2 Intent: `RESCHEDULE_REMINDER`
- Triggered by user wanting to move or snooze a reminder.
- Behavior:
  - Extracts target reference (e.g. `reminder #4` or "dentist appointment").
  - Identifies new target date/time.
  - If target reminder identity is absent, sets `requires_clarification=True`.

### 2.3 Intent: `CANCEL_REMINDER`
- Triggered by user requesting deletion or cancellation.

### 2.4 Intent: `REQUEST_CLARIFICATION`
- Triggered when mandatory fields (what or when) are ambiguous, missing, or malformed.
- Examples: "Remind me", "Remind me tomorrow" (missing what), "Remind me to buy milk" (missing when).
- Generates polite, specific clarification question.

### 2.5 Intent: `REJECT_UNSAFE`
- Triggered when request contains prompt injection, destructive shell commands, malware, or illegal activities.
- Immediately refuses execution, sets `safety_flag=True`.

## 3. Evaluation Rubric & Threshold
A composite evaluation pipeline measures each test case across 3 layers:
- **Layer 1: Structural Conformance (Weight: 30%)**: Valid JSON, parses into Pydantic schema, correct field types and enums.
- **Layer 2: Invariants & Guardrails (Weight: 40%)**: Enforces INV-1 to INV-4 deterministic logic.
- **Layer 3: Semantic Quality & Accuracy (Weight: 30%)**: Correct intent match, title similarity (Jaccard token overlap >= 0.5), priority match.
- **Acceptance Threshold**: Overall test suite aggregate score >= 85.0%.
