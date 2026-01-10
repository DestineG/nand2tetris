## 第 8 章：VM 翻译器（完整版）

本目录是根据《计算机系统要素（Nand2Tetris）》第 8 章实现的 **完整版 VM 翻译器**。  
它整合了第 6 章的汇编器和第 7 章的 VM 翻译器，支持单文件和多文件处理，并自动插入初始化和跳转代码。

---

### 功能概述

- **整合功能**
  - 整合了第 6 章的 Hack 汇编器（`.asm` → `.hack`）
  - 整合了第 7 章的 VM 翻译器（`.vm` → `.asm`）
  - 支持完整的编译流程：`.vm` → `.asm` → `.hack`
  - 根据输出文件扩展名自动选择输出格式（`.asm` 或 `.hack`）

- **单文件和多文件支持**
  - **单文件模式**：处理单个 `.vm` 文件
  - **多文件模式**：处理整个目录下的所有 `.vm` 文件，自动合并生成一个 `.asm` 文件

- **自动初始化与跳转**
  - 自动生成 **Bootstrap 代码**：
    - 初始化物理段指针（SP、LCL、ARG、THIS、THAT）
    - 如果检测到 `Sys.init` 函数，自动插入调用代码并跳转
  - 无需手动在生成的汇编代码前添加初始化代码

- **支持的指令类型**
  - 继承第 7 章的所有 VM 指令支持：
    - 算术与逻辑运算（`add`、`sub`、`neg`、`eq`、`gt`、`lt`、`and`、`or`、`not`）
    - 内存访问（`push`、`pop` 各内存段）
    - 程序流程控制（`label`、`goto`、`if-goto`）
    - 函数调用（`function`、`call`、`return`）

---

### 代码结构

- `parser.py`：主程序，完成从 `.vm` 到 `.asm` 或 `.hack` 的整个转换流程：
  - `generate_bootstrap_code`：生成 Bootstrap 代码，包括段指针初始化和 `Sys.init` 调用
  - `vm_translator`：VM 翻译器主函数
    - 支持单文件模式：处理单个 `.vm` 文件
    - 支持多文件模式：遍历目录下所有 `.vm` 文件并合并
    - 自动检测 `Sys.init` 函数并生成相应的调用代码
    - 根据输出文件扩展名自动选择输出格式：
      - 输出 `.asm` 文件：直接写入汇编代码
      - 输出 `.hack` 文件：先生成 `.asm` 文件，再调用第 6 章的汇编器转换为 `.hack` 文件

---

### 使用方法

在项目根目录下，使用 Python 运行：

```python
from chapter_8.parser import vm_translator

# 单文件模式
vm_translator(
    r"chapter_8\ProgramFlow\FibonacciSeries\FibonacciSeries.vm",
    r"chapter_8\ProgramFlow\FibonacciSeries\FibonacciSeries.asm"
)

# 多文件模式（处理整个目录，输出汇编文件）
vm_translator(
    r"chapter_8\FunctionCalls\StaticsTest",
    r"chapter_8\FunctionCalls\StaticsTest\StaticsTest.asm"
)

# 多文件模式（直接输出二进制文件）
vm_translator(
    r"chapter_8\FunctionCalls\FibonacciElement",
    r"chapter_8\FunctionCalls\FibonacciElement\FibonacciElement.hack"
)
```

或者直接运行 `parser.py`：

```bash
python chapter_8/parser.py
```

（需要在 `parser.py` 的 `__main__` 部分修改输入和输出路径）

---

### 关键实现思路回顾

- **整合设计**
  - 复用第 6 章的 `hack_assembler` 函数（`.asm` → `.hack`）
  - 复用第 7 章的 `parse_vm_file` 函数和 `templateDict` 模板字典
  - 通过 `vm_translator` 函数统一处理单文件和多文件场景
  - 根据输出文件扩展名自动判断是否需要调用汇编器

- **Bootstrap 代码生成**
  - **段指针初始化**：设置 SP=256、LCL=300、ARG=400、THIS=3000、THAT=4000
  - **自动检测 `Sys.init`**：遍历所有 VM 文件生成的汇编代码，查找是否包含 `Sys.init` 函数
  - **自动调用**：如果找到 `Sys.init`，使用 `call` 指令模板生成调用代码并插入到 Bootstrap 代码末尾

- **多文件处理**
  - 遍历目录下所有 `.vm` 文件，逐个调用 `parse_vm_file` 进行翻译
  - 将所有生成的汇编代码按顺序合并，确保函数和静态变量的命名唯一性（依赖第 7 章的实现）

- **工作流程**
  1. 检测输入路径是文件还是目录
  2. 处理所有 `.vm` 文件，生成汇编代码
  3. 检测是否存在 `Sys.init` 函数
  4. 生成 Bootstrap 代码（初始化 + 可选的 `Sys.init` 调用）
  5. 将 Bootstrap 代码与翻译后的汇编代码合并
  6. 根据输出文件扩展名：
     - 如果是 `.asm`：直接写入汇编代码
     - 如果是 `.hack`：先写入临时 `.asm` 文件，调用 `hack_assembler` 转换为 `.hack`，然后删除临时文件

---

### 测试

本项目已通过以下测试用例：

- **ProgramFlow 测试**
  - ✅ `FibonacciSeries` - 斐波那契数列生成测试

- **FunctionCalls 测试**
  - ✅ `StaticsTest` - 静态变量测试（多文件场景，包含 `Class1.vm`、`Class2.vm`、`Sys.vm`）

其他测试用例（如 `BasicLoop`、`SimpleFunction`、`NestedCall`、`FibonacciElement`）尚未完成测试。

---

### 总结

这一章的实现整合了第 6 章和第 7 章的功能，  
通过 **单文件/多文件处理、自动初始化、自动跳转** 等特性，  
实现了完整的 VM 翻译器，能够处理复杂的多文件 VM 程序，  
为后续章节（如编译器）的实现提供了完整的工具链支持。

注意：多文件处理时，确保不同文件中的函数名和静态变量名不会冲突（静态变量使用 `<filename>.<index>` 格式，函数名应保持唯一）。

vm 文件中 Static 唯一性依赖于文件名的唯一性，所以 Static 是文件内共享，文件外隔离；Function 和 label 的唯一性依赖于函数名的唯一性，所以 Function 是全局共享