"""Tests for filesystem candidate path provider adapter."""

from pathlib import Path

from py_project_analyzer.adapters.filesystem_candidate_path_provider import (
    FileSystemCandidatePathProvider,
)


def test_should_list_all_files_as_relative_posix_paths(tmp_path: Path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.py").write_text("print('a')", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "readme.md").write_text("# readme", encoding="utf-8")

    provider = FileSystemCandidatePathProvider()

    result = provider.list_candidate_paths(str(tmp_path))

    assert result == ["docs/readme.md", "src/a.py"]
