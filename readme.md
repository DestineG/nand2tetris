## Hack Assembler 结构

```bash
Hack Assembler
└─ hack_assembler(input_file)
   ├─ extract_instructions
   │  └─ raw asm lines
   │     ├─ remove comments
   │     └─ remove empty lines
   │
   ├─ extract_pseudo_instructions
   │  ├─ pseudo instructions
   │  │  └─ (LABEL) → symbol, rom_address
   │  └─ pure instructions
   │
   ├─ build_symbol_table
   │  ├─ predefined symbols
   │  │  ├─ SP, LCL, ARG, THIS, THAT
   │  │  ├─ R0 ~ R15
   │  │  ├─ SCREEN
   │  │  └─ KBD
   │  │
   │  ├─ label symbols
   │  │  └─ symbol → instruction address
   │  │
   │  └─ variable symbols
   │     └─ symbol → RAM address (from 16)
   │
   ├─ replace_symbols
   │  └─ @symbol → @address
   │
   ├─ instruction translation
   │  ├─ A-instruction
   │  │  └─ parse_a_instruction
   │  │     └─ 0vvvvvvvvvvvvvvv
   │  │
   │  └─ C-instruction
   │     └─ parse_c_instruction
   │        ├─ dest
   │        ├─ comp
   │        └─ jump
   │           └─ translate_c_instruction
   │              └─ 111accccccdddjjj
   │
   └─ output
      └─ write .hack binary file
```

**核心特点**

* 典型的 **两遍扫描**
* 没有 AST，直接是“文本 → 语义 → 编码”
* 符号表是整个系统第一次正式出现的“全局状态”

---

## VM Translator 结构

```bash
VM Translator
└─ vm_translator(input_path)
   ├─ input dispatch
   │  ├─ single .vm file
   │  └─ directory of .vm files
   │
   ├─ (optional) bootstrap code
   │  ├─ SP = 256
   │  ├─ LCL / ARG / THIS / THAT init
   │  └─ call Sys.init
   │
   └─ parse_vm_file
      ├─ extract_instructions
      │  └─ VM commands (no comments)
      │
      ├─ for each VM instruction
      │  ├─ arithmetic / logical
      │  │  └─ add | sub | neg | eq | gt | lt | and | or | not
      │  │
      │  ├─ memory access
      │  │  ├─ push segment index
      │  │  └─ pop  segment index
      │  │
      │  ├─ program flow
      │  │  ├─ label
      │  │  ├─ goto
      │  │  └─ if-goto
      │  │     └─ function-scoped labels
      │  │
      │  ├─ function declaration
      │  │  └─ function name nLocals
      │  │     ├─ update current function
      │  │     └─ initialize local variables
      │  │
      │  ├─ function call
      │  │  └─ call name nArgs
      │  │     ├─ push return address
      │  │     ├─ save LCL / ARG / THIS / THAT
      │  │     ├─ reposition ARG / LCL
      │  │     └─ goto function entry
      │  │
      │  └─ return
      │     ├─ restore caller frame
      │     ├─ reposition SP
      │     └─ goto return address
      │
      ├─ template dispatch
      │  └─ templateDict[command]
      │     └─ VM → Hack ASM expansion
      │
      └─ output
         └─ concatenated ASM code
```

---

## jack 类结构

``` bash
Main
├─ Class Variable Declarations
│  ├─ static varType
│  │  └─ varName ( , varName )*
│  └─ field varType
│     └─ varName ( , varName )*
│
└─ Subroutine Declarations
   ├─ Constructor
   │  ├─ subroutine name
   │  ├─ return type
   │  │  └─ void | varType
   │  ├─ parameter list
   │  │  └─ ( varType varName ( , varType varName )* )?
   │  └─ subroutine body
   │     ├─ subroutine var declarations
   │     │  └─ var varType varName ( , varName )*
   │     └─ statements
   │        ├─ let statement
   │        │  ├─ varName
   │        │  ├─ [ expression ]?
   │        │  └─ expression
   │        │
   │        ├─ if statement
   │        │  ├─ condition: expression
   │        │  ├─ then: statements
   │        │  └─ else: statements (optional)
   │        │
   │        ├─ while statement
   │        │  ├─ condition: expression
   │        │  └─ body: statements
   │        │
   │        ├─ do statement
   │        │  └─ subroutineCall
   │        │
   │        └─ return statement
   │           └─ expression?
   │
   ├─ Method
   │  ├─ subroutine name
   │  ├─ return type
   │  │  └─ void | varType
   │  ├─ parameter list
   │  │  └─ ( varType varName ( , varType varName )* )?
   │  └─ subroutine body
   │     ├─ subroutine var declarations
   │     │  └─ var varType varName ( , varName )*
   │     └─ statements
   │        └─ (same as above)
   │
   └─ Function
      ├─ subroutine name
      ├─ return type
      │  └─ void | varType
      ├─ parameter list
      │  └─ ( varType varName ( , varType varName )* )?
      └─ subroutine body
         ├─ subroutine var declarations
         │  └─ var varType varName ( , varName )*
         └─ statements
            └─ (same as above)
   
Statements Expansion
└─ statements
   ├─ let statement
   │  ├─ varName
   │  ├─ [ expression ]?
   │  └─ expression
   │
   ├─ if statement
   │  ├─ condition: expression
   │  ├─ then: statements
   │  └─ else: statements (optional)
   │
   ├─ while statement
   │  ├─ condition: expression
   │  └─ body: statements
   │
   ├─ do statement
   │  └─ subroutineCall
   │
   └─ return statement
      └─ expression?

Subroutine Call
└─ subroutineCall
   ├─ subroutineName
   │  └─ expressionList
   │
   └─ ( className | varName )
      └─ subroutineName
         └─ expressionList

Expression List
└─ expressionList
   └─ ( expression ( , expression )* )?

Expression
└─ expression
   ├─ term
   └─ ( op term )*

Term
└─ term
   ├─ integerConstant
   ├─ stringConstant
   ├─ keywordConstant
   │  └─ true | false | null | this
   ├─ varName
   ├─ varName
   │  └─ [ expression ]
   ├─ subroutineCall
   ├─ ( expression )
   └─ unaryOp
      └─ term

Operator
└─ op
   ├─ +
   ├─ -
   ├─ *
   ├─ /
   ├─ &
   ├─ |
   ├─ <
   ├─ >
   └─ =

Unary Operator
└─ unaryOp
   ├─ -
   └─ ~

Variable Type
└─ varType
   ├─ int
   ├─ char
   ├─ boolean
   └─ className

```

