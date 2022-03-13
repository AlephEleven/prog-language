'''
Given a list of tokens, we want to use a set of concrete syntax rules in order to create a
syntax tree, and finalize it by making an AST
'''

'''
Converts token to non-terminal token, i.e holds general type used for matching in CST
'''

class CST:
    def __init__(self):
        pass

    def concrete_type(token):
        match token:
            case {"NUMBER": _}:
                return {"EXP": token}
            case {"PLUS": _} | {"MINUS": _} | {"MULT": _} | {"DIV": _}:
                return {"OP": token}
            case other:
                return other

    '''
    Converts token list to list of non-terminal tokens
    '''
    def concrete_list(tk_list):
        return [CST.concrete_type(i) for i in tk_list]

    '''
    Concrete Syntax for language, checks for pattern in concrete list, if none found, returns current index (head)
    loops through entire list
    '''
    def concrete_defs(conc_list, prec=-1):
        match conc_list, prec:
            case [], _:
                return []
            #<Exp> := (<Exp>)
            case [{"LBRAC": lp}, {"EXP": e}, {"RBRAC": rp}, *t], 1:
                return [{"EXP": [{"LBRAC": lp}, {"EXP": e}, {"RBRAC": rp}]}] + CST.concrete_defs(t, prec)
            #<Exp> := <Exp> <BOp> <Exp> (with PEMDAS precedence)
            case [{"EXP": e1}, {"OP": op}, {"EXP": e2}, *t], _ if prec > 1:
                match op, prec:
                    case {"MULT": _} | {"DIV": _}, 2:
                        return [{"EXP": [{"EXP": e1}, {"OP": op}, {"EXP": e2}]}] + CST.concrete_defs(t, prec)
                    case {"PLUS": _} | {"MINUS": _}, 3:
                        return [{"EXP": [{"EXP": e1}, {"OP": op}, {"EXP": e2}]}] + CST.concrete_defs(t, prec)
                    case _, _:
                        return [{"EXP": e1}]+CST.concrete_defs([{"OP": op}, {"EXP": e2}] + t, prec)
            #<Any> := <Any>
            case [h, *t], _:
                return [h]+CST.concrete_defs(t, prec)


    '''
    Generates a Concrete Syntax Tree, loops through concrete definitions, and continously pattern matches
    from left-to-right until there are no changes when given to the defintions twice (or as set alarm)

    Raises exception if unable to make CST (list)
    '''
    def gen_CST(conc_list, alarm=2):
        i = 0
        cst = conc_list
        while(i < alarm):
            tmp_cst = cst
            cst = CST.concrete_defs(cst, 1)
            cst = CST.concrete_defs(cst, 2)
            cst = CST.concrete_defs(cst, 3)

            i = i+1 if tmp_cst==cst else 0

        if len(cst) > 1:
            raise Exception("Parser Error: Invalid syntax, could not parse")

        return cst

    def parse_tokens(tk_list):
        return CST.gen_CST(CST.concrete_list(tk_list))



