"""Lexical analyzer for the Conditional Statement Compiler."""
import re
from dataclasses import dataclass


@dataclass
class Token:
    kind: str
    value: str
    line: int
    column: int


class LexicalError(Exception):
    pass


TOKEN_SPEC = [
    ("WHITESPACE", r"[ \t\r]+"),
    ("NEWLINE",    r"\n"),
    ("FLOATNUM",   r"[0-9]+\.[0-9]+"),
    ("NUMBER",     r"[0-9]+"),
    ("ID",         r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("RELOP",      r"<=|>=|==|!=|<|>"),
    ("EQUALS",     r"="),
    ("SEMI",       r";"),
    ("LPAREN",     r"\("),
    ("RPAREN",     r"\)"),
    ("LBRACE",     r"\{"),
    ("RBRACE",     r"\}"),
]
TOKEN_RE = re.compile("|".join(
    f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC
))


def tokenize(source):
    """Convert source text into tokens, retaining line and column positions."""
    tokens = []
    pos = 0
    line = 1
    column = 1

    while pos < len(source):
        match = TOKEN_RE.match(source, pos)

        if not match:
            char = source[pos]
            raise LexicalError(
                f"Lexical error at line {line}, column {column}: "
                f"invalid character {char!r}"
            )

        kind = match.lastgroup
        value = match.group()

        if kind == "NEWLINE":
            line += 1
            column = 1
        elif kind != "WHITESPACE":
            if kind == "ID":
                if value in ("if", "else"):
                    kind = value.upper()
                elif value in ("int", "float", "char"):
                    kind = "TYPE"
            tokens.append(Token(kind, value, line, column))
            column += len(value)
        else:
            column += len(value)

        pos = match.end()

    tokens.append(Token("EOF", "", line, column))
    return tokens


def token_lines(tokens):
    """Format tokens for display in the existing Tokens tab."""
    lines = [f"{'No.':<5} {'TOKEN TYPE':<12} {'LEXEME':<16} {'POSITION'}",
             "-" * 55]
    for number, token in enumerate(tokens):
        if token.kind == "EOF":
            continue
        lines.append(
            f"{number + 1:<5} {token.kind:<12} {token.value:<16} "
            f"line {token.line}, column {token.column}"
        )
    if len(lines) == 2:
        lines.append("No tokens found.")
    return "\n".join(lines)
