"""Schema Validator (Layer 1 Structural Validation for Part 1B).

Validates that raw AI output is valid JSON and strictly satisfies the Pydantic
schema contracts (field types, enums, nullability).
"""
import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from layer1_structural import evaluate_layer1

validate_schema = evaluate_layer1

__all__ = ["evaluate_layer1", "validate_schema"]
