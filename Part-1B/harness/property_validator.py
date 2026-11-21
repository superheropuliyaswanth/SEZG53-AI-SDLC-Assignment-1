"""Property Validator (Layer 2 Invariant and Property Validation for Part 1B).

Validates deterministic behavioral properties:
- INV-1: Clarification consistency
- INV-2: Future datetime guard
- INV-3: Safety integrity
- INV-4: Reschedule target binding
"""
import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from layer2_property import evaluate_layer2

validate_properties = evaluate_layer2

__all__ = ["evaluate_layer2", "validate_properties"]
