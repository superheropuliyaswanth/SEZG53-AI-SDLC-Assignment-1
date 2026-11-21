"""Semantic Evaluator (Layer 3 Semantic & Quality Validation for Part 1B).

Evaluates natural language semantic quality, intent classification accuracy,
and key information extraction without relying on brittle exact string equality.
"""
import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from layer3_semantic import evaluate_layer3

evaluate_semantics = evaluate_layer3

__all__ = ["evaluate_layer3", "evaluate_semantics"]
