"""Pydantic schemas and output contracts for Part 1B Natural-Language Reminder Agent."""
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class IntentEnum(str, Enum):
    CREATE_REMINDER = "CREATE_REMINDER"
    RESCHEDULE_REMINDER = "RESCHEDULE_REMINDER"
    CANCEL_REMINDER = "CANCEL_REMINDER"
    REQUEST_CLARIFICATION = "REQUEST_CLARIFICATION"
    REJECT_UNSAFE = "REJECT_UNSAFE"


class PriorityEnum(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ReminderItem(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Clean summary of the reminder task")
    due_datetime: str = Field(..., description="ISO 8601 UTC string e.g. 2026-11-14T17:00:00Z")
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM)
    tags: List[str] = Field(default_factory=list)

    @field_validator("due_datetime")
    @classmethod
    def validate_iso_datetime(cls, v: str) -> str:
        try:
            # Must parse as valid ISO datetime
            clean_str = v.replace("Z", "+00:00")
            datetime.fromisoformat(clean_str)
            return v
        except Exception as e:
            raise ValueError(f"Invalid ISO 8601 timestamp '{v}': {e}")


class ReminderAgentResponse(BaseModel):
    intent: IntentEnum
    reminder: Optional[ReminderItem] = None
    reschedule_target_id: Optional[str] = None
    requires_clarification: bool = False
    clarification_prompt: Optional[str] = None
    safety_flag: bool = False
    confidence: float = Field(..., ge=0.0, le=1.0)
