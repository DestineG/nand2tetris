## 第 7 章：VM 翻译器（VM Translator）

本目录是根据《计算机系统要素（Nand2Tetris）》第 7 章实现的 **VM 翻译器**。  
它可以把 `.vm` 虚拟机代码转换为 Hack 汇编代码（`.asm`），为后续的汇编器处理做准备。

---

### 功能概述

- **支持的指令类型**
  - **算术与逻辑运算**
    - `add`、`sub`、`neg`：基本算术运算
    - `eq`、`gt`、`lt`：比较运算（结果为 -1 表示真，0 表示假）
    - `and`、`or`、`not`：按位逻辑运算
  - **内存访问指令**
    - `push <segment> <index>` / `pop <segment> <index>`  
      支持的段：`constant`、`local`（LCL）、`argument`（ARG）、`this`、`that`、`temp`（R5-R12）、`pointer`（THIS/THAT）、`static`
  - **程序流程控制**
    - `label <label>`：定义标签（函数作用域内）
    - `goto <label>`：无条件跳转
    - `if-goto <label>`：条件跳转（栈顶非零时跳转）
  - **函数调用**
    - `function <name> <nLocals>`：定义函数，初始化局部变量为 0
    - `call <name> <nArgs>`：调用函数，保存调用者状态
    - `return`：函数返回，恢复调用者状态

---

### 代码结构

- `parser.py`：主程序，完成从 `.vm` 到 `.asm` 的整个转换流程：
  - `extract_instructions`：读取源文件，去除注释和空行，得到纯净的 VM 指令列表。
  - `parse_vm_file`：解析 VM 指令，根据指令类型匹配对应的模板函数，生成汇编代码。
- `templates.py`：包含所有 VM 指令对应的汇编代码模板：
  - `Arithmetic`：算术与逻辑运算指令的模板（`add`、`sub`、`neg`、`eq`、`gt`、`lt`、`and`、`or`、`not`）
  - `MemoryAccess`：内存访问指令的模板（`push`、`pop` 各内存段）
  - `ProgramFlow`：程序流程控制指令的模板（`label`、`goto`、`if-goto`）
  - `FunctionCalling`：函数调用指令的模板（`function`、`call`、`return`）

---

### 使用方法

在项目根目录下，使用 Python 运行：

```python
from chapter_7.parser import parse_vm_file

# 解析 VM 文件并生成汇编文件
vm_path = "path/to/your/file.vm"
output_path = "path/to/output/file.asm"
parse_vm_file(vm_path, output_path)
```

示例（以测试用例为例）：

```python
# 解析 BasicTest.vm 并生成 BasicTest.asm
parse_vm_file(
    r"chapter_7\MemoryAccess\BasicTest\BasicTest.vm",
    r"chapter_7\MemoryAccess\BasicTest\BasicTest.asm"
)
```

---

### 关键实现思路回顾

- **模板化设计**
  - 每种 VM 指令对应一个模板函数，通过 `templateDict` 字典进行映射。
  - 模板函数返回对应的 Hack 汇编代码字符串，便于组合和复用。
- **指令分类处理**
  - 算术指令：直接操作栈顶元素，生成对应的汇编代码。
  - 内存访问指令：根据不同的内存段（`local`、`argument`、`this`、`that`、`temp`、`pointer`、`static`）生成不同的地址计算和访问代码。
  - 流程控制指令：使用函数作用域标签（`<function>$<label>`），避免不同函数间的标签冲突。
  - 函数调用指令：实现完整的调用协议，包括保存/恢复调用者状态、设置被调用者参数和局部变量。
- **特殊处理**
  - **比较操作**：`eq`、`gt`、`lt` 使用类级别的计数器生成唯一标签（如 `EQ_TRUE_0`、`EQ_TRUE_1`），避免多次比较时的标签冲突。
  - **静态变量**：使用 `<filename>.<index>` 格式命名，确保不同文件间的静态变量不会冲突。
  - **函数调用协议**：
    - `call` 时：保存返回地址、LCL、ARG、THIS、THAT 到栈中，设置 ARG = SP - nArgs - 5，LCL = SP，然后跳转到函数。
    - `return` 时：将返回值放到 ARG[0]，恢复 SP、THAT、THIS、ARG、LCL，跳转到返回地址。

---

### 测试

本项目已通过以下测试用例：

- **StackArithmetic 测试**
  - ✅ `SimpleAdd` - 简单加法测试
  - ✅ `StackTest` - 完整栈操作测试（包含所有算术和逻辑运算）

- **MemoryAccess 测试**
  - ✅ `BasicTest` - 基础内存访问测试（local、argument、this、that、constant）
  - ✅ `PointerTest` - 指针操作测试（pointer 段）
  - ✅ `StaticTest` - 静态变量测试（static 段）

所有生成的 `.asm` 文件已通过对应的 `.cmp` 对比文件验证，测试结果完全匹配。

---

### 总结

这一章的实现从零开始手写了一个完整的 VM 翻译器，  
通过 **指令解析、模板匹配、代码生成** 等步骤，  
把“虚拟机代码”成功翻译为“Hack 汇编代码”，  
为后续章节（如编译器）的实现奠定了基础

FunctionCalling/ProgramFlow 中的指令标签唯一性依赖于传入的虚拟机指令的 functionName，所以务必确保 functionName 的唯一性