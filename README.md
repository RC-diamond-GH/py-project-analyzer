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

工具包含一个最小 CLI（位于 `src/main.py`），支持对任意路径进行扫描并导出多种格式的图表。

### 基本参数
- `--root`: 待分析的项目根目录路径（默认值：`.`，即当前目录）。
- `--format`: 输出文件的格式。支持 `mermaid`, `json`, `plantuml` 三种格式（默认值：`mermaid`）。
- `--out`: 输出文件的保存路径（默认值：`graph.md`）。

### 常见用法示例

1. **扫描当前目录并导出默认的 Mermaid 类图**
   ```bash
   poetry run python src/main.py
   ```
   > 这将在当前目录生成一个包含 Mermaid 语法类图的 `graph.md` 文件。

2. **分析指定项目并导出 PlantUML 图表**
   ```bash
   poetry run python src/main.py --root /path/to/my_project --format plantuml --out my_project_arch.puml
   ```

3. **导出结构化的 JSON 数据用于二次开发**
   ```bash
   poetry run python src/main.py --root /path/to/my_project --format json --out my_project_data.json
   ```
   > 生成的 JSON 将包含所有被分析文件中的定义及依赖关系。

## Testing

执行所有单元测试并查看结果：

```bash
poetry run pytest
```