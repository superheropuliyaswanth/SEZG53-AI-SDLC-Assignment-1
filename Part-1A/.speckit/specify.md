# Feature Specification: Smart Todo & Task CLI (Part 1A)

## 1. Overview
The Smart Todo & Task CLI is a deterministic, local task management application providing reliable CRUD operations, tag-based filtering, priority-based sorting, and enforced task status lifecycles with JSON file persistence.

## 2. Requirements & User Stories

### US-1: Task Creation (Create)
- Command: `todo add --title "..." [--desc "..."] [--priority HIGH|MEDIUM|LOW] [--tags "t1,t2"]`
- Acceptance Criteria:
  - Task is assigned the next available positive integer ID.
  - Default priority is `MEDIUM` if omitted.
  - Tags are stripped of whitespace and converted to lowercase.
  - Status defaults to `TODO`.
  - Timestamps `created_at` and `updated_at` are populated in ISO 8601 UTC format.
  - Exit code `0` on success.
  - Fails with exit code `1` if title is empty or exceeds 120 characters.

### US-2: Task Listing & Filtering (Read)
- Command: `todo list [--tag TAG] [--status STATUS] [--sort-priority]`
- Acceptance Criteria:
  - Without filters, lists all active and completed tasks.
  - `--tag <tag>` filters tasks containing the exact tag (case-insensitive).
  - `--status <status>` filters tasks by exact status enum.
  - `--sort-priority` sorts descending by priority (`HIGH` > `MEDIUM` > `LOW`). For identical priorities, tie-breaks by `created_at` ascending.
  - Returns exit code `0`.

### US-3: Task Retrieval (Read Single)
- Command: `todo get <id>`
- Acceptance Criteria:
  - Returns detailed JSON representation of the task if found (exit code `0`).
  - Returns exit code `2` with error message if ID does not exist.

### US-4: Task Status Lifecycle Transitions (Update)
- Commands:
  - `todo start <id>`: Transitions `TODO` -> `IN_PROGRESS`
  - `todo complete <id>`: Transitions `IN_PROGRESS` -> `COMPLETED`
  - `todo cancel <id>`: Transitions `TODO` or `IN_PROGRESS` -> `CANCELLED`
  - `todo reopen <id>`: Transitions `COMPLETED` -> `TODO`
- Acceptance Criteria:
  - Only valid transitions defined in Constitution Section 4 are permitted.
  - Attempting an illegal transition (e.g., `TODO` -> `COMPLETED` directly) must reject the operation, preserve the existing state, and exit with code `3`.
  - On valid transition, `updated_at` is updated to current UTC timestamp. Exit code `0`.

### US-5: Task Deletion (Delete)
- Command: `todo delete <id>`
- Acceptance Criteria:
  - Removes task from store and persists updated dataset.
  - Exit code `0` on success.
  - Exit code `2` if ID not found.

## 3. Storage Specification
- Target file: `tasks.json` in user-specified directory (or current working directory).
- Atomic write sequence:
  1. Serialize tasks to formatted JSON string.
  2. Write to `<filename>.tmp`.
  3. Flush and sync to disk.
  4. Atomically replace `<filename>` with `<filename>.tmp`.
