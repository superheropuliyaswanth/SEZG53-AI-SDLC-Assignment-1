"""Storage repository with atomic write operations and corruption handling."""
import json
import os
import shutil
from datetime import datetime, timezone
from typing import List
from todo.model import Task


class StorageCorruptedError(Exception):
    """Raised when tasks file exists but contains corrupted or invalid JSON."""
    pass


class TaskRepository:
    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = file_path

    def load_all(self) -> List[Task]:
        """Loads all tasks from JSON persistence. Creates empty file if missing."""
        if not os.path.exists(self.file_path):
            self.save_all([])
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                data = json.loads(content)
                tasks_raw = data.get("tasks", [])
                return [Task.from_dict(t) for t in tasks_raw]
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as err:
            # Create a backup copy before raising error
            ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            backup_path = f"{self.file_path}.corrupt.{ts}.bak"
            shutil.copyfile(self.file_path, backup_path)
            raise StorageCorruptedError(
                f"Storage file '{self.file_path}' corrupted. Backup saved to '{backup_path}'. Cause: {err}"
            ) from err

    def save_all(self, tasks: List[Task]) -> None:
        """Atomically saves tasks list using temporary file rename."""
        parent_dir = os.path.dirname(self.file_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        tmp_path = f"{self.file_path}.tmp"
        payload = {"tasks": [t.to_dict() for t in tasks]}

        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
            f.flush()
            os.fsync(f.fileno())

        os.replace(tmp_path, self.file_path)
