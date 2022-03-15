from lexer import Token
from parser import CST
from abstree import *
from ds import *

'''
Here is where we want to finally evaluate expressions that come from the AST
'''

def valof(eval_e):
    return eval_e.vals.vals


def eval_expr(exp):
    match exp.id:
        case "Int":
            return return_exp(exp)
        case "Var":
            return return_exp(exp)
        case "Add":
            (e1, e2) = exp.vals
            v1 = pass_exp(eval_expr(int_of_Int(e1)), valof)
            v2 = pass_exp(eval_expr(int_of_Int(e2)), valof)
            res = v1+v2
            return return_exp(expr({"NUMBER": res}))





'''
Application functions
'''

def string_to_CST(s):
    return CST.parse_tokens(Token.parse_string(s))

def display_CST(s):
    CST.display_tree(string_to_CST(s))

def parse(s):
    return f"Parse: {AST.parse_CST_print(string_to_CST(s))}"

def interp(s):
    return f"Result: {result(eval_expr(AST.parse_CST(string_to_CST(s))))}"

print(interp("2+3"))