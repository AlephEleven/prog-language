import pprint
import sys

def clean_excep(s):
    sys.tracebacklimit = 0
    raise Exception(s)

def cst_error():
    return clean_excep("Parser Error: Invalid syntax, unable to parse CST")
'''
Given a list of tokens, we want to use a set of concrete syntax rules in order to create a
syntax tree, and finalize it by making an AST
'''

'''
Concrete Syntax:

<Exp> ::= <ID> | <NUMBER> | {bool}
<Exp> ::= (<Exp>) | (-<Exp>)
<Exp> ::= <Exp> <OP> <Exp>
<Exp> ::= <Exp>
<Exp> ::= <Exp> and <Exp> | <Exp> or <Exp> | not <Exp>
<Exp> ::= iszero(<Exp>)
<Exp> ::= abs(<Exp>)
<Exp> ::= max(<Exp>,<Exp>) | min(<Exp>,<Exp>)
<Exp> ::= begin <Exp> ... <Exp> end
<Exp> ::= for <Exp>:<Exp> <Exp> endf
<Exp> ::= while <Exp> <Exp> endw

<Exp> ::= [<Exp>, ..., <Exp>]
<Exp> ::= <Exp>[<Exp>]
<Exp> ::= len(<Exp>)
<Exp> ::= append(<Exp>, <Exp>)
<Exp> ::= pop(<Exp>)
<Exp> ::= push(<Exp>, <Exp>)

<Exp> ::= print(<Exp>)

bool = true | false
<BOp> ::= <+|-|*|/|%>


Precendence:
1 - (), func()
2 - Mult/Div/Mod
3 - Add/Sub
4 - begin end
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
        case {"PLUS": _} | {"MINUS": _} | {"MULT": _} | {"DIV": _} | {"MOD": _}:
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
    
    def exp_list_to_tk_be(matching):
        i = 1
        for tk in matching:
            for key in tk:
                i += 1
                #print(key)

                if key !="EXP" and key=="KEY" and tk["KEY"]=="end":
                    return (True, i)

                if key !="EXP":
                    return (False, i)

        return (False, i)
    
    def exp_list_to_tk_arr(matching):
        i = 1
        exp_com = 0
        exp_com_l = ["EXP", "COMMA"]
        for tk in matching:
            for key in tk:
                i += 1
                if key != exp_com_l[exp_com%2] and key=="RSBRAC":
                    return (True, i)
                if key != exp_com_l[exp_com%2]:
                    return (False, i)
                exp_com += 1
        return (False, i)

    '''
    Concrete Syntax for language, checks for pattern in concrete list, if none found, returns current index (head)
    loops through entire list

    THIS IS WHERE YOU ADD KEYWORD MATCHING FOR CST
    '''
    def concrete_defs(conc_list, prec=-1):
        match conc_list, prec:
            case [], _:
                return []
            #<Exp> ::= <Exp>[<Exp>]
            case [{"EXP": e1}, {"LSBRAC": ls}, {"EXP": e2}, {"RSBRAC": rs}, *t], 0:
                return CST.exp_cont(conc_list[:4], t, prec)
            #<Exp> ::= [<Exp>, ..., <Exp>]
            case [{"LSBRAC": ls}, *t], 1:
                exps = CST.exp_list_to_tk_arr(t)
                if(exps[0]):
                    return CST.exp_cont(conc_list[:exps[1]], conc_list[exps[1]:], prec)
                else:
                    return [{"LSBRAC": ls}]+CST.concrete_defs(t, prec)
            #<Exp> ::= begin <Exp> ... <Exp> end
            case [{"KEY": "begin"}, *t], 4:
                exps = CST.exp_list_to_tk_be(t)
                if(exps[0]):
                    return CST.exp_cont(conc_list[:exps[1]], conc_list[exps[1]:], prec)
                else:
                    return [{"KEY": "begin"}]+CST.concrete_defs(t, prec)
            #<Exp> ::= for <Exp/Int>:<Exp/Int> <Exp> endf
            case [{"KEY": "for"}, {"EXP": e1}, {"COLON": cl}, {"EXP": e2}, {"EXP": e3}, {"KEY": "endf"}, *t], 4:
                return CST.exp_cont(conc_list[:6], t, prec)
            #<Exp> ::= while <Exp/Bool> <Exp> endw
            case [{"KEY": "while"}, {"EXP": e1}, {"EXP": e2}, {"KEY": "endw"}, *t], 4:
                return CST.exp_cont(conc_list[:4], t, prec)
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
            #<Exp> ::= not <Exp>
            case [{"KEY": "not"}, {"EXP": e}, *t], 1:
                return CST.exp_cont(conc_list[:2], t, prec)
            #<Exp> ::= abs(<Exp>)
            case [{'KEY': "abs"}, {"LBRAC": lp}, {"EXP": e}, {"RBRAC": rp}, *t], 1:
                return CST.exp_cont(conc_list[:4], t, prec)
            #<Exp> ::= iszero(<Exp>)
            case [{'KEY': "iszero"}, {"LBRAC": lp}, {"EXP": e}, {"RBRAC": rp}, *t], 1:
                return CST.exp_cont(conc_list[:4], t, prec)
            #<Exp> ::= len(<Exp>)
            case [{'KEY': "len"}, {"LBRAC": lp}, {"EXP": e}, {"RBRAC": rp}, *t], 1:
                return CST.exp_cont(conc_list[:4], t, prec)
            #<Exp> ::= print(<Exp>)
            case [{'KEY': "print"}, {"LBRAC": lp}, {"EXP": e}, {"RBRAC": rp}, *t], 1:
                return CST.exp_cont(conc_list[:4], t, prec)
            #<Exp> ::= pop(<Exp>)
            case [{'KEY': "pop"}, {"LBRAC": lp}, {"EXP": e}, {"RBRAC": rp}, *t], 1:
                return CST.exp_cont(conc_list[:4], t, prec)
            #<Exp> ::= push(<Exp/Arr>, <Exp>)
            case [{'KEY': "push"}, {"LBRAC": lp}, {"EXP": e}, {"COMMA": _} ,{"EXP": e2}, {"RBRAC": rp}, *t], 1:
                return CST.exp_cont(conc_list[:6], t, prec)
            #<Exp> ::= max(<Exp>,<Exp>)
            case [{'KEY': "max"}, {"LBRAC": lp}, {"EXP": e1}, {"COMMA": com}, {"EXP": e2}, {"RBRAC": rp}, *t], 1:
                return CST.exp_cont(conc_list[:6], t, prec)
            #<Exp> ::= min(<Exp>,<Exp>)
            case [{'KEY': "min"}, {"LBRAC": lp}, {"EXP": e1}, {"COMMA": com}, {"EXP": e2}, {"RBRAC": rp}, *t], 1:
                return CST.exp_cont(conc_list[:6], t, prec)
            #<Exp> ::= append(<Exp>,<Exp>)
            case [{'KEY': "append"}, {"LBRAC": lp}, {"EXP": e1}, {"COMMA": com}, {"EXP": e2}, {"RBRAC": rp}, *t], 1:
                return CST.exp_cont(conc_list[:6], t, prec)
            #<Exp> ::= (<Exp>)
            case [{"LBRAC": lp}, {"EXP": e}, {"RBRAC": rp}, *t], 1:
                return CST.exp_cont(conc_list[:3], t, prec)
            #<Exp> ::= (-<Exp>)
            case [{"LBRAC": lp}, {"OP": {"MINUS": _}}, {"EXP": e}, {"RBRAC": rp}, *t], 1:
                return [{"LBRAC": lp}, {"EXP": {"NUMBER": 0}}, {"OP": {"MINUS": "-"}}, {"EXP": e}, {"RBRAC": rp}]+CST.concrete_defs(t, prec)
            #<Exp> ::= <Exp> <BOp> <Exp> (with PEMDAS precedence)
            case [{"EXP": e1}, {"OP": op}, {"EXP": e2}, *t], _ if prec > 1:
                match op, prec:
                    case {"MULT": _} | {"DIV": _} | {"MOD": _}, 2:
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
            cst_error()

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
        



