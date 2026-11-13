# Task Breakdown & Acceptance Criteria (Part 1A)

## Task WBS

| Task ID | Component | Description | Acceptance Criteria |
|---|---|---|---|
| T-101 | `model.py` | Implement Enums and Task dataclass with serialization | Validates priority ranking, status values, serialization to/from dict |
| T-102 | `storage.py` | Implement atomic JSON storage repository | Tests atomic write, non-existent file auto-init, corrupt backup handling |
| T-103 | `service.py` | Implement state machine & CRUD business logic | Validates allowed transitions, rejects illegal transitions with code 3, tags normalization, priority sorting |
| T-104 | `cli.py` | Implement CLI entry point and subcommands | CLI returns correct exit codes (0, 1, 2, 3) and formatted outputs |
| T-105 | `tests/` | Implement comprehensive pytest test suite | 100% assertions against Constitution and Specification criteria |
| T-106 | `.harness/` | Implement static lint, bandit SAST, and test harness runner | Harness executes all gates, captures stdout/stderr, produces machine-readable JSON report |
| T-107 | `evidence/` | Execute harness, capture initial failure, record repair, generate `harness-log.md` | Contains initial generation, failure evidence, repair diff, final pass, human review |
