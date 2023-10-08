import csv

class TransitionTable:
    def __init__(self, table_filepath):
        with open(table_filepath) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            self.alphabet = csv_reader.__next__()[1:]
            self.table = {}
            for line in csv_reader:
                nterm = line[0]
                self.table[nterm] = {}
                for col_idx, rule in enumerate(line[1:]):
                    self.table[nterm][self.alphabet[col_idx]] = rule.split(' ')

class Child:
    def __init__(self, val):
        self.val = val

    def display(self, indent=""):
        print(f"{indent}Leaf Node: {self.val}")


class InnerProd:
    def __init__(self, nterm):
        self.nterm = nterm
        self.children = []

    def display(self, indent=""):
        print(f"{indent}Inner Node: {self.nterm}:")
        for child in self.children:
            child.display(indent + "\t")


def top_down_alg(tokens: list, tbl: TransitionTable):
    sparent = InnerProd(None)
    stack = [(sparent, '$'), (sparent, 'Grammar')]
    token = tokens[0]
    tokens = tokens[1:]
    parent, X = stack.pop()

    while X != '$':
        if X in tbl.alphabet:
            if X == token.domain_name():
                parent.children.append(Child(token))
                token = tokens[0]
                tokens = tokens[1:]
            else:
                raise ValueError(f"Expected {X}, got {token.domain_name()}")
        elif X in tbl.table:
            inner = InnerProd(X)
            if token.domain_name() in tbl.table[X]:
                if tbl.table[X][token.domain_name()][0] == "ERROR":
                    raise ValueError(f"Error for {token}")
                elif tbl.table[X][token.domain_name()][0] != "eps":
                    for elem in reversed(tbl.table[X][token.domain_name()]):
                        stack.append((inner, elem))
                    parent.children.append(inner)
            else:
                raise ValueError(f"Rule for token:{token.domain_name()} in {tbl.table[X].keys()} isn't found")
        else:
            raise ValueError(f"Unexpected {X} found in table")
        parent, X = stack.pop()

    return sparent.children[0]