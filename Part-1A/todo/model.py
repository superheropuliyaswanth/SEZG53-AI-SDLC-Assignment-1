"""Domain models and data definitions for Smart Todo & Task CLI (Part 1A)."""
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict, Any


class Status(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Priority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

    @property
    def rank(self) -> int:
        ranks = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
        return ranks.get(self.value, 1)


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    status: Status = Status.TODO
    priority: Priority = Priority.MEDIUM
    tags: List[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        data["priority"] = self.priority.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        return cls(
            id=int(data["id"]),
            title=str(data["title"]),
            description=str(data.get("description", "")),
            status=Status(data.get("status", Status.TODO.value)),
            priority=Priority(data.get("priority", Priority.MEDIUM.value)),
            tags=list(data.get("tags", [])),
            created_at=str(data.get("created_at", "")),
            updated_at=str(data.get("updated_at", ""))
        )
