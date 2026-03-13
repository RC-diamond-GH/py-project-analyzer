"""Minimal CLI for py-project-analyzer."""

from __future__ import annotations

import argparse
from pathlib import Path

from py_project_analyzer.adapters.filesystem_candidate_path_provider import (
    FileSystemCandidatePathProvider,
)
from py_project_analyzer.services.code_analysis_service import (
    CodeAnalysisService,
    FileAnalysisResult,
)
from py_project_analyzer.services.dependency_link_service import DependencyLinkService
from py_project_analyzer.services.output_render_service import (
    JsonOutputRenderService,
    MermaidOutputRenderService,
    PlantUmlOutputRenderService,
)
from py_project_analyzer.services.project_scan_service import ProjectScanService


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="py-project-analyzer",
        description="Analyze Python project dependencies and render outputs.",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Root directory to analyze (default: current directory).",
    )
    parser.add_argument(
        "--format",
        choices=["mermaid", "json", "plantuml"],
        default="mermaid",
        help="Output format (default: mermaid).",
    )
    parser.add_argument(
        "--out",
        default="graph.md",
        help="Output file path (default: graph.md).",
    )
    return parser


def run(root: str, fmt: str, out: str) -> int:
    root_path = Path(root).resolve()
    scan_service = ProjectScanService()
    provider = FileSystemCandidatePathProvider()
    analysis_service = CodeAnalysisService()
    link_service = DependencyLinkService()

    candidate_files = scan_service.plan_targets(str(root_path), provider)
    per_file: dict[str, FileAnalysisResult] = {}

    for relative_path in candidate_files:
        file_path = root_path / relative_path
        try:
            source = file_path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"[WARN] read failed: {relative_path} -> {exc}")
            continue

        try:
            per_file[relative_path] = analysis_service.analyze_source(source)
        except ValueError as exc:
            print(f"[WARN] parse failed: {relative_path} -> {exc}")
            continue

    project_data = link_service.link(per_file)

    renderers = {
        "mermaid": MermaidOutputRenderService(),
        "json": JsonOutputRenderService(),
        "plantuml": PlantUmlOutputRenderService(),
    }
    render_service = renderers[fmt]

    out_text = render_service.render(project_data)

    out_path = Path(out)
    out_path.write_text(out_text, encoding="utf-8")

    print(f"Analyzed files: {len(per_file)}")
    print(f"Output saved to: {out_path} (format: {fmt})")
    return 0


def main() -> int:
    args = build_arg_parser().parse_args()
    return run(args.root, args.format, args.out)


if __name__ == "__main__":
    raise SystemExit(main())
