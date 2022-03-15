# prog-language

Full interpreter written in python, from lexing to interpreting.

interpreter portion heavily based on course textbook: https://github.com/ebonelli/PLaF/

## Includes

- Lexing: Converts string to list of tokens
- Parser: Parses list of tokens to Concrete Syntax Tree (CST, dictionary tree-based)
- AST: Converts CST to Abstract Syntax Tree (stacked function-based)
- Interpreter: Interprets AST and returns final result
- Ds: extended functions for cleaner interpreter

## CST

Exp ::= ID | NUMBER

Exp ::= (Exp)

Exp ::= Exp OP Exp

Exp ::= Exp

OP ::= +|-|*|/

Precendence:
1.  ()
2.  Mult/Div
3.  Add/Sub

## Testing

Via interp.py

### Display CST

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
