# 程序的驱动机制

**语言是 Python，入口是命令行 CLI（例如 `argparse`），核心分析利用 Python 内置的 `ast` 模块结合 `Visitor` 模式驱动遍历，异常处理方式是基于 `try...except` 捕获特定阶段（如文件 I/O、单文件语法解析失败）的异常并利用 `logging` 模块记录警告，保证主流程不中断。**
