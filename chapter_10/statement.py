# chapter_10/statement.py

from chapter_10.utils.utils import skip_whitespace
from chapter_10.expression import handle_expression, handle_expressionList

STATEMENT_HANDLER = {}

def register_handler(keyword):
    def decorator(func):
        STATEMENT_HANDLER[keyword] = func
        return func
    return decorator

def handle_statements(statements: str):
    assert isinstance(statements, str)

    i = 0
    n = len(statements)
    res = ""

    while i < n:
        i = skip_whitespace(statements, i)
        if i >= n:
            break

        # 识别关键字
        for keyword in STATEMENT_HANDLER:
            if statements.startswith(keyword, i):
                handler = STATEMENT_HANDLER[keyword]
                break
        else:
            raise AssertionError(f"Unknown statement at: {statements[i:i+20]}")

        # --------- 简单语句（; 结尾）---------
        if keyword in ("let", "do", "return"):
            end = statements.find(";", i)
            assert end != -1, "Missing ';'"
            stmt = statements[i:end + 1]
            res += handler(stmt)
            i = end + 1

        # --------- while / if（{} 结尾）---------
        else:
            start = i
            depth = 0
            in_string = False
            stmt_end = -1

            while i < n:
                c = statements[i]
                if c == '"':
                    in_string = not in_string
                if not in_string:
                    if c == "{":
                        depth += 1
                    elif c == "}":
                        depth -= 1

                        # 如果是 if/while 的初始块，深度为 0 时可能还没结束整个 if-else 链
                        if depth == 0 and keyword == "if":
                            # 暂存当前位置，继续扫描看看是否有 elif/else
                            j = skip_whitespace(statements, i + 1)
                            if statements.startswith("elif", j) or statements.startswith("else", j):
                                i = j
                                continue
                            else:
                                stmt_end = i + 1
                                break
                        elif depth == 0:
                            stmt_end = i + 1
                            break
                i += 1

            if stmt_end == -1:
                raise AssertionError("Unclosed block statement")

            stmt = statements[start:stmt_end]
            res += handler(stmt)
            i = stmt_end

    return (
        "<statements>\n"
        + res
        + "</statements>\n"
    )

@register_handler("let")
def handle_let_statement(statement):
    # 合法性检查
    assert type(statement) == str, "Statement must be a string"
    statement = statement.strip()
    assert statement.startswith("let "), "Not a let statement"
    assert statement.endswith(";"), "Let statement must end with a semicolon"

    res = ""
    res += "<keyword>let</keyword>\n"

    # 拆解 let 语句
    var, expr = statement.replace("let ", "").rstrip(";").split("=", 1)
    var, expr = var.strip(), expr.strip()

    # 处理 var
    if all(symbol in var for symbol in ["[", "]"]):
        # 提取 变量名 和 索引表达式
        var_name, index = var.split("[", 1)
        # 去除索引表达式末尾的 "]"
        assert index.endswith("]"), "Index expression must end with ']'"
        index = index[:-1].strip()

        # 组合结果
        res += f"<identifier>{var_name.strip()}</identifier>\n"
        res += "<symbol>[</symbol>\n"
        res += handle_expression(index)
        res += "<symbol>]</symbol>\n"
    else:
        res += f"<identifier>{var}</identifier>\n"

    res += "<symbol>=</symbol>\n"

    # 处理 expr
    res += handle_expression(expr)

    # 结束符号
    res += "<symbol>;</symbol>\n"
    return (
        "<letStatement>\n"
        + res
        + "</letStatement>\n"
    )

# statement = "let message = \"Score=100\";"
# print(handle_let_statement(statement))

