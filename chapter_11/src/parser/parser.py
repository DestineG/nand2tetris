# src/parser/parser.py

from ..lexer.lexer import Lexer, token_types_alias


class Parser:
    def __init__(self, jack_file_path):
        self.lexer = Lexer(jack_file_path)
        # lexer 初始化后，指向第一个 token
        assert self.lexer.has_more_tokens(), "输入文件为空或无有效词法单元"
        self.lexer.advance()
        self.current_token_type, self.current_token_value = self.lexer.token()
    
    def eat(self, expected_type, next_token=False):
        assert self.lexer.token_type() == expected_type, f"预期类型 {expected_type}，但得到 {self.lexer.token_type()}，值为 {self.lexer.token_value()}"
        if next_token:
            assert self.lexer.has_more_tokens(), "无更多词法单元"
            self.lexer.advance()
            self.current_token_type, self.current_token_value = self.lexer.token()

    def compile_class_var_dec(self):
        self.eat(token_types_alias["keyword"], next_token=True)     # static | field
        if self.current_token_type == token_types_alias["keyword"] and self.current_token_value in ("int", "char", "boolean"):  # type
            self.eat(token_types_alias["keyword"], next_token=True)
        elif self.current_token_type == token_types_alias["identifier"]:
            self.eat(token_types_alias["identifier"], next_token=True)
        else:
            raise ValueError(f"预期类型或类名，但得到 {self.current_token_value}")
        self.eat(token_types_alias["identifier"], next_token=True)  # varName

        while self.current_token_value == ',':
            self.eat(token_types_alias["symbol"], next_token=True)      # ','
            self.eat(token_types_alias["identifier"], next_token=True)  # varName

        self.eat(token_types_alias["symbol"], next_token=True)  # ';'
    
    def compile_parameter_list(self):
        # 空参数列表
        if self.current_token_value == ')':
            return
        if self.current_token_type == token_types_alias["keyword"] and self.current_token_value in ("int", "char", "boolean"):
            self.eat(token_types_alias["keyword"], next_token=True)  # type
        elif self.current_token_type == token_types_alias["identifier"]:
            self.eat(token_types_alias["identifier"], next_token=True)  # type
        else:
            raise ValueError("参数列表中类型错误")
        self.eat(token_types_alias["identifier"], next_token=True)  # varName
        while self.current_token_value == ',':
            self.eat(token_types_alias["symbol"], next_token=True)      # ','
            if self.current_token_type == token_types_alias["keyword"] and self.current_token_value in ("int", "char", "boolean"):
                self.eat(token_types_alias["keyword"], next_token=True)  # type
            elif self.current_token_type == token_types_alias["identifier"]:
                self.eat(token_types_alias["identifier"], next_token=True)  # type
            else:
                raise ValueError("参数列表中类型错误")
            self.eat(token_types_alias["identifier"], next_token=True)  # varName

    def compile_subroutine_var_dec(self):
        self.eat(token_types_alias["keyword"], next_token=True)     # 'var'
        if self.current_token_type == token_types_alias["keyword"] and self.current_token_value in ("int", "char", "boolean"):  # type
            self.eat(token_types_alias["keyword"], next_token=True)
        elif self.current_token_type == token_types_alias["identifier"]:
            self.eat(token_types_alias["identifier"], next_token=True)
        else:
            raise ValueError(f"预期类型或类名，但得到 {self.current_token_value}")
        self.eat(token_types_alias["identifier"], next_token=True)  # varName

        while self.current_token_value == ',':
            self.eat(token_types_alias["symbol"], next_token=True)      # ','
            self.eat(token_types_alias["identifier"], next_token=True)  # varName

        self.eat(token_types_alias["symbol"], next_token=True)  # ';'

    def compile_term(self):
        # 一元运算符
        if self.current_token_value in ('-', '~'):
            self.eat(token_types_alias["symbol"], next_token=True)  # unaryOp
            self.compile_term()
        
        # 括号内表达式
        elif self.current_token_value == '(':
            self.eat(token_types_alias["symbol"], next_token=True)  # '('
            self.compile_expression()
            self.eat(token_types_alias["symbol"], next_token=True)  # ')'

        # 整数常量
        elif self.current_token_type == token_types_alias["integerConstant"]:
            self.eat(token_types_alias["integerConstant"], next_token=True)
        
        # 字符串常量
        elif self.current_token_type == token_types_alias["stringConstant"]:
            self.eat(token_types_alias["stringConstant"], next_token=True)

        # 关键字常量
        elif self.current_token_type == token_types_alias["keyword"] and self.current_token_value in ('true', 'false', 'null', 'this'):
            self.eat(token_types_alias["keyword"], next_token=True)
        
        # 标识符
        elif self.current_token_type == token_types_alias["identifier"]:
            next_token = self.lexer.peek()
            if next_token is None:
                raise ValueError("意外的文件结尾")
            next_token_type, next_token_value = next_token
            # 数组访问
            if next_token_value == '[':
                self.eat(token_types_alias["identifier"], next_token=True)  # varName
                self.eat(token_types_alias["symbol"], next_token=True)      # '['
                self.compile_expression()
                self.eat(token_types_alias["symbol"], next_token=True)      # ']'
            # 子程序调用
            elif next_token_value in ('(', '.'):
                self.eat(token_types_alias["identifier"], next_token=True)  # subroutineName | className | varName
                if self.current_token_value == '.':
                    self.eat(token_types_alias["symbol"], next_token=True)      # '.'
                    self.eat(token_types_alias["identifier"], next_token=True)  # subroutineName
                self.eat(token_types_alias["symbol"], next_token=True)      # '('
                # expressionList
                if self.current_token_value != ')':
                    self.compile_expression()
                    while self.current_token_value == ',':
                        self.eat(token_types_alias["symbol"], next_token=True)  # ','
                        self.compile_expression()
                self.eat(token_types_alias["symbol"], next_token=True)      # ')'
            # 变量
            else:
                self.eat(token_types_alias["identifier"], next_token=True)  # varName

    def compile_expression(self):
        self.compile_term()
        while self.current_token_value in ('+', '-', '*', '/', '&', '|', '<', '>', '='):
            self.eat(token_types_alias["symbol"], next_token=True)  # op
            self.compile_term()

    def compile_let(self):
        self.eat(token_types_alias["keyword"], next_token=True)  # 'let'
        self.eat(token_types_alias["identifier"], next_token=True)  # varName
        if self.current_token_value == '[':
            self.eat(token_types_alias["symbol"], next_token=True)  # '['
            self.compile_expression()
            self.eat(token_types_alias["symbol"], next_token=True)  # ']'
        self.eat(token_types_alias["symbol"], next_token=True)  # '='
        self.compile_expression()
        self.eat(token_types_alias["symbol"], next_token=True)  # ';'
    
    def compile_if(self):
        self.eat(token_types_alias["keyword"], next_token=True)  # 'if'
        self.eat(token_types_alias["symbol"], next_token=True)   # '('
        self.compile_expression()
        self.eat(token_types_alias["symbol"], next_token=True)   # ')'
        self.eat(token_types_alias["symbol"], next_token=True)   # '{'
        self.compile_subroutine_statements()
        self.eat(token_types_alias["symbol"], next_token=True)   # '}'
        if self.current_token_value == 'else':
            self.eat(token_types_alias["keyword"], next_token=True)  # 'else'
            self.eat(token_types_alias["symbol"], next_token=True)   # '{'
            self.compile_subroutine_statements()
            self.eat(token_types_alias["symbol"], next_token=True)   # '}'
    
    def compile_while(self):
        self.eat(token_types_alias["keyword"], next_token=True)  # 'while'
        self.eat(token_types_alias["symbol"], next_token=True)   # '('
        self.compile_expression()
        self.eat(token_types_alias["symbol"], next_token=True)   # ')'
        self.eat(token_types_alias["symbol"], next_token=True)   # '{'
        self.compile_subroutine_statements()
        self.eat(token_types_alias["symbol"], next_token=True)   # '}'
    
    def compile_do(self):
        self.eat(token_types_alias["keyword"], next_token=True)  # 'do'
        # subroutineCall
        self.eat(token_types_alias["identifier"], next_token=True)  # subroutineName | className | varName
        if self.current_token_value == '.':
            self.eat(token_types_alias["symbol"], next_token=True)      # '.'
            self.eat(token_types_alias["identifier"], next_token=True)  # subroutineName
        self.eat(token_types_alias["symbol"], next_token=True)      # '('
        # expressionList
        if self.current_token_value != ')':
            self.compile_expression()
            while self.current_token_value == ',':
                self.eat(token_types_alias["symbol"], next_token=True)  # ','
                self.compile_expression()
        self.eat(token_types_alias["symbol"], next_token=True)      # ')'
        self.eat(token_types_alias["symbol"], next_token=True)      # ';'
    
    def compile_return(self):
        self.eat(token_types_alias["keyword"], next_token=True)  # 'return'
        if self.current_token_value != ';':
            self.compile_expression()
        self.eat(token_types_alias["symbol"], next_token=True)      # ';'

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

    def compile_subroutine_body(self):
        self.eat(token_types_alias["symbol"], next_token=True)      # '{'

        while self.current_token_value == 'var':
            self.compile_subroutine_var_dec()

        self.compile_subroutine_statements()

        self.eat(token_types_alias["symbol"], next_token=True)      # '}'
        

    def compile_subroutine_dec(self):
        self.eat(token_types_alias["keyword"], next_token=True)  # constructor | function | method

        if self.current_token_value in ('void', 'int', 'char', 'boolean'):
            self.eat(token_types_alias["keyword"], next_token=True)
        else:
            self.eat(token_types_alias["identifier"], next_token=True)

        self.eat(token_types_alias["identifier"], next_token=True)  # subroutineName
        self.eat(token_types_alias["symbol"], next_token=True)      # '('
        self.compile_parameter_list()
        self.eat(token_types_alias["symbol"], next_token=True)      # ')'
        self.compile_subroutine_body()

    def compile_class(self):
        self.eat(token_types_alias["keyword"], next_token=True)     # 'class'
        self.eat(token_types_alias["identifier"], next_token=True)  # className
        self.eat(token_types_alias["symbol"], next_token=True)      # '{'

        while self.current_token_value in ('static', 'field'):
            self.compile_class_var_dec()

        while self.current_token_value in ('constructor', 'function', 'method'):
            self.compile_subroutine_dec()

        self.eat(token_types_alias["symbol"])  # '}'（文件结尾，不前进）


if __name__ == "__main__":
    # 简单测试
    jack_path = 'inputs/Square.jack'
    parser = Parser(jack_path)
    print("开始解析类...")
    parser.compile_class()
    print("解析完成")