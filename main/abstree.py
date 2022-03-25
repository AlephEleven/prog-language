'''
Given a Concrete Syntax Tree, we want to convert it to an Abstract Syntax Tree that contains the direct functions we
want to evaluate.
'''

#short-form for making mini classes (exprs for this case)
def expr_cls(name, params, str_rep):
    return type(name, (object,), {"vals": params, "str": str_rep, "id":name})

#prettier get function for string-rep of expr_cls
def est(expr_obj):
    return expr(expr_obj).str

def est_no_expr(expr_obj):
    return expr_obj.str

'''
List of expression in Abstract Syntax

THIS IS WHERE YOU ADD FUNCTION-TYPE for AST
'''
def expr(token):
    match token:
        case {"NUMBER": v}:
            return expr_cls("Int", v, f"Int {v}")
        case {"BOOL": v}:
            return expr_cls("Bool", v, f"Bool {v}")
        case {"ID": v}:
            return expr_cls("Var", v, f'Var "{v}"')
        case {"EAdd": [v1, v2]}:
            return expr_cls("Add", (expr(v1), expr(v2)), f"Add({est(v1)}, {est(v2)})")
        case {"ESub": [v1, v2]}:
            return expr_cls("Sub", (expr(v1), expr(v2)), f"Sub({est(v1)}, {est(v2)})")
        case {"EMul": [v1, v2]}:
            return expr_cls("Mul", (expr(v1), expr(v2)), f"Mul({est(v1)}, {est(v2)})")
        case {"EDiv": [v1, v2]}:
            return expr_cls("Div", (expr(v1), expr(v2)), f"Div({est(v1)}, {est(v2)})")
        case {"EMod": [v1, v2]}:
            return expr_cls("Mod", (expr(v1), expr(v2)), f"Mod({est(v1)}, {est(v2)})")
        case {"EIzero": v}:
            return expr_cls("IsZero?", expr(v), f"IsZero?({est(v)})")
        case {"ETrue": _}:
            return expr({"BOOL": True})
        case {"EFalse": _}:
            return expr({"BOOL": False})
        case {"EAnd": [v1, v2]}:
            return expr_cls("And", (expr(v1), expr(v2)), f"And({est(v1)}, {est(v2)})")
        case {"EOr": [v1, v2]}:
            return expr_cls("Or", (expr(v1), expr(v2)), f"Or({est(v1)}, {est(v2)})")
        case {"ENot": v}:
            return expr_cls("Not", (expr(v)), f"Not({est(v)})")
        case {"EAbs": v}:
            return expr_cls("Abs", expr(v), f"Abs({est(v)})")
        case {"ELen": v}:
            return expr_cls("Len", expr(v), f"Len({est(v)})")
        case {"EPrint": v}:
            return expr_cls("Print", expr(v), f"Print({est(v)})")
        case {"EPop": v}:
            return expr_cls("Pop", expr(v), f"Pop({est(v)})")
        case {"EPush": [v1, v2]}:
            return expr_cls("Push", (expr(v1), expr(v2)), f"Push({est(v1)}, {est(v2)})")
        case {"EMax": [v1, v2]}:
            return expr_cls("Max", (expr(v1), expr(v2)), f"Max({est(v1)}, {est(v2)})")
        case {"EMin": [v1, v2]}:
            return expr_cls("Min", (expr(v1), expr(v2)), f"Min({est(v1)}, {est(v2)})")
        case {"EIte": [v1, v2, v3]}:
            return expr_cls("ITE", (expr(v1), expr(v2), expr(v3)), f"ITE({est(v1)}, {est(v2)}, {est(v3)})")
        case {"ELet": [id, defin, body]}:
            return expr_cls("Let", (expr(id), expr(defin), expr(body)), f"Let({est(id)}, {est(defin)}, {est(body)})")
        case {"ELine": vs}:
            return expr_cls("Line", [expr(v) for v in vs], f"Line({[est(v) for v in vs]})")
        case {"EFor": [v1, v2, v3]}:
            return expr_cls("For", (expr(v1), expr(v2), expr(v3)), f"For({est(v1)}, {est(v2)}, {est(v3)})")
        case {"EWhile": [v1, v2]}:
            return expr_cls("While", (expr(v1), expr(v2)), f"While({est(v1)}, {est(v2)})")
        case {"EArr": vs}:
            return expr_cls("Arr", [expr(v) for v in vs], f"Arr({[est(v) for v in vs]})")
        case {"EArrAcc": [v1, v2]}:
            return expr_cls("ArrAcc", (expr(v1), expr(v2)), f"ArrAcc({est(v1)}, {est(v2)})")
        case {"EAppend": [v1, v2]}:
            return expr_cls("Append", (expr(v1), expr(v2)), f"Append({est(v1)}, {est(v2)})")
        case v:
            return AST.abs_defs({"EXP": v})

