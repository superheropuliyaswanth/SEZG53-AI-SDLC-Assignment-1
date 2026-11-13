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
