"""TDD test list for DependencyLinkService."""

from py_project_analyzer.services.code_analysis_service import FileAnalysisResult
from py_project_analyzer.services.dependency_link_service import DependencyLinkService


def test_should_link_cross_file_calls_using_global_registry():
    """Intent: connect caller file to callee file by definition name."""
    service = DependencyLinkService()
    per_file = {
        "a.py": FileAnalysisResult(definitions=["fa"], raw_calls=["fb"]),
        "b.py": FileAnalysisResult(definitions=["fb"], raw_calls=[]),
    }

    result = service.link(per_file)

    assert result["a.py"]["dependencies"] == {"b.py": ["fb"]}


def test_should_not_link_calls_to_same_file_definitions():
    """Intent: self-defined symbols should not generate cross-file edges."""
    service = DependencyLinkService()
    per_file = {
        "a.py": FileAnalysisResult(definitions=["fa"], raw_calls=["fa"]),
    }

    result = service.link(per_file)

    assert result["a.py"]["dependencies"] == {}