class AST:
    def __init__(self):
        pass

    '''
    Recursively replaces nodes in CST with expressions defined by AST in expr

    THIS IS WHERE YOU ADD AST MATCHING
    '''
    def abs_defs(conc_tree):
        match conc_tree:
            case {"EXP": v}:
                match v:
                    case [{"EXP": e1}, {"LSBRAC": _}, {"EXP": e2}, {"RSBRAC": _}]:
                        return expr({"EArrAcc": [e1, e2]})
                    case [{"LSBRAC": _}, *t, {"RSBRAC": _}]:
                        arr = v[1:len(v)-1]
                        return expr({"EArr": [list(e.values())[0] for e in arr[::2]]})
                    case [{"KEY": "while"}, {"EXP": e1}, {"EXP": e2}, {"KEY": "endw"}]:
                        return expr({"EWhile": [e1, e2]})
                    case [{"KEY": "for"}, {"EXP": e1}, {"COLON": cl}, {"EXP": e2}, {"EXP": e3}, {"KEY": "endf"}]:
                        return expr({"EFor": [e1, e2, e3]})
                    case [{"KEY": "begin"}, *t, {"KEY": "end"}]:
                        return expr({"ELine": [list(e.values())[0] for e in v[1:len(v)-1]]})
                    case [{"KEY": "let"}, {"EXP": id}, {"EQUAL": eq}, {"EXP": defin}, {"KEY": "in"}, {"EXP": body}]:
                        return expr({"ELet": [id, defin, body]})
                    case [{"KEY": "if"}, {"EXP": e1}, {"KEY": "then"}, {"EXP": e2}, {"KEY": "else"}, {"EXP": e3}]:
                        return expr({"EIte": [e1, e2, e3]})
                    case [{"EXP": e1}, {"KEY": "and"}, {"EXP": e2}]:
                        return expr({"EAnd": [e1, e2]})
                    case [{"EXP": e1}, {"KEY": "or"}, {"EXP": e2}]:
                        return expr({"EOr": [e1, e2]})
                    case [{"KEY": "not"}, {"EXP": e}]:
                        return expr({"ENot": e})
                    case [{"KEY": "iszero"}, {"LBRAC": _}, {"EXP": e}, {"RBRAC": _}]:
                        return expr({"EIzero": e})
                    case [{"EXP": "true"}]:
                        return expr({"ETrue": "true"})
                    case [{"EXP": "false"}]:
                        return expr({"EFalse": "false"})
                    case [{"KEY": "abs"}, {"LBRAC": _}, {"EXP": e}, {"RBRAC": _}]:
                        return expr({"EAbs": e})
                    case [{"KEY": "len"}, {"LBRAC": _}, {"EXP": e}, {"RBRAC": _}]:
                        return expr({"ELen": e})
                    case [{"KEY": "print"}, {"LBRAC": _}, {"EXP": e}, {"RBRAC": _}]:
                        return expr({"EPrint": e})
                    case [{"KEY": "pop"}, {"LBRAC": _}, {"EXP": e}, {"RBRAC": _}]:
                        return expr({"EPop": e})
                    case [{"KEY": "push"}, {"LBRAC": _}, {"EXP": e1}, {"COMMA": _} ,{"EXP": e2}, {"RBRAC": _}]:
                        return expr({"EPush": [e1, e2]})
                    case [{'KEY': "max"}, {"LBRAC": _}, {"EXP": e1}, {"COMMA": _}, {"EXP": e2}, {"RBRAC": _}]:
                        return expr({"EMax": [e1, e2]})
                    case [{'KEY': "min"}, {"LBRAC": _}, {"EXP": e1}, {"COMMA": _}, {"EXP": e2}, {"RBRAC": _}]:
                        return expr({"EMin": [e1, e2]})
                    case [{'KEY': "append"}, {"LBRAC": _}, {"EXP": e1}, {"COMMA": _}, {"EXP": e2}, {"RBRAC": _}]:
                        return expr({"EAppend": [e1, e2]})
                    case [{"LBRAC": _}, {"EXP": e}, {"RBRAC": _}] | {"EXP": e}:
                        return expr(e)
                    case [{"EXP": e1}, {"OP": op}, {"EXP": e2}]:
                        match op:
                            case {"PLUS": _}:
                                return expr({"EAdd": [e1, e2]})
                            case {"MINUS": _}:
                                return expr({"ESub": [e1, e2]})
                            case {"MULT": _}:
                                return expr({"EMul": [e1, e2]})
                            case {"DIV": _}:
                                return expr({"EDiv": [e1, e2]})
                            case {"MOD": _}:
                                return expr({"EMod": [e1, e2]})

                    case _:
                        return expr_cls("invalid", {"str": -1}, "Invalid")
            case _:
                return expr_cls("invalid", {"str": -1}, "Invalid")

    '''
    Converts a CST (dictionary tree-type) to an AST (stacked class-type)

    (final product of abstree)
    '''
    def parse_CST(conc_tree):
        return AST.abs_defs(conc_tree[0])

    #returns string-rep of entire AST
    def parse_CST_print(conc_tree):
        return AST.parse_CST(conc_tree).str