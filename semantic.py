"""Basic semantic checks and symbol-table management."""
import re


class SemanticAnalyzer:
    def __init__(self):
        self.symbols = {}
        self.errors = []

    def declare(self, name, type_name):
        if name in self.symbols:
            self.errors.append(
                f"Semantic error: duplicate declaration '{name}'."
            )
        else:
            self.symbols[name] = type_name

    def check_expression(self, expression):
        if re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", expression):
            if expression not in self.symbols:
                self.errors.append(
                    f"Semantic error: undeclared variable '{expression}'."
                )

    def symbol_table_text(self):
        return "\n".join(
            ["IDENTIFIER       TYPE", "-" * 28] +
            [f"{name:<16} {type_name}" for name, type_name in self.symbols.items()]
        ) or "No symbols declared."
