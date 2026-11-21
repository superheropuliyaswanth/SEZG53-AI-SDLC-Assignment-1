# Task Breakdown & Acceptance Criteria (Part 1B)

## Tasks

| Task ID | Component | Description | Acceptance Criteria |
|---|---|---|---|
| T-201 | `schemas.py` | Define Pydantic models for request & response | Strict validation of enums, ISO dates, nullability |
| T-202 | `prompts/` | Author system prompt and safety guardrails | Explicit clarification instructions and refusal boundaries |
| T-203 | `evals/dataset.json` | Curate 18 evaluation cases covering 6 categories | Normal, boundary, ambiguous, missing info, malformed, adversarial |
| T-204 | `agent.py` | Implement agent parser with date resolution & rules | Handles relative time, tags, intent classification, safety guard |
| T-205 | `.harness/` | Implement 3-layer evaluators and runner | Layer 1 (schema), Layer 2 (invariants), Layer 3 (semantics) + 85% threshold |
| T-206 | `evidence/` | Execute harness, capture initial failure, record repair, log results | Detailed trace of initial failure (<85%), repair, re-evaluation (>90%), human review |
