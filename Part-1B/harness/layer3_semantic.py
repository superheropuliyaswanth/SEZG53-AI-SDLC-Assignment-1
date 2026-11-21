"""Layer 3: Semantic & Quality Evaluator for Part 1B.

Evaluates natural language semantic quality, intent classification accuracy,
and key information extraction without relying on brittle exact string equality.
"""
from typing import Dict, Any, Tuple
import re


def tokenize(text: str) -> set:
    if not text:
        return set()
    clean = re.sub(r"[^\w\s]", "", text.lower())
    return set(clean.split())


def jaccard_similarity(set_a: set, set_b: set) -> float:
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a.intersection(set_b))
    union = len(set_a.union(set_b))
    return intersection / union if union > 0 else 0.0


def evaluate_layer3(output_data: Dict[str, Any], test_case: Dict[str, Any]) -> Tuple[bool, float, list]:
    """Computes semantic quality score based on intent match, token overlap, and property alignment.
    Returns: (passed: bool, score: float [0.0 - 1.0], notes: list[str])
    """
    notes = []
    points = 0.0
    total_weights = 1.0

    actual_intent = output_data.get("intent")
    expected_intent = test_case.get("expected_intent")

    # 1. Intent Alignment (Weight: 0.50)
    if actual_intent == expected_intent:
        points += 0.50
    else:
        notes.append(f"Intent mismatch: expected '{expected_intent}', got '{actual_intent}'")

    # 2. Key Token & Semantic Fidelity (Weight: 0.35)
    expected_props = test_case.get("expected_properties", {})
    key_tokens = set(expected_props.get("key_tokens", []))
    
    if key_tokens and output_data.get("reminder"):
        title = output_data["reminder"].get("title", "")
        title_tokens = tokenize(title)
        overlap = jaccard_similarity(key_tokens, title_tokens)
        if overlap >= 0.3 or key_tokens.issubset(title_tokens):
            points += 0.35
        else:
            points += 0.35 * max(0.0, overlap / 0.3)
            notes.append(f"Title token overlap low ({overlap:.2f}) for '{title}' vs expected {key_tokens}")
    elif expected_props.get("clarification_keywords") and output_data.get("clarification_prompt"):
        prompt = output_data["clarification_prompt"].lower()
        matched = [kw for kw in expected_props["clarification_keywords"] if kw in prompt]
        if matched:
            points += 0.35
        else:
            points += 0.15
            notes.append("Clarification prompt did not contain recommended clarifying keywords.")
    else:
        # If no key tokens expected (e.g. guardrail refusal or cancel), award weight if intent aligned
        if actual_intent == expected_intent:
            points += 0.35

    # 3. Priority and Tag Alignment (Weight: 0.15)
    expected_prio = expected_props.get("expected_priority")
    if expected_prio and output_data.get("reminder"):
        actual_prio = output_data["reminder"].get("priority")
        if actual_prio == expected_prio:
            points += 0.15
        else:
            notes.append(f"Priority mismatch: expected '{expected_prio}', got '{actual_prio}'")
    else:
        points += 0.15

    score = min(1.0, max(0.0, points / total_weights))
    passed = (score >= 0.70)
    return (passed, score, notes)
