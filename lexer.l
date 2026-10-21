
%{
#include "parser.tab.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
%}

%option noyywrap
%option yylineno

ID          [a-zA-Z_][a-zA-Z0-9_]*
NUMBER      [0-9]+
FLOATNUM    [0-9]+"."[0-9]+

%%

"if"                        { return IF; }
"else"                      { return ELSE; }
"int"|"float"|"char"        { return TYPE; }

"<="|">="|"=="|"!="|"<"|">" {
    yylval.str = strdup(yytext);
    return RELOP;
}

{FLOATNUM} {
    yylval.str = strdup(yytext);
    return FLOATNUM;
}

{NUMBER} {
    yylval.str = strdup(yytext);
    return NUMBER;
}

{ID} {
    yylval.str = strdup(yytext);
    return ID;
}

"="                         { return '='; }
";"                         { return ';'; }
"("                         { return '('; }
")"                         { return ')'; }
"{"                         { return '{'; }
"}"                         { return '}'; }

"//".*                      { /* Ignore single-line comments */ }
[ \t\r\n]+                  { /* Ignore whitespace */ }

. {
    printf("Lexical error at line %d: invalid character '%s'\n", yylineno, yytext);
    return INVALID;
}

%%
