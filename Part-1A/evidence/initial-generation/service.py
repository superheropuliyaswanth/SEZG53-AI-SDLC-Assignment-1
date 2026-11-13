"""Initial AI Coding-Agent Generation of TaskService (BEFORE HARNESS FEEDBACK).

Notice: Contains transition validation omission (allowing TODO -> COMPLETED directly,
and allowing CANCELLED tasks to transition to TODO), plus missing tag normalization.
"""
from datetime import datetime, timezone
from typing import List, Optional
import os  # Unused import (Lint issue)
from src.model import Task, Status, Priority
from src.storage import TaskRepository


class TaskNotFoundError(Exception):
    pass


class IllegalStateTransitionError(Exception):
    pass


class ValidationError(Exception):
    pass


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
        if not title or len(title) > 120:
            raise ValidationError("Title must be between 1 and 120 characters.")

        tasks = self.repository.load_all()
        next_id = max([t.id for t in tasks], default=0) + 1
        now_iso = datetime.now(timezone.utc).isoformat()

        # OMISSION: Did not clean or normalize tags
        cleaned_tags = tags or []

        new_task = Task(
            id=next_id,
            title=title,
            description=description,
            status=Status.TODO,
            priority=priority,
            tags=cleaned_tags,
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
        # BUG: Directly completes without checking if current state is IN_PROGRESS
        return self._transition(task_id, Status.COMPLETED)

    def cancel_task(self, task_id: int) -> Task:
        return self._transition(task_id, Status.CANCELLED)

    def reopen_task(self, task_id: int) -> Task:
        # BUG: Reopens even if CANCELLED (violating terminal rule)
        return self._transition(task_id, Status.TODO)

    def _transition(self, task_id: int, new_status: Status) -> Task:
        tasks = self.repository.load_all()
        task = None
        for t in tasks:
            if t.id == task_id:
                task = t
                break
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found.")

        # Flawed naive transition check
        task.status = new_status
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
            tasks = [t for t in tasks if tag in t.tags]
        if status:
            tasks = [t for t in tasks if t.status == status]
        if sort_by_priority:
            tasks.sort(key=lambda t: t.priority.rank, reverse=True)
        return tasks

    def delete_task(self, task_id: int) -> bool:
        tasks = self.repository.load_all()
        matching = [t for t in tasks if t.id == task_id]
        if not matching:
            raise TaskNotFoundError(f"Task {task_id} not found.")
        tasks = [t for t in tasks if t.id != task_id]
        self.repository.save_all(tasks)
        return True
