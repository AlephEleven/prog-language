import pprint
import sys

def clean_excep(s):
    sys.tracebacklimit = 0
    raise Exception(s)
'''
Given a list of tokens, we want to use a set of concrete syntax rules in order to create a
syntax tree, and finalize it by making an AST
'''

'''
Concrete Syntax:

<Exp> ::= <ID> | <NUMBER> | {bool}
<Exp> ::= (<Exp>)
<Exp> ::= <Exp> <OP> <Exp>
<Exp> ::= <Exp>
<Exp> ::= <Exp> and <Exp>
<Exp> ::= <Exp> or <Exp>
<Exp> ::= iszero(<Exp>)
<Exp> ::= abs(<Exp>)
<Exp> ::= max(<Exp>) | min(<Exp>)


bool = true | false
<BOp> ::= <+|-|*|/>


Precendence:
1 - (), func()
2 - Mult/Div
3 - Add/Sub
'''



'''
Converts token to non-terminal token, i.e holds general type used for matching in CST
'''
def concrete_type(token):
    match token:
        # <Exp> ::= <ID> | <NUMBER>
        case {"ID": _} | {"NUMBER": _}:
            return {"EXP": token}
        # <BOp> ::= <+|-|*|/>
        case {"PLUS": _} | {"MINUS": _} | {"MULT": _} | {"DIV": _}:
            return {"OP": token}
        case other:
            return other

class CST:
    def __init__(self):
        pass

    def exp_cont(matching, tail, prec):
        return [{"EXP": matching}] + CST.concrete_defs(tail, prec)

    '''
    Converts token list to list of non-terminal tokens
    '''
    def concrete_list(tk_list):
        return [concrete_type(i) for i in tk_list]

    '''
    Checks if list of matchings all have keynames "EXP", used for making sure expressions are evaluated in begin <EXP> ... <EXP> end
    '''
    def is_exp_list(matching):
        for tk in matching:
            for key in tk:
                if key != "EXP":
                    return False
        return True

    '''
    Concrete Syntax for language, checks for pattern in concrete list, if none found, returns current index (head)
    loops through entire list

    THIS IS WHERE YOU ADD KEYWORD MATCHING FOR CST
    '''
    def concrete_defs(conc_list, prec=-1):
        match conc_list, prec:
            case [], _:
                return []
            #<Exp> ::= begin <EXP> ... <EXP> end
            case [{"KEY": "begin"}, *t, {"KEY": "end"}], 4 if CST.is_exp_list(t):
                return CST.exp_cont(conc_list, [], prec)
            #<Exp> ::= true
            case [{'EXP': {"ID": "true"}}, *t], 0:
                return CST.exp_cont([{'EXP': "true"}], t, prec)
            #<Exp> ::= false
            case [{'EXP': {"ID": "false"}}, *t], 0:
                return CST.exp_cont([{'EXP': "false"}], t, prec)
            #<Exp> ::= let <Exp/Id> = <Exp> in <Exp>
            case [{"KEY": "let"}, {"EXP": id}, {"EQUAL": eq}, {"EXP": defin}, {"KEY": "in"}, {"EXP": body}, *t], 1:
                return CST.exp_cont(conc_list[:6], t, prec)
            #<Exp> ::= if <Exp> then <Exp> else <Exp>
            case [{"KEY": "if"}, {"EXP": e1}, {"KEY": "then"}, {"EXP": e2}, {"KEY": "else"}, {"EXP": e3}, *t], 1:
                return CST.exp_cont(conc_list[:6], t, prec)
            #<Exp> ::= <Exp> and <Exp>
            case [{"EXP": e1}, {"KEY": "and"}, {"EXP": e2}, *t], 1:
                return CST.exp_cont(conc_list[:3], t, prec)
            #<Exp> ::= <Exp> or <Exp>
            case [{"EXP": e1}, {"KEY": "or"}, {"EXP": e2}, *t], 1:
                return CST.exp_cont(conc_list[:3], t, prec)
            #<Exp> ::= abs(<Exp>)
            case [{'KEY': "abs"}, {"LBRAC": lp}, {"EXP": e}, {"RBRAC": rp}, *t], 1:
                return CST.exp_cont(conc_list[:4], t, prec)
            #<Exp> ::= iszero(<Exp>)
            case [{'KEY': "iszero"}, {"LBRAC": lp}, {"EXP": e}, {"RBRAC": rp}, *t], 1:
                return CST.exp_cont(conc_list[:4], t, prec)
            #<Exp> ::= max(<Exp>,<Exp>)
            case [{'KEY': "max"}, {"LBRAC": lp}, {"EXP": e1}, {"COMMA": com}, {"EXP": e2}, {"RBRAC": rp}, *t], 1:
                return CST.exp_cont(conc_list[:6], t, prec)
            #<Exp> ::= min(<Exp>,<Exp>)
            case [{'KEY': "min"}, {"LBRAC": lp}, {"EXP": e1}, {"COMMA": com}, {"EXP": e2}, {"RBRAC": rp}, *t], 1:
                return CST.exp_cont(conc_list[:6], t, prec)
            #<Exp> ::= (<Exp>)
            case [{"LBRAC": lp}, {"EXP": e}, {"RBRAC": rp}, *t], 1:
                return CST.exp_cont(conc_list[:3], t, prec)
            #<Exp> ::= <Exp> <BOp> <Exp> (with PEMDAS precedence)
            case [{"EXP": e1}, {"OP": op}, {"EXP": e2}, *t], _ if prec > 1:
                match op, prec:
                    case {"MULT": _} | {"DIV": _}, 2:
                        return CST.exp_cont(conc_list[:3], t, prec)
                    case {"PLUS": _} | {"MINUS": _}, 3:
                        return CST.exp_cont(conc_list[:3], t, prec)
                    case _, _:
                        return [{"EXP": e1}]+CST.concrete_defs([{"OP": op}, {"EXP": e2}] + t, prec)
            #<Exp> ::= <Exp>
            case [h, *t], _:
                return [h]+CST.concrete_defs(t, prec)


    '''
    Generates a Concrete Syntax Tree, loops through concrete definitions, and continously pattern matches
    from left-to-right until there are no changes when given to the defintions twice (or as set alarm)

    Raises exception if unable to make CST (list)
    '''
    def gen_CST(conc_list, alarm=2, debug=False):
        i = 0
        cst = conc_list
        while(i < alarm):
            tmp_cst = cst
            cst = CST.concrete_defs(cst, 0)
            cst = CST.concrete_defs(cst, 1)
            cst = CST.concrete_defs(cst, 2)
            cst = CST.concrete_defs(cst, 3)
            cst = CST.concrete_defs(cst, 4)

            i = i+1 if tmp_cst==cst else 0

        if len(cst) > 1:
            if(debug):
                CST.display_tree(cst)
            clean_excep("Parser Error: Invalid syntax, unable to parse CST")

        return cst
    '''
    Converts a token list to a CST

    (final product of parser)
    '''
    def parse_tokens(tk_list):
        res = CST.gen_CST(CST.concrete_list(tk_list))

        try:
            res[0]["EXP"]
        except:
            clean_excep("Parser Error: Invalid syntax, Given a single keyword")

        match res[0]["EXP"]:
            case {"NUMBER": _} | {"ID": _}:
                return [{"EXP": res[0]}]
            case _:
                return res

    #displays entire CST
    def display_tree(conc_tree):
        pprint.pprint(conc_tree, width=1)
        



