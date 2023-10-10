import re
from enum import Enum, auto
from dataclasses import dataclass

configuration = {
    "term": "\'[^']*\'|[a-z]",
    "nterm": "([A-Z\d]+)",
    "comment": "\\#.*\\n",
    "ws": "\\s+",
    "keywords": "(axiom|terminal|non-terminal|epsilon)",
    "assign": "\\::=",
    "alt": "\\|",
    "comma": "\\,",
    "lparen": "\\(",
    "rparen": "\\)",
    "star": "\\*",
    "semi-comma": "\\;"
}

class TokenType(Enum):
    KW = auto()
    ALTER = auto()
    TERM = auto()
    NTERM = auto()
    ASSIGN = auto()
    COMMENT = auto()
    LPAREN = auto()
    RPAREN = auto()
    STAR = auto()
    EOF = auto()
    UNMATCHED = auto()
    COMMA = auto()
    SEMI_COMMA = auto


@dataclass
class Token:
    tag: TokenType
    value: str = ""

    def domain_name(self):
        if self.tag == TokenType.KW:
            return self.value
        else:
            return self.tag.name

@dataclass
class Coords(Token):
    line: int = 0
    start: int = 0
    end: int = 0

    def __repr__(self) -> str:
        if self.tag == TokenType.KW:
            return f"{self.value} ({self.line},{self.start}) - ({self.line}, {self.end})"
        return f"{self.tag.name} ({self.line},{self.start}) - ({self.line}, {self.end}): {self.value}"

class Lexer:
    def __init__(self):
        self.tokens = {
            TokenType.TERM: configuration["term"],
            TokenType.NTERM: configuration["nterm"],
            TokenType.COMMENT: configuration["comment"],
            TokenType.KW: configuration["keywords"],
            TokenType.ASSIGN: configuration["assign"],
            TokenType.ALTER: configuration["alt"],
            TokenType.COMMA: configuration["comma"],
            TokenType.SEMI_COMMA: configuration["semi-comma"],
            TokenType.LPAREN: configuration["lparen"],
            TokenType.RPAREN: configuration["rparen"],
            TokenType.STAR: configuration["star"]
        }
        self.tokens_compiled = {k: re.compile(v) for k, v in self.tokens.items()}
        self.pattern = re.compile('(' + ')|('.join(self.tokens.values()) + ')')

    def match_token(self, input_txt: str) -> Token:
        match = self.pattern.match(input_txt)
        if not match:
            return Token(TokenType.UNMATCHED, input_txt[0])
        max_token_type, max_end_ind = self.find_max_match(input_txt)
        return Token(max_token_type, input_txt[:max_end_ind])

    def find_max_match(self, input_txt: str):
        max_token_type, max_end_ind = None, 0
        for token_type, regex in self.tokens_compiled.items():
            submatch = regex.match(input_txt)
            if submatch and submatch.span()[1] >= max_end_ind:
                max_end_ind = submatch.span()[1]
                max_token_type = token_type
        return max_token_type, max_end_ind

    def tokenization(self, input_txt: str) -> list:
        tokens = []
        raw_index = 0
        line_index = 1
        inline_index = 1

        while raw_index < len(input_txt):
            token = self.match_token(input_txt[raw_index:])

            if token.tag == TokenType.UNMATCHED:
                if token.value.isspace():
                    raw_index += len(token.value)
                    inline_index += len(token.value)
                else:
                    print('syntax error:', (line_index, inline_index))
                    raw_index += 1
                    inline_index += 1
            elif token.tag == TokenType.COMMENT:
                line_index += 1
                inline_index = 1
                raw_index += len(token.value)
            elif token.tag == TokenType.SEMI_COMMA:
                tokens.append(Coords(token.tag, ";", line_index, inline_index, inline_index + len(token.value) - 1))
                line_index += 1
                inline_index = 1
                raw_index += 1
            elif token.tag != TokenType.UNMATCHED:
                tokens.append(
                    Coords(token.tag, token.value, line_index, inline_index, inline_index + len(token.value) - 1))
                inline_index += len(token.value)
                raw_index += len(token.value)

        tokens.append(Coords(TokenType.EOF, "", line_index, inline_index, inline_index))
        return tokens


if __name__ == "__main__":
    lexer = Lexer()
    tokens = lexer.tokenization(open('input.txt', 'rt').read())
    for token in tokens:
        print(token)
