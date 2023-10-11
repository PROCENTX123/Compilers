import os
import re

from ..scanner.coords import Coords
from ..scanner.token import Token
from ..syntax.syntax import Term


class Scanner:
    NEWLINE = "newline"
    BLANK = "blank"
    newline_expr = r'\R'
    blank_expr = r'[ \t]+'

    def __init__(self, filepath, termsexpr):
        with open(filepath, 'r') as file:
            self.text = file.read()
        self.regexp = termsexpr
        pattern = self.set_pattern()
        self.p = re.compile(pattern, re.DOTALL)
        self.m = self.p.finditer(self.text)
        self.coord = Coords(1, 1, 0)
        self.image = ''
        self.log = []

    @staticmethod
    def make_group(name, expr):
        return f"(?<{name}>({expr}))"

    def set_pattern(self):
        res = (
            self.make_group(self.BLANK, self.blank_expr) + "|"
            + self.make_group(self.NEWLINE, self.newline_expr)
        )
        for name, expr in self.regexp.items():
            res += "|" + self.make_group(name, expr)
        return res

    def is_type(self, type):
        return self.image.group(type) is not None

    def get_text(self):
        return self.text

    def return_token(self, type):
        last = self.coord
        self.coord = self.coord.shift(len(self.image))
        log_entry = f"{type} {last}-{self.coord}: <{self.image}>\n"
        self.log.append(log_entry)
        return Token(type, self.image, last, self.coord)

    def next_token(self):
        if self.coord.pos >= len(self.text):
            return Token(Term.EOF, self.coord)

        if self.m:
            match = next(self.m, None)
            if match and match.start() != self.coord.pos:
                log_entry = f"SYNTAX ERROR: {self.coord}\n"
                self.log.append(log_entry)
                print(f"SYNTAX ERROR: {self.coord}")
                os.sys.exit(-1)

            if match:
                image = match.group(self.BLANK)
                if image:
                    self.coord = self.coord.shift(len(image))
                    return self.next_token()

                image = match.group(self.NEWLINE)
                if image:
                    self.coord = self.coord.newline()
                    self.coord = self.coord.shift(len(image) - 1)
                    return self.next_token()

                for name, expr in self.regexp.items():
                    if self.is_type(name):
                        return self.return_token(name)

                print(f"ERROR {self.coord} {self.text[self.coord.pos:]}")
                return self.next_token()

        log_entry = f"SYNTAX ERROR: {self.coord}\n"
        self.log.append(log_entry)
        print(f"SYNTAX ERROR: {self.coord}")
        return Token(Term.EOF, self.coord)