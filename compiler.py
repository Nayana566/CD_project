"""Coordinates lexer, parser, and semantic analysis for the existing web UI."""
from lexer import tokenize, LexicalError, token_lines
from parser import Parser, SyntaxErrorInSource, ast_lines, build_parse_tree, parse_tree_lines


def compile_source(source):
    try:
        tokens = tokenize(source)
    except LexicalError as error:
        return {
            "output": str(error), "lexical": "Failed", "syntax": "Not completed",
            "semantic": "Not completed", "ast": "", "tokens": "", "parse_tree": "",
            "symbol_table": ""
        }

    tokens_text = token_lines(tokens)
    try:
        parser = Parser(tokens)
        tree = parser.parse()
    except SyntaxErrorInSource as error:
        return {
            "output": "Lexical analysis successful.\n" + str(error),
            "lexical": "Successful", "syntax": "Failed", "semantic": "Not completed",
            "ast": "", "tokens": tokens_text, "parse_tree": "", "symbol_table": ""
        }

    output_lines = [
        "Lexical analysis successful.",
        f"Tokens recognized: {len(tokens) - 1}",
        "Syntax analysis successful."
    ]
    if parser.semantic_errors:
        output_lines.extend(parser.semantic_errors)
        output_lines.extend(["Semantic analysis failed.", "Program is invalid."])
        semantic_status = "Failed"
    else:
        output_lines.extend(["Semantic analysis successful.", "Program is valid."])
        semantic_status = "Successful"

    tree_text = "\n".join(ast_lines(tree))
    concrete_tree_text = "\n".join(parse_tree_lines(build_parse_tree(tree)))
    symbols_text = parser.semantic.symbol_table_text()
    output_lines.extend(["", "Tokens:", tokens_text, "", "Parse Tree:", concrete_tree_text,
                         "", "Abstract Syntax Tree:", tree_text])

    return {
        "output": "\n".join(output_lines),
        "lexical": "Successful", "syntax": "Successful", "semantic": semantic_status,
        "tokens": tokens_text, "parse_tree": concrete_tree_text, "ast": tree_text,
        "symbol_table": symbols_text
    }
