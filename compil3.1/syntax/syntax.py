from ..scanner.coords import Coords


class RHS(list):
    def __init__(self, *symbols):
        super().__init__(symbols)

    def reverse(self):
        rule = RHS()
        rule.extend(reversed(self))
        return rule

    def set_coords(self, c):
        self.coords = c

    def get_coords(self):
        return self.coords

    def print_constructor(self):
        if self == RHS.EPSILON:
            return "RHS.EPSILON"
        res = "new RHS("
        if self:
            res += f"\n                {self[0].print_constructor()}"
        for symbol in self[1:]:
            res += f",\n                {symbol.print_constructor()}"
        res += "\n                )"
        return res

    coords = Coords.undefined()

    @staticmethod
    def is_epsilon(rhs):
        return not rhs

    @staticmethod
    def is_error(rhs):
        return rhs is None


RHS.EPSILON = RHS()
RHS.ERROR = None


class Symbol:
    def __init__(self, type, start=None, follow=None):
        self.type = type
        self.start = start or Coords.undefined()
        self.follow = follow or Coords.undefined()

    def get_type(self):
        return self.type

    def __str__(self):
        return self.type

    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.type == other.type
        elif isinstance(other, str):
            return self.type == other
        return False

    def to_dot(self):
        return ""

    def coords_to_string(self):
        return f"{self.start}-{self.follow}"

    def get_start(self):
        return self.start

    def get_follow(self):
        return self.follow

    def print_constructor(self):
        return "*** Error in Symbol.printConstructor(): no public constructor"


class Rules(list):
    def __init__(self, *rules):
        super().__init__(rules)

    def print_constructor(self):
        res = "Rules("
        if self:
            res += f"\n        {self[0].print_constructor()}"
        for rule in self[1:]:
            res += f",\n        {rule.print_constructor()}"
        res += "\n)\n"
        return res


class Nonterm(Symbol):
    def __init__(self, type, start=None, follow=None):
        super().__init__(type, start, follow)

    def __str__(self):
        return "<" + super().__str__() + ">"

    def to_dot(self):
        return f"[label=\"{self.get_type()}\"][color=green]\n"

    def print_constructor(self):
        return f"new Nonterm(\"{self.get_type()}\")"


class Term(Symbol):
    EOF = "$"
    EPSILON = ""

    def __init__(self, type, start=None, follow=None):
        super().__init__(type, start, follow)

    def __str__(self):
        return "\"" + super().__str__() + "\""

    def to_dot(self):
        return f"[label=\"{self.get_type()}\"][color=black]\n"

    @staticmethod
    def as_term_list(*names):
        return [Term(name) for name in names]

    def print_constructor(self):
        return f"new Term(\"{self.get_type()}\")"


Term.eps = Term(Term.EPSILON)