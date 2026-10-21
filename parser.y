
%code requires {
    #include "ast.h"
}

%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ast.h"

int yylex(void);
void yyerror(const char *s);
extern int yylineno;
extern FILE *yyin;

char *symbols[100];
int symbol_count = 0;
int semantic_errors = 0;
ASTNode *root = NULL;

int is_declared(const char *name)
{
    for (int i = 0; i < symbol_count; i++) {
        if (strcmp(symbols[i], name) == 0)
            return 1;
    }
    return 0;
}

void declare_variable(char *name)
{
    if (is_declared(name)) {
        printf("Semantic error: duplicate declaration '%s'.\n", name);
        semantic_errors++;
    } else if (symbol_count < 100) {
        symbols[symbol_count++] = strdup(name);
    } else {
        printf("Semantic error: symbol table is full.\n");
        semantic_errors++;
    }
}

void check_variable(char *name)
{
    if (!is_declared(name)) {
        printf("Semantic error: undeclared variable '%s'.\n", name);
        semantic_errors++;
    }
}

void check_expression(char *expr)
{
    if (expr != NULL &&
        ((expr[0] >= 'a' && expr[0] <= 'z') ||
         (expr[0] >= 'A' && expr[0] <= 'Z') ||
         expr[0] == '_')) {
        check_variable(expr);
    }
}
%}

%union {
    char *str;
    ASTNode *node;
}

%token IF ELSE TYPE
%token <str> ID NUMBER FLOATNUM RELOP
%token INVALID

%type <str> Expr
%type <node> Program StmtList Stmt Declaration
%type <node> Assignment IfStmt ElsePart Block Cond

%start Program
%define parse.error verbose

%%

Program
    : StmtList
      {
          root = $1;
      }
    ;

StmtList
    : Stmt StmtList
      {
          $$ = $1;

          if ($$ != NULL) {
              ASTNode *temp = $$;

              while (temp->next != NULL)
                  temp = temp->next;

              temp->next = $2;
          } else {
              $$ = $2;
          }
      }
    | %empty
      {
          $$ = NULL;
      }
    ;

Stmt
    : Declaration
      {
          $$ = $1;
      }
    | Assignment
      {
          $$ = $1;
      }
    | IfStmt
      {
          $$ = $1;
      }
    | Block
      {
          $$ = $1;
      }
    ;

Declaration
    : TYPE ID ';'
      {
          declare_variable($2);
          $$ = create_node("Declaration", $2, NULL, NULL);
          free($2);
      }
    ;

Assignment
    : ID '=' Expr ';'
      {
          check_variable($1);
          check_expression($3);

          $$ = create_node(
              "Assignment",
              $1,
              create_node("Expression", $3, NULL, NULL),
              NULL
          );

          free($1);
          free($3);
      }
    ;

IfStmt
    : IF '(' Cond ')' Block ElsePart
      {
          $$ = create_node(
              "IF",
              NULL,
              $3,
              create_node("Body", NULL, $5, $6)
          );
      }
    ;

ElsePart
    : ELSE Block
      {
          $$ = create_node("ELSE", NULL, $2, NULL);
      }
    | ELSE IfStmt
      {
          $$ = create_node("ELSE-IF", NULL, $2, NULL);
      }
    | %empty
      {
          $$ = NULL;
      }
    ;

Block
    : '{' StmtList '}'
      {
          $$ = create_node("Block", NULL, $2, NULL);
      }
    ;

Cond
    : Expr RELOP Expr
      {
          check_expression($1);
          check_expression($3);

          char buffer[256];

          snprintf(
              buffer,
              sizeof(buffer),
              "%s %s %s",
              $1,
              $2,
              $3
          );

          $$ = create_node("Condition", buffer, NULL, NULL);

          free($1);
          free($2);
          free($3);
      }
    ;

Expr
    : ID
      {
          $$ = $1;
      }
    | NUMBER
      {
          $$ = $1;
      }
    | FLOATNUM
      {
          $$ = $1;
      }
    ;

%%

void yyerror(const char *s)
{
    printf("Syntax error at line %d: %s\n", yylineno, s);
}

int main(int argc, char *argv[])
{
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (yyin == NULL) {
            fprintf(stderr, "Cannot open file '%s'.\n", argv[1]);
            return 1;
        }
    }

    int result = yyparse();

    if (result == 0) {
        printf("Syntax analysis successful.\n");

        if (semantic_errors == 0) {
            printf("Semantic analysis successful.\n");
            printf("Program is valid.\n");
        } else {
            printf("Semantic analysis failed.\n");
            printf("Program is invalid.\n");
        }

        printf("\nAbstract Syntax Tree:\n");
        print_ast(root, 0);
        free_ast(root);
    }

    for (int i = 0; i < symbol_count; i++)
        free(symbols[i]);

    if (argc > 1)
        fclose(yyin);

    if (result != 0)
        return 1;
    return semantic_errors > 0 ? 2 : 0;
}
