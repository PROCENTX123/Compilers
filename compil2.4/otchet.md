% Лабораторная работа № 2.4 «Множества FIRST для РБНФ»
% 13 октября 2023 г.
% Григорьев Роман, ИУ9-62Б

# Цель работы
Целью данной работы является изучение алгоритма построения множеств FIRST для расширенной формы 
Бэкуса-Наура.

# Индивидуальный вариант
```
# объявления тоже надо проверять
non-terminal E, T, F;
terminal '+', '-', '*', '/',
  '(', ')', n;

E ::= T ( ('+' | '-') T )*;
T ::= F ( ('*' | '/') F )*;
F ::= n | '-' F | '(' E ')';
```

# Реализация

## Неформальное описание синтаксиса входного языка
Язык представления правил грамматики, декларация нетерминалов начинается со слова non-terminal,
терминалы со слова terminal. Списки терминалов, как и списки нетерминалов
внутри себя разделяются запятыми. 
нетерминалы могут группироватся в скобках, нетерминалы записаны с большой буквы,
итерация клини обозначается замыкающимися круглыми скобками со звездой на конце.

## Лексическая структура
```
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
```

## Грамматика языка
```
Grammar -> {NTermDecl | TermDecl | RuleDecl} EOF
NTermDecl -> "non-terminal" NTERM NTermList
TermDecl -> "terminal" TERM TermList
NTermList -> COMMA NTERM NTermList | SEMI_COMMA
TermList -> COMMA TERM TermList | SEMI_COMMA
RuleDecl -> NTERM ASSIGN expr SEMI_COMMA
expr -> Alter {ALTER Alter}
Alter -> Concat {Concat}
Concat -> NTERM | TERM | Grouping
Grouping -> LPAREN Expr RPAREN
Star -> Grouping*
```

## Программная реализация

lexer.py
``` python
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
    SEMI_COMMA = auto()
    EPS = auto()


@dataclass(frozen=True)
class Token:
    tag: TokenType
    value: str = ""

    def domain_name(self):
        if self.tag == TokenType.KW:
            return self.value
        else:
            return self.tag.name

@dataclass(frozen=True)
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
                tokens.append(Coords(token.tag, ";", line_index,
                 inline_index, inline_index + len(token.value) - 1))
                line_index += 1
                inline_index = 1
                raw_index += 1
            elif token.tag != TokenType.UNMATCHED:
                tokens.append(
                    Coords(token.tag, token.value, line_index,
                     inline_index, inline_index + len(token.value) - 1))
                inline_index += len(token.value)
                raw_index += len(token.value)

        tokens.append(Coords(TokenType.EOF, "", line_index, inline_index, inline_index))
        return tokens

```

