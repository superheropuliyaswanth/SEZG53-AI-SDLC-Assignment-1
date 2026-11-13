"""Unit and Contract Tests for Smart Todo & Task CLI (Part 1A).

Derived directly from .speckit/constitution.md and .speckit/specify.md.
"""
import pytest
import os
import json
import tempfile
from src.model import Task, Status, Priority
from src.storage import TaskRepository, StorageCorruptedError
from src.service import TaskService, IllegalStateTransitionError, TaskNotFoundError, ValidationError


@pytest.fixture
def temp_repo():
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_file = os.path.join(tmpdir, "tasks.json")
        repo = TaskRepository(repo_file)
        yield repo


@pytest.fixture
def service(temp_repo):
    return TaskService(temp_repo)


# =========================================================================
# 1. Model & Data Integrity Tests
# =========================================================================
def test_task_model_serialization():
    task = Task(
        id=1,
        title="Test Task",
        description="A sample description",
        status=Status.TODO,
        priority=Priority.HIGH,
        tags=["work", "backend"],
        created_at="2026-11-13T10:00:00Z",
        updated_at="2026-11-13T10:00:00Z"
    )
    data = task.to_dict()
    assert data["id"] == 1
    assert data["title"] == "Test Task"
    assert data["status"] == "TODO"
    assert data["priority"] == "HIGH"
    assert data["tags"] == ["work", "backend"]

    reconstituted = Task.from_dict(data)
    assert reconstituted.id == task.id
    assert reconstituted.status == Status.TODO
    assert reconstituted.priority == Priority.HIGH


def test_priority_ordering():
    assert Priority.HIGH.rank > Priority.MEDIUM.rank
    assert Priority.MEDIUM.rank > Priority.LOW.rank


# =========================================================================
# 2. Storage & Atomic Persistence Tests
# =========================================================================
def test_storage_initializes_empty_file(temp_repo):
    tasks = temp_repo.load_all()
    assert tasks == []
    assert os.path.exists(temp_repo.file_path)


def test_storage_atomic_save_and_reload(temp_repo):
    task = Task(id=1, title="Persistent Task", status=Status.TODO, priority=Priority.MEDIUM)
    temp_repo.save_all([task])
    
    loaded = temp_repo.load_all()
    assert len(loaded) == 1
    assert loaded[0].id == 1
    assert loaded[0].title == "Persistent Task"


def test_storage_corrupted_backup(temp_repo):
    with open(temp_repo.file_path, "w") as f:
        f.write("{ INVALID JSON DATA }}}")
    
    with pytest.raises(StorageCorruptedError):
        temp_repo.load_all()


# =========================================================================
# 3. Service Layer CRUD & Validation Tests
# =========================================================================
def test_create_task_valid(service):
    task = service.add_task(
        title="Implement Harness",
        description="Write deterministic guards",
        priority=Priority.HIGH,
        tags=["engineering", "python"]
    )
    assert task.id == 1
    assert task.title == "Implement Harness"
    assert task.status == Status.TODO
    assert task.priority == Priority.HIGH
    assert "engineering" in task.tags
    assert task.created_at != ""
    assert task.updated_at != ""


def test_create_task_empty_title_fails(service):
    with pytest.raises(ValidationError):
        service.add_task(title="", description="Empty title test")


def test_create_task_title_too_long_fails(service):
    long_title = "A" * 121
    with pytest.raises(ValidationError):
        service.add_task(title=long_title)


def test_tag_normalization(service):
    task = service.add_task(
        title="Tagged Task",
        tags=["  Urgent  ", "WORK", "backend", "work"]
    )
    # Expected: trimmed, lowercased, deduplicated
    assert sorted(task.tags) == ["backend", "urgent", "work"]


def test_delete_task(service):
    t = service.add_task(title="To be deleted")
    assert service.delete_task(t.id) is True
    assert service.get_task(t.id) is None


def test_delete_nonexistent_task(service):
    with pytest.raises(TaskNotFoundError):
        service.delete_task(999)


# =========================================================================
# 4. Deterministic State Machine Transition Contract Tests
# =========================================================================
def test_valid_lifecycle_transitions(service):
    # TODO -> IN_PROGRESS -> COMPLETED
    task = service.add_task(title="Lifecycle Happy Path")
    assert task.status == Status.TODO

    task = service.start_task(task.id)
    assert task.status == Status.IN_PROGRESS

    task = service.complete_task(task.id)
    assert task.status == Status.COMPLETED


def test_reopen_completed_task(service):
    # COMPLETED -> TODO (Reopen)
    task = service.add_task(title="Task to Reopen")
    service.start_task(task.id)
    service.complete_task(task.id)

    task = service.reopen_task(task.id)
    assert task.status == Status.TODO


def test_cancel_from_todo_and_in_progress(service):
    t1 = service.add_task(title="Cancel from TODO")
    service.cancel_task(t1.id)
    assert service.get_task(t1.id).status == Status.CANCELLED

    t2 = service.add_task(title="Cancel from IN_PROGRESS")
    service.start_task(t2.id)
    service.cancel_task(t2.id)
    assert service.get_task(t2.id).status == Status.CANCELLED


def test_illegal_status_transition_todo_to_completed(service):
    """Specification rule: Cannot transition directly from TODO to COMPLETED without IN_PROGRESS."""
    task = service.add_task(title="Skip in progress")
    with pytest.raises(IllegalStateTransitionError):
        service.complete_task(task.id)


def test_cancelled_task_is_terminal(service):
    """Specification rule: CANCELLED is terminal; cannot restart or reopen."""
    task = service.add_task(title="Terminal test")
    service.cancel_task(task.id)
    
    with pytest.raises(IllegalStateTransitionError):
        service.start_task(task.id)

    with pytest.raises(IllegalStateTransitionError):
        service.reopen_task(task.id)


# =========================================================================
# 5. Priority Sorting & Tag Filtering Tests
# =========================================================================
def test_priority_sorting(service):
    service.add_task(title="Low Task", priority=Priority.LOW)
    service.add_task(title="High Task", priority=Priority.HIGH)
    service.add_task(title="Medium Task", priority=Priority.MEDIUM)

    sorted_tasks = service.list_tasks(sort_by_priority=True)
    assert [t.priority for t in sorted_tasks] == [Priority.HIGH, Priority.MEDIUM, Priority.LOW]


def test_tag_filtering(service):
    service.add_task(title="Backend Dev", tags=["dev", "python"])
    service.add_task(title="Frontend Dev", tags=["dev", "react"])
    service.add_task(title="Marketing Campaign", tags=["marketing"])

    dev_tasks = service.list_tasks(tag="dev")
    assert len(dev_tasks) == 2

    python_tasks = service.list_tasks(tag="python")
    assert len(python_tasks) == 1
    assert python_tasks[0].title == "Backend Dev"
