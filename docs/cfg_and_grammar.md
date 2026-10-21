# CFG and Grammar

## Tokens

| Token | Pattern |
|-------|---------|
| IF | `if` |
| ELSE | `else` |
| TYPE | `int` \| `float` \| `char` |
| ID | `[a-zA-Z_][a-zA-Z0-9_]*` |
| NUMBER | `[0-9]+` |
| FLOATNUM | `[0-9]+"."[0-9]+` |
| RELOP | `<` `>` `<=` `>=` `==` `!=` |
| Symbols | `=` `;` `(` `)` `{` `}` |

## Context-Free Grammar

G = (V, T, P, S), with S = Program

```
Program     → StmtList
StmtList    → Stmt StmtList
            | ε
Stmt        → Declaration
            | Assignment
            | IfStmt
            | Block
Declaration → TYPE ID ;
Assignment  → ID = Expr ;
IfStmt      → IF ( Cond ) Block ElsePart
ElsePart    → ELSE Block
            | ELSE IfStmt
            | ε
Block       → { StmtList }
Cond        → Expr RELOP Expr
Expr        → ID | NUMBER | FLOATNUM
```

## Notes

- **No dangling-else ambiguity:** both branches must be `{ }` blocks, so every `else` attaches to the nearest unmatched `if` without shift/reduce conflicts.
- **Nesting:** `Block → { StmtList }` and `StmtList` can contain `IfStmt`, so conditionals nest to any depth.
- **else-if:** `ElsePart → ELSE IfStmt` lets you write `if … else if … else` ladders.

## Example derivation

`if (a > 1) { b = 2; }`

```
Program ⇒ StmtList ⇒ Stmt StmtList ⇒ IfStmt
        ⇒ IF ( Cond ) Block ElsePart
        ⇒ IF ( Expr RELOP Expr ) { StmtList } ε
        ⇒ IF ( ID > NUMBER ) { Assignment } 
        ⇒ if ( a > 1 ) { b = 2 ; }
```
