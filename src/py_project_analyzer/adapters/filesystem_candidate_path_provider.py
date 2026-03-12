"""Filesystem adapter for candidate path discovery."""

from __future__ import annotations

from pathlib import Path

from py_project_analyzer.services.project_scan_service import CandidatePathProvider


class FileSystemCandidatePathProvider(CandidatePathProvider):
    """Lists candidate file paths by walking local filesystem."""

    def list_candidate_paths(self, root_dir: str) -> list[str]:
        root = Path(root_dir)
        candidates: list[str] = []
        for item in root.rglob("*"):
            if item.is_file():
                candidates.append(item.relative_to(root).as_posix())
        return sorted(candidates)
