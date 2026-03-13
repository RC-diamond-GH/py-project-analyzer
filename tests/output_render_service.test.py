"""TDD test list for OutputRenderService."""

from py_project_analyzer.services.output_render_service import (
    JsonOutputRenderService,
    MermaidOutputRenderService,
    PlantUmlOutputRenderService,
)


def test_should_render_mermaid_class_diagram_from_project_data():
    """Intent: produce a readable Mermaid classDiagram text."""
    service = MermaidOutputRenderService()
    project_data = {
        "a.py": {"definitions": ["fa"], "dependencies": {"b.py": ["fb"]}},
        "b.py": {"definitions": ["fb"], "dependencies": {}},
    }

    mermaid = service.render(project_data)

    assert "classDiagram" in mermaid
    assert "a_py --> b_py : call fb()" in mermaid


def test_should_render_json_output():
    """Intent: produce pretty JSON for machine processing."""
    service = JsonOutputRenderService()
    project_data = {"a.py": {"definitions": ["fa"], "dependencies": {}}}

    json_text = service.render(project_data)

    assert '"a.py"' in json_text
    assert '"definitions"' in json_text


def test_should_render_plantuml_class_diagram_from_project_data():
    """Intent: produce a readable PlantUML class diagram text."""
    service = PlantUmlOutputRenderService()
    project_data = {
        "a.py": {"definitions": ["fa"], "dependencies": {"b.py": ["fb"]}},
        "b.py": {"definitions": ["fb"], "dependencies": {}},
    }

    plantuml = service.render(project_data)

    assert "@startuml" in plantuml
    assert "@enduml" in plantuml
    assert "class \"a.py\" as a_py {" in plantuml
    assert "a_py --> b_py : call fb()" in plantuml
