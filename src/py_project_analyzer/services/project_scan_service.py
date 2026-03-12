"""Project scan strategy service (pure filtering)."""

from __future__ import annotations

from pathlib import PurePath
from typing import Protocol


DEFAULT_EXCLUDE_DIRS = {
    "__pycache__",
    ".venv",
    ".git",
    ".pytest_cache",
    "examples",
}


class ProjectScanService:
    """Filters candidate paths with deterministic scan rules."""

    def __init__(self, exclude_dirs: set[str] | None = None) -> None:
        self._exclude_dirs = exclude_dirs or DEFAULT_EXCLUDE_DIRS

    def filter_python_files(self, candidate_paths: list[str]) -> list[str]:
        """Keep non-hidden .py files outside excluded directories."""
        accepted: list[str] = []
        for path_str in candidate_paths:
            path = PurePath(path_str)
            if any(part in self._exclude_dirs for part in path.parts):
                continue
            if path.name.startswith("."):
                continue
            if path.suffix != ".py":
                continue
            accepted.append(path_str)
        return sorted(accepted)

    def plan_targets(self, root_dir: str, provider: "CandidatePathProvider") -> list[str]:
        """Get candidates from provider, then apply filter strategy."""
        return self.filter_python_files(provider.list_candidate_paths(root_dir))


class CandidatePathProvider(Protocol):
    """Dependency interface for loading candidate paths from environment."""

    def list_candidate_paths(self, root_dir: str) -> list[str]:
        """Return all candidate paths under root_dir."""
