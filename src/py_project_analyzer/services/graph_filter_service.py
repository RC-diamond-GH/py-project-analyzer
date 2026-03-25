"""Graph filtering service for post-processing project dependency graph."""

from __future__ import annotations

from copy import deepcopy

from py_project_analyzer.services.dependency_link_service import ProjectData


class GraphFilterService:
    """Applies module/function filtering and subgraph extraction."""

    def apply_module_exclusions(
        self,
        project_data: ProjectData,
        excluded_modules: set[str],
    ) -> ProjectData:
        if not excluded_modules:
            return deepcopy(project_data)

        filtered: ProjectData = {}
        for module, data in project_data.items():
            if module in excluded_modules:
                continue
            dependencies = data.get("dependencies", {})
            if not isinstance(dependencies, dict):
                dependencies = {}
            next_dependencies = {
                target: calls
                for target, calls in dependencies.items()
                if target not in excluded_modules
            }
            filtered[module] = {
                "definitions": list(data.get("definitions", [])),
                "dependencies": next_dependencies,
            }
        return filtered

    def apply_function_exclusions(
        self,
        project_data: ProjectData,
        excluded_functions: set[str],
    ) -> ProjectData:
        if not excluded_functions:
            return deepcopy(project_data)

        filtered: ProjectData = {}
        for module, data in project_data.items():
            definitions = data.get("definitions", [])
            if not isinstance(definitions, list):
                definitions = []
            kept_definitions = [
                func for func in definitions if func not in excluded_functions
            ]

            dependencies = data.get("dependencies", {})
            if not isinstance(dependencies, dict):
                dependencies = {}
            kept_dependencies: dict[str, list[str]] = {}
            for target, calls in dependencies.items():
                if not isinstance(calls, list):
                    continue
                kept_calls = [name for name in calls if name not in excluded_functions]
                if kept_calls:
                    kept_dependencies[target] = kept_calls

            filtered[module] = {
                "definitions": kept_definitions,
                "dependencies": kept_dependencies,
            }
        return filtered

    def apply_private_function_exclusion(
        self,
        project_data: ProjectData,
    ) -> ProjectData:
        """Hide all functions starting with '_' in definitions and edge labels."""
        filtered: ProjectData = {}
        for module, data in project_data.items():
            definitions = data.get("definitions", [])
            if not isinstance(definitions, list):
                definitions = []
            kept_definitions = [
                func for func in definitions if not (isinstance(func, str) and func.startswith("_"))
            ]

            dependencies = data.get("dependencies", {})
            if not isinstance(dependencies, dict):
                dependencies = {}
            kept_dependencies: dict[str, list[str]] = {}
            for target, calls in dependencies.items():
                if not isinstance(calls, list):
                    continue
                kept_calls = [
                    name
                    for name in calls
                    if not (isinstance(name, str) and name.startswith("_"))
                ]
                if kept_calls:
                    kept_dependencies[target] = kept_calls

            filtered[module] = {
                "definitions": kept_definitions,
                "dependencies": kept_dependencies,
            }
        return filtered

    def extract_module_subgraph(
        self,
        project_data: ProjectData,
        modules: set[str],
    ) -> ProjectData:
        """Extract a recursive downstream subgraph from seed modules."""
        if not modules:
            return deepcopy(project_data)

        included: set[str] = set()
        stack = [module for module in modules if module in project_data]
        while stack:
            module = stack.pop()
            if module in included:
                continue
            included.add(module)

            data = project_data.get(module, {})
            dependencies = data.get("dependencies", {})
            if not isinstance(dependencies, dict):
                continue
            for target in dependencies:
                if target in project_data and target not in included:
                    stack.append(target)

        subgraph: ProjectData = {}
        for module, data in project_data.items():
            if module not in included:
                continue
            dependencies = data.get("dependencies", {})
            if not isinstance(dependencies, dict):
                dependencies = {}
            kept_dependencies = {
                target: calls
                for target, calls in dependencies.items()
                if target in included
            }
            subgraph[module] = {
                "definitions": list(data.get("definitions", [])),
                "dependencies": kept_dependencies,
            }
        return subgraph
