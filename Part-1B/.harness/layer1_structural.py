"""Layer 1: Structural Validation for Part 1B.

Validates that raw AI output is valid JSON and strictly satisfies the Pydantic
schema contracts (field types, enums, nullability).
"""
import json
from typing import Dict, Any, Tuple
from pydantic import ValidationError
from src.schemas import ReminderAgentResponse


def evaluate_layer1(output_data: Dict[str, Any]) -> Tuple[bool, float, list]:
    """Validates structural schema conformance.
    Returns: (passed: bool, score: float [0.0 - 1.0], errors: list[str])
    """
    errors = []
    try:
        validated = ReminderAgentResponse(**output_data)
        return (True, 1.0, [])
    except ValidationError as e:
        for err in e.errors():
            loc = " -> ".join(str(x) for x in err.get("loc", []))
            msg = err.get("msg", "Validation error")
            errors.append(f"Schema error at '{loc}': {msg}")
        return (False, 0.0, errors)
    except Exception as e:
        errors.append(f"Unexpected structural failure: {e}")
        return (False, 0.0, errors)
