# Conditional Statement Compiler Front End

A Compiler Design mini project that implements a **compiler front end for conditional statements** (`if`, `if-else`, `else if` and nested conditionals) using **C, Flex and Bison**.

The compiler checks that conditions and statement blocks are written correctly. It does lexical, syntax and semantic analysis, then prints an **Abstract Syntax Tree (AST)**.

---

## Features

- **Lexical analysis** (Flex): finds keywords, identifiers, numbers, relational operators and symbols. It reports invalid characters with their line numbers.
- **Syntax analysis** (Bison): checks the grammar of
  - simple `if`
  - `if-else`
  - `else if` ladders
  - nested conditionals of any depth
  - conditions of the form `expr RELOP expr`
  - statement blocks `{ ... }`
- **Semantic analysis**: uses a symbol table to catch
  - undeclared variables
  - duplicate declarations
- **AST generation**: prints the program structure as an indented tree.
- **Error reporting**: line-numbered messages, e.g. `Syntax error at line 2: syntax error, unexpected '{', expecting ')'`.

---

## Supported Language

```c
int a;                 // declarations: int | float | char
float f;
a = 10;                // assignment: ID = ID | NUMBER | FLOAT ;
if (a > 5) {           // relational ops: < > <= >= == !=
    if (a != 7) {      // nested if
        f = 1.5;
    }
} else if (a == 0) {   // else-if ladder
    a = 1;
} else {
    a = 2;
}
```

---

## Project Structure

```
CD_project/
├── lexer.l              # Flex lexical analyzer
├── parser.y             # Bison grammar, semantic checks, main()
├── ast.h / ast.c        # AST node definition, printing, cleanup
├── Makefile             # Build automation
├── tests/
│   ├── valid/           # Programs that must be accepted
│   ├── invalid/         # Programs that must be rejected
│   └── run_tests.sh     # Automated test runner
├── docs/                # Architecture, grammar, report, viva questions
├── presentation/        # Presentation outline
└── screenshots/         # Output screenshots
```

---

## Requirements

- GCC
- Flex
- Bison
- Make (optional)

**Ubuntu / WSL:** `sudo apt install gcc flex bison make`
**Windows:** use MSYS2 (`pacman -S gcc flex bison make`) or WSL.

---

## Build & Run

```bash
# Using make
make
./ifcompiler tests/valid/if_else.txt

# Manual build
bison -d parser.y
flex lexer.l
gcc -o ifcompiler parser.tab.c lex.yy.c ast.c

# Read from stdin
./ifcompiler < tests/valid/nested_if.txt
```

Run all tests:

```bash
make test
```

---

## Sample Output

**Input** (`tests/valid/if_else.txt`):

```c
int a;
int b;
if (a > 10) {
     b = 20;
}
else {
b = 30;
}
```

**Output:**

```
Syntax analysis successful.
Semantic analysis successful.
Program is valid.

Abstract Syntax Tree:
Declaration: a
Declaration: b
IF
  Condition: a > 10
  Body
    Block
      Assignment: b
        Expression: 20
    ELSE
      Block
        Assignment: b
          Expression: 30
```

**Invalid input** (`tests/invalid/missing_paren.txt`):

```
Syntax error at line 2: syntax error, unexpected '{', expecting RELOP or ')'
```

**Semantic error** (`tests/invalid/undeclared.txt`):

```
Semantic error: undeclared variable 'b'.
Syntax analysis successful.
Semantic analysis failed.
Program is invalid.
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Valid program |
| 1 | Lexical / syntax error |
| 2 | Semantic error |

---

## Grammar (summary)

```
Program     → StmtList
StmtList    → Stmt StmtList | ε
Stmt        → Declaration | Assignment | IfStmt | Block
Declaration → TYPE ID ;
Assignment  → ID = Expr ;
IfStmt      → if ( Cond ) Block ElsePart
ElsePart    → else Block | else IfStmt | ε
Block       → { StmtList }
Cond        → Expr RELOP Expr
Expr        → ID | NUMBER | FLOATNUM
```

See [docs/cfg_and_grammar.md](docs/cfg_and_grammar.md) for full details.

---

## Documentation

- [Architecture](docs/architecture.md)
- [CFG & Grammar](docs/cfg_and_grammar.md)
- [Project Report](docs/project_report.md)
- [Viva Questions](docs/viva_questions.md)

---

## License

This project is licensed under the [MIT License](LICENSE).
