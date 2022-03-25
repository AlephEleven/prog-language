# prog-language

Full interpreter written in python, from lexing to interpreting.

interpreter portion heavily based on course textbook: https://github.com/ebonelli/PLaF/

## Includes

- Lexing: Converts string to list of tokens
- Parser: Parses list of tokens to Concrete Syntax Tree (CST, dictionary tree-based)
- AST: Converts CST to Abstract Syntax Tree (stacked function-based)
- Interpreter: Interprets AST and returns final result
- Ds: extended functions for cleaner interpreter, including Environment for variable handling

## CST

```
Concrete Syntax:

<Exp> ::= <ID> | <NUMBER> | {bool}
<Exp> ::= (<Exp>) | (-<Exp>)
<Exp> ::= <Exp> <OP> <Exp>
<Exp> ::= <Exp>
<Exp> ::= <Exp> and <Exp> | <Exp> or <Exp> | not <Exp>
<Exp> ::= iszero(<Exp>)
<Exp> ::= abs(<Exp>)
<Exp> ::= max(<Exp>,<Exp>) | min(<Exp>,<Exp>)
<Exp> ::= begin <Exp> ... <Exp> end
<Exp> ::= for <Exp>:<Exp> <Exp> endf
<Exp> ::= while <Exp> <Exp> endw

<Exp> ::= [<Exp>, ..., <Exp>]
<Exp> ::= <Exp>[<Exp>]
<Exp> ::= len(<Exp>)
<Exp> ::= append(<Exp>, <Exp>)
<Exp> ::= pop(<Exp>)
<Exp> ::= push(<Exp>, <Exp>)

<Exp> ::= print(<Exp>)

bool = true | false
<BOp> ::= <+|-|*|/|%>


Precendence:
1 - (), func()
2 - Mult/Div/Mod
3 - Add/Sub
4 - begin end
```

## Testing

Via execute folder in command line:

```
$ python3.10 runlang.py filename [interp|parse|CST|tokens] (py)
```

Note: optional "py" tag puts a begin end wrapper between the input file, alike to pythonic code

Via interp.py:

### Tokens

shows tokens formed from string
```
>>> string_to_tokens("3+2*4")
[{'NUMBER': 3}, {'PLUS': '+'}, {'NUMBER': 2}, {'MULT': '*'}, {'NUMBER': 4}]
```

### CST

displays dictionary tree of CST via pprint printing
```
display_CST(s)
```

```
>>> display_CST("3+2*4")
[{'EXP': [{'EXP': {'NUMBER': 3}},
          {'OP': {'PLUS': '+'}},
          {'EXP': [{'EXP': {'NUMBER': 2}},
                   {'OP': {'MULT': '*'}},
                   {'EXP': {'NUMBER': 4}}]}]}]
```

### Parse

shows parsed results of input, (to-be run on interpreter code)
```
parse(s)
```

```
>>> parse("3+2*4")
'Parse: Add(Int 3, Mul(Int 2, Int 4))'
```

### Interp

interprets input and returns result, or error if invalid string given
```
interp(s)
```

```
>>> interp("3+2*4")
'Result: Ok (Int 11)'
```

Requires Python 3.10 and pprint to run
