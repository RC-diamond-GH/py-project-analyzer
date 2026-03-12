import ast
import json
from collections import defaultdict

# ---------------------------------------------------------
# 1. 定义 AST 遍历器：专门用来提取定义和调用
# ---------------------------------------------------------
class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        # 记录当前文件中定于了哪些类和方法
        self.definitions = []
        # 记录当前文件中发起了哪些调用
        self.calls = set()

    def visit_ClassDef(self, node):
        self.definitions.append(node.name)
        self.generic_visit(node)  # 继续遍历类里面的内容

    def visit_FunctionDef(self, node):
        # 忽略魔法方法（可选）
        if not node.name.startswith("__"):
            self.definitions.append(node.name)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.definitions.append(node.name)
        self.generic_visit(node)

    def visit_Call(self, node):
        # 尝试提取被调用的名字
        # 例如: func() -> ast.Name
        # 例如: obj.func() -> ast.Attribute
        call_name = None
        if isinstance(node.func, ast.Name):
            call_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            call_name = node.func.attr
        
        if call_name:
            self.calls.add(call_name)
            
        self.generic_visit(node)

# ---------------------------------------------------------
# 2. 核心分析功能
# ---------------------------------------------------------
def analyze_project(files_dict):
    project_data = {}
    global_registry = {} # 记录 "名字 -> 所属文件"
    
    # 第一阶段：解析所有文件，提取定义和内部调用
    for filename, code in files_dict.items():
        try:
            tree = ast.parse(code)
        except Exception as e:
            print(f"Error parsing file {filename}: {e}")
            continue
        analyzer = CodeAnalyzer()
        analyzer.visit(tree)
        
        project_data[filename] = {
            "definitions": analyzer.definitions,
            "raw_calls": list(analyzer.calls),
            "dependencies": {} # 存放对其他文件的调用汇总
        }
        
        # 登记到全局名册
        for def_name in analyzer.definitions:
            global_registry[def_name] = filename

    # 第二阶段：连线（跨文件依赖分析）
    for filename, data in project_data.items():
        deps = defaultdict(list)
        for call in data["raw_calls"]:
            # 如果调用的函数/类在全局名册中，且不是当前文件自己定义的
            if call in global_registry and global_registry[call] != filename:
                target_file = global_registry[call]
                deps[target_file].append(call)
        data["dependencies"] = dict(deps)
        # 清理掉不再需要的原始调用记录
        del data["raw_calls"]

    return project_data

# ---------------------------------------------------------
# 3. 渲染器：将分析得到的字典转化为 Mermaid 格式
# ---------------------------------------------------------
def generate_mermaid(project_data):
    lines = ["classDiagram", "direction TD", ""]
    
    # 定义带有成员的模块（类）
    for filename, data in project_data.items():
        lines.append(f"class {filename} {{") # 用反引号包裹文件名避免语法错误
        for definition in data["definitions"]:
            lines.append(f"    +{definition}()")
        lines.append("}\n")
        
    # 定义依赖关系（连线）
    for source_file, data in project_data.items():
        for target_file, called_items in data["dependencies"].items():
            # 拼接调用的项并使用 <br> 换行
            calls_str = "<br>".join([f"{item}()" for item in called_items])
            lines.append(f"{source_file} --> {target_file} : call {calls_str}")
            
    return "\n".join(lines)

# ---------------------------------------------------------
# 4. 测试与演示
# ---------------------------------------------------------
import os
def getAllSrcData() -> dict[str, str]:
    # 递归的遍历所有文件（不包含.开头的文件和文件夹），并返回所有.py文件的内容
    # 排除文件夹：__pycache__, .venv, .git, .pytest_cache
    exclude_dirs = ["__pycache__", ".venv", ".git", ".pytest_cache", "examples"]
    src_data = {}
    for root, dirs, files in os.walk("."):
        if any(dir in dirs for dir in exclude_dirs):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            continue
        for file in files:
            if file.startswith(".") or not file.endswith(".py"):
                continue
            with open(os.path.join(root, file), "r") as f:
                try:
                    src_data[os.path.join(root, file).replace('/', '.').replace('\\', '.').replace('..', '')] = f.read()
                except Exception as e:
                    print(f"Error reading file {root}/{file}: {e}")
                    continue
    
    # add main.py
    with open("main.py", "r") as f:
        src_data["main.py"] = f.read()

    return src_data
if __name__ == "__main__":
    src_data = getAllSrcData()
    for file in src_data.keys():
        print(file)
    # exit()

    # 1. 分析代码结构
    analyzed_data = analyze_project(src_data)
    
    # 2. 输出 JSON
    print("========== 1. 输出的 JSON 结构 ==========")
    json_output = json.dumps(analyzed_data, indent=4, ensure_ascii=False)
    print(json_output)
    
    print("\n========== 2. 生成的 Mermaid 代码 ==========")
    # 3. 输出 Mermaid
    mermaid_code = generate_mermaid(analyzed_data)
    with open("graph.md", "w") as f:
        f.write(mermaid_code)
