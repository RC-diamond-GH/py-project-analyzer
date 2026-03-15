"""Tests for graph filtering service features."""

from py_project_analyzer.services.graph_filter_service import GraphFilterService


def _sample_graph() -> dict[str, dict[str, object]]:
    return {
        "a.py": {
            "definitions": ["fa", "mask_me"],
            "dependencies": {"b.py": ["fb", "mask_me"], "c.py": ["fc"]},
        },
        "b.py": {
            "definitions": ["fb"],
            "dependencies": {"c.py": ["fc"]},
        },
        "c.py": {
            "definitions": ["fc", "mask_me"],
            "dependencies": {},
        },
    }


def test_should_exclude_modules_and_related_edges():
    service = GraphFilterService()
    graph = _sample_graph()

    result = service.apply_module_exclusions(graph, {"c.py"})

    assert "c.py" not in result
    assert result["a.py"]["dependencies"] == {"b.py": ["fb", "mask_me"]}
    assert result["b.py"]["dependencies"] == {}


def test_should_exclude_functions_from_definitions_and_edges():
    service = GraphFilterService()
    graph = _sample_graph()

    result = service.apply_function_exclusions(graph, {"mask_me"})

    assert result["a.py"]["definitions"] == ["fa"]
    assert result["c.py"]["definitions"] == ["fc"]
    assert result["a.py"]["dependencies"] == {"b.py": ["fb"], "c.py": ["fc"]}


def test_should_drop_edge_if_all_called_functions_are_excluded():
    service = GraphFilterService()
    graph = {
        "a.py": {"definitions": ["fa"], "dependencies": {"b.py": ["mask_me"]}},
        "b.py": {"definitions": ["mask_me"], "dependencies": {}},
    }

    result = service.apply_function_exclusions(graph, {"mask_me"})

    assert result["a.py"]["dependencies"] == {}
    assert result["b.py"]["definitions"] == []


def test_should_extract_module_subgraph_by_selected_nodes():
    service = GraphFilterService()
    graph = _sample_graph()

    result = service.extract_module_subgraph(graph, {"a.py", "b.py"})

    assert set(result.keys()) == {"a.py", "b.py"}
    assert result["a.py"]["dependencies"] == {"b.py": ["fb", "mask_me"]}
