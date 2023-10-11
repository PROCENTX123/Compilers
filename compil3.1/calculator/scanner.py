import re

from ..scanner.token import Token
from ..syntax.syntax import Term


class ArithmeticScanner:
    def __init__(self, filepath):
        self.regular_expressions = self.static_reg_expressions()
        self.filepath = filepath
        self.text = ""
        self.coord = None
        self.m = None
        self.log = ""

    @staticmethod
    def static_reg_expressions():
        exprs = {}
        exprs["n"] = r"[0-9]+"
        exprs["PLUS"] = r"\+"
        exprs["STAR"] = r"\*"
        exprs["OPENBRACE"] = r"\("
        exprs["CLOSEBRACE"] = r"\)"
        return exprs

    def return_token(self, type):
        last = self.coord
        self.coord = self.coord.shift(len(self.image))
        self.log += f"{type} {last}-{self.coord}: <{self.image}>\n"
        if re.match(r"[0-9]+", self.image):
            return Token(type, self.image, last, self.coord)
        return Token(self.image, self.image, last, self.coord)

    def next_token(self):
        if self.coord.pos >= len(self.text):
            return Token(Term.EOF, self.coord)
        if self.m.find():
            if self.m.start() != self.coord.pos:
                self.log += f"SYNTAX ERROR: {self.coord.pos}{self.coord}\n"
                print(f"SYNTAX ERROR: {self.coord.pos}{self.coord}")
                exit(-1)
            if self.image := self.m.group("BLANK"):
                self.coord = self.coord.shift(len(self.image))
                return self.next_token()
            if self.image := self.m.group("NEWLINE"):
                self.coord = self.coord.newline()
                self.coord = self.coord.shift(len(self.image) - 1)
                return self.next_token()
            for s in self.regular_expressions:
                if self.is_type(s):
                    return self.return_token(s)
            print("ERROR", self.coord, self.text[self.coord.pos:])
            return self.next_token()
        else:
            self.log += f"SYNTAX ERROR: {self.coord}\n"
            self.log += f"SYNTAX ERROR: {self.coord}\n"
            print(f"SYNTAX ERROR: {self.coord}")
            return Token(Term.EOF, self.coord)