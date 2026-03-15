"""Dev entry: run CLI via package (python src/main.py or python -m main)."""
from py_project_analyzer.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
