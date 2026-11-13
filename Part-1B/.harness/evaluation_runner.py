"""Unified Non-Deterministic Evaluation Runner for Part 1B.

Orchestrates the 3-Layer Harness:
- Layer 1: Structural Validation (Weight 30%)
- Layer 2: Invariants & Guardrails (Weight 40%)
- Layer 3: Semantic / Quality Evaluation (Weight 30%)

Compares overall aggregate score against declared threshold (85.0%).
Generates structured JSON evidence and actionable diagnostic feedback.
"""
import os
import sys
import json
from datetime import datetime, timezone

# Ensure Part-1B is in path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PART1B_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PART1B_DIR not in sys.path:
    sys.path.insert(0, PART1B_DIR)

from layer1_structural import evaluate_layer1
from layer2_property import evaluate_layer2
from layer3_semantic import evaluate_layer3
from src.agent import parse_natural_language_reminder

ACCEPTANCE_THRESHOLD = 85.0  # Percentage required to PASS


def run_evaluation_pipeline(dataset_path: str, evidence_output_path: str = None) -> dict:
    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    print("=" * 80)
    print("RUNNING 3-LAYER NON-DETERMINISTIC EVALUATION HARNESS - PART 1B")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print(f"Evaluation Dataset: {len(dataset)} test cases | Threshold: {ACCEPTANCE_THRESHOLD}%")
    print("=" * 80)

    case_results = []
    total_l1_score = 0.0
    total_l2_score = 0.0
    total_l3_score = 0.0
    total_composite_score = 0.0

    print(f"{'Case ID':<8} | {'Category':<22} | {'L1 (30%)':<8} | {'L2 (40%)':<8} | {'L3 (30%)':<8} | {'Score':<8} | {'Verdict'}")
    print("-" * 80)

    for case in dataset:
        case_id = case["id"]
        category = case["category"]
        user_input = case["input"]

        # 1. AI Application / Model Call
        generated_output = parse_natural_language_reminder(user_input)

        # 2. Layer 1: Structural Validation
        l1_pass, l1_score, l1_errors = evaluate_layer1(generated_output)

        # 3. Layer 2: Invariant & Property Validation
        l2_pass, l2_score, l2_errors = evaluate_layer2(generated_output, case)

        # 4. Layer 3: Semantic & Quality Evaluation
        l3_pass, l3_score, l3_notes = evaluate_layer3(generated_output, case)

        # 5. Composite Score Calculation
        composite = (0.30 * l1_score) + (0.40 * l2_score) + (0.30 * l3_score)
        composite_pct = composite * 100.0
        case_verdict = "PASS" if composite_pct >= 70.0 and l1_pass and l2_pass else "FAIL"

        total_l1_score += l1_score
        total_l2_score += l2_score
        total_l3_score += l3_score
        total_composite_score += composite_pct

        print(f"{case_id:<8} | {category:<22} | {l1_score * 100:>7.1f}% | {l2_score * 100:>7.1f}% | {l3_score * 100:>7.1f}% | {composite_pct:>6.1f}% | {case_verdict}")

        case_results.append({
            "id": case_id,
            "category": category,
            "input": user_input,
            "generated_output": generated_output,
            "layer1": {"passed": l1_pass, "score": l1_score, "errors": l1_errors},
            "layer2": {"passed": l2_pass, "score": l2_score, "violations": l2_errors},
            "layer3": {"passed": l3_pass, "score": l3_score, "notes": l3_notes},
            "composite_score": round(composite_pct, 2),
            "verdict": case_verdict
        })

    n = len(dataset)
    avg_l1 = (total_l1_score / n) * 100.0
    avg_l2 = (total_l2_score / n) * 100.0
    avg_l3 = (total_l3_score / n) * 100.0
    aggregate_score = total_composite_score / n
    overall_status = "PASS" if aggregate_score >= ACCEPTANCE_THRESHOLD else "FAIL"
    human_decision = "ACCEPT" if overall_status == "PASS" else "REJECT"

    print("=" * 80)
    print(f"AVERAGE LAYER 1 (Structural):  {avg_l1:.2f}%")
    print(f"AVERAGE LAYER 2 (Invariants):  {avg_l2:.2f}%")
    print(f"AVERAGE LAYER 3 (Semantic):    {avg_l3:.2f}%")
    print(f"AGGREGATE COMPOSITE SCORE:     {aggregate_score:.2f}% (Threshold: {ACCEPTANCE_THRESHOLD}%)")
    print(f"OVERALL EVALUATION VERDICT:    {overall_status} -> Human Decision: {human_decision}")
    print("=" * 80)

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "application": "Part-1B Natural-Language Reminder Agent",
        "threshold_declared": ACCEPTANCE_THRESHOLD,
        "aggregate_score": round(aggregate_score, 2),
        "overall_status": overall_status,
        "human_decision": human_decision,
        "layer_averages": {
            "layer1_structural": round(avg_l1, 2),
            "layer2_invariants": round(avg_l2, 2),
            "layer3_semantic": round(avg_l3, 2)
        },
        "total_cases": n,
        "passed_cases": sum(1 for c in case_results if c["verdict"] == "PASS"),
        "cases": case_results
    }

    if evidence_output_path:
        os.makedirs(os.path.dirname(evidence_output_path), exist_ok=True)
        with open(evidence_output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"Evaluation report saved to: {evidence_output_path}")

    return report


if __name__ == "__main__":
    dpath = os.path.join(PART1B_DIR, "evals", "dataset.json")
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PART1B_DIR, "evidence", "eval-results.json")
    rep = run_evaluation_pipeline(dpath, out)
    sys.exit(0 if rep["overall_status"] == "PASS" else 1)
