
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ast.h"

ASTNode *create_node(
    const char *type,
    const char *value,
    ASTNode *left,
    ASTNode *right
)
{
    ASTNode *node = malloc(sizeof(ASTNode));

    if (node == NULL) {
        fprintf(stderr, "Memory allocation failed.\n");
        exit(EXIT_FAILURE);
    }

    node->type = strdup(type);
    node->value = value ? strdup(value) : NULL;

    node->left = left;
    node->right = right;
    node->next = NULL;

    if (node->type == NULL ||
        (value != NULL && node->value == NULL)) {
        fprintf(stderr, "Memory allocation failed.\n");
        exit(EXIT_FAILURE);
    }

    return node;
}

void print_ast(ASTNode *node, int depth)
{
    if (node == NULL)
        return;

    for (int i = 0; i < depth; i++)
        printf("  ");

    printf("%s", node->type);

    if (node->value != NULL)
        printf(": %s", node->value);

    printf("\n");

    print_ast(node->left, depth + 1);
    print_ast(node->right, depth + 1);
    print_ast(node->next, depth);
}

void free_ast(ASTNode *node)
{
    if (node == NULL)
        return;

    free_ast(node->left);
    free_ast(node->right);
    free_ast(node->next);

    free(node->type);
    free(node->value);
    free(node);
}
