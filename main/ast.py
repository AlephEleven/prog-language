from lexer import Token
from parser import CST















s = "(2+2)*3"
print(CST.parse_tokens(Token.parse_string(s)))