my_parser.py
``` python
from lexer import TokenType, Token

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.tokens_idx = 0
        self.tree = {}
        self.rules = {}
        self.nterms = []
        self.terms = []
        pass

    def current_token_tag(self):
        return self.tokens[self.tokens_idx].tag

    def current_token(self):
        return self.tokens[self.tokens_idx]

    def next_token(self):
        self.tokens_idx += 1
        return self.tokens[self.tokens_idx]

    # Grammar = {NTermDecl | TermDecl | RuleDecl} EOF
    def ParseGrammar(self):
        node = {"name": "Grammar", "children": []}
        while self.current_token_tag() != TokenType.EOF:
            if self.tokens[self.tokens_idx].domain_name() == "non-terminal":
                node["children"].append(self.ParseNtermsDecl())
            elif self.tokens[self.tokens_idx].domain_name() == "terminal":
                node["children"].append(self.ParseTermsDecl())
            elif self.current_token_tag() == TokenType.NTERM:
                node["children"].append(self.ParseRuleDecl())
            else:
                raise ValueError(f"Unexpected token {self.tokens[self.tokens_idx]}")
        return node


    # NtermsDecl = "non-terminal" NTERM NTermList.
    def ParseNtermsDecl(self):
        node = {"name": "NtermsDecl", "children": []}
        tok = self.next_token()
        if tok.tag == TokenType.NTERM:
            self.nterms.append(tok.value)
            node["children"].append(tok)
            node["children"].append(self.ParseNtermList())
        else:
            raise ValueError(f"Expected TokenType.NTERM, got {tok.domain_name()}")
        return node

    # NTermList -> COMMA NTERM NTermList | SEMI_COMMA
    def ParseNtermList(self):
        node = {"name": "NtermList", "children": []}
        tok = self.next_token()
        if tok.tag == TokenType.SEMI_COMMA:
            self.next_token()
        elif tok.tag == TokenType.COMMA:
            tok = self.next_token()
            self.nterms.append(tok.value)
            node["children"].append(tok)
            node["children"].append(self.ParseNtermList())
        else:
            raise ValueError(f"Expected TokenType.COMMA, got {tok.domain_name()}")
        return node

    #TermDecl -> "terminal" TERM TermList
    def ParseTermsDecl(self):
        node = {"name": "TermsDecl", "children": []}
        tok = self.next_token()
        if tok.tag == TokenType.TERM:
            self.terms.append(tok.value)
            node["children"].append(tok)
            node["children"].append(self.ParseTermList())
        else:
            raise ValueError(f"Expected TokenType.TERM, got {tok.domain_name()}")
        return node

    # TermList -> COMMA TERM TermList | SEMI_COMMA
    def ParseTermList(self):
        node = {"name": "TermList", "children": []}
        self.next_token()
        if self.current_token_tag() == TokenType.SEMI_COMMA:
            self.next_token()
        elif self.current_token_tag() == TokenType.COMMA:
            tok = self.next_token()
            self.terms.append(tok.value)
            node["children"].append(tok)
            node["children"].append(self.ParseTermList())
        else:
            raise ValueError(f"Expected TokenType.COMMA, got {self.current_token().domain_name()}")
        return node

    #RuleDecl -> NTERM ASSIGN expr SEMI_COMMA
    def ParseRuleDecl(self):
        node = {"name": "RuleDecl", "children": []}
        if self.current_token_tag() == TokenType.NTERM:
            left = self.current_token().value
            node["children"].append(self.current_token())
            self.next_token()
            if self.current_token_tag() == TokenType.ASSIGN:
                node["children"].append(self.current_token())
                self.next_token()
                right = self.ParseExpr()
                node["children"].append(right)
                self.rules[left] = right
                if self.current_token_tag() == TokenType.SEMI_COMMA:
                    self.next_token()
                else:
                    raise ValueError(f"Expected TokenType.SEMI_COMMA,
                     got {self.current_token().domain_name()}")
            else:
                raise ValueError(f"Expected TokenType.ASSIGN,
                 got {self.current_token().domain_name()}")
        else:
            raise ValueError(f"Expected TokenType.NTERM,
             got {self.current_token().domain_name()}")
        return node

    #expr -> Alter {ALTER Alter}
    def ParseExpr(self):
        node = {"name": "Expr", "children": []}
        node["children"].append(self.ParseAlter())
        while self.current_token_tag() == TokenType.ALTER:
            node["children"].append(self.current_token())
            self.next_token()
            node["children"].append(self.ParseAlter())
        return node

    #Altern -> Concat {Concat}
    def ParseAlter(self):
        node = {"name": "Alter", "children": []}
        node["children"].append(self.ParseConcat())
        while self.current_token_tag() in (TokenType.NTERM, TokenType.TERM, TokenType.LPAREN):
            node["children"].append(self.ParseConcat())
        return node

    # Concat -> NTERM | TERM | Grouping
    def ParseConcat(self):
        node = {"name": "Concat", "children": []}
        if self.current_token_tag() == TokenType.NTERM or self.current_token_tag() == TokenType.TERM:
            node["children"].append(self.current_token())
            self.next_token()
        elif self.current_token_tag() == TokenType.LPAREN:
            node["children"].append(self.ParseGrouping())
        else:
            raise ValueError(f"Unexpected token {self.tokens[self.tokens_idx]}")
        return node

    #Grouping -> LPAREN Expr RPAREN
    def ParseGrouping(self):
        node = {"name": "Grouping", "children": []}
        if self.current_token_tag() == TokenType.LPAREN:
            node["children"].append(self.current_token())
            self.next_token()
            node["children"].append(self.ParseExpr())
            if self.current_token_tag() == TokenType.RPAREN:
                node["children"].append(self.current_token())
                self.next_token()
                node["children"].append(self.ParseStar())
                self.next_token()
            else:
                raise ValueError(f"Expected TokenType.RPAREN, got {self.current_token().domain_name()}")
        else:
            raise ValueError(f"Expected TokenType.LPAREN, got {self.current_token().domain_name()}")
        return node

    #Star -> Grouping*
    def ParseStar(self):
        node = {"name": "Star", "children": []}
        if self.current_token_tag() == TokenType.STAR:
            node["children"].append(self.current_token())
        return node


    def calculate_first_set(self):
        self.__first = {key: {} for key in self.nterms}
        changed = True

        while changed:
            changed = False

            for left, right in self.rules.items():
                first_expr = self.__get_first_expr(right)

                if self.__first[left] != first_expr:
                    changed = True
                    self.__first[left] = first_expr

        return {key: list(value.keys()) for key, value in self.__first.items()}

    def __get_first_expr(self, expr_tree):
        first_list = {}
        for child in expr_tree.get("children", []):
            first_list.update(self.__get_first_altern(child))
        return first_list

    def __get_first_altern(self, altern_tree, idx=0):
        if not isinstance(altern_tree, dict) or not altern_tree.get("children", None):
            return {}

        if idx >= len(altern_tree["children"]):
            return {}

        first_concat = self.__get_first_concat(altern_tree["children"][idx])
        other_concat = self.__get_first_altern(altern_tree, idx + 1)

        if not other_concat or len(other_concat.items()) == 0:
            return first_concat

        if TokenType.EPS in [token.tag for token in first_concat.keys()]:
            buffer = {key: value for key, value in first_concat.items() if key.tag != TokenType.EPS}
            buffer.update(other_concat)
            return buffer

        return first_concat

    def __get_first_concat(self, concat_tree):
        first_token = concat_tree["children"][0]

        if isinstance(first_token, dict):
            if first_token["name"] == "Star":
                first_expr = self.__get_first_expr(first_token["children"][1])
                if TokenType.EPS not in [token.tag for token in first_expr.keys()]:
                    first_expr[Token(TokenType.EPS, "epsilon")] = True
                return first_expr
            elif first_token["name"] == "Grouping":
                return self.__get_first_expr(first_token["children"][1])
        elif first_token.tag == TokenType.TERM:
            return {first_token: True}
        elif first_token.tag == TokenType.NTERM:
            return self.__first[first_token.value]
        elif first_token.tag == TokenType.LPAREN:
            return self.__get_first_expr(concat_tree["children"][1])
```

