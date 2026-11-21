# Technical Plan: Architecture & Evaluation Harness (Part 1B)

## 1. Module Layout
```
Part-1B/
├── src/
│   ├── __init__.py
│   ├── schemas.py      # Pydantic schemas (Layer 1 contract)
│   ├── agent.py        # Natural Language Reminder Agent & parser logic
│   └── rules.py        # Invariant & safety guardrail checks
├── prompts/
│   ├── system_prompt.txt
│   └── guardrails.txt
├── evals/
│   └── dataset.json    # 18 gold-standard evaluation cases
├── .harness/
│   ├── layer1_structural.py
│   ├── layer2_property.py
│   ├── layer3_semantic.py
│   └── evaluation_runner.py
└── evidence/
    ├── initial-generation/
    ├── final-generation/
    ├── eval-results-initial.json
    ├── eval-results.json
    └── harness-log.md
```

## 2. 3-Layer Single Evaluation Pipeline Architecture
```
  [evals/dataset.json]
           │
           ▼
  [Reminder Agent / Inference]
           │
           ▼
  [Generated Response JSON]
           │
   ┌───────┴───────┐
   ▼               ▼               ▼
[Layer 1:       [Layer 2:       [Layer 3:
 Structural      Invariant &     Semantic /
 Pydantic        Property        Quality
 Validation]     Guards]         Heuristics]
   │               │               │
   └───────┬───────┴───────────────┘
           ▼
[Aggregate Score: L1(30%) + L2(40%) + L3(30%)]
           │
      Score >= 85.0%?
      ┌────┴────┐
     YES        NO
      │          │
      ▼          ▼
   [PASS]      [FAIL] -> Structured Evidence -> Self-Healing Repair
```
