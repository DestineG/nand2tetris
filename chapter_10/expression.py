# chapter_10/expression.py

def is_wrapped_by_parentheses(expr: str) -> bool:
    expr = expr.strip()
    if not expr or expr[0] != '(' or expr[-1] != ')':
        return False

    count = 0
    for i, ch in enumerate(expr):
        if ch == '(':
            count += 1
        elif ch == ')':
            count -= 1

        # 最外层括号提前闭合 → 不是整体包裹
        if count == 0 and i < len(expr) - 1:
            return False

    return count == 0

# 判断 expr[i] 处的 '-' 或 '~' 是否为 unary op
# 即判断其前面是否为表达式结束符号
def is_unary_op(expr, i):
    # expr[i] 是 '-' 或 '~'
    if i == 0:
        return True

    j = i - 1
    while j >= 0 and expr[j].isspace():
        j -= 1

    if j < 0:
        return True

    return expr[j] in "(,[+-*/&|<>="

def handle_expression(expr):
    # 合法性检查
    assert type(expr) == str, "Expression must be a string"
    expr = expr.strip()
    
    operators = set("+-*/&|<>=")
    xml_escape_table = {
        "&": "&amp;",
        ">": "&gt;",
        "<": "&lt;",
    }
    # 拆分 part
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

        if c in "([":
            depth += 1
        elif c in ")]":
            depth -= 1
        elif c in operators and depth == 0:
            # unary op 不参与 expression 拆分
            if c in "-~" and is_unary_op(expr, i):
                continue

            parts.append(expr[last_index + 1:i].strip())
            parts.append(c)
            last_index = i
    final_part = expr[last_index + 1 :].strip()
    if final_part:
        parts.append(final_part)
    
    # 遍历 parts, 递归处理
    res = ""
    for i, part in enumerate(parts):
        part = part.strip()
        if part in operators:
            res += "<symbol>" + xml_escape_table.get(part, part) + "</symbol>\n"
        else:
            # 0. 两端为一对()的递归处理
            if is_wrapped_by_parentheses(part):
                res += "<term>\n"
                res += "<symbol>(</symbol>\n"
                res += handle_expression(part[1:-1].strip())
                res += "<symbol>)</symbol>\n"
                res += "</term>\n"
            # 1. 字符串常量
            elif part.startswith('"') and part.endswith('"'):
                res += "<term>\n"
                res += "<stringConstant>" + part[1:-1] + "</stringConstant>\n"
                res += "</term>\n"
            # 2. 整数常量
            elif part.isdigit():
                res += "<term>\n"
                res += "<integerConstant>" + part + "</integerConstant>\n"
                res += "</term>\n"
            # 3. 数组访问
            elif "[" in part and part.endswith("]"):
                var, index = part.split("[", 1)
                index = index[:-1].strip()
                res += "<term>\n"
                res += "<identifier>" + var.strip() + "</identifier>\n"
                res += "<symbol>[</symbol>\n"
                res += handle_expression(index)
                res += "<symbol>]</symbol>\n"
                res += "</term>\n"
            # 4. 子程序调用
            elif "(" in part and part.endswith(")"):
                call, args = part.split("(", 1)
                args = args[:-1].strip()
                res += "<term>\n"
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
                res += "</term>\n"
            # 5. 普通标识符
            else:
                if part.startswith(("-", "~")):
                    res += "<term>\n"
                    res += "<symbol>" + part[0] + "</symbol>\n"
                    res += handle_expression(part[1:].strip())
                    res += "</term>\n"
                else:
                    res += "<term>\n"
                    res += "<identifier>" + part + "</identifier>\n"
                    res += "</term>\n"
    
    return (
        "<expression>\n"
        + res
        + "</expression>\n"
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
    
    # 处理每个 expression
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
    # # 测试代码
    # test_expressions = [
    #     '((y + size) < 254) & ((x + size) < 510)',
    #     # 'x + y * (z - 2)',
    #     # '"hello" + " " + "world"',
    #     # 'array[5 + i]',
    #     # 'Math.sqrt(4)',
    #     # '(a + b) * (c - d) / e',
    #     # 'Output.printString("The result is: " + result)',
    #     # 'obj.method(a, b + c, foo())',
    #     # 'arr[i + 1] * (x - y)',
    # ]

    # for expr in test_expressions:
    #     print("Expression:", expr)
    #     print(handle_expression(expr))
    #     print("-----")
    expr = '-x'
    print("Expression:", expr)
    print(handle_expression(expr))