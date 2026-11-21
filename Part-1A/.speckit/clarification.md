# Clarifications & Edge-Case Resolutions (Part 1A)

## Ambiguity Clarifications

### Q1: What happens if `tasks.json` does not exist at startup?
**Resolution**: The application initializes an empty JSON file with `{"tasks": []}` automatically without throwing an error.

### Q2: What happens if `tasks.json` is corrupted or contains malformed JSON?
**Resolution**: The application creates a timestamped backup copy (`tasks.corrupt.<timestamp>.bak`), raises a descriptive `StorageCorruptedError`, and refuses destructive overwrite. Exit code `4`.

### Q3: How should multiple tags be parsed from CLI?
**Resolution**: Tags can be provided as a comma-separated string (e.g. `--tags "work, urgent, finance"`). Leading/trailing whitespace is trimmed, converted to lowercase, duplicates removed, and stored as a clean list `["work", "urgent", "finance"]`.

### Q4: Can a `CANCELLED` task be restarted or completed?
**Resolution**: Per Constitution Section 4, a `CANCELLED` task is terminal. It cannot be moved directly to `IN_PROGRESS` or `COMPLETED`. Attempting to do so raises `IllegalStateTransitionError` with exit code `3`.

### Q5: What is the deterministic tie-breaking order for priority sorting?
**Resolution**: When two tasks have the same priority level:
1. `priority` (HIGH=3, MEDIUM=2, LOW=1 descending)
2. `created_at` timestamp (ascending: older tasks first)
3. `id` (ascending)
