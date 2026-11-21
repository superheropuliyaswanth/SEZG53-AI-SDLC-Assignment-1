"""Contract tests for CLI subcommands and process exit codes (Part 1A)."""
import os
import json
import tempfile
import pytest
from src.cli import main


@pytest.fixture
def cli_env():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "cli_tasks.json")
        yield file_path


def test_cli_add_and_get(cli_env, capsys):
    ret = main(["--file", cli_env, "add", "--title", "CLI Task", "--priority", "HIGH", "--tags", "test,cli"])
    assert ret == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["success"] is True
    assert data["task"]["id"] == 1
    assert data["task"]["priority"] == "HIGH"

    # Get task
    ret_get = main(["--file", cli_env, "get", "1"])
    assert ret_get == 0
    captured_get = capsys.readouterr()
    task_data = json.loads(captured_get.out)
    assert task_data["id"] == 1


def test_cli_lifecycle_and_transition_error(cli_env, capsys):
    # Add
    main(["--file", cli_env, "add", "--title", "Lifecycle Task"])
    
    # Attempt illegal skip to complete (TODO -> COMPLETED)
    ret_illegal = main(["--file", cli_env, "complete", "1"])
    assert ret_illegal == 3
    err = capsys.readouterr().err
    assert "Illegal transition" in err

    # Valid start (TODO -> IN_PROGRESS)
    ret_start = main(["--file", cli_env, "start", "1"])
    assert ret_start == 0

    # Valid complete (IN_PROGRESS -> COMPLETED)
    ret_comp = main(["--file", cli_env, "complete", "1"])
    assert ret_comp == 0

    # Valid reopen (COMPLETED -> TODO)
    ret_reopen = main(["--file", cli_env, "reopen", "1"])
    assert ret_reopen == 0


def test_cli_not_found(cli_env, capsys):
    ret = main(["--file", cli_env, "get", "999"])
    assert ret == 2
    err = capsys.readouterr().err
    assert "not found" in err


def test_cli_list_filter_by_tag(cli_env, capsys):
    main(["--file", cli_env, "add", "--title", "Work Task", "--tags", "work,urgent"])
    main(["--file", cli_env, "add", "--title", "Personal Task", "--tags", "personal"])
    capsys.readouterr()  # flush output buffer

    ret = main(["--file", cli_env, "list", "--tag", "work"])
    assert ret == 0
    captured = capsys.readouterr()
    tasks = json.loads(captured.out)
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Work Task"


def test_cli_list_sort_by_priority(cli_env, capsys):
    main(["--file", cli_env, "add", "--title", "Low Task", "--priority", "LOW"])
    main(["--file", cli_env, "add", "--title", "High Task", "--priority", "HIGH"])
    main(["--file", cli_env, "add", "--title", "Med Task", "--priority", "MEDIUM"])
    capsys.readouterr()

    ret = main(["--file", cli_env, "list", "--sort-priority"])
    assert ret == 0
    captured = capsys.readouterr()
    tasks = json.loads(captured.out)
    assert len(tasks) == 3
    assert tasks[0]["priority"] == "HIGH"
    assert tasks[1]["priority"] == "MEDIUM"
    assert tasks[2]["priority"] == "LOW"


def test_cli_delete_and_cancel_lifecycle(cli_env, capsys):
    main(["--file", cli_env, "add", "--title", "Task to Cancel"])
    main(["--file", cli_env, "add", "--title", "Task to Delete"])
    capsys.readouterr()

    # Cancel task 1
    ret_cancel = main(["--file", cli_env, "cancel", "1"])
    assert ret_cancel == 0
    out_cancel = capsys.readouterr().out
    assert "cancelled" in out_cancel.lower()

    # Delete task 2
    ret_del = main(["--file", cli_env, "delete", "2"])
    assert ret_del == 0
    out_del = capsys.readouterr().out
    assert "deleted" in out_del.lower()

    # Verify task 2 is gone
    ret_get = main(["--file", cli_env, "get", "2"])
    assert ret_get == 2
