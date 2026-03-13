"""Rendering service for JSON and Mermaid outputs."""

from __future__ import annotations

import json
import re


from typing import Protocol

ProjectData = dict[str, dict[str, object]]


def _to_alias(name: str) -> str:
    alias = re.sub(r"[^A-Za-z0-9_]", "_", name)
    if not alias:
        alias = "UnknownFile"
    if alias[0].isdigit():
        alias = f"F_{alias}"
    return alias


class OutputRenderService(Protocol):
    """Interface for rendering project data into text formats."""

    def render(self, project_data: ProjectData) -> str:
        """Render the given project data into a string."""
        ...


class JsonOutputRenderService:
    """Renders project data as JSON."""

    def render(self, project_data: ProjectData) -> str:
        return json.dumps(project_data, indent=4, ensure_ascii=False)


class MermaidOutputRenderService:
    """Renders project data as a Mermaid classDiagram."""

    def render(self, project_data: ProjectData) -> str:
        lines = ["classDiagram", "direction TD", ""]
        aliases = {name: _to_alias(name) for name in project_data}

        for filename, data in project_data.items():
            alias = aliases[filename]
            lines.append(f"%% file: {filename}")
            lines.append(f"class {alias} {{")
            definitions = data.get("definitions", [])
            for definition in definitions:
                lines.append(f"    +{definition}()")
            lines.append("}")
            lines.append("")

        for source_file, data in project_data.items():
            source_alias = aliases[source_file]
            dependencies = data.get("dependencies", {})
            if not isinstance(dependencies, dict):
                continue
            for target_file, called_items in dependencies.items():
                target_alias = aliases.get(target_file)
                if not target_alias:
                    continue
                if isinstance(called_items, list):
                    calls_str = ", ".join(f"{item}()" for item in called_items)
                else:
                    calls_str = ""
                label = f" : call {calls_str}" if calls_str else ""
                lines.append(f"{source_alias} --> {target_alias}{label}")

        return "\n".join(lines)


class PlantUmlOutputRenderService:
    """Renders project data as a PlantUML class diagram."""

    def render(self, project_data: ProjectData) -> str:
        lines = ["@startuml name", ""]
        aliases = {name: _to_alias(name) for name in project_data}

        for filename, data in project_data.items():
            alias = aliases[filename]
            lines.append(f"class \"{filename}\" as {alias} {{")
            definitions = data.get("definitions", [])
            for definition in definitions:
                lines.append(f"    +{definition}()")
            lines.append("}")
            lines.append("")

        for source_file, data in project_data.items():
            source_alias = aliases[source_file]
            dependencies = data.get("dependencies", {})
            if not isinstance(dependencies, dict):
                continue
            for target_file, called_items in dependencies.items():
                target_alias = aliases.get(target_file)
                if not target_alias:
                    continue
                if isinstance(called_items, list):
                    calls_str = ", ".join(f"{item}()" for item in called_items)
                else:
                    calls_str = ""
                label = f" : call {calls_str}" if calls_str else ""
                lines.append(f"{source_alias} --> {target_alias}{label}")

        lines.append("@enduml")
        return "\n".join(lines)
