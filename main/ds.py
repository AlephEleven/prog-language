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


def int_of_Int(exp):
    match exp.id:
        case "Int":
            return exp
        case _:
            raise Exception("Expected an Int!")