@register_handler("return")
def handle_return_statement(statement):
    # 合法性检查
    assert type(statement) == str, "Statement must be a string"
    statement = statement.strip()
    assert statement.startswith("return"), "Not a return statement"
    assert statement.endswith(";"), "Return statement must end with a semicolon"

    res = ""
    res += "<keyword>return</keyword>\n"

    # 处理返回值表达式
    expr = statement.replace("return", "").rstrip(";").strip()
    if expr:
        res += handle_expression(expr)

    # 结束符号
    res += "<symbol>;</symbol>\n"

    return (
        "<returnStatement>\n"
        + res
        + "</returnStatement>\n"
    )

# statement = "return x + 1;"
# print(handle_return_statement(statement))

@register_handler("do")
def handle_do_statement(statement):
    # 合法性检查
    assert type(statement) == str, "Statement must be a string"
    statement = statement.strip()
    assert statement.startswith("do "), "Not a do statement"
    assert statement.endswith(";"), "Do statement must end with a semicolon"

    res = ""
    res += "<keyword>do</keyword>\n"

    # 提取子程序调用 处理子程序调用
    subroutine_call = statement.replace("do ", "").rstrip(";").strip()
    callPart, argsPart = subroutine_call.split("(", 1)
    
    # 处理 callPart
    assert callPart.count(".") <= 1, "Invalid subroutine call format"
    if "." in callPart:
        caller, subroutine_name = callPart.split(".", 1)
        res += f"<identifier>{caller.strip()}</identifier>\n"
        res += "<symbol>.</symbol>\n"
        res += f"<identifier>{subroutine_name.strip()}</identifier>\n"
    else:
        res += f"<identifier>{callPart.strip()}</identifier>\n"

    # 处理 argsPart    
    assert argsPart.endswith(")"), "Arguments must end with ')'"
    argsPart = argsPart[:-1].strip()
    res += "<symbol>(</symbol>\n"
    res += handle_expressionList(argsPart)
    res += "<symbol>)</symbol>\n"

    # 结束符号
    res += "<symbol>;</symbol>\n"

    return (
        "<doStatement>\n"
        + res
        + "</doStatement>\n"
    )

# statement = "do Output.printInt(x, func(a, \"hello\", b + c), \"world\");"
# print(handle_do_statement(statement))

@register_handler("while")
def handle_while_statement(statement: str):
    assert isinstance(statement, str), "statement must be a string"
    statement = statement.strip()
    assert statement.startswith("while "), "Not a while statement"
    assert statement.endswith("}"), "While statement must end with '}'"

    # 寻找第一个 (
    open_paren_index = statement.find("(")
    assert open_paren_index != -1, "While statement must contain '('"

    # 用状态机寻找匹配的 )
    depth = 0
    in_string = False
    close_paren_index = -1
    for i in range(open_paren_index, len(statement)):
        c = statement[i]
        # 更新 in_string 状态
        if c == '"' :
            in_string = not in_string
            continue

        # 字符串内的括号不处理
        if in_string:
            continue

        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                close_paren_index = i
                break
    assert close_paren_index != -1, "No matching ')' found for while condition"

    # 从 close_paren_index 寻找第一个 {
    open_brace_index = statement.find("{", close_paren_index)
    assert open_brace_index != -1, "While statement must contain '{'"

    # 用状态机寻找匹配的 }
    depth = 0
    in_string = False
    close_brace_index = -1
    for i in range(open_brace_index, len(statement)):
        c = statement[i]
        # 更新 in_string 状态
        if c == '"' :
            in_string = not in_string
            continue

        # 字符串内的括号不处理
        if in_string:
            continue

        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                close_brace_index = i
                break
    assert close_brace_index != -1, "No matching '}' found for while body"

    condition = statement[open_paren_index + 1 : close_paren_index].strip()
    body = statement[open_brace_index + 1 : close_brace_index].strip()
    return (
        "<whileStatement>\n"
        "<keyword>while</keyword>\n"
        "<symbol>(</symbol>\n"
        + handle_expression(condition) +
        "<symbol>)</symbol>\n"
        "<symbol>{</symbol>\n"
        + handle_statements(body) +
        "<symbol>}</symbol>\n"
        "</whileStatement>\n"
    )

