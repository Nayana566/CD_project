# Viva Questions

**1. What is a compiler front end?**
The phases that analyse the source program: lexical, syntax and semantic analysis. They produce an intermediate representation such as an AST.

**2. What does Flex do?**
It generates a lexical analyzer (`yylex()`) from regular-expression rules, turning characters into tokens.

**3. What does Bison do?**
It generates an LALR(1) parser (`yyparse()`) from a context-free grammar.

**4. How do Flex and Bison communicate?**
Bison calls `yylex()` for each token. Token values are passed through `yylval`. `bison -d` creates `parser.tab.h`, which the lexer includes.

**5. What is the dangling-else problem? How does this project avoid it?**
In `if (a) if (b) x; else y;` it is unclear which `if` the `else` belongs to. Here every branch must be a `{ }` block, so the grammar is unambiguous.

**6. How are nested conditionals supported?**
`Block → { StmtList }` and `Stmt → IfStmt`, so an `if` can appear inside any block. This recursion allows any depth.

**7. How is `else if` handled?**
With the rule `ElsePart → ELSE IfStmt`.

**8. What does syntax validation of a condition mean here?**
The condition must be `Expr RELOP Expr` inside parentheses. Missing operands, a missing operator or missing parentheses all cause a syntax error.

**9. What semantic checks are done?**
Undeclared variables and duplicate declarations, using a symbol table.

**10. What is an AST? How is it different from a parse tree?**
An AST keeps only the meaningful structure (no punctuation or helper non-terminals). A parse tree shows every grammar symbol.

**11. What is `yylineno`?**
A Flex variable that tracks the current line number. It is turned on with `%option yylineno` and used in error messages.

**12. What does `%define parse.error verbose` do?**
It makes Bison report the unexpected token and the tokens it expected.

**13. Why is the `%empty` rule used?**
It marks an ε-production, e.g. an empty statement list or an optional `else`.

**14. What is the role of `%union`?**
It declares the possible types of semantic values (`char *` for lexemes, `ASTNode *` for tree nodes).
