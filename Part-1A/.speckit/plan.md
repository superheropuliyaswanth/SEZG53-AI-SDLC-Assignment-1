# Technical Architecture & Implementation Plan (Part 1A)

## 1. Module Structure
```
src/
├── __init__.py
├── model.py      # Domain entities: Task, Priority, Status, TransitionMatrix
├── storage.py    # Atomic JSON repository persistence & error recovery
├── service.py    # Core business service, state validation, filtering & sorting
└── cli.py        # CLI interface using standard library argparse
```

## 2. Component Design

### 2.1 Domain Layer (`model.py`)
- Python `Enum`: `Status` (`TODO`, `IN_PROGRESS`, `COMPLETED`, `CANCELLED`)
- Python `Enum`: `Priority` (`HIGH`, `MEDIUM`, `LOW`) with integer ranking values for unambiguous comparison.
- Dataclass `Task`:
  - `id: int`
  - `title: str`
  - `description: str = ""`
  - `status: Status = Status.TODO`
  - `priority: Priority = Priority.MEDIUM`
  - `tags: List[str] = field(default_factory=list)`
  - `created_at: str = ""`
  - `updated_at: str = ""`

### 2.2 Storage Layer (`storage.py`)
- `TaskRepository`:
  - `load_all() -> List[Task]`
  - `save_all(tasks: List[Task]) -> None`: uses temporary file atomic rename (`os.replace`).
  - Safe error handling for corrupted files with backup preservation.

### 2.3 Service Layer (`service.py`)
- `TaskService`:
  - Encapsulates state machine transition logic:
    ```python
    VALID_TRANSITIONS = {
        Status.TODO: {Status.IN_PROGRESS, Status.CANCELLED},
        Status.IN_PROGRESS: {Status.COMPLETED, Status.CANCELLED},
        Status.COMPLETED: {Status.TODO}, # Explicit reopen
        Status.CANCELLED: set() # Terminal
    }
    ```
  - `add_task(title, description, priority, tags) -> Task`
  - `transition_status(task_id, target_status) -> Task`
  - `filter_tasks(tag, status, sort_by_priority) -> List[Task]`
  - `delete_task(task_id) -> bool`

### 2.4 Presentation Layer (`cli.py`)
- Uses `argparse` with subcommands: `add`, `list`, `get`, `start`, `complete`, `cancel`, `reopen`, `delete`.
- Returns compliant exit codes (0, 1, 2, 3, 4).

## 3. Harness Integration
- Three distinct gates:
  1. Syntax & Lint Guard (`flake8` / `ruff`)
  2. Security Guard (`bandit`)
  3. Deterministic Unit & Contract Tests (`pytest`)
- Integrated Harness Runner (`run_harness.py`) orchestrates all gates and exports structured JSON evidence.