# statement = "while ( (x < (y + 1)) ) { do call(); }"
# result = handle_while_statement(statement)
# print(statement)
# print(result)

@register_handler("if")
def handle_if_statement(statement: str):
    assert isinstance(statement, str), "statement must be a string"
    statement = statement.strip()
    assert statement.startswith("if"), "Not an if statement"
    assert statement.endswith("}"), "If statement must end with '}'"

    res = ""
    exist_block = True
    start = 0

    while exist_block:
        is_if = statement.startswith("if", start)
        is_elif = statement.startswith("elif", start)
        is_else = statement.startswith("else", start)

        assert is_if or is_elif or is_else, "Invalid if/elif/else structure"

        # ---------- 情况 1：if / elif，需要解析 () ----------
        if is_if or is_elif:
            # 找到第一个 (
            open_paren_index = statement.find("(", start)
            assert open_paren_index != -1, "If/elif statement must contain '('"

            # 用状态机寻找匹配的 )
            depth = 0
            in_string = False
            close_paren_index = -1
            for i in range(open_paren_index, len(statement)):
                c = statement[i]
                if c == '"':
                    in_string = not in_string
                    continue
                if in_string:
                    continue
                if c == "(":
                    depth += 1
                elif c == ")":
                    depth -= 1
                    if depth == 0:
                        close_paren_index = i
                        break
            assert close_paren_index != -1, "No matching ')' found"

            # 从 close_paren_index 寻找第一个 {
            open_brace_index = statement.find("{", close_paren_index)
            assert open_brace_index != -1, "If/elif statement must contain '{'"

            condition = statement[
                open_paren_index + 1 : close_paren_index
            ].strip()

        # ---------- 情况 2：else，只解析 {} ----------
        else:
            condition = None
            open_brace_index = statement.find("{", start)
            assert open_brace_index != -1, "Else statement must contain '{'"

        # ---------- 公共部分：解析 {} ----------
        depth = 0
        in_string = False
        close_brace_index = -1
        for i in range(open_brace_index, len(statement)):
            c = statement[i]
            if c == '"':
                in_string = not in_string
                continue
            if in_string:
                continue
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    close_brace_index = i
                    break
        assert close_brace_index != -1, "No matching '}' found"

        body = statement[
            open_brace_index + 1 : close_brace_index
        ].strip()

        # ---------- 生成 XML ----------
        if is_if:
            res += (
                "<keyword>if</keyword>\n"
                "<symbol>(</symbol>\n"
                + handle_expression(condition) +
                "<symbol>)</symbol>\n"
                "<symbol>{</symbol>\n"
                + handle_statements(body) +
                "<symbol>}</symbol>\n"
            )
        elif is_elif:
            res += (
                "<keyword>else</keyword>\n"
                "<keyword>if</keyword>\n"
                "<symbol>(</symbol>\n"
                + handle_expression(condition) +
                "<symbol>)</symbol>\n"
                "<symbol>{</symbol>\n"
                + handle_statements(body) +
                "<symbol>}</symbol>\n"
            )
        else:  # else
            res += (
                "<keyword>else</keyword>\n"
                "<symbol>{</symbol>\n"
                + handle_statements(body) +
                "<symbol>}</symbol>\n"
            )

        start = close_brace_index + 1
        start = skip_whitespace(statement, start)
        exist_block = (
            statement.startswith("else", start) or
            statement.startswith("elif", start)
        )

    return (
        "<ifStatement>\n"
        + res
        + "</ifStatement>\n"
    )

# statement = "if (x > 0) { let x = x - 1; } else { do Output.printInt(x); }"
# result = handle_if_statement(statement)
# print(statement)
# print(result)

if __name__ == "__main__":
    statements = """
    let x = 5;
    do Output.printInt(x);
    if (x > 0) { let x = x - 1; }
    while (x > 0) {
        let x[9 + a] = x - 1;
    }
    let y = "hello world" + z;
    return;
    """
    print(handle_statements(statements))