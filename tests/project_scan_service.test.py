"""TDD test list for ProjectScanService."""

from py_project_analyzer.services.project_scan_service import ProjectScanService

def test_should_keep_only_python_files_after_exclusion_rules():
    """Intent: only .py files are kept, ignored dirs removed."""
    service = ProjectScanService(exclude_dirs={"__pycache__", ".git", ".venv"})
    files = [
        "src/main.py",
        "src/.hidden.py",
        "src/readme.md",
        "src/core/service.py",
        ".git/hooks/pre-commit.py",
        "pkg/__pycache__/cache.py",
        "pkg/module.txt",
    ]

    assert service.filter_python_files(files) == [
        "src/core/service.py",
        "src/main.py",
    ]


def test_should_return_deterministic_sorted_paths():
    """Intent: output order is stable for reproducible analysis."""
    service = ProjectScanService()
    files = ["b.py", "a.py", "c.py"]

    assert service.filter_python_files(files) == ["a.py", "b.py", "c.py"]


def test_should_use_provider_dependency_interface_to_plan_targets():
    """Intent: service consumes provider interface, keeps pure strategy logic."""

    class FakeProvider:
        def list_candidate_paths(self, root_dir: str) -> list[str]:
            assert root_dir == "/demo"
            return ["src/a.py", "src/.b.py", "docs/readme.md"]

    service = ProjectScanService()

    assert service.plan_targets("/demo", FakeProvider()) == ["src/a.py"]
