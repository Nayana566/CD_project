# Project Report

## Title
Compiler Front End for Conditional Statements (if, if-else, nested)

## Problem Statement
Build a compiler front end that recognises `if`, `if-else` and nested conditional statements, and checks the syntax of conditions and statement blocks.

## Objectives
- Tokenise the source program with Flex.
- Define a context-free grammar for conditionals and parse it with Bison.
- Check conditions (`expr RELOP expr`) and braced statement blocks.
- Detect semantic errors (undeclared / redeclared variables).
- Build and display an Abstract Syntax Tree.

## Tools Used
| Tool | Purpose |
|------|---------|
| Flex | Lexical analyzer generator |
| Bison | LALR(1) parser generator |
| GCC | C compiler |
| Make | Build automation |

## Methodology
1. Write token definitions in `lexer.l`.
2. Write grammar rules and semantic actions in `parser.y`.
3. Build AST nodes in each grammar action (`ast.c`).
4. Keep a symbol table for declaration checks.
5. Test with valid and invalid programs (`tests/`).

## Test Cases

| File | Expected | Checks |
|------|----------|--------|
| valid/simple_if.txt | Accept | basic `if` |
| valid/if_else.txt | Accept | `if-else` |
| valid/nested_if.txt | Accept | 3-level nesting |
| valid/else_if_ladder.txt | Accept | `else if` chain |
| invalid/missing_paren.txt | Syntax error | missing `)` in condition |
| invalid/missing_relop.txt | Syntax error | condition with no relational operator |
| invalid/missing_brace.txt | Syntax error | unclosed block |
| invalid/dangling_else.txt | Syntax error | `else` with no `if` |
| invalid/undeclared.txt | Semantic error | undeclared variable in condition |
| invalid/redeclaration.txt | Semantic error | duplicate declaration |

## Limitations
- Conditions support only a single relational comparison (no `&&`, `||`, `!`).
- Expressions have no arithmetic operators.
- Statement bodies must be braced blocks.
- No intermediate code generation (front end only).

## Future Enhancements
- Logical operators and arithmetic expressions.
- Type checking between `int`/`float`/`char`.
- Three-address code generation for conditionals.
- Scoped symbol tables per block.

## Conclusion
The project shows the main phases of a compiler front end (lexical, syntax and semantic analysis) for conditional statements. It produces clear error messages and an AST for valid programs.
