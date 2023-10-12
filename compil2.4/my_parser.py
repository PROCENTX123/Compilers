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
                    raise ValueError(f"Expected TokenType.SEMI_COMMA, got {self.current_token().domain_name()}")
            else:
                raise ValueError(f"Expected TokenType.ASSIGN, got {self.current_token().domain_name()}")
        else:
            raise ValueError(f"Expected TokenType.NTERM, got {self.current_token().domain_name()}")
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
