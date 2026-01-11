# chapter_10/Class.py

from chapter_10.var import handle_var, handle_classVar
from chapter_10.statement import handle_statements

def handle_subroutineParamList(paramListStr):
    assert isinstance(paramListStr, str), "Input must be a string."
    paramListStr = paramListStr.strip()
    # 处理空参数列表的情况
    if paramListStr == "":
        return "<parameterList>\n</parameterList>\n"
    
    res = ""
    params = [param.strip() for param in paramListStr.split(",")]
    for index, param in enumerate(params):
        type_end = param.find(" ")
        paramType = param[:type_end].strip()
        paramName = param[type_end + 1 :].strip()
        res += "<keyword>" + paramType + "</keyword>\n"
        res += "<identifier>" + paramName + "</identifier>\n"
        if index != len(params) - 1:
            res += "<symbol>,</symbol>\n"
    return (
        "<parameterList>\n"
        + res
        + "</parameterList>\n"
    )

def handle_subroutineBody(subroutineBodyStr):
    assert isinstance(subroutineBodyStr, str), "Input must be a string."
    subroutineBodyStr = subroutineBodyStr.strip()
    assert subroutineBodyStr.startswith("{"), "Subroutine body must start with '{'."
    assert subroutineBodyStr.endswith("}"), "Subroutine body must end with '}'."

    res = ""

    restBodyStr = subroutineBodyStr[1:-1].strip()
    # 处理 varDec
    while restBodyStr.startswith("var "):
        varDecEnd = restBodyStr.find(";") + 1
        varDecStr = restBodyStr[:varDecEnd].strip()
        restBodyStr = restBodyStr[varDecEnd:].strip()
        res += handle_var(varDecStr)
    # 处理 statements
    res += handle_statements(restBodyStr)

    return res

def handle_subroutine(subroutineStr):
    assert isinstance(subroutineStr, str), "Input must be a string."
    subroutineStr = subroutineStr.strip()
    assert subroutineStr.startswith(("constructor ", "function ", "method ")), "Subroutine definition must start with 'constructor', 'function', or 'method'."
    assert subroutineStr.endswith("}"), "Subroutine definition must end with '}'."

    res = ""

    # 提取 subroutine 类型
    subroutineTypeEnd = subroutineStr.find(" ")
    subroutineType = subroutineStr[:subroutineTypeEnd]
    restStr = subroutineStr[subroutineTypeEnd + 1:].strip()
    res += "<keyword>" + subroutineType + "</keyword>\n"

    # 提取返回类型
    returnTypeEnd = restStr.find(" ")
    returnType = restStr[:returnTypeEnd]
    restStr = restStr[returnTypeEnd + 1:].strip()
    res += "<keyword>" + returnType + "</keyword>\n"

    # 提取 subroutine 名称
    subroutineNameEnd = restStr.find("(")
    subroutineName = restStr[:subroutineNameEnd]
    restStr = restStr[subroutineNameEnd + 1:].strip()
    res += "<identifier>" + subroutineName + "</identifier>\n"

    # 提取 params 列表 有限状态机
    deepth = 1
    is_string = False
    ind = -1
    for i, ch in enumerate(restStr):
        if ch == '"':
            is_string = not is_string
        if is_string:
            continue
        if ch == '(':
            deepth += 1
        elif ch == ')':
            deepth -= 1
            if deepth == 0:
                ind = i
                break
    paramListStr = restStr[:ind].strip()
    restStr = restStr[ind + 1:].strip()
    res += "<symbol>(</symbol>\n"
    res += handle_subroutineParamList(paramListStr)
    res += "<symbol>)</symbol>\n"

    # 提取 subroutine body 有限状态机
    deepth = 0
    is_string = False
    ind = -1
    for i, ch in enumerate(restStr):
        if ch == '"':
            is_string = not is_string
        if is_string:
            continue
        if ch == '{':
            deepth += 1
        elif ch == '}':
            deepth -= 1
            if deepth == 0:
                ind = i
                break
    subroutineBodyStr = restStr[:ind + 1].strip()
    res += "<subroutineBody>\n"
    res += "<symbol>{</symbol>\n"
    res += handle_subroutineBody(subroutineBodyStr)
    res += "<symbol>}</symbol>\n"
    res += "</subroutineBody>\n"

    return (
        "<subroutineDec>\n"
        + res
        + "</subroutineDec>\n"
    )

def handle_classBody(classBodyStr):
    assert isinstance(classBodyStr, str), "Input must be a string."
    classBodyStr = classBodyStr.strip()
    assert classBodyStr.startswith("{"), "Class body must start with '{'."
    assert classBodyStr.endswith("}"), "Class body must end with '}'."

    res = ""

    restBodyStr = classBodyStr[1:-1].strip()
    # 处理 classVarDec
    while restBodyStr.startswith(("static ", "field ")):
        classVarDecEnd = restBodyStr.find(";") + 1
        classVarDecStr = restBodyStr[:classVarDecEnd].strip()
        restBodyStr = restBodyStr[classVarDecEnd:].strip()
        res += handle_classVar(classVarDecStr)

    # 处理 subroutineDec
    while restBodyStr.startswith(("constructor ", "function ", "method ")):
        # 提取 subroutineDec 有限状态机
        deepth = 0
        is_string = False
        ind = -1
        for i, ch in enumerate(restBodyStr):
            if ch == '"':
                is_string = not is_string
            if is_string:
                continue
            if ch == '{':
                deepth += 1
            elif ch == '}':
                deepth -= 1
                if deepth == 0:
                    ind = i
                    break
        subroutineDecStr = restBodyStr[:ind + 1].strip()
        restBodyStr = restBodyStr[ind + 1:].strip()
        res += handle_subroutine(subroutineDecStr)
    
    return (
        "<symbol>{</symbol>\n"
        + res
        + "<symbol>}</symbol>\n"
    )

def handle_class(classStr):
    assert isinstance(classStr, str), "Input must be a string."
    classStr = classStr.strip()
    assert classStr.startswith("class "), "Class definition must start with 'class'."
    assert classStr.endswith("}"), "Class definition must end with '}'."

    res = ""

    restStr = classStr
    # 提取 class 关键字
    classKeywordEnd = restStr.find(" ")
    classKeyword = restStr[:classKeywordEnd]
    restStr = restStr[classKeywordEnd + 1:].strip()
    res += "<keyword>" + classKeyword + "</keyword>\n"

    # class 名称
    classNameEnd = restStr.find("{")
    className = restStr[:classNameEnd].strip()
    restStr = restStr[classNameEnd:].strip()
    res += "<identifier>" + className + "</identifier>\n"

    # classBody 有限状态机
    depth = 0
    is_string = False
    ind = -1
    for i, ch in enumerate(restStr):
        if ch == '"':
            is_string = not is_string
        if is_string:
            continue
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                ind = i
                break
    classBodyStr = restStr[:ind + 1].strip()
    restStr = restStr[ind + 1:].strip()
    assert restStr == "", "Extra content after class body."
    res += handle_classBody(classBodyStr)

    return (
        "<class>\n"
        + res
        + "</class>\n"
    )


if __name__ == "__main__":
    cls = """
    class Main {
        static boolean test;

        function void main() {
            var SquareGame game;
            let game = game;
            do game.run();
            do game.dispose();
            return;
        }

        function void more() {
            var boolean b;
            if (b) {
            }
            else {
            }
            return;
        }
    }
    """
    print(cls)
    print("\n\n")
    print(handle_class(cls))