# prog-language

Full interpreter written in python, from lexing to interpreting.

interpreter portion heavily based on course textbook: https://github.com/ebonelli/PLaF/

## Includes

- Lexing: Converts string to list of tokens
- Parser: Parses list of tokens to Concrete Syntax Tree (CST, dictionary tree-based)
- AST: Converts CST to Abstract Syntax Tree (stacked function-based)
- Interpreter: Interprets AST and returns final result
- Ds: extended functions cleaner interpreter
