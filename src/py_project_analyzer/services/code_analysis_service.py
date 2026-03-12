"""AST-based single file code analysis service."""

from __future__ import annotations

import ast
from dataclasses import dataclass


@dataclass(frozen=True)
class FileAnalysisResult:
    definitions: list[str]
    raw_calls: list[str]


class _CodeAnalyzer(ast.NodeVisitor):
    def __init__(self) -> None:
        self.definitions: list[str] = []
        self.calls: set[str] = set()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.definitions.append(node.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if not node.name.startswith("__"):
            self.definitions.append(node.name)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        if not node.name.startswith("__"):
            self.definitions.append(node.name)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        call_name: str | None = None
        if isinstance(node.func, ast.Name):
            call_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            call_name = node.func.attr
        if call_name:
            self.calls.add(call_name)
        self.generic_visit(node)


class CodeAnalysisService:
    """Extracts definitions and call names from source code."""

    def analyze_source(self, source_code: str) -> FileAnalysisResult:
        try:
            tree = ast.parse(source_code)
        except SyntaxError as exc:
            raise ValueError(f"invalid python source: {exc.msg}") from exc

        analyzer = _CodeAnalyzer()
        analyzer.visit(tree)
        return FileAnalysisResult(
            definitions=analyzer.definitions,
            raw_calls=sorted(analyzer.calls),
        )
