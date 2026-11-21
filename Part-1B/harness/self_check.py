"""Harness Self-Check Suite for Part 1B (Non-Deterministic Evaluation).

Demonstrates that each of the 3 evaluation layers independently catches defects:
1. Layer 1 (Structural): Tested with invalid JSON/Pydantic types -> Expect FAIL
2. Layer 2 (Invariants): Tested with Rule INV-1 violation (clarification true + reminder present) -> Expect FAIL
3. Layer 3 (Semantic): Tested with intent mismatch and zero token overlap -> Expect FAIL
4. Clean Run: Evaluates production agent across dataset -> Expect PASS (>85%)
"""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PART1B_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PART1B_DIR not in sys.path:
    sys.path.insert(0, PART1B_DIR)

from layer1_structural import evaluate_layer1
from layer2_property import evaluate_layer2
from layer3_semantic import evaluate_layer3
from evaluation_runner import run_evaluation_pipeline


def run_part1b_self_check():
    os.chdir(PART1B_DIR)
    print("=" * 80)
    print("HARNESS SELF-CHECK PART 1B: Verifying 3-layer sensitivity to defects")
    print("=" * 80)
    results = []

    # 1. Layer 1 test: Invalid Pydantic types / missing fields
    bad_schema = {"intent": "INVALID_INTENT_NAME", "confidence": 1.5}
    l1_pass, l1_score, l1_errors = evaluate_layer1(bad_schema)
    results.append(("Layer 1 (Structural)", "Invalid Intent Enum & Confidence > 1.0", "FAIL", "FAIL" if not l1_pass else "PASS", not l1_pass))

    # 2. Layer 2 test: Invariant INV-1 violation (clarification true + reminder object exists)
    bad_invariant = {
        "intent": "REQUEST_CLARIFICATION",
        "requires_clarification": True,
        "clarification_prompt": "What time?",
        "reminder": {"title": "Should Not Exist", "due_datetime": "2026-11-14T10:00:00Z"},
        "confidence": 0.9
    }
    dummy_case = {"expected_properties": {"requires_clarification": True}}
    l2_pass, l2_score, l2_errors = evaluate_layer2(bad_invariant, dummy_case)
    results.append(("Layer 2 (Invariants)", "Rule INV-1: Clarification true but reminder not null", "FAIL", "FAIL" if not l2_pass else "PASS", not l2_pass))

    # 3. Layer 3 test: Intent mismatch & zero token overlap
    bad_semantic = {
        "intent": "CANCEL_REMINDER",
        "confidence": 0.95
    }
    semantic_case = {
        "expected_intent": "CREATE_REMINDER",
        "expected_properties": {"key_tokens": ["submit", "taxes"]}
    }
    l3_pass, l3_score, l3_notes = evaluate_layer3(bad_semantic, semantic_case)
    results.append(("Layer 3 (Semantic)", "Intent mismatch (CANCEL vs CREATE) & 0 token overlap", "FAIL", "FAIL" if not l3_pass else "PASS", not l3_pass))

    # 4. Clean Run on production dataset
    dpath = os.path.join(PART1B_DIR, "evals", "dataset.json")
    rep = run_evaluation_pipeline(dpath)
    clean_passed = (rep["overall_status"] == "PASS")
    results.append(("All 3 Layers Combined", f"Production Agent on 18 cases (Score: {rep['aggregate_score']}%)", "PASS", "PASS" if clean_passed else "FAIL", clean_passed))

    # Print summary table
    print("\n" + f"{'Layer / Target':<25} | {'Tested Input Scenario':<45} | {'Exp':<5} | {'Obs':<5} | {'Status'}")
    print("-" * 95)
    for layer, scenario, exp, obs, ok in results:
        status_str = "VERIFIED" if ok else "FAILED"
        print(f"{layer:<25} | {scenario:<45} | {exp:<5} | {obs:<5} | {status_str}")
    print("=" * 95)

    all_verified = all(r[4] for r in results)
    print(f"PART 1B SELF-CHECK RESULT: {'ALL 3 EVALUATION LAYERS PROVEN SENSITIVE' if all_verified else 'SELF-CHECK FAILED'}\n")
    return all_verified


if __name__ == "__main__":
    ok = run_part1b_self_check()
    sys.exit(0 if ok else 1)
