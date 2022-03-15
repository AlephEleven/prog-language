from calendar import c
from lexer import Token
from parser import CST
from abstree import *
from ds import *

'''
Here is where we want to finally evaluate expressions that come from the AST
'''

#evaluates an expression, then binds it
def pass_eval(exp, f):
    return pass_exp(eval_expr(exp), f).vals

#returns result with type
def return_type(res, i_type):
    return return_exp(expr({i_type: res}))

#throws error
def ret_error(s):
    result(error_exp(s))

#evaluate expression
def eval_expr(exp):
    match exp.id:
        case "Int":
            (n) = exp
            return return_exp(n)
        case "Var":
            return return_exp(exp)
        case "Add":
            (e1, e2) = exp.vals
            v1 = pass_eval(e1, int_of_Int)
            v2 = pass_eval(e2, int_of_Int)
            ans = v1+v2
            return return_type(int(ans),"NUMBER")
        case "Sub":
            (e1, e2) = exp.vals
            v1 = pass_eval(e1, int_of_Int)
            v2 = pass_eval(e2, int_of_Int)
            ans = v1-v2
            return return_type(int(ans),"NUMBER")
        case "Mul":
            (e1, e2) = exp.vals
            v1 = pass_eval(e1, int_of_Int)
            v2 = pass_eval(e2, int_of_Int)
            ans = v1*v2
            return return_type(int(ans),"NUMBER")
        case "Div":
            (e1, e2) = exp.vals
            v1 = pass_eval(e1, int_of_Int)
            v2 = pass_eval(e2, int_of_Int)
            if v2==0:
                ret_error("Division by zero")
            ans = v1/v2
            return return_type(int(ans),"NUMBER")
        case _:
            ret_error("Not implemented")


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

print(interp("3/2"))