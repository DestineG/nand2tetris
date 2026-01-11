# chapter_10/templates.py

def validate_brackets(s):
    """
    验证括号结构是否合法
    """
    stack = []

    pair = {
        "(": ")",
        "[": "]",
    }

    for tok, ind in s:
        if tok in pair:  # 左括号
            stack.append((tok, ind))

        elif tok in pair.values():  # 右括号
            if not stack:
                raise SyntaxError(
                    f"Unmatched closing '{tok}' at position {ind}"
                )

            left_tok, left_ind = stack.pop()
            if pair[left_tok] != tok:
                raise SyntaxError(
                    f"Mismatched brackets '{left_tok}' at {left_ind} "
                    f"and '{tok}' at {ind}"
                )

    if stack:
        left_tok, left_ind = stack[-1]
        raise SyntaxError(
            f"Unmatched opening '{left_tok}' at position {left_ind}"
        )

def getRootBrackets(s):
    """
    获取顶层括号对索引
    """
    validate_brackets(s)
    stack = []
    res = []

    for tok, ind in s:
        if tok in "([":
            # 如果当前在最外层，记录这个 opening
            if not stack:
                open_ind = ind
            stack.append(tok)

        elif tok in ")]":
            stack.pop()
            # 如果刚好回到最外层，说明这是第一层闭合
            if not stack:
                res.append((open_ind, ind))

    return res

def parse_brackets(expression, templates):
    """
    解析表达式中的括号，并替换为模板标签
    """
    # 收集括号
    s = []
    for ind, tok in enumerate(expression):
        if tok in "()[]":
            s.append((tok, ind))

    # 获取顶层括号对
    match = getRootBrackets(s)

    # 递归出口：没有括号，直接返回原字符串
    if not match:
        return expression

    res = ""
    for i, (open_ind, close_ind) in enumerate(match):
        if i == 0:
            res += expression[:open_ind]
        else:
            prev_close = match[i - 1][1]
            res += expression[prev_close + 1:open_ind]

        # 左括号
        res += templates[expression[open_ind]]

        # 递归解析括号内部
        res += parse_brackets(expression[open_ind + 1:close_ind], templates)

        # 右括号
        res += templates[expression[close_ind]]

    # 补上最后一段
    res += expression[match[-1][1] + 1:]
    return res

default_templates = {
    "(": "<smallLeft>",
    ")": "<smallRight>",
    "[": "<bigLeft>",
    "]": "<bigRight>",
}
def replace_brackets(expression, templates=default_templates):
    """
    解析表达式中的括号，并替换为模板标签
    """
    return parse_brackets(expression, templates)


if __name__ == "__main__":
    exp = "3 + 5 * (a[i + 1 * (b * 4)] - 8) + c + d[2] * e[1 + i * (f * 3)]"
    result = replace_brackets(exp)
    print(exp)
    print(result)
    print(exp.replace(" ", ""))
    print(result.replace("<smallLeft>", "(").replace("<smallRight>", ")").replace("<bigLeft>", "[").replace("<bigRight>", "]").replace(" ", ""))
