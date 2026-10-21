
#ifndef AST_H
#define AST_H

typedef struct ASTNode ASTNode;

struct ASTNode {
    char *type;
    char *value;
    ASTNode *left;
    ASTNode *right;
    ASTNode *next;
};

ASTNode *create_node(
    const char *type,
    const char *value,
    ASTNode *left,
    ASTNode *right
);

void print_ast(ASTNode *node, int depth);

void free_ast(ASTNode *node);

#endif
