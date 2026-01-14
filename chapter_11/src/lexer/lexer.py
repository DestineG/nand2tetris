# src/lexer/lexer.py

from ..utils.fileio import read_jack_file

def remove_comments(lines):
    """
    移除 Jack 代码中的注释（单行注释和多行注释）

    参数:
        lines (list of str): Jack 代码行列表

    返回:
        list of str: 移除注释后的 Jack 代码行列表
    
    注:
        不支持嵌套块注释移除
    """
    in_block_comment = False
    pure_lines = []

    for ind, line in enumerate(lines):
        in_string = False
        new_line = ''

        i = 0
        while i < len(line):
            ch = line[i]

            if in_block_comment:
                if ch == '*' and i + 1 < len(line) and line[i + 1] == '/':
                    in_block_comment = False
                    i += 2
                else:
                    i += 1
                continue

            if in_string:
                new_line += ch
                if ch == '"':
                    in_string = False
                i += 1
                continue

            if ch == '/' and i + 1 < len(line):
                next_ch = line[i + 1]
                if next_ch == '/':
                    break
                elif next_ch == '*':
                    in_block_comment = True
                    i += 2
                    continue

            if ch == '"':
                in_string = True
                new_line += ch
                i += 1
                continue

            new_line += ch
            i += 1

        if new_line.strip():
            pure_lines.append(new_line.strip())

    return pure_lines


# 词法单元类型别名
token_types_alias = {
    "keyword": "keyword",
    "symbol": "symbol",
    "identifier": "identifier",
    "integerConstant": "integerConstant",
    "stringConstant": "stringConstant"
}
# Jack 语言的符号和关键字
symbols = "{}()[].,;+-*/&|<>=~"
keywords = set(
    [
        "class", "constructor", "function", "method", "field",
        "static", "var", "int", "char", "boolean",
        "void", "true", "false", "null", "this",
        "let", "do", "if", "else", "while",
        "return"
    ]
)

def emit_identifier_or_keyword_or_integer(token):
    """
    根据 token 内容判断其类型并返回对应的词法单元

    参数:
        token (str): 待判断的 token 字符串

    返回:
        tuple: 词法单元，格式为 (类型, 值)
    """
    if token in keywords:
        return (token_types_alias["keyword"], token)
    elif token.isdigit():
        return (token_types_alias["integerConstant"], token)
    else:
        return (token_types_alias["identifier"], token)

def tokenizer(code_lines):
    """
    将 Jack 代码行拆分为词法单元列表

    参数:
        code_lines (list of str): Jack 代码行列表

    返回:
        list of tuples: 词法单元列表，每个词法单元为 (类型, 值)
    """
    tokens = []
    for line in code_lines:
        in_string = False
        index_start_ch = 0
        for ind, ch in enumerate(line):
            # 字符串处理
            if ch == '"':
                if not in_string:
                    token = line[index_start_ch:ind].strip()
                    if token:
                        tokens.append(emit_identifier_or_keyword_or_integer(token))
                    index_start_ch = ind + 1
                else:
                    token = line[index_start_ch:ind].strip()
                    if token:
                        tokens.append((token_types_alias["stringConstant"], token))
                    index_start_ch = ind + 1
                in_string = not in_string
                continue

            # 如果在字符串中，跳过后续处理
            if in_string:
                continue

            # symbol 处理
            if line[ind] in symbols:
                token = line[index_start_ch:ind].strip()
                if token:
                    tokens.append(emit_identifier_or_keyword_or_integer(token))
                tokens.append((token_types_alias["symbol"], line[ind]))
                index_start_ch = ind + 1
            
            # 空白处理
            elif ch.isspace():
                token = line[index_start_ch:ind].strip()
                if token:
                    tokens.append(emit_identifier_or_keyword_or_integer(token))
                index_start_ch = ind + 1

        if index_start_ch < len(line):
            token = line[index_start_ch:].strip()
            if token:
                tokens.append(emit_identifier_or_keyword_or_integer(token))
    return tokens


class Lexer:
    """
    Jack 语言词法分析器

    参数:
        jack_file_path (str): Jack 源文件路径

    属性:
        tokens (list of tuples): 词法单元列表
        current_index (int): 当前词法单元索引
    """
    def __init__(self, jack_file_path=None):
        lines = read_jack_file(jack_file_path)
        code_lines = remove_comments(lines)
        self.tokens = tokenizer(code_lines)
        self.current_index = -1
        self.class_name = None
    
    def set_class_name(self, class_name):
        self.class_name = class_name
    
    def get_class_name(self):
        return self.class_name

    def has_more_tokens(self) -> bool:
        return self.current_index + 1 < len(self.tokens)

    def advance(self) -> None:
            self.current_index += 1
    
    def token(self) -> tuple:
        return self.tokens[self.current_index]
    
    def peek(self) -> tuple:
        if self.current_index + 1 < len(self.tokens):
            return self.tokens[self.current_index + 1]
        return None

    def token_value(self) -> str:
        _, token_value = self.tokens[self.current_index]
        return token_value
    
    def token_type(self) -> str:
        token_type, _ = self.tokens[self.current_index]
        return token_type
    
    def keyword(self):
        token_type, token_value = self.tokens[self.current_index]
        if token_type == token_types_alias["keyword"]:
            return token_value
        raise ValueError("当前 token 不是关键字")

    def symbol(self):
        token_type, token_value = self.tokens[self.current_index]
        if token_type == token_types_alias["symbol"]:
            return token_value
        raise ValueError("当前 token 不是符号")
    
    def identifier(self):
        token_type, token_value = self.tokens[self.current_index]
        if token_type == token_types_alias["identifier"]:
            return token_value
        raise ValueError("当前 token 不是标识符")
    
    def int_val(self):
        token_type, token_value = self.tokens[self.current_index]
        if token_type == token_types_alias["integerConstant"]:
            return int(token_value)
        raise ValueError("当前 token 不是整数常量")
    
    def string_val(self):
        token_type, token_value = self.tokens[self.current_index]
        if token_type == token_types_alias["stringConstant"]:
            return token_value
        raise ValueError("当前 token 不是字符串常量")


if __name__ == "__main__":
    # 简单测试
    jack_path = 'inputs/Square.jack'
    lexer = Lexer(jack_path)
    while lexer.has_more_tokens():
        lexer.advance()
        token = lexer.tokens[lexer.current_index]
        print(token)