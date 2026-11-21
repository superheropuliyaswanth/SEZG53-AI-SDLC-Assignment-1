"""Main entry point for Smart Todo application (Part 1A)."""
import sys

try:
    from todo.cli import main
except ImportError:
    from src.cli import main

if __name__ == "__main__":
    sys.exit(main())
