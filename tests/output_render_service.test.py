"""TDD test list for OutputRenderService."""

from py_project_analyzer.services.output_render_service import OutputRenderService


def test_should_render_mermaid_class_diagram_from_project_data():
    """Intent: produce a readable Mermaid classDiagram text."""
    service = OutputRenderService()
    project_data = {
        "a.py": {"definitions": ["fa"], "dependencies": {"b.py": ["fb"]}},
        "b.py": {"definitions": ["fb"], "dependencies": {}},
    }

    mermaid = service.render_mermaid(project_data)

    assert "classDiagram" in mermaid
    assert "a_py --> b_py : call fb()" in mermaid


def test_should_render_json_output():
    """Intent: produce pretty JSON for machine processing."""
    service = OutputRenderService()
    project_data = {"a.py": {"definitions": ["fa"], "dependencies": {}}}

    json_text = service.render_json(project_data)

    assert '"a.py"' in json_text
    assert '"definitions"' in json_text
