# src/parser/parser.py

from ..lexer.lexer import Lexer, token_types_alias
from ..semantic.symbol_table import SymbolTable
from ..codegen.codegen import CodeGenerator

class Parser:
    def __init__(self, jack_file_path=None, output_file=None):
        self.lexer = Lexer(jack_file_path)
        # lexer 初始化后，指向第一个 token
        assert self.lexer.has_more_tokens(), "输入文件为空或无有效词法单元"
        self.lexer.advance()
        self.current_token_type, self.current_token_value = self.lexer.token()
        self.symbol_table = SymbolTable()
        self.codegen = CodeGenerator(output_file)
        self.label_index = 0

    def eat(self, expected_type, next_token=False):
        assert self.lexer.token_type() == expected_type, f"预期类型 {expected_type}，但得到 {self.lexer.token_type()}，值为 {self.lexer.token_value()}"
        token = self.lexer.token()
        if next_token:
            assert self.lexer.has_more_tokens(), "无更多词法单元"
            self.lexer.advance()
            self.current_token_type, self.current_token_value = self.lexer.token()
        return token

    def compile_class_var_dec(self):
        # 变量种类为: 'static' | 'field'
        _, kind = self.eat(token_types_alias["keyword"], next_token=True)     # static | field
        if self.current_token_type == token_types_alias["keyword"] and self.current_token_value in ("int", "char", "boolean"):  # type
            _, var_type = self.eat(token_types_alias["keyword"], next_token=True)
        elif self.current_token_type == token_types_alias["identifier"]:
            _, var_type = self.eat(token_types_alias["identifier"], next_token=True)
        else:
            raise ValueError(f"预期类型或类名，但得到 {self.current_token_value}")
        _, var_name = self.eat(token_types_alias["identifier"], next_token=True)  # varName
        self.symbol_table.define(var_name, var_type, kind)
        while self.current_token_value == ',':
            self.eat(token_types_alias["symbol"], next_token=True)      # ','
            _, var_name = self.eat(token_types_alias["identifier"], next_token=True)  # varName
            self.symbol_table.define(var_name, var_type, kind)

        self.eat(token_types_alias["symbol"], next_token=True)  # ';'
    
    def compile_parameter_list(self):
        # 空参数列表
        if self.current_token_value == ')':
            return
        if self.current_token_type == token_types_alias["keyword"] and self.current_token_value in ("int", "char", "boolean"):
            _, var_type = self.eat(token_types_alias["keyword"], next_token=True)  # type
        elif self.current_token_type == token_types_alias["identifier"]:
            _, var_type = self.eat(token_types_alias["identifier"], next_token=True)  # type
        else:
            raise ValueError("参数列表中类型错误")
        _, var_name = self.eat(token_types_alias["identifier"], next_token=True)  # varName
        # 变量种类默认为 'arg' 类型
        self.symbol_table.define(var_name, var_type, 'arg')
        while self.current_token_value == ',':
            self.eat(token_types_alias["symbol"], next_token=True)      # ','
            if self.current_token_type == token_types_alias["keyword"] and self.current_token_value in ("int", "char", "boolean"):
                _, var_type = self.eat(token_types_alias["keyword"], next_token=True)  # type
            elif self.current_token_type == token_types_alias["identifier"]:
                _, var_type = self.eat(token_types_alias["identifier"], next_token=True)  # type
            else:
                raise ValueError("参数列表中类型错误")
            _, var_name = self.eat(token_types_alias["identifier"], next_token=True)  # varName
            self.symbol_table.define(var_name, var_type, 'arg')

    def compile_subroutine_var_dec(self):
        # 变量种类默认为 'var' 类型
        self.eat(token_types_alias["keyword"], next_token=True)     # 'var'
        if self.current_token_type == token_types_alias["keyword"] and self.current_token_value in ("int", "char", "boolean"):  # type
            _, var_type = self.eat(token_types_alias["keyword"], next_token=True)
        elif self.current_token_type == token_types_alias["identifier"]:
            _, var_type = self.eat(token_types_alias["identifier"], next_token=True)
        else:
            raise ValueError(f"预期类型或类名，但得到 {self.current_token_value}")
        _, var_name = self.eat(token_types_alias["identifier"], next_token=True)  # varName
        self.symbol_table.define(var_name, var_type, "var")

        while self.current_token_value == ',':
            self.eat(token_types_alias["symbol"], next_token=True)      # ','
            _, var_name = self.eat(token_types_alias["identifier"], next_token=True)  # varName
            self.symbol_table.define(var_name, var_type, "var")
        self.eat(token_types_alias["symbol"], next_token=True)  # ';'

    def compile_expression_list(self):
        """
        解析实参列表并返回参数个数
        """
        n_args = 0
        if self.current_token_value != ')':
            self.compile_expression()
            n_args = 1
            while self.current_token_value == ',':
                self.eat(token_types_alias["symbol"], next_token=True)  # ','
                self.compile_expression()
                n_args += 1
        return n_args

    def compile_term(self):
        # 一元运算符
        if self.current_token_value in ('-', '~'):
            _, unary_op = self.eat(token_types_alias["symbol"], next_token=True)  # unaryOp
            self.compile_term()
            if unary_op == '-': self.codegen.write_arithmetic('neg')
            elif unary_op == '~': self.codegen.write_arithmetic('not')
        
        # 括号内表达式
        elif self.current_token_value == '(':
            self.eat(token_types_alias["symbol"], next_token=True)  # '('
            self.compile_expression()
            self.eat(token_types_alias["symbol"], next_token=True)  # ')'

        # 整数常量
        elif self.current_token_type == token_types_alias["integerConstant"]:
            _, int_value = self.eat(token_types_alias["integerConstant"], next_token=True)
            self.codegen.write_push('constant', int_value)

        # 字符串常量
        elif self.current_token_type == token_types_alias["stringConstant"]:
            _, string_value = self.eat(token_types_alias["stringConstant"], next_token=True)

            # 首先在堆栈中创建一个新的字符串对象
            self.codegen.write_push('constant', len(string_value))
            self.codegen.write_call('String.new', 1)
            # 然后逐字符添加到字符串对象中
            for char in string_value:
                self.codegen.write_push('constant', ord(char))
                self.codegen.write_call('String.appendChar', 2)
                # String.appendChar 会返回字符串对象自身的引用在栈顶，
                # 但我们不需要使用它，所以丢弃，避免栈污染
                self.codegen.write_pop('temp', 0)

        # 关键字常量
        elif self.current_token_type == token_types_alias["keyword"] and self.current_token_value in ('true', 'false', 'null', 'this'):
            _, keyword_const = self.eat(token_types_alias["keyword"], next_token=True)
            if keyword_const == 'this': self.codegen.write_push('pointer', 0)
            else: self.codegen.write_push('constant', 0)
            if keyword_const == 'true': self.codegen.write_arithmetic('not')

        # 标识符
        elif self.current_token_type == token_types_alias["identifier"]:
            next_token = self.lexer.peek()
            if next_token is None:
                raise ValueError("意外的文件结尾")
            _, next_token_value = next_token
            # 数组访问
            if next_token_value == '[':
                _, var_name = self.eat(token_types_alias["identifier"], next_token=True)  # varName
                # 基地址入栈
                kind = self.symbol_table.kind_of(var_name)
                idx = self.symbol_table.index_of(var_name)
                self.codegen.write_push(kind, idx)

                # 偏移量计算
                self.eat(token_types_alias["symbol"], next_token=True)      # '['
                self.compile_expression()
                self.eat(token_types_alias["symbol"], next_token=True)      # ']'

                # 基地址 + 偏移量，计算出目标地址
                self.codegen.write_arithmetic('add')
                # 将目标地址存入 pointer 1
                self.codegen.write_pop('pointer', 1)
                # 取出目标地址中的值入栈
                self.codegen.write_push('that', 0)
            # 跨类调用
            elif next_token_value == '.':
                _, name = self.eat(token_types_alias["identifier"], next_token=True)  # className | varName
                self.eat(token_types_alias["symbol"], next_token=True)      # '.'
                _, sub_name = self.eat(token_types_alias["identifier"], next_token=True)  # subroutineName

                type_of_name = self.symbol_table.type_of(name)
                # 类名
                if type_of_name is not None:
                    kind = self.symbol_table.kind_of(name)
                    idx = self.symbol_table.index_of(name)
                    # 将对象引用入栈作为第一个参数
                    self.codegen.write_push(kind, idx)
                    # 调用类方法，由此可以看出对象方法调用实际上
                    # 就是将对象引用作为第一个参数传递给类方法，然后执行类代码
                    full_name = f"{type_of_name}.{sub_name}"
                    # 此处隐式传递了一个参数（对象引用），所以参数数量加 1
                    n_args = 1
                else:
                    # 静态方法调用，不需要传递对象引用
                    full_name = f"{name}.{sub_name}"
                    # 参数数量为 0
                    n_args = 0
                self.eat(token_types_alias["symbol"], next_token=True)      # '('
                # 实参列表解析并入栈，同时统计参数数量
                n_args += self.compile_expression_list()
                self.eat(token_types_alias["symbol"], next_token=True)      # ')'
                # 生成调用指令
                self.codegen.write_call(full_name, n_args)
            # 本类调用
            elif next_token_value == '(':
                _, sub_name = self.eat(token_types_alias["identifier"], next_token=True)  # subroutineName
                # 将 this 指针入栈作为第一个参数
                self.codegen.write_push('pointer', 0)
                full_name = f"{self.lexer.get_class_name()}.{sub_name}"
                n_args = 1
                self.eat(token_types_alias["symbol"], next_token=True)      # '('
                # 实参列表解析并入栈，同时统计参数数量
                n_args += self.compile_expression_list()
                self.eat(token_types_alias["symbol"], next_token=True)      # ')'
                # 生成调用指令
                self.codegen.write_call(full_name, n_args)
            # 变量
            else:
                _, var_name = self.eat(token_types_alias["identifier"], next_token=True)  # varName
                kind = self.symbol_table.kind_of(var_name)
                idx = self.symbol_table.index_of(var_name)
                self.codegen.write_push(kind, idx)

    def compile_expression(self):
        # 第一个 term 的计算结果入栈
        self.compile_term()
        while self.current_token_value in ('+', '-', '*', '/', '&', '|', '<', '>', '='):
            _, op = self.eat(token_types_alias["symbol"], next_token=True)  # op
            # 第二个 term 的计算结果入栈
            self.compile_term()

            # 生成算术指令
            if op == '+': self.codegen.write_arithmetic('add')
            elif op == '-': self.codegen.write_arithmetic('sub')
            elif op == '*': self.codegen.write_call('Math.multiply', 2)
            elif op == '/': self.codegen.write_call('Math.divide', 2)
            elif op == '&': self.codegen.write_arithmetic('and')
            elif op == '|': self.codegen.write_arithmetic('or')
            elif op == '<': self.codegen.write_arithmetic('lt')
            elif op == '>': self.codegen.write_arithmetic('gt')
            elif op == '=': self.codegen.write_arithmetic('eq')

    def compile_let(self):
        self.eat(token_types_alias["keyword"], next_token=True) # 'let'
        _, var_name = self.eat(token_types_alias["identifier"], next_token=True)
        
        is_array = False
        if self.current_token_value == '[':
            is_array = True
            # 数组基地址入栈
            kind = self.symbol_table.kind_of(var_name)
            idx = self.symbol_table.index_of(var_name)
            self.codegen.write_push(kind, idx)
            
            # 偏移量计算
            self.eat(token_types_alias["symbol"], next_token=True) # '['
            self.compile_expression() 
            self.eat(token_types_alias["symbol"], next_token=True) # ']'
            
            # 基地址 + 偏移量，计算出目标地址
            self.codegen.write_arithmetic('add')

        self.eat(token_types_alias["symbol"], next_token=True) # '='

        # 计算等号右侧的表达式
        self.compile_expression()
        self.eat(token_types_alias["symbol"], next_token=True) # ';'

        # 生成最终存储指令；此时栈顶为表达式的值
        if is_array:
            # 此时栈顶 = 值，次栈顶 = 目标地址
            # 让 that 指针指向目标地址；使用 pop that 0 把值存入目标地址
            self.codegen.write_pop('temp', 0)
            self.codegen.write_pop('pointer', 1)
            self.codegen.write_push('temp', 0)
            self.codegen.write_pop('that', 0)
        else:
            # 普通变量赋值
            kind = self.symbol_table.kind_of(var_name)
            idx = self.symbol_table.index_of(var_name)
            self.codegen.write_pop(kind, idx)
    
    def compile_if(self):
        # 生成唯一的 TRUE 和 FALSE 标签
        true_label = f"IF_TRUE_{self.label_index}"
        false_label = f"IF_FALSE_{self.label_index}"
        end_label = f"IF_END_{self.label_index}"
        self.label_index += 1

        self.eat(token_types_alias["keyword"], next_token=True)  # 'if'
        # 条件表达式计算结果入栈
        self.eat(token_types_alias["symbol"], next_token=True)   # '('
        self.compile_expression()
        self.eat(token_types_alias["symbol"], next_token=True)   # ')'
        # 生成条件跳转指令 结果为 true 时跳转到 TRUE 标签
        self.codegen.write_if(true_label)
        # 条件为 false，跳转到 FALSE 标签
        self.codegen.write_goto(false_label)
        # 生成 TRUE 标签
        self.codegen.write_label(true_label)
        # if 语句块
        self.eat(token_types_alias["symbol"], next_token=True)   # '{'
        self.compile_subroutine_statements()
        self.eat(token_types_alias["symbol"], next_token=True)   # '}'
        # 跳转到 END 标签
        self.codegen.write_goto(end_label)
        # else 语句块
        if self.current_token_value == 'else':
            # 生成 FALSE 标签
            self.codegen.write_label(false_label)
            self.eat(token_types_alias["keyword"], next_token=True)  # 'else'
            self.eat(token_types_alias["symbol"], next_token=True)   # '{'
            self.compile_subroutine_statements()
            self.eat(token_types_alias["symbol"], next_token=True)   # '}'
        else:
            self.codegen.write_label(false_label)
        # 生成 END 标签
        self.codegen.write_label(end_label)
    
    def compile_while(self):
        # 生成唯一 START 和 END 标签
        start_label = f"WHILE_START_{self.label_index}"
        end_label = f"WHILE_END_{self.label_index}"
        self.label_index += 1
        self.eat(token_types_alias["keyword"], next_token=True)  # 'while'
        # 生成循环开始标签
        self.codegen.write_label(start_label)
        # 条件表达式
        self.eat(token_types_alias["symbol"], next_token=True)   # '('
        self.compile_expression()
        self.eat(token_types_alias["symbol"], next_token=True)   # ')'
        # 生成条件跳转指令 结果为 false 时跳出循环
        self.codegen.write_arithmetic('not')
        # if-goto 当栈顶为 true 时跳转，但 jack 的 while 跳转逻辑是为 false 时跳转，
        # 所以这里需要先取反
        self.codegen.write_if(end_label)
        # 循环体
        self.eat(token_types_alias["symbol"], next_token=True)   # '{'
        self.compile_subroutine_statements()
        self.eat(token_types_alias["symbol"], next_token=True)   # '}'
        # 生成循环结束标签
        self.codegen.write_goto(start_label)
        self.codegen.write_label(end_label)

    def compile_do(self):
        self.eat(token_types_alias["keyword"], next_token=True)  # 'do'
        # subroutineCall
        self.compile_term()  # 利用 compile_term 处理子程序调用
        self.eat(token_types_alias["symbol"], next_token=True)      # ';'
        # 丢弃子程序返回值
        self.codegen.write_pop('temp', 0)

    def compile_return(self):
        self.eat(token_types_alias["keyword"], next_token=True)  # 'return'
        if self.current_token_value != ';':
            self.compile_expression()
        else:
            # 无返回值时，默认返回 0
            self.codegen.write_push('constant', 0)
        self.eat(token_types_alias["symbol"], next_token=True)      # ';'
        # 生成返回指令
        self.codegen.write_return()

    def compile_subroutine_statements(self):
        while self.current_token_value in ('let', 'if', 'while', 'do', 'return'):
            if self.current_token_value == 'let':
                self.compile_let()
            elif self.current_token_value == 'if':
                self.compile_if()
            elif self.current_token_value == 'while':
                self.compile_while()
            elif self.current_token_value == 'do':
                self.compile_do()
            elif self.current_token_value == 'return':
                self.compile_return()

    def compile_subroutine_body(self, subroutine_type, subroutine_name):
        self.eat(token_types_alias["symbol"], next_token=True)      # '{'

        # 处理局部变量声明
        while self.current_token_value == 'var':
            self.compile_subroutine_var_dec()
        
        # 生成函数定义指令
        n_locals = self.symbol_table.var_count('var')
        full_subroutine_name = f"{self.lexer.get_class_name()}.{subroutine_name}"
        self.codegen.write_function(full_subroutine_name, n_locals)

        # 构造函数需要为对象分配内存并设置 this 指针
        if subroutine_type == 'constructor':
            # 分配内存
            n_fields = self.symbol_table.var_count('field')
            self.codegen.write_push('constant', n_fields)
            self.codegen.write_call('Memory.alloc', 1)
            # 设置 this 指针
            self.codegen.write_pop('pointer', 0)
        
        elif subroutine_type == 'method':
            # 方法调用时，隐式传递了 this 参数，设置 this 指针
            self.codegen.write_push('argument', 0)
            self.codegen.write_pop('pointer', 0)

        self.compile_subroutine_statements()

        self.eat(token_types_alias["symbol"], next_token=True)      # '}'
        

    def compile_subroutine_dec(self):
        self.symbol_table.start_subroutine()
        _, subroutine_type = self.eat(token_types_alias["keyword"], next_token=True)  # constructor | function | method

        if subroutine_type == 'method':
            # 方法隐式传递 this 参数，所以形参数量加 1
            self.symbol_table.define('this', self.lexer.get_class_name(), 'arg')

        # 返回类型
        if self.current_token_value in ('void', 'int', 'char', 'boolean'):
            self.eat(token_types_alias["keyword"], next_token=True)
        elif self.current_token_type == token_types_alias["identifier"]:
            self.eat(token_types_alias["identifier"], next_token=True)
        else:
            raise ValueError(f"无效的返回类型: {self.current_token_value}")

        # 获取子程序名
        _, subroutine_name = self.eat(token_types_alias["identifier"], next_token=True)  # subroutineName

        self.eat(token_types_alias["symbol"], next_token=True)      # '('
        self.compile_parameter_list()
        self.eat(token_types_alias["symbol"], next_token=True)      # ')'
        self.compile_subroutine_body(subroutine_type, subroutine_name)

    def compile_class(self):
        self.eat(token_types_alias["keyword"], next_token=True)     # 'class'
        _, class_name = self.eat(token_types_alias["identifier"], next_token=True)  # className
        self.lexer.set_class_name(class_name)
        self.eat(token_types_alias["symbol"], next_token=True)      # '{'

        while self.current_token_value in ('static', 'field'):
            self.compile_class_var_dec()

        while self.current_token_value in ('constructor', 'function', 'method'):
            self.compile_subroutine_dec()

        self.eat(token_types_alias["symbol"])  # '}'（文件结尾，不前进）


if __name__ == "__main__":
    # 简单测试
    jack_file_path = r"D:\Data\resource\计算机系统要素资源\projects\chapter_11\inputs\Square.jack"
    output_file = r"D:\Data\resource\计算机系统要素资源\projects\chapter_11\build\Square.vm"
    parser = Parser(jack_file_path, output_file)
    print("开始解析类...")
    parser.compile_class()
    print("解析完成")