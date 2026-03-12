"""TDD test list for CodeAnalysisService."""

import pytest

from py_project_analyzer.services.code_analysis_service import CodeAnalysisService


def test_should_extract_class_and_function_definitions():
    """Intent: collect class/function names from one file."""
    service = CodeAnalysisService()
    source = """
class UserService:
    pass

def login():
    return True
"""
    result = service.analyze_source(source)

    assert result.definitions == ["UserService", "login"]


def test_should_ignore_dunder_function_definitions():
    """Intent: dunder methods are not part of exported definitions."""
    service = CodeAnalysisService()
    source = """
def __private():
    pass

def public_api():
    return 1
"""
    result = service.analyze_source(source)

    assert result.definitions == ["public_api"]


def test_should_extract_call_names_from_name_and_attribute_nodes():
    """Intent: both func() and obj.func() should be recognized."""
    service = CodeAnalysisService()
    source = """
def entry():
    helper()
    user_service.query()
"""
    result = service.analyze_source(source)

    assert result.raw_calls == ["helper", "query"]


def test_should_raise_value_error_for_invalid_python_code():
    """Intent: invalid source should be explicitly surfaced."""
    service = CodeAnalysisService()

    with pytest.raises(ValueError):
        service.analyze_source("def broken(:\n    pass")
