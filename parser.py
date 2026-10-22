"""Recursive-descent parser and parse-tree formatting."""
from semantic import SemanticAnalyzer


class SyntaxErrorInSource(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.semantic = SemanticAnalyzer()
        # Keep these attributes available for compatibility with the original parser.
        self.symbols = self.semantic.symbols
        self.semantic_errors = self.semantic.errors
        self.lexical_token_count = len(tokens) - 1

    def current(self):
        return self.tokens[self.pos]

    def accept(self, kind):
        if self.current().kind == kind:
            token = self.current()
            self.pos += 1
            return token
        return None

    def expect(self, kind, expected_text=None):
        token = self.accept(kind)
        if token is None:
            current = self.current()
            expected = expected_text or kind
            got = current.value if current.value else "end of input"
            raise SyntaxErrorInSource(
                f"Syntax error at line {current.line}, column "
                f"{current.column}: expected {expected}, got {got!r}"
            )
        return token

    def parse(self):
        statements = []
        while self.current().kind != "EOF":
            statements.append(self.parse_statement())
        return {"type": "Program", "children": statements}

    def parse_statement(self):
        kind = self.current().kind
        if kind == "TYPE":
            return self.parse_declaration()
        if kind == "ID":
            return self.parse_assignment()
        if kind == "IF":
            return self.parse_if()
        if kind == "LBRACE":
            return self.parse_block()

        current = self.current()
        got = current.value if current.value else "end of input"
        raise SyntaxErrorInSource(
            f"Syntax error at line {current.line}, column "
            f"{current.column}: unexpected {got!r}"
        )

    def parse_declaration(self):
        type_token = self.expect("TYPE")
        name = self.expect("ID", "identifier")
        self.expect("SEMI", "';'")
        self.semantic.declare(name.value, type_token.value)
        return {"type": "Declaration", "value": f"{type_token.value} {name.value}"}

    def parse_assignment(self):
        name = self.expect("ID")
        self.expect("EQUALS", "'='")
        expression = self.parse_expression()
        self.expect("SEMI", "';'")
        self.semantic.check_expression(expression)
        return {
            "type": "Assignment",
            "value": name.value,
            "children": [{"type": "Expression", "value": expression}]
        }

    def parse_if(self):
        self.expect("IF")
        self.expect("LPAREN", "'('")
        left = self.parse_expression()
        relop = self.expect("RELOP", "relational operator")
        right = self.parse_expression()
        self.expect("RPAREN", "')'")
        self.semantic.check_expression(left)
        self.semantic.check_expression(right)

        condition = {"type": "Condition", "value": f"{left} {relop.value} {right}"}
        then_block = self.parse_block()
        else_block = None
        if self.accept("ELSE"):
            else_block = self.parse_block()

        children = [condition, {"type": "Body", "children": [then_block]}]
        if else_block is not None:
            children[1]["children"].append({"type": "ELSE", "children": [else_block]})
        return {"type": "IF", "children": children}

    def parse_block(self):
        self.expect("LBRACE", "'{'")
        statements = []
        while self.current().kind not in ("RBRACE", "EOF"):
            statements.append(self.parse_statement())
        self.expect("RBRACE", "'}'")
        return {"type": "Block", "children": statements}

    def parse_expression(self):
        token = self.current()
        if token.kind in ("ID", "NUMBER", "FLOATNUM"):
            self.pos += 1
            return token.value
        got = token.value if token.value else "end of input"
        raise SyntaxErrorInSource(
            f"Syntax error at line {token.line}, column {token.column}: "
            f"expected identifier or number, got {got!r}"
        )


def ast_lines(node, depth=0):
    lines = ["  " * depth + node["type"] +
             (f": {node['value']}" if node.get("value") is not None else "")]
    for child in node.get("children", []):
        lines.extend(ast_lines(child, depth + 1))
    return lines


def _tree_node(label, children=None):
    return {"label": label, "children": children or []}


def build_parse_tree(node):
    """Build the grammar-style tree shown in the Parse Tree tab."""
    kind = node["type"]
    value = node.get("value")
    children = node.get("children", [])

    if kind == "Program":
        return _tree_node("Program", [build_parse_tree(c) for c in children] or [_tree_node("ε")])
    if kind == "Declaration":
        parts = value.split(" ", 1)
        return _tree_node("Declaration", [_tree_node("TYPE: " + parts[0]),
            _tree_node("id: " + parts[1]), _tree_node("SEMI: ;")])
    if kind == "Assignment":
        expr = children[0].get("value", "") if children else ""
        return _tree_node("Assignment", [_tree_node("id: " + str(value)),
            _tree_node("EQUALS: ="), _tree_node("Expression", [_tree_node("Value: " + str(expr))]),
            _tree_node("SEMI: ;")])
    if kind == "IF":
        condition = children[0] if children else {"value": ""}
        body = children[1] if len(children) > 1 else {"children": []}
        condition_node = _tree_node("Condition", [_tree_node(condition.get("value", ""))])
        body_children = body.get("children", [])
        then_block = body_children[0] if body_children else {"type": "Block", "children": []}
        then_node = _tree_node("Then", [build_parse_tree(then_block)])
        else_node = _tree_node("Else", [build_parse_tree(body_children[1]["children"][0])]
            if len(body_children) > 1 and body_children[1].get("children") else [_tree_node("ε")])
        return _tree_node("IF", [_tree_node("if"), _tree_node("("), condition_node,
            _tree_node(")"), then_node, else_node])
    if kind == "Block":
        return _tree_node("Block", [_tree_node("{"),
            _tree_node("StatementList", [build_parse_tree(c) for c in children] or [_tree_node("ε")]),
            _tree_node("}")])
    return _tree_node(kind + (": " + str(value) if value is not None else ""),
                      [build_parse_tree(c) for c in children])


def parse_tree_lines(node, prefix="", is_last=True, is_root=True):
    label = node["label"]
    lines = [label] if is_root else [prefix + ("└── " if is_last else "├── ") + label]
    children = node.get("children", [])
    child_prefix = "" if is_root else prefix + ("    " if is_last else "│   ")
    for index, child in enumerate(children):
        lines.extend(parse_tree_lines(child, child_prefix, index == len(children) - 1, False))
    return lines
