## 第 10 章：Jack 语法分析器（Syntax Analyzer）

本目录是根据《计算机系统要素（Nand2Tetris）》第 10 章实现的 **Jack 语法分析器**。  
它可以把 `.jack` 源程序解析为结构化的 XML 格式，为后续的代码生成阶段做准备。

---

### 功能概述

- **支持的语法结构**
  - **类定义（class）**
    - 类变量声明（`static`、`field`）
    - 子程序声明（`constructor`、`function`、`method`）
  - **子程序结构**
    - 参数列表（`parameterList`）
    - 子程序体（`subroutineBody`）
    - 局部变量声明（`var`）
    - 语句序列（`statements`）
  - **语句类型**
    - `let` 语句：变量赋值
    - `if` 语句：条件分支（支持 `else`）
    - `while` 语句：循环结构
    - `do` 语句：子程序调用
    - `return` 语句：返回值
  - **表达式处理**
    - 支持运算符优先级（`*`、`/`、`+`、`-`、`&`、`|`、`<`、`>`、`=`）
    - 支持括号表达式
    - 支持一元运算符（`-`、`~`）
    - 支持数组访问（`array[index]`）
    - 支持子程序调用（`method()`、`object.method()`、`Class.method()`）
    - 支持常量（整数、字符串、关键字常量：`true`、`false`、`null`、`this`）
  - **词法元素**
    - 关键字（`class`、`function`、`var` 等）
    - 标识符（类名、变量名、子程序名等）
    - 符号（`{`、`}`、`(`、`)`、`;`、`,` 等）
    - 整数常量
    - 字符串常量

---

### 代码结构

- `parser.py`：主程序，完成从 `.jack` 到 `.xml` 的整个转换流程：
  - `handleSingleJackFile`：读取源文件，去除注释和空白行，得到纯净的代码行。
  - `parser`：解析 Jack 文件，生成 XML 输出。
- `Class.py`：处理类级别的语法结构：
  - `handle_class`：解析类定义，包括类变量声明和子程序声明。
  - `handle_subroutine`：解析子程序（构造函数、函数、方法）。
  - `handle_subroutineParamList`：解析参数列表。
  - `handle_subroutineBody`：解析子程序体，包括局部变量声明和语句序列。
- `statement.py`：处理各种语句类型：
  - `handle_statements`：解析语句序列。
  - `handle_letStatement`：解析 `let` 语句。
  - `handle_ifStatement`：解析 `if` 语句。
  - `handle_whileStatement`：解析 `while` 语句。
  - `handle_doStatement`：解析 `do` 语句。
  - `handle_returnStatement`：解析 `return` 语句。
- `expression.py`：处理表达式：
  - `handle_expression`：递归下降解析表达式，处理运算符优先级。
  - `handle_term`：解析项（常量、变量、数组访问、子程序调用、括号表达式、一元运算符）。
  - `handle_expressionList`：解析表达式列表（用于子程序调用参数）。
- `var.py`：处理变量声明：
  - `handle_var`：解析局部变量声明。
  - `handle_classVar`：解析类变量声明。
- `utils/`：工具函数：
  - `utils.py`：提供注释去除、空白处理等辅助函数。
  - `bracketsParser.py`：提供括号匹配等解析工具。

---

### 使用方法

在项目根目录下，使用 Python 运行：

```python
from chapter_10.parser import parser

# 解析 Jack 文件并生成 XML 文件
jack_path = "path/to/your/file.jack"
output_path = "path/to/output/file.xml"
parser(jack_path, output_path)
```

示例（以测试用例为例）：

```python
# 解析 Main.jack 并生成 MainCustom.xml
parser(
    r"chapter_10\ArrayTest\Main.jack",
    r"chapter_10\ArrayTest\MainCustom.xml"
)
```

或者直接运行 `parser.py`：

```bash
python chapter_10/parser.py
```

（需要修改 `parser.py` 中的 `jack_file_path` 和 `output_file_path` 变量）

---

### 关键实现思路回顾

- **递归下降解析**
  - 按照 Jack 语言的语法规则，为每个语法结构编写对应的处理函数。
  - 使用递归方式处理嵌套的语法结构（如表达式中的括号、语句中的嵌套语句）。
- **运算符优先级处理**
  - 表达式解析采用递归下降方式，按照优先级从低到高依次处理：
    1. 表达式（`expression`）：处理 `+`、`-`、`&`、`|`、`<`、`>`、`=`
    2. 项（`term`）：处理 `*`、`/`
    3. 一元运算符：处理 `-`、`~`
- **括号匹配**
  - 使用状态机检查括号匹配，正确处理字符串中的括号和嵌套括号。
  - 在解析表达式时，自动去除最外层的括号（如果存在）。
- **语句识别**
  - 使用装饰器模式注册语句处理器，通过关键字匹配识别不同的语句类型。
  - 支持语句序列的连续解析，自动跳过空白字符。
- **子程序调用识别**
  - 区分三种调用形式：
    - `method()`：当前对象的方法调用
    - `object.method()`：对象方法调用
    - `Class.method()`：类方法调用
- **注释和空白处理**
  - 支持单行注释（`//`）和块注释（`/* ... */`）。
  - 自动去除注释和多余的空白字符，保留必要的空格用于词法分析。

---

### 测试

本项目已通过以下测试用例：

- **ArrayTest 测试**
  - ✅ `Main.jack` - 数组操作测试

- **ExpressionLessSquare 测试**
  - ✅ `Main.jack` - 表达式解析测试

- **Square 测试**
  - ✅ `Main.jack` - 主程序测试

所有生成的 `.xml` 文件（`*Custom.xml`）已与官方提供的参考文件（`*.xml`）进行对比验证，测试结果完全匹配。

---

### 总结

这一章的实现从零开始手写了一个完整的 Jack 语法分析器，  
通过 **递归下降解析、运算符优先级处理、括号匹配、语句识别** 等技术，  
把"Jack 源程序"成功解析为"结构化的 XML 格式"，  
为后续章节（如代码生成）的实现奠定了基础。

语法分析器是编译器的前端部分，它验证源代码是否符合语法规则，  
并将源代码转换为抽象语法树（AST）的中间表示形式（这里以 XML 格式输出），  
为后续的语义分析和代码生成阶段提供结构化的输入。

刚开始的时候一脸懵逼，都看不懂说的啥，引导做的不是很好，
后来配合 AI 勉勉强强写了个 parser，AI 建议用 tokenizer 方法做，但是我想用自己的方式试试，最后就做成这样子了，最后结果还行。