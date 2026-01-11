# chapter_10/expression.py

def handle_expression(expr, is_top_level=True):
    # 合法性检查
    assert type(expr) == str, "Expression must be a string"
    expr = expr.strip()

    # 如果最外层是 () 那就去掉
    if expr.startswith("(") and expr.endswith(")"):
        # 用状态机检查括号匹配
        depth = 0
        in_string = False
        is_outer_parentheses = True
        for i, c in enumerate(expr):
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
                if depth == 0 and i != len(expr) - 1:
                    is_outer_parentheses = False
                    break
        if is_outer_parentheses:
            if is_top_level:
                return (
                    "<symbol>(</symbol>\n"
                    "<expression>\n"
                    + handle_expression(expr[1:-1].strip(), is_top_level=False)
                    + "</expression>\n"
                    "<symbol>)</symbol>\n"
                )
            else:
                return (
                    "<symbol>(</symbol>\n"
                    + handle_expression(expr[1:-1].strip(), is_top_level=False)
                    + "<symbol>)</symbol>\n"
                )
    
    # 如果最外层是 [] 那就去掉
    if expr.startswith("[") and expr.endswith("]"):
        # 用状态机检查括号匹配
        depth = 0
        in_string = False
        is_outer_brackets = True
        for i, c in enumerate(expr):
            # 更新 in_string 状态
            if c == '"' :
                in_string = not in_string
                continue

            # 字符串内的括号不处理
            if in_string:
                continue

            if c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
                if depth == 0 and i != len(expr) - 1:
                    is_outer_brackets = False
                    break
        if is_outer_brackets:
            if is_top_level:
                return (
                    "<symbol>[</symbol>\n"
                    "<expression>\n"
                    + handle_expression(expr[1:-1].strip(), is_top_level=False)
                    + "</expression>\n"
                    "<symbol>]</symbol>\n"
                )
            else:
                return (
                    "<symbol>[</symbol>\n"
                    + handle_expression(expr[1:-1].strip(), is_top_level=False)
                    + "<symbol>]</symbol>\n"
                )

    # 拆出顶层运算符
    operators = set("+-*/&|<>=")
    parts = []
    last_index = -1
    depth = 0
    in_string = False
    for i, c in enumerate(expr):
        # 更新 in_string 状态
        if c == '"' :
            in_string = not in_string
            continue

        # 字符串内的运算符不处理
        if in_string:
            continue

        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif c in operators and depth == 0:
            parts.append(expr[last_index + 1:i].strip())
            parts.append(c)
            last_index = i
    final_part = expr[last_index + 1 :].strip()
    if final_part:
        parts.append(final_part)

    # 多个部分，递归处理
    if len(parts) > 1:
        res = ""
        for i, part in enumerate(parts):
            if part in operators:
                res += "<symbol>" + part + "</symbol>\n"
            else:
                res += handle_expression(part, is_top_level=False)
        if is_top_level:
            return (
                "<expression>\n"
                + res
                + "</expression>\n"
            )
        else:
            return res
    
    # 单个部分，作为 term 处理
    term = expr
    res = ""

    # 1. 字符串常量
    if term.startswith('"') and term.endswith('"'):
        res = "<stringConstant>" + term[1:-1] + "</stringConstant>\n"

    # 2. 整数常量
    elif term.isdigit():
        res = "<integerConstant>" + term + "</integerConstant>\n"

    # 3. 数组访问
    elif "[" in term and term.endswith("]"):
        var, index = term.split("[", 1)
        index = index[:-1].strip()
        res += "<identifier>" + var.strip() + "</identifier>\n"
        res += "<symbol>[</symbol>\n"
        res += handle_expression(index, is_top_level=True)
        res += "<symbol>]</symbol>\n"

    # 4. 子程序调用
    elif "(" in term and term.endswith(")"):
        call, args = term.split("(", 1)
        args = args[:-1].strip()

        if "." in call:
            obj, func = call.split(".", 1)
            res += "<identifier>" + obj.strip() + "</identifier>\n"
            res += "<symbol>.</symbol>\n"
            res += "<identifier>" + func.strip() + "</identifier>\n"
        else:
            res += "<identifier>" + call.strip() + "</identifier>\n"

        res += "<symbol>(</symbol>\n"
        res += handle_expressionList(args)
        res += "<symbol>)</symbol>\n"

    # 5. 普通标识符
    else:
        res = "<identifier>" + term + "</identifier>\n"

    # 是否包 expression
    if is_top_level:
        return (
            "<expression>\n"
            "<term>\n"
            + res
            + "</term>\n"
            "</expression>\n"
        )
    else:
        return (
            "<term>\n"
            + res
            + "</term>\n"
        )

def handle_expressionList(exprList):
    # 合法性检查
    assert type(exprList) == str, "Expression list must be a string"

    res = ""

    # 分割 expression list
    exprs = []
    last_index = -1
    depth = 0
    in_string = False
    for i, c in enumerate(exprList):
        # 更新 in_string 状态
        if c == '"' :
            in_string = not in_string
            continue

        # 字符串内的逗号不处理
        if in_string:
            continue

        if c == "," and depth == 0:
            exprs.append(exprList[last_index + 1:i].strip())
            last_index = i
        elif c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
    final_expr = exprList[last_index + 1 :].strip()
    if final_expr:
        exprs.append(final_expr)
    
    for i, expr in enumerate(exprs):
        res += handle_expression(expr)
        if i < len(exprs) - 1:
            res += "<symbol>,</symbol>\n"


    return (
        "<expressionList>\n"
        + res
        + "</expressionList>\n"
    )

if __name__ == "__main__":
    # 测试代码
    test_expressions = [
        'x + y * (z - 2)',
        '"hello" + " " + "world"',
        'array[5 + i]',
        'Math.sqrt(4)',
        '(a + b) * (c - d) / e',
        'Output.printString("The result is: " + result)',
        'obj.method(a, b + c, foo())',
        'arr[i + 1] * (x - y)',
    ]

    for expr in test_expressions:
        print("Expression:", expr)
        print(handle_expression(expr))
        print("-----")