**示例代码**
``` java
class Main {
    // 类字段
    static int MAX_COUNT;
    field int counter;
    
    // 类构造函数
    constructor Main new() {
        let counter = 0;
        return this;
    }

    // 类方法(实例方法)
    method void increment() {
        if (this.counter < MAX_COUNT) {
            let this.counter = this.counter + 1;
        }
    }

    // 类函数(静态方法)
    function int getMaxCount() {
        return MAX_COUNT;
    }

    // 类函数(静态方法)
    function void setMaxCount(int max) {
        let MAX_COUNT = max;
    }

    // 类函数(静态方法)
    function int mul(int a, int b) {
        var int i, result;
        let result = 0;
        let i = 0;
        while (i < b) {
            let result = result + a;
            let i = i + 1;
        }
        return result;
    }

    // 类函数(静态方法)
    function int fibonacci(int n) {
        if (n <= 1) {
            return n;
        }
        return Main.fibonacci(n - 1) + Main.fibonacci(n - 2);
    }
}
```

---

## jack parser 结构

``` bash
compile_class
├─ eat('class')
├─ eat(className)
│  └─ lexer.set_class_name(className)
├─ eat('{')
│
├─ while token in ('static', 'field')
│  └─ compile_class_var_dec
│     ├─ eat('static' | 'field')
│     ├─ eat(type)
│     ├─ eat(varName)
│     ├─ while token == ','
│     │  └─ eat(varName)
│     └─ eat(';')
│
├─ while token in ('constructor', 'function', 'method')
│  └─ compile_subroutine_dec
│     ├─ symbol_table.start_subroutine
│     ├─ eat('constructor' | 'function' | 'method')
│     │
│     ├─ if method
│     │  └─ symbol_table.define('this', className, 'arg')
│     │
│     ├─ eat(returnType)
│     ├─ eat(subroutineName)
│     ├─ eat('(')
│     ├─ compile_parameter_list
│     │  ├─ if not ')'
│     │  │  ├─ eat(type)
│     │  │  ├─ eat(varName)
│     │  │  └─ symbol_table.define(arg)
│     │  └─ while token == ','
│     │     └─ repeat
│     ├─ eat(')')
│     │
│     └─ compile_subroutine_body
│        ├─ eat('{')
│        │
│        ├─ while token == 'var'
│        │  └─ compile_subroutine_var_dec
│        │
│        ├─ codegen.write_function
│        │
│        ├─ if constructor
│        │  ├─ codegen.write_push(constant, fieldCount)
│        │  ├─ codegen.write_call(Memory.alloc)
│        │  └─ codegen.write_pop(pointer, 0)
│        │
│        ├─ if method
│        │  ├─ codegen.write_push(argument, 0)
│        │  └─ codegen.write_pop(pointer, 0)
│        │
│        ├─ compile_subroutine_statements
│        │  └─ (let | if | while | do | return)*
│        │
│        └─ eat('}')
│
└─ eat('}')
```

---

## 总结

| 层级             | 本质             |
| -------------- | -------------- |
| Hack Assembler | 指令级语义 → 机器编码   |
| VM Translator  | 栈式 IR → 底层指令序列 |
| Jack Compiler  | 语法结构 → 栈式 IR   |

---

## 结语

至此，本书就差不多学完了，在 AI 的配合下，从底层开始，实现了 `VM → Hack asm → Bin` 的翻译器，随后又采用自上而下的递归下降分析实现了 `Jack → VM` 的编译器，构建了一条完整的 `Jack → Bin` 编译工具链，大致弄懂了其中 70% 的内容，让我对计算机系统和编译器有了一个更加全面的认识。

(ps: AI 确实是一位好老师，常常能够在关键节点上提供及时的引导，帮助我少走不少弯路。)

这是一本好书，或者说，是一本很适合我当前阶段的书。如果一开始就让我去看《龙书》之类的经典教材，可能连词法分析那一章都坚持不下来，哈哈。

希望大家也都能从这本书中，学到自己想学的东西。
