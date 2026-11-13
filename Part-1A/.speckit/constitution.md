# Engineering Constitution: Smart Todo & Task CLI/API (Part 1A)

## 1. Fundamental Principles
1. **Determinism Above All**: Given identical inputs and local state, the system must produce identical outputs and side-effects. No hidden non-deterministic dependencies.
2. **Binary Testability**: Every functional requirement and constraint must be verifiable via automated, binary (PASS/FAIL) assertions.
3. **Fail-Safe Persistence**: File mutations must be atomic. Storage corruption must be impossible even during abrupt process termination.
4. **State Machine Integrity**: Tasks follow a strict lifecycle state machine. Illegal transitions must be rejected with informative error codes.
5. **No Secrets / Zero External Dependencies for Core Logic**: Pure Python standard library for storage and models, verified with static linting and security scans.

## 2. Mandatory Engineering Constraints
- **Language**: Python 3.10+
- **Code Style & Linting**: Zero errors under `flake8` (max line length 100).
- **Security Guard**: Zero medium or high severity issues detected by `bandit`.
- **Exit Codes**:
  - `0`: Successful execution.
  - `1`: Invalid user input / parameter validation error.
  - `2`: Resource not found (e.g. task ID does not exist).
  - `3`: Illegal state transition attempt.
  - `4`: Storage I/O failure.

## 3. Data Integrity & Schema Invariants
- Each Task MUST contain: `id` (int), `title` (str, 1-120 chars), `description` (str), `status` (Enum: `TODO`, `IN_PROGRESS`, `COMPLETED`, `CANCELLED`), `priority` (Enum: `HIGH`, `MEDIUM`, `LOW`), `tags` (List[str], alphanumeric lowercase), `created_at` (ISO 8601 UTC), `updated_at` (ISO 8601 UTC).
- Task IDs are positive monotonically increasing integers.
- Atomic write: write to temporary file `.tmp` and rename atomically to target `tasks.json`.

## 4. Lifecycle State Machine
```
   [TODO] --------> [IN_PROGRESS] --------> [COMPLETED]
     |                     |
     +-----> [CANCELLED] <-+
```
- Allowed:
  - `TODO` -> `IN_PROGRESS`
  - `TODO` -> `CANCELLED`
  - `IN_PROGRESS` -> `COMPLETED`
  - `IN_PROGRESS` -> `CANCELLED`
  - `COMPLETED` -> `TODO` (Only via explicit `reopen` command with status reason)
- Strictly Prohibited (Immediate Exit Code 3):
  - `TODO` -> `COMPLETED` (Cannot complete without being in progress)
  - `COMPLETED` -> `IN_PROGRESS` (Must reopen to TODO first)
  - `CANCELLED` -> `IN_PROGRESS` (Cancelled tasks cannot be put directly in progress)
  - `CANCELLED` -> `TODO` (Cancelled tasks cannot be reverted directly to TODO)
