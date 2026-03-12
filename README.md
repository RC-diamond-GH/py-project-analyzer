# py-project-analyzer

> Reverse Engineering tool for open source python projects.

`py-project-analyzer` 是一个静态代码分析工具。它可以递归扫描目标 Python 工程中的所有文件，基于抽象语法树（AST）提取其中的类、函数定义及其互相调用的关系，最后计算出一张全局的跨文件依赖网络，并渲染输出为 `JSON` 或 `Mermaid` 格式。

工具目前的主要使用场景为：快速分析未知工程、架构可视化、以及为 LLM 代码生成/问答提供更宏观的高层项目结构支持。

## Features

- **AST-based Extraction**: 基于 Python 内置 AST 进行提取，不运行代码，分析安全、速度快。
- **Cross-File Linking**: 自动将不同文件中的函数调用，关联到实际的定义文件，生成网状依赖图。
- **Mermaid Render**: 直接输出为 Mermaid 类图语法，方便潜入 Markdown。
- **JSON Render**: 提供结构化的分析结果，可供二次处理或作为 AI 工具链的数据集。
- **Fault-Tolerant**: 若个别文件出现语法错误会导致跳过该文件，不会使得主进程中断。

## Installation

本项目利用 `poetry` 进行依赖和构建环境的管理。

```bash
# 1. 安装依赖
poetry install
```

## Usage

工具包含一个最小 CLI（在 `src/main.py`），支持对任意路径进行扫描：

```bash
# 分析当前目录，默认输出 graph.md 与 graph.json
poetry run python src/main.py --root .

# 指定目标路径，并重定向输出文件名
poetry run python src/main.py --root /path/to/project --mermaid-out result.md --json-out result.json
```

## Testing

执行所有单元测试并查看结果：

```bash
poetry run pytest
```