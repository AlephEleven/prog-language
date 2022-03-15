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

'''
List of expression in Abstract Syntax
'''
def expr(token):
    match token:
        case {"NUMBER": v}:
            return expr_cls("Int", v, f"Int {v}")
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
        case v:
            return AST.abs_defs({"EXP": v})

class AST:
    def __init__(self):
        pass

    '''
    Recursively replaces nodes in CST with expressions defined by AST in expr
    '''
    def abs_defs(conc_tree):
        match conc_tree:
            case {"EXP": v}:
                match v:
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