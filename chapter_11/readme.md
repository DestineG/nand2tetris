这是基于 **《计算机系统要素》第十一章** 的 **Jack 语言编译器** 项目实现（Python 版本）。  

- **词法分析（Lexer）**
- **语法分析（Parser）**
- **语义分析（Semantic）**
- **代码生成（Code Generator）** → 可以生成 VM 代码或者中间代码。

---

## 目录结构

``` bash
jack_compiler/
├── README.md                  # 项目说明文档
├── requirements.txt           # Python 库依赖（如 ply 等）
├── src/                       # 源代码目录
│   ├── __init__.py            # 包初始化
│   ├── main.py                # 编译器入口
│   ├── lexer/                 # 词法分析模块
│   │   ├── __init__.py
│   │   └── lexer.py
│   ├── parser/                # 语法分析模块
│   │   ├── __init__.py
│   │   └── parser.py
│   ├── semantic/              # 语义分析模块
│   │   ├── __init__.py
│   │   └── semantic.py
│   ├── codegen/               # 代码生成模块
│   │   ├── __init__.py
│   │   └── codegen.py
│   └── utils/                 # 工具函数模块
│       ├── __init__.py
│       └── utils.py
├── inputs/                    # Jack 源程序文件，作为测试输入
│   ├── Main.jack
│   └── Square.jack
├── build/                     # 编译器生成的 VM 文件
└── docs/                      # 项目相关文档
```

---

## 开发建议

* 先实现 **lexer**，再实现 **parser**，最后实现 **semantic** 和 **codegen**。
* 建议使用 **测试驱动开发（TDD）**。
* 输出文件统一存放在 `output/` 目录，方便管理和验证。
