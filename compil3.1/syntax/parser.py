from ..scanner.scanner import Scanner
from ..scanner.token import Token
from ..syntax.syntax import Nonterm, RHS, Symbol, Term


class ParseNode:
    def __init__(self, symbol: Symbol, parent: 'ParseNode' = None):
        self.symbol = symbol
        self.number = 0
        self.children = []
        self.parent = parent

    def set_number(self, number: int):
        self.number = number

    def set_token(self, token: Token):
        self.symbol = token

    def get_symbol(self) -> Symbol:
        return self.symbol

    def get_symbol_at(self, n: int) -> Symbol:
        return self.children[n].symbol

    def add_children(self, nodes: RHS):
        for s in nodes:
            self.children.append(ParseNode(s, self))

    def is_the_most_right_child(self) -> bool:
        return self.parent and self.parent.index(self) == len(self.parent.children) - 1

    def is_root(self) -> bool:
        return not self.parent

    def succ(self) -> 'ParseNode':
        if self.is_root():
            return self

        res = self.parent
        prev = self
        while not res.is_root() and prev.is_the_most_right_child():
            prev = res
            res = res.parent

        if res.is_root() and prev.is_the_most_right_child():
            return self  # This branch is already the rightmost, no successor will exist
        res = res.children[res.index(prev) + 1]

        while not res.is_leaf():
            res = res.children[0]
        return res

    def get_child_at(self, child_index: int) -> 'ParseNode':
        return self.children[child_index]

    def get_child_count(self) -> int:
        return len(self.children)

    def get_parent(self) -> 'ParseNode':
        return self.parent

    def get_index(self, node: 'ParseNode') -> int:
        if isinstance(node, ParseNode):
            return self.children.index(node)
        else:
            return -1

    def get_allows_children(self) -> bool:
        return not isinstance(self.symbol, Token)

    def is_leaf(self) -> bool:
        return not self.children

    def children(self):
        return iter(self.children)

    def to_dot(self) -> str:
        res = f"{self.number} {self.symbol.to_dot()}"
        for child in self.children:
            res += child.to_dot()
            res += f"{self.number}->{child.number}\n"
        return res


class ParseTree:
    def __init__(self, axiom: Nonterm):
        self.root = ParseNode(axiom)
        self.current = self.root
        self.current_number = 0
        self.update()

    def update(self):
        self.current_number += 1
        self.current.set_number(self.current_number)

    def add(self, rule: RHS):
        if not rule.is_empty():
            self.current.add_children(rule)
            self.current = self.current.get_child_at(0)
        else:
            self.current = self.current.succ()
        self.update()

    def set_token(self, token: Token):
        self.current.set_token(token)
        self.current = self.current.succ()
        self.update()

    def to_dot(self):
        return "digraph {\n" + self.root.to_dot() + "}\n"

    def get_root(self):
        return self.root

    def get_child(self, parent, index):
        return parent.get_child_at(index)

    def get_child_count(self, parent):
        return parent.get_child_count()

    def is_leaf(self, node):
        return node.is_leaf()

    def value_for_path_changed(self, path, new_value):
        pass

    def get_index_of_child(self, parent, child):
        return parent.get_index(child)

    def add_tree_model_listener(self, l):
        pass

    def remove_tree_model_listener(self, l):
        pass


class Parser:

    def __init__(self, terms, nonterms, axiom, q):
        self.terms = terms.copy()
        self.nonterms = nonterms.copy()
        self.axiom = axiom
        self.q = q.copy()

    def get_log(self):
        return "\n".join(self.log)

    def delta(self, N, T):
        i = self.nonterms.index(N.get_type())
        j = self.terms.index(T.get_type())
        if i == -1:
            print("[Parser.delta]: no nonterm " + str(N) + " is found in " + str(self.nonterms))
        if j == -1:
            print("[Parser.delta]: no term " + str(T.get_type()) + " is found in " + str(self.terms))
        return self.q[i][j]

    def print_error(self, tok, expected):
        self.log.append("***ERROR: " + str(expected) + " expected, got: " + str(tok))

    def top_down_parse(self, scanner):
        self.log = []
        stack = []
        stack.append(Term(Term.EOF))
        stack.append(self.axiom)
        self.parse_tree = ParseTree(self.axiom)
        tok = scanner.next_token()
        while stack:
            self.log.append(str(stack) + "-----------" + str(tok))
            X = stack.pop()
            if isinstance(X, Term):
                if X == tok:
                    self.parse_tree.set_token(tok)
                    tok = scanner.next_token()
                else:
                    self.print_error(tok, X)
                    return self.parse_tree
            else:
                next_rule = self.delta(X, tok)
                if RHS.is_error(next_rule):
                    self.print_error(tok, X)
                    return self.parse_tree
                else:
                    stack.extend(next_rule.reverse())
                    self.parse_tree.add(next_rule)
        return self.parse_tree

    def get_parse_tree(self):
        return self.parse_tree

    def add_file(self, path):
        dotfile = os.path.join(path)
        try:
            with open(dotfile, 'w') as file:
                file.write(self.parse_tree.to_dot())
        except IOError:
            print("File " + dotfile + " cannot be read.")


class GrammarScanner(Scanner):
    NONTERMINAL = "N"
    TERMINAL = "T"

    @staticmethod
    def get_reg_expressions():
        exprs = {
            "COMMA": ",",
            "ORSIGN": "\\|",
            "COLON": ";",
            "EQSIGN": "::=",
            "NONTERMINALSIGN": "non-terminal",
            "TERMINALSIGN": "terminal",
            "AXIOMSIGN": "axiom",
            "EPSILON": "epsilon",
            GrammarScanner.NONTERMINAL: "[A-Z]+1?",
            GrammarScanner.TERMINAL: "(\'[^\\s\']*\'|[a-z]|[0-9]*)"
        }
        return exprs

    def __init__(self, filepath):
        super().__init__(filepath, GrammarScanner.reg_expressions)

    def return_token(self, type):
        last = self.coord
        self.coord = self.coord.shift(len(self.image))
        self.log.append(f"{type} {last}-{self.coord}: <{self.image}>\n")
        if type == GrammarScanner.TERMINAL or type == GrammarScanner.NONTERMINAL:
            return Token(type, self.image, last, self.coord)
        return Token(self.image, self.image, last, self.coord)


GrammarScanner.reg_expressions = GrammarScanner.get_reg_expressions()