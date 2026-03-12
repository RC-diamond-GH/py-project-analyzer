"""Rendering service for JSON and Mermaid outputs."""

from __future__ import annotations

import json
import re


class OutputRenderService:
    """Render project data into human/machine readable text."""

    def render_json(self, project_data: dict[str, dict[str, object]]) -> str:
        return json.dumps(project_data, indent=4, ensure_ascii=False)

    def render_mermaid(self, project_data: dict[str, dict[str, object]]) -> str:
        lines = ["classDiagram", "direction TD", ""]
        aliases = {name: self._to_alias(name) for name in project_data}

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

    def _to_alias(self, name: str) -> str:
        alias = re.sub(r"[^A-Za-z0-9_]", ".", name)
        if not alias:
            alias = "UnknownFile"
        if alias[0].isdigit():
            alias = f"F_{alias}"
        return alias
