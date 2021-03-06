from lexer import Token
from parser import CST
from abstree import *
from ds import *

'''
Here is where we want to finally evaluate expressions that come from the AST
'''

#evaluates an expression, then binds it
def pass_eval(exp, f=lambda x:x):
    return pass_exp(eval_expr(exp), f).vals

#returns result with type
def return_type(res, i_type):
    #print(res, i_type)
    match i_type:
        case "NUMBER":
            wrapper = int
        case "BOOL":
            wrapper = bool
        case _:
            wrapper = lambda x: x

    return return_exp(expr({i_type: wrapper(res)}))

'''
Evaluates Expression

THIS IS WHERE YOU ADD FUNCTIONS IMPLEMENTED IN PARSER/ABSTREE/LEXER
'''

env = empty_env()

g_store = Store()

def eval_expr(exp):
    global env
    match exp.id:
        case "Int":
            (n) = exp
            return return_exp(n)
        case "Var":
            (n) = exp
            ans = apply_env(n, env)
            return ans
        case "Bool":
            (n) = exp
            return return_exp(n)
        case "Arr":
            (n) = exp
            new_vals = []
            for i in n.vals:
                new_vals += [return_val(eval_expr(i))]
            ans = update_arr(new_vals)
            return return_exp(ans)
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
        case "Mod":
            (e1, e2) = exp.vals
            v1 = pass_eval(e1, int_of_Int)
            v2 = pass_eval(e2, int_of_Int)
            ans = v1%v2
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
        case "Not":
            (e) = exp.vals
            v = pass_eval(e, bool_of_Bool)
            ans = not v
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
            if v1: return eval_expr(e2)
            else: return eval_expr(e3)
        case "Let":
            (id, defin, body) = exp.vals
            d = return_val(eval_expr(defin))
            env = extend_env(id, d, env)
            return eval_expr(body)
        case "Line":
            (es) = exp.vals
            if len(es)==0:
                return return_exp(expr_cls("Unit", "", "Unit()"))
            for e in es[:-1]:
                eval_expr(e)
            return eval_expr(es[-1])
        case "For":
            (e1, e2, e3) = exp.vals
            v1 = pass_eval(e1, int_of_Int)
            v2 = pass_eval(e2, int_of_Int)
            for i in range(v1, v2):
                eval_expr(e3)
        case "While":
            (e1, e2) = exp.vals
            v1 = pass_eval(e1, bool_of_Bool)
            if(v1):
                eval_expr(e2)
                eval_expr(exp)
        case "ArrAcc":
            (e1, e2) = exp.vals
            v1 = pass_eval(e1, arr_of_Arr)
            v2 = pass_eval(e2, int_of_Int)
            if(v2>=len(v1) or v2<0):
                ret_error("Array out of bounds")
            ans = v1[v2]
            return eval_expr(ans)
        case "Len":
            (e) = exp.vals
            v = pass_eval(e, arr_of_Arr)
            ans = len(v)
            return return_type(ans,"NUMBER")
        case "Append":
            (e1, e2) = exp.vals
            v1 = pass_eval(e1, arr_of_Arr)
            v2 = pass_eval(e2, arr_of_Arr)
            ans = update_arr(v1+v2)
            return eval_expr(ans)
        case "Pop":
            (e) = exp.vals
            v = pass_eval(e, arr_of_Arr)
            ans = update_arr(v[1:])
            return eval_expr(ans)
        case "Push":
            (e1, e2) = exp.vals
            v1 = pass_eval(e1, arr_of_Arr)
            v2 = e2
            ans = update_arr([v2]+v1)
            return eval_expr(ans)
        case "Print":
            (e) = exp.vals
            v = eval_expr(e)
            print(result(v))
        case "NewRef":
            (e) = exp.vals
            v = eval_expr(e)
            ref_expr = {"NUMBER": len(g_store.ls)}
            g_store.newref(e)
            ans = expr_cls("Ref", expr(ref_expr), f"Ref({est(ref_expr)})")
            return return_exp(ans)
        case "DeRef":
            (e) = exp.vals
            v = pass_eval(e, int_of_Ref)
            ans = g_store.deref(v.vals)
            return return_exp(ans)
        case "SetRef":
            (e1, e2) = exp.vals
            v1 = pass_eval(e1, int_of_Ref)
            v2 = return_val(eval_expr(e2))
            g_store.setref(v1.vals, v2)
            ans = expr_cls("Unit", "", "Unit()")
            return return_exp(ans)
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

def get_glob_env():
    global env
    return return_val(env).str

def get_refs():
    global g_store
    return g_store


