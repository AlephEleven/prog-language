import sys
sys.path.append(sys.path[0].replace("execute", "main"))
from interp import *

args = sys.argv

usage = f"Usage: {args[0]} filename [interp|parse|CST|tokens|all] (py)"

if(len(args) < 3 or len(args) > 4):
    raise Exception(f"{usage}\n Error: too many/less flags specified ({len(args)-1})")

F = open(args[1], "r")
content = F.read()

if(len(args)==4):
    match args[3]:
        case "py":
            content = "begin "+content+" end"
        case _:
            raise Exception(f"{usage}\n Error: invalid third argument ({args[3]})")

match args[2]:
    case "interp":
        print(interp(content))
    case "parse":
        print(parse(content))
    case "CST":
        display_CST(content)
    case "tokens":
        print(string_to_tokens(content))
    case "debug":
        interp(content)
        print("Environment:")
        print(get_glob_env())
        print(get_refs())
    case "all":
        print(string_to_tokens(content))
        display_CST(content)
        print(parse(content))
        print(interp(content))
    case _:
        print(usage)