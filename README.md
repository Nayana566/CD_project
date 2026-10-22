# Conditional Statement Compiler — Python + Web UI

This educational compiler front end is written in Python and uses Flask for its browser interface. The compiler logic is separated into three modules: `lexer.py`, `parser.py`, and `semantic.py`. `compiler.py` connects these modules to the existing web UI.

## Features
- Lexical analysis with a numbered token list, token type, lexeme, line and column
- Syntax parsing for declarations, assignments, braced blocks, and nested `if-else`
- Grammar-style parse tree displayed with branches similar to a compiler derivation tree
- Abstract Syntax Tree (AST)
- Basic semantic checks for duplicate declarations and undeclared variables
- Symbol table and status panels in the web UI

## Files
- `app.py` — Flask web application and compile endpoint
- `templates/index.html` — existing user interface (unchanged)
- `lexer.py` — token definitions and lexical analysis
- `parser.py` — recursive-descent syntax parser, AST and parse-tree formatting
- `semantic.py` — semantic checks and symbol-table management
- `compiler.py` — coordinates the modules and returns the data expected by the UI
- `requirements.txt` — Python dependency list

## Run on Windows / VS Code
1. Keep all Python files, `requirements.txt`, `README.md`, and the `templates` folder together in the same project folder.
2. Open this project folder in VS Code.
3. Open Terminal → New Terminal.
4. Install Flask:
   ```powershell
   py -m pip install -r requirements.txt
   ```
5. Start the app:
   ```powershell
   py app.py
   ```
6. Open `http://127.0.0.1:5000` in your browser.
7. Enter a program and click **Compile Program**. Use the existing tabs to view Result, Tokens, Parse Tree, AST, Semantic Report, and Symbol Table.

## Supported language example
```c
int a;
int b;
a = 5;
if (a > 10) {
    if (b < 20) {
        a = 6;
    } else {
        a = 7;
    }
} else {
    b = 30;
}
```

Supported declarations: `int a;`, `float b;`, `char c;`. Assignments support a single identifier or numeric value, for example `a = 5;` or `b = a;`. Conditions support a single identifier or number on each side of `<`, `>`, `<=`, `>=`, `==`, or `!=`. Braced blocks and nested `if-else` are supported.

## Current limitations
Arithmetic expressions such as `a = b + 2;`, character literals, type compatibility checks, block-local scopes, and executing the input program are not implemented. The compiler parses the source and reports compiler-front-end information; it does not execute the source program.
