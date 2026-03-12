"""Cross-file dependency linking service."""

from __future__ import annotations

from collections import defaultdict

from py_project_analyzer.services.code_analysis_service import FileAnalysisResult

ProjectData = dict[str, dict[str, object]]


class DependencyLinkService:
    """Build dependency graph from per-file analysis results."""

    def link(self, per_file_results: dict[str, FileAnalysisResult]) -> ProjectData:
        project_data: ProjectData = {}
        global_registry: dict[str, str] = {}

        for filename, result in per_file_results.items():
            project_data[filename] = {
                "definitions": result.definitions,
                "dependencies": {},
            }
            for name in result.definitions:
                global_registry[name] = filename

        for filename, result in per_file_results.items():
            deps: defaultdict[str, list[str]] = defaultdict(list)
            for call in result.raw_calls:
                target_file = global_registry.get(call)
                if target_file is None or target_file == filename:
                    continue
                deps[target_file].append(call)
            project_data[filename]["dependencies"] = dict(deps)

        return project_data
