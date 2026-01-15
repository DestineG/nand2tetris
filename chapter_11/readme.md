
## 第 11 章：Jack 编译器（Compiler）

本项目是基于《**计算机系统要素（Nand2Tetris）**》第 11 章实现的 **Jack 语言编译器（Python 版本）**。
编译器以 `.jack` 源文件为输入，输出对应的 `.vm` 虚拟机代码，可直接在官方 **VM Emulator** 中运行。

---

## 功能概述

### 1. 词法分析（Lexer）

* 实现位置：`src/lexer/lexer.py`
* 功能：

  * 去除单行注释 `//` 和多行注释 `/* ... */`
  * 将源代码拆分为 Token 流，支持以下类型：

    * 关键字（Keyword）
    * 符号（Symbol）
    * 整数常量（Integer Constant）
    * 字符串常量（String Constant）
    * 标识符（Identifier）

---

### 2. 语法分析（Parser）

* 实现位置：`src/parser/parser.py`
* 使用 **递归下降分析法（Recursive Descent Parsing）**
* 支持 Jack 语言的完整语法结构：

  * 类（Class）
  * 子程序（Constructor / Function / Method）
  * 语句（let / if / while / do / return）
  * 表达式与项（Expression / Term）
* 在语法解析过程中**直接驱动代码生成模块**，不再构建中间 XML 语法树。

---

### 3. 语义分析与符号表（Symbol Table）

* 实现位置：`src/semantic/symbol_table.py`
* 维护两级作用域：

  * **类级作用域（Class Level）**
  * **子程序级作用域（Subroutine Level）**
* 对每个符号记录以下信息：

  * 名称（Name）
  * 类型（Type）
  * 种类（Kind：`static` / `field` / `arg` / `var`）
  * 索引（Index）
* 在代码生成阶段，用于确定变量对应的 **VM 段（Segment）** 及其偏移量。

---

### 4. 代码生成（Code Generation）

* 实现位置：`src/codegen/codegen.py`
* 提供标准 VM 指令的封装接口：

  * `push`, `pop`
  * `add`, `sub`, `neg`, `eq`, `gt`, `lt`, `and`, `or`, `not`
  * `label`, `goto`, `if-goto`
  * `call`, `function`, `return`
* 负责将：

  * 表达式计算
  * 流程控制（if / while）
  * 函数与方法调用（含对象方法与静态方法）

  翻译为对应的 VM 指令序列。

---

## 目录结构

```bash
chapter_11/
├── readme.md                  # 项目说明文档
├── build/                     # 编译输出目录（.vm 文件）
│   └── Fibonacci.vm
├── figures/                   # 截图与资源
├── inputs/                    # 测试用 Jack 源文件
│   └── Fibonacci.jack
├── src/                       # 编译器源代码
│   ├── __init__.py
│   ├── main.py                # 编译器入口（支持目录级编译）
│   ├── lexer/                 # 词法分析
│   │   └── lexer.py
│   ├── parser/                # 语法分析（驱动代码生成）
│   │   └── parser.py
│   ├── semantic/              # 符号表与语义信息
│   │   └── symbol_table.py
│   ├── codegen/               # VM 代码生成
│   │   └── codegen.py
│   ├── utils/                 # 工具模块
│   │   └── fileio.py
│   └── test/                  # 测试脚本
│       └── test.py
```

---

## 使用方法

### 命令行方式

在项目根目录下运行：

```bash
# 编译 inputs 目录下的所有 .jack 文件
python -m chapter_11.src.main D:\Data\resource\计算机系统要素资源\projects\chapter_11\inputs
```

---

### 代码调用方式

```python
from chapter_11.src.main import compile_directory

compile_directory(r"path/to/your/jack/files")
```

编译完成后，生成的 `.vm` 文件将输出到 `chapter_11/build` 目录
（或与源文件同目录，具体取决于 `main.py` 中的配置）。

---

## 关键实现思路

### 1. 从 XML 到 VM 的转变

* 第 10 章：生成 XML 语法树，用于验证解析正确性
* 第 11 章：**不再生成 XML**

  * 在 `parser.py` 中边解析边调用 `codegen`
  * 解析到表达式时，直接递归计算并将结果压入 VM 栈
* 编译器整体由「**语法驱动生成代码**」完成

---

### 2. 变量与 VM 内存段映射

符号表负责将 Jack 变量映射到 VM 内存段：

| Jack 变量类型 | VM 段       |
| --------- | ---------- |
| `static`  | `static`   |
| `field`   | `this`     |
| `arg`     | `argument` |
| `var`     | `local`    |

---

### 3. 子程序调用规则

* **构造函数（constructor）**

  * 调用 `Memory.alloc` 分配对象内存
  * 设置 `pointer 0`（`this`）指向新对象

* **方法（method）**

  * 调用时隐式传入 `this` 作为第一个参数

* **函数（function）**

  * 普通静态函数调用，不涉及对象实例

---

### 4. 流程控制实现

* `if` / `while` 语句通过生成**唯一 Label**
* 使用 `if-goto` 与 `goto` 指令完成条件跳转

---

## 测试结果

使用 `inputs/Fibonacci.jack` 进行测试：

1. 成功编译生成 `Fibonacci.vm`
2. 在 **VM Emulator / CPU Emulator** 中加载并运行
3. 程序行为与预期一致
![run](./figures/image.png)
