import sys
sys.path.append(sys.path[0].replace("execute", "main"))
from interp import *

args = sys.argv

usage = f"Usage: {args[0]} filename [interp|parse|CST|tokens|all]"

if(len(args) != 3):
    raise Exception(f"{usage}\n Error: too many/less flags specified ({len(args)-1})")

F = open(args[1], "r")
content = F.read()

match args[2]:
    case "interp":
        print(interp(content))
    case "parse":
        print(parse(content))
    case "CST":
        display_CST(content)
    case "tokens":
        print(string_to_tokens(content))
    case "all":
        print(string_to_tokens(content))
        display_CST(content)
        print(parse(content))
        print(interp(content))
    case _:
        print(usage)