from lexer import Token
from parser import CST
from abstree import AST


def string_to_CST(s):
    return CST.parse_tokens(Token.parse_string(s))

def display_CST(s):
    CST.display_tree(string_to_CST(s))

def parse(s):
    return f"Parse: {AST.parse_CST_print(string_to_CST(s))}"

print(parse("2+3*4"))