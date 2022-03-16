from abstree import expr_cls

'''
Abstracted Results
'''

#evaluates final result 
def result(exp):
    match exp.id:
        case "Error":
            raise Exception(exp.vals)
        case "Ok":
            return f"Ok ({exp.vals.str})"

#Abstracted valid exp type
def return_exp(exp):
    return expr_cls("Ok", exp, f"Ok ({exp})")

#gets expression from return val
def return_val(ret):
    return ret.vals

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