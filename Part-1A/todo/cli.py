"""CLI entry point for Smart Todo & Task application (Part 1A)."""
import argparse
import sys
import json
from todo.model import Status, Priority
from todo.storage import TaskRepository, StorageCorruptedError
from todo.service import TaskService, TaskNotFoundError, IllegalStateTransitionError, ValidationError


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="todo",
        description="Smart Todo & Task Manager CLI"
    )
    parser.add_argument("--file", default="tasks.json", help="Path to tasks.json storage file")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    add_p = subparsers.add_parser("add", help="Add a new task")
    add_p.add_argument("--title", required=True, help="Task title (1-120 chars)")
    add_p.add_argument("--desc", default="", help="Task description")
    add_p.add_argument("--priority", choices=["HIGH", "MEDIUM", "LOW"], default="MEDIUM", help="Priority")
    add_p.add_argument("--tags", default="", help="Comma-separated tags")

    # list
    list_p = subparsers.add_parser("list", help="List tasks")
    list_p.add_argument("--tag", default=None, help="Filter by tag")
    list_p.add_argument("--status", choices=["TODO", "IN_PROGRESS", "COMPLETED", "CANCELLED"], default=None)
    list_p.add_argument("--sort-priority", action="store_true", help="Sort descending by priority")

    # get
    get_p = subparsers.add_parser("get", help="Get a single task by ID")
    get_p.add_argument("id", type=int, help="Task ID")

    # start
    start_p = subparsers.add_parser("start", help="Move task to IN_PROGRESS")
    start_p.add_argument("id", type=int, help="Task ID")

    # complete
    comp_p = subparsers.add_parser("complete", help="Complete task")
    comp_p.add_argument("id", type=int, help="Task ID")

    # cancel
    canc_p = subparsers.add_parser("cancel", help="Cancel task")
    canc_p.add_argument("id", type=int, help="Task ID")

    # reopen
    reop_p = subparsers.add_parser("reopen", help="Reopen completed task to TODO")
    reop_p.add_argument("id", type=int, help="Task ID")

    # delete
    del_p = subparsers.add_parser("delete", help="Delete task")
    del_p.add_argument("id", type=int, help="Task ID")

    return parser


def main(args=None) -> int:
    parser = create_parser()
    parsed = parser.parse_args(args)

    repo = TaskRepository(parsed.file)
    service = TaskService(repo)

    try:
        if parsed.command == "add":
            tags_list = [t.strip() for t in parsed.tags.split(",") if t.strip()]
            priority_enum = Priority(parsed.priority)
            task = service.add_task(
                title=parsed.title,
                description=parsed.desc,
                priority=priority_enum,
                tags=tags_list
            )
            print(json.dumps({"success": True, "task": task.to_dict()}, indent=2))
            return 0

        elif parsed.command == "list":
            status_enum = Status(parsed.status) if parsed.status else None
            tasks = service.list_tasks(
                tag=parsed.tag,
                status=status_enum,
                sort_by_priority=parsed.sort_priority
            )
            print(json.dumps([t.to_dict() for t in tasks], indent=2))
            return 0

        elif parsed.command == "get":
            task = service.get_task(parsed.id)
            if not task:
                print(f"Error: Task {parsed.id} not found.", file=sys.stderr)
                return 2
            print(json.dumps(task.to_dict(), indent=2))
            return 0

        elif parsed.command == "start":
            task = service.start_task(parsed.id)
            print(f"Task {task.id} started. Status: {task.status.value}")
            return 0

        elif parsed.command == "complete":
            task = service.complete_task(parsed.id)
            print(f"Task {task.id} completed. Status: {task.status.value}")
            return 0

        elif parsed.command == "cancel":
            task = service.cancel_task(parsed.id)
            print(f"Task {task.id} cancelled. Status: {task.status.value}")
            return 0

        elif parsed.command == "reopen":
            task = service.reopen_task(parsed.id)
            print(f"Task {task.id} reopened. Status: {task.status.value}")
            return 0

        elif parsed.command == "delete":
            service.delete_task(parsed.id)
            print(f"Task {parsed.id} deleted.")
            return 0

    except ValidationError as e:
        print(f"Validation Error: {e}", file=sys.stderr)
        return 1
    except TaskNotFoundError as e:
        print(f"Not Found: {e}", file=sys.stderr)
        return 2
    except IllegalStateTransitionError as e:
        print(f"State Transition Error: {e}", file=sys.stderr)
        return 3
    except StorageCorruptedError as e:
        print(f"Storage Error: {e}", file=sys.stderr)
        return 4
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
