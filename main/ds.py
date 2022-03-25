from abstree import expr_cls, est_no_expr
import sys

def clean_excep(s):
    sys.tracebacklimit = 0
    raise Exception(s)

'''
Abstracted Results
'''

#evaluates final result 
def result(exp):
    match exp.id:
        case "Error":
            clean_excep(exp.vals)
        case "Ok":
            return f"Ok ({exp.vals.str})"

#Abstracted valid exp type
def return_exp(exp):
    return expr_cls("Ok", exp, f"Ok ({exp})")

#gets expression from return val
def return_val(ret):
    return ret.vals

def rem_ok(exp):
    match exp.id:
        case "Ok":
            return exp.vals
        case _:
            return exp

#Abstracted error type
def error_exp(s):
    return expr_cls("Error", s, f'Error "{s}"')


#binding function, checks whether to propagate error, or apply function
def pass_exp(exp, f):
    match exp.id:
        case "Error":
            return exp
        case "Ok":
            return f(return_val(exp))

#throws error
def ret_error(s):
    result(error_exp(s))


'''
Variable Environments
'''

def empty_env():
    return expr_cls("EmptyEnv", None, f"EmptyEnv")

def extend_env(id, defin, env):
    return return_exp(expr_cls("ExtendEnv", (id, defin, env), f"ExtendEnv({id}, {defin}, {env})"))

def apply_env_h(id, env):
    match env.id:
        case "EmptyEnv":
            ret_error(f"{id.str} not found!")
        case "ExtendEnv":
            if id.vals==env.vals[0].vals:
                return return_exp(env.vals[1])
            else:
                return apply_env_h(id, rem_ok(env.vals[2]))

def apply_env(id, env):
    return apply_env_h(id, rem_ok(env))


'''
Type checking
'''

def match_generic(exp):
    match exp.id:
        case "Int": return "NUMBER"
        case "Bool": return "BOOL"
        case "Var": return "ID"
        case _: return "E"+exp.id.capitalize()

def exp_of_Exp(exp):
    return exp

def int_of_Int(exp):
    match exp.id:
        case "Int":
            return exp
        case _:
            raise Exception("Expected an Int!")

def bool_of_Bool(exp):
    match exp.id:
        case "Bool":
            return exp
        case _:
            raise Exception("Expected an Bool!")

def arr_of_Arr(exp):
    match exp.id:
        case "Arr":
            return exp
        case _:
            raise Exception("Expected an Arr!")

def update_arr(ans):
    return expr_cls("Arr", [ele for ele in ans], f"Arr({[est_no_expr(ele) for ele in ans]})")