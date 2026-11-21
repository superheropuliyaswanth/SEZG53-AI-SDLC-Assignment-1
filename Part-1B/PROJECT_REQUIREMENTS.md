# Part 1B: Natural-Language Reminder Agent - Project Requirements

## Course Context
- Course: AI-Augmented Software Development Life Cycle (SEZG534)
- Assignment: Assignment 1 - Spec-Driven Development & Harness Engineering
- Component: Part 1B - Non-Deterministic AI Application (10 Marks)

## Functional Requirements
1. **Natural Language Understanding**: Parse unstructured, multi-intent, or ambiguous user reminder requests into strict structured JSON.
2. **Mandatory Schema Fields**:
   - `action`: CREATE, SNOOZE, CANCEL, CLARIFY, REJECT
   - `title`: Short normalized task name
   - `due_date`: ISO 8601 UTC timestamp strictly in the future relative to execution reference time
   - `priority`: HIGH, MEDIUM, LOW
   - `tags`: List of lowercase normalized categorization strings
   - `confidence`: Confidence score between 0.0 and 1.0
   - `clarification_needed`: Boolean flag and question string when mandatory fields are missing
3. **Safety & Guardrails**:
   - Intercept prompt injection attacks (e.g., instructions to ignore system prompt or dump keys).
   - Reject destructive commands (e.g., `rm -rf`, DROP DATABASE, system sabotage).
4. **Offline & Live Dual-Mode Inference**:
   - Zero-dependency rule-based fallback engine for offline deterministic evaluation.
   - Live Google Gemini API connectivity via `.env` configuration.
5. **Harness Evaluation**:
   - 3-Layer evaluation: Schema structure, Invariant properties, Semantic similarity.
   - Minimum acceptance score: >= 85.0%.
