# chapter_10/var.py

def handle_var(codeline):
    # 合法性检查
    assert isinstance(codeline, str), "codeline must be a string"
    codeline = codeline.strip()
    assert codeline.startswith("var "), "codeline must start with 'var '"
    assert codeline.endswith(";"), "codeline must end with ';'"

    res = ""
    res += "<keyword>var</keyword>\n"

    # 去掉 var 和 ;
    body = codeline[4:-1].strip()

    # type + vars
    parts = body.split()
    assert len(parts) >= 2, "Invalid var declaration"

    var_type = parts[0]
    var_names = body[len(var_type):].strip()

    # type
    if var_type in ("int", "char", "boolean"):
        res += f"<keyword>{var_type}</keyword>\n"
    else:
        res += f"<identifier>{var_type}</identifier>\n"

    # varName (, varName)*
    names = [v.strip() for v in var_names.split(",")]
    for i, name in enumerate(names):
        res += f"<identifier>{name}</identifier>\n"
        if i < len(names) - 1:
            res += "<symbol>,</symbol>\n"

    res += "<symbol>;</symbol>\n"
    return (
        "<varDec>\n"
        + res
        + "</varDec>\n"
    )

# codeline = "var  int  x, y, z;"
# print(codeline)
# print(handle_var(codeline))

def handle_classVar(codeline):
    assert isinstance(codeline, str), "codeline must be a string"
    codeline = codeline.strip()
    assert codeline.startswith(("static ", "field ")), "codeline must start with 'static ' or 'field '"
    assert codeline.endswith(";"), "codeline must end with ';'"

    res = ""
    # 去掉 static/field 和 ;
    if codeline.startswith("static "):
        res += "<keyword>static</keyword>\n"
        body = codeline[7:-1].strip()
    else:
        res += "<keyword>field</keyword>\n"
        body = codeline[6:-1].strip()
    
    # type + vars
    parts = body.split()
    assert len(parts) >= 2, "Invalid classVar declaration"
    var_type = parts[0]
    var_names = body[len(var_type):].strip()

    # type
    if var_type in ("int", "char", "boolean"):
        res += f"<keyword>{var_type}</keyword>\n"
    else:
        res += f"<identifier>{var_type}</identifier>\n"

    # varName (, varName)*
    names = [v.strip() for v in var_names.split(",")]
    for i, name in enumerate(names):
        res += f"<identifier>{name}</identifier>\n"
        if i < len(names) - 1:
            res += "<symbol>,</symbol>\n"
    
    res += "<symbol>;</symbol>\n"
    return (
        "<classVarDec>\n"
        + res
        + "</classVarDec>\n"
    )

# codeline = "field  int  x, y, z;"
# print(codeline)
# print(handle_classVar(codeline))