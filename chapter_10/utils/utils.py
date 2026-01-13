# chapter_10/utils/utils.py

import re

def remove_comments_and_whitespace(lines):
    cleaned_lines = []
    in_block_comment = False

    for line in lines:
        i = 0
        result = ""
        in_string = False  # 字符串状态
        
        while i < len(line):
            # 1. 处理字符串状态开关 (只有在非注释状态下才生效)
            if not in_block_comment and line[i] == '"':
                in_string = not in_string
                result += line[i]
                i += 1
                continue

            # 2. 如果在字符串里，什么都不管，直接加字符
            if in_string:
                result += line[i]
                i += 1
                continue

            # 3. 处理块注释（只有在非字符串状态下才生效）
            if not in_block_comment and line[i:i+2] == "/*":
                in_block_comment = True
                i += 2
            elif in_block_comment and line[i:i+2] == "*/":
                in_block_comment = False
                i += 2
            # 4. 处理行注释
            elif not in_block_comment and line[i:i+2] == "//":
                break
            # 5. 正常的代码内容
            else:
                if not in_block_comment:
                    result += line[i]
                i += 1

        result = result.strip()
        if result:
            cleaned_lines.append(result)

    return cleaned_lines

# 定义 Jack 语言中所有可能的 Token 形状
TOKEN_REGEX = re.compile(
    r'(?P<keyword>while|if|else|let|do|method|function|constructor|int|boolean|char|void|var|static|field|class|return|true|false|null|this)'
    r'|(?P<symbol>[{}()\[\].,;+\-*/&|<>=~])'
    r'|(?P<integerConstant>\d+)'
    r'|(?P<stringConstant>"[^"\n]*")'
    r'|(?P<identifier>[a-zA-Z_][a-zA-Z0-9_]*)'
)

def tokenize(lines):
    all_code = " ".join(lines)
    tokens = []
    
    # 使用 finditer 像扫描仪一样从头扫到尾
    for match in TOKEN_REGEX.finditer(all_code):
        for name, value in match.groupdict().items():
            if value is not None:
                # 字符串常量需要特殊处理：去掉引号
                if name == "stringConstant":
                    tokens.append((name, value[1:-1]))
                else:
                    tokens.append((name, value))
                break
    return tokens

def skip_whitespace(s: str, i: int) -> int:
    while i < len(s) and s[i].isspace():
        i += 1
    return i

# 判断表达式是否可以被进一步分解
def can_decompose(expr: str) -> bool:
    assert isinstance(expr, str)
    expr = expr.strip()

    if not expr:
        return False

    # 1️⃣ 能否剥离最外层 () 或 []
    def has_outer_pair(left, right):
        if not (expr.startswith(left) and expr.endswith(right)):
            return False
        depth = 0
        in_string = False
        for i, c in enumerate(expr):
            if c == '"':
                in_string = not in_string
                continue
            if in_string:
                continue
            if c == left:
                depth += 1
            elif c == right:
                depth -= 1
                if depth == 0 and i != len(expr) - 1:
                    return False
        return depth == 0

    if has_outer_pair("(", ")") or has_outer_pair("[", "]"):
        return True

    # 2️⃣ 顶层运算符
    operators = set("+-*/&|<>=")
    depth = 0
    in_string = False
    for c in expr:
        if c == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif c in operators and depth == 0:
            return True

    # 3️⃣ 数组访问 / 子程序调用
    if "[" in expr and expr.endswith("]"):
        return True
    if "(" in expr and expr.endswith(")"):
        return True

    return False
