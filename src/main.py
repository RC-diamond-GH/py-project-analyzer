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
from py_project_analyzer.services.output_render_service import OutputRenderService
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
        "--mermaid-out",
        default="graph.md",
        help="Output path for Mermaid text (default: graph.md).",
    )
    parser.add_argument(
        "--json-out",
        default="graph.json",
        help="Output path for JSON result (default: graph.json).",
    )
    return parser


def run(root: str, mermaid_out: str, json_out: str) -> int:
    root_path = Path(root).resolve()
    scan_service = ProjectScanService()
    provider = FileSystemCandidatePathProvider()
    analysis_service = CodeAnalysisService()
    link_service = DependencyLinkService()
    render_service = OutputRenderService()

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
    json_text = render_service.render_json(project_data)
    mermaid_text = render_service.render_mermaid(project_data)

    Path(json_out).write_text(json_text, encoding="utf-8")
    Path(mermaid_out).write_text(mermaid_text, encoding="utf-8")

    print(f"Analyzed files: {len(per_file)}")
    print(f"JSON output: {json_out}")
    print(f"Mermaid output: {mermaid_out}")
    return 0


def main() -> int:
    args = build_arg_parser().parse_args()
    return run(args.root, args.mermaid_out, args.json_out)


if __name__ == "__main__":
    raise SystemExit(main())
