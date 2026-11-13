"""Core service layer for Smart Todo & Task CLI (Repaired & Validated).

Enforces deterministic state transitions, tag normalization, and priority sorting.
"""
from datetime import datetime, timezone
from typing import List, Optional, Set, Dict
from src.model import Task, Status, Priority
from src.storage import TaskRepository


class TaskNotFoundError(Exception):
    """Raised when task ID does not exist."""
    pass


class IllegalStateTransitionError(Exception):
    """Raised when an invalid state transition is requested."""
    pass


class ValidationError(Exception):
    """Raised when task parameters fail validation."""
    pass


# Deterministic state machine transition rules per Constitution Section 4
VALID_TRANSITIONS: Dict[Status, Set[Status]] = {
    Status.TODO: {Status.IN_PROGRESS, Status.CANCELLED},
    Status.IN_PROGRESS: {Status.COMPLETED, Status.CANCELLED},
    Status.COMPLETED: {Status.TODO},  # Explicit reopen only
    Status.CANCELLED: set()            # Strictly terminal
}


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        tags: Optional[List[str]] = None
    ) -> Task:
        clean_title = (title or "").strip()
        if not clean_title or len(clean_title) > 120:
            raise ValidationError("Title must be between 1 and 120 characters.")

        tasks = self.repository.load_all()
        next_id = max([t.id for t in tasks], default=0) + 1
        now_iso = datetime.now(timezone.utc).isoformat()

        # Tag normalization: strip whitespace, lowercase, remove duplicates preserving order
        normalized_tags: List[str] = []
        if tags:
            for raw_tag in tags:
                clean = raw_tag.strip().lower()
                if clean and clean not in normalized_tags:
                    normalized_tags.append(clean)

        new_task = Task(
            id=next_id,
            title=clean_title,
            description=description.strip(),
            status=Status.TODO,
            priority=priority,
            tags=normalized_tags,
            created_at=now_iso,
            updated_at=now_iso
        )
        tasks.append(new_task)
        self.repository.save_all(tasks)
        return new_task

    def get_task(self, task_id: int) -> Optional[Task]:
        tasks = self.repository.load_all()
        for t in tasks:
            if t.id == task_id:
                return t
        return None

    def start_task(self, task_id: int) -> Task:
        return self._transition(task_id, Status.IN_PROGRESS)

    def complete_task(self, task_id: int) -> Task:
        return self._transition(task_id, Status.COMPLETED)

    def cancel_task(self, task_id: int) -> Task:
        return self._transition(task_id, Status.CANCELLED)

    def reopen_task(self, task_id: int) -> Task:
        return self._transition(task_id, Status.TODO)

    def _transition(self, task_id: int, target_status: Status) -> Task:
        tasks = self.repository.load_all()
        task = None
        for t in tasks:
            if t.id == task_id:
                task = t
                break

        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found.")

        current_status = task.status
        allowed_targets = VALID_TRANSITIONS.get(current_status, set())

        if target_status not in allowed_targets:
            raise IllegalStateTransitionError(
                f"Illegal transition: Cannot move task {task_id} from '{current_status.value}' "
                f"to '{target_status.value}'. Allowed targets: {[s.value for s in allowed_targets]}"
            )

        task.status = target_status
        task.updated_at = datetime.now(timezone.utc).isoformat()
        self.repository.save_all(tasks)
        return task

    def list_tasks(
        self,
        tag: Optional[str] = None,
        status: Optional[Status] = None,
        sort_by_priority: bool = False
    ) -> List[Task]:
        tasks = self.repository.load_all()

        if tag:
            clean_tag = tag.strip().lower()
            tasks = [t for t in tasks if clean_tag in t.tags]

        if status:
            tasks = [t for t in tasks if t.status == status]

        if sort_by_priority:
            # Sort by Priority rank descending, then created_at ascending, then id ascending
            tasks.sort(key=lambda t: (-t.priority.rank, t.created_at, t.id))

        return tasks

    def delete_task(self, task_id: int) -> bool:
        tasks = self.repository.load_all()
        matching = [t for t in tasks if t.id == task_id]
        if not matching:
            raise TaskNotFoundError(f"Task {task_id} not found.")

        tasks = [t for t in tasks if t.id != task_id]
        self.repository.save_all(tasks)
        return True
