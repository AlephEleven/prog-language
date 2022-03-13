from lexer import Token

'''
Given a list of tokens, we want to use a set of concrete syntax rules in order to create a
syntax tree, and finalize it by making an AST
'''

def concrete_type(token):
    match token:
        case {"NUMBER": _}:
            return {"EXP": token}
        case {"PLUS": _} | {"MINUS": _} | {"MULT": _} | {"DIV": _}:
            return {"OP": token}
        case other:
            return other

def concrete_list(tk_list):
    return [concrete_type(i) for i in tk_list]

def concrete_defs(conc_list):
    match conc_list:
        case []:
            return []
        #<Exp> := <EXP> <BOp> <Exp>
        case [{"EXP": e1}, {"OP": op}, {"EXP": e2}, *t]:
            return [{"EXP": [{"EXP": e1}, {"OP": op}, {"EXP": e2}]}] + concrete_defs(t)
        #<Exp> := (<Exp>)
        case [{"LBRAC": lp}, {"EXP": e}, {"RBRAC": rp}, *t]:
            return [{"EXP": [{"LBRAC": lp}, {"EXP": e}, {"RBRAC": rp}]}] + concrete_defs(t)
        #<Any> := <Any>
        case [h, *t]:
            return [h]+concrete_defs(t)

defs = concrete_list(Token.parse_string("1+1+1+1+1+1+1+1+1+1+1"))

def gen_CST(conc_list, alarm=2):
    i = 0
    cst = conc_list
    while(i < alarm):
        tmp_cst = cst
        cst = concrete_defs(cst)

        i = i+1 if tmp_cst==cst else 0

    if len(cst) > 1:
        raise Exception("Parser Error: Invalid syntax, could not parse")

    return cst