main.py
``` python
from lexer import Lexer
from my_parser import Parser


if __name__ == "__main__":
    lexer = Lexer()
    tokens = lexer.tokenization(open('input.txt', 'rt').read())
    for tok in tokens:
        print(tok)
    parser = Parser(tokens)
    parser.ParseGrammar()
    firsts = parser.calculate_first_set()
    for nterm, first in firsts.items():
        print(f'{nterm} - FIRST: {first}')
```

# Тестирование

Входные данные

```
# объявления тоже надо проверять
non-terminal E, T, F;
terminal '+', '-', '*', '/',
'(', ')', n;

E ::= T ( ('+' | '-') T )*;
T ::= F ( ('*' | '/') F )*;
F ::= n | '-' F | '(' E ')';

```

Вывод на `stdout`

```
E - FIRST: [TERM (6,8) - (6, 8): n, TERM (6,12) - (6, 14): '-', TERM (6,20) - (6, 22): '(']
T - FIRST: [TERM (6,8) - (6, 8): n, TERM (6,12) - (6, 14): '-', TERM (6,20) - (6, 22): '(']
F - FIRST: [TERM (6,8) - (6, 8): n, TERM (6,12) - (6, 14): '-', TERM (6,20) - (6, 22): '(']
```

# Вывод
В ходе данной лабораторной работы я ознакомился с методами формирования наборов FIRST
для РБНФ и успешно реализовал этот процесс для конкретного типа РБНФ,
указанного в моем индивидуальном варианте.
