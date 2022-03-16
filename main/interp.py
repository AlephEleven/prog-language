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
    match i_type:
        case "NUMBER":
            wrapper = int
        case "BOOL":
            wrapper = bool
        case _:
            wrapper = lambda x: x

    return return_exp(expr({i_type: wrapper(res)}))

#throws error
def ret_error(s):
    result(error_exp(s))

'''
Evaluates Expression

THIS IS WHERE YOU ADD FUNCTIONS IMPLEMENTED IN PARSER/ABSTREE/LEXER
'''
def eval_expr(exp):
    match exp.id:
        case "Int":
            (n) = exp
            return return_exp(n)
        case "Var":
            (n) = exp
            return return_exp(n)
        case "Bool":
            (n) = exp
            return return_exp(n)
        case "Add":
            (e1, e2) = exp.vals
            v1 = pass_eval(e1, int_of_Int)
            v2 = pass_eval(e2, int_of_Int)
            ans = v1+v2
            return return_type(ans,"NUMBER")
        case "Sub":
            (e1, e2) = exp.vals
            v1 = pass_eval(e1, int_of_Int)
            v2 = pass_eval(e2, int_of_Int)
            ans = v1-v2
            return return_type(ans,"NUMBER")
        case "Mul":
            (e1, e2) = exp.vals
            v1 = pass_eval(e1, int_of_Int)
            v2 = pass_eval(e2, int_of_Int)
            ans = v1*v2
            return return_type(ans,"NUMBER")
        case "Div":
            (e1, e2) = exp.vals
            v1 = pass_eval(e1, int_of_Int)
            v2 = pass_eval(e2, int_of_Int)
            if v2==0:
                ret_error("Division by zero")
            ans = v1/v2
            return return_type(ans,"NUMBER")
        case "IsZero?":
            (e) = exp.vals
            v = pass_eval(e, int_of_Int)
            ans = v==0
            return return_type(ans,"BOOL")
        case "And":
            (e1, e2) = exp.vals
            v1 = pass_eval(e1, bool_of_Bool)
            v2 = pass_eval(e2, bool_of_Bool)
            ans = v1 and v2
            return return_type(ans,"BOOL")
        case "Or":
            (e1, e2) = exp.vals
            v1 = pass_eval(e1, bool_of_Bool)
            v2 = pass_eval(e2, bool_of_Bool)
            ans = v1 or v2
            return return_type(ans,"BOOL")
        case "Abs":
            (e) = exp.vals
            v = pass_eval(e, int_of_Int)
            ans = abs(v)
            return return_type(ans,"NUMBER")
        case "Max":
            (e1, e2) = exp.vals
            v1 = pass_eval(e1, int_of_Int)
            v2 = pass_eval(e2, int_of_Int)
            ans = max(v1, v2)
            return return_type(ans,"NUMBER")
        case "Min":
            (e1, e2) = exp.vals
            v1 = pass_eval(e1, int_of_Int)
            v2 = pass_eval(e2, int_of_Int)
            ans = min(v1, v2)
            return return_type(ans,"NUMBER")
        case "ITE":
            (e1, e2, e3) = exp.vals
            v1 = pass_eval(e1, bool_of_Bool)
            v2 = pass_eval(e2, exp_of_Exp)
            v3 = pass_eval(e3, exp_of_Exp)
            
            if v1:
                ans = v2
                ans_type = match_generic(e2)
            else:
                ans = v3
                ans_type = match_generic(e3)

            return return_type(ans, ans_type)
        case _:
            ret_error("Not implemented")


'''
Application functions
'''

def string_to_tokens(s):
    return Token.parse_string(s)

def string_to_CST(s):
    return CST.parse_tokens(Token.parse_string(s))

def display_CST(s):
    CST.display_tree(string_to_CST(s))

def parse(s):
    return f"Parse: {AST.parse_CST_print(string_to_CST(s))}"

def interp(s):
    return f"Result: {result(eval_expr(AST.parse_CST(string_to_CST(s))))}"