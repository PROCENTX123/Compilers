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

    # Grammar = NTermDecl "terminal" TERM TermList Rule RuleList EOF
    def ParseGrammar(self):
        node = {"name": "Grammar", "children": []}
        if self.tokens[self.tokens_idx].domain_name() == non-terminal:
            node["children"].append(self.ParseNtermDecl())
        if self.tokens[]
        while self.current_token_tag() != TokenType.EOF:
            node["children"].append(self.ParseDeclaration())
        return node

    # Declaration = AxiomDecl | NtermsDecl | TermsDecl | RuleDecl.
    def ParseDeclaration(self):
        node = {"name": "Grammar", "children": []}
        if self.tokens[self.tokens_idx].domain_name() == "$NTERM":
            node["children"].append(self.ParseNtermsDecl())
        elif self.tokens[self.tokens_idx].domain_name() == "$TERM":
            node["children"].append(self.ParseTermsDecl())
        elif self.tokens[self.tokens_idx].domain_name() == "$RULE":
            node["children"].append(self.ParseRuleDecl())
        else:
            raise ValueError(f"Unexpected token {self.tokens[self.tokens_idx]}")
        return node

    # NtermsDecl = "$NTERM" NTERM {NTERM}.
    def ParseNtermsDecl(self):
        node = {"name": "NtermsDecl", "children": []}
        tok = self.next_token()
        if tok.tag == TokenType.NTERM:
            self.nterms.append(tok.value)
            node["children"].append(tok)
            tok = self.next_token()
            while tok.tag == TokenType.NTERM:
                self.nterms.append(tok.value)
                node["children"].append(tok)
                tok = self.next_token()
        else:
            raise ValueError(f"Expected TokenType.NTERM, got {tok.domain_name()}")
        return node

    # TermsDecl = "$TERM" TERM {TERM}.
    def ParseTermsDecl(self):
        node = {"name": "TermsDecl", "children": []}
        tok = self.next_token()
        if tok.tag == TokenType.TERM:
            self.terms.append(tok.value)
            node["children"].append(tok)
            tok = self.next_token()
            while tok.tag == TokenType.TERM:
                self.terms.append(tok.value)
                node["children"].append(tok)
                tok = self.next_token()
        else:
            raise ValueError(f"Expected TokenType.NTERM, got {tok.domain_name()}")
        return node

    # RuleDecl = "$RULE" NTERM ASSIGN Expr.
    def ParseRuleDecl(self):
        node = {"name": "RuleDecl", "children": []}
        self.next_token()
        if self.current_token().tag == TokenType.NTERM:
            left = self.current_token().value
            node["children"].append(self.current_token())
            self.next_token()
            if self.current_token().tag == TokenType.ASSIGN:
                node["children"].append(self.current_token())
                self.next_token()
                right = self.ParseExpr()
                node["children"].append(right)
                self.rules[left] = right
            else:
                raise ValueError(f"Expected TokenType.ASSIGN, got {self.current_token().domain_name()}")
        else:
            raise ValueError(f"Expected TokenType.NTERM, got {self.current_token().domain_name()}")
        return node

    # Expr = Altern {ALTERN Altern}.
    def ParseExpr(self):
        node = {"name": "Expr", "children": []}
        node["children"].append(self.ParseAltern())
        while self.current_token_tag() == TokenType.ALTERN:
            node["children"].append(self.current_token())
            self.next_token()
            node["children"].append(self.ParseAltern())
        return node

    #Altern = Concat {Concat}.
    def ParseAltern(self):
        node = {"name": "Altern", "children": []}
        node["children"].append(self.ParseConcat())
        while self.current_token_tag() == TokenType.NTERM or self.current_token_tag() == TokenType.TERM or \
        self.current_token_tag() == TokenType.LEFTPAREN or self.current_token_tag() == TokenType.LEFTFPAREN:
            node["children"].append(self.ParseConcat())
        return node

    # Concat = NTERM | TERM | Grouping | Option.
    def ParseConcat(self):
        node = {"name": "Concat", "children": []}
        if self.current_token_tag() == TokenType.NTERM or self.current_token_tag() == TokenType.TERM:
            node["children"].append(self.current_token())
            self.next_token()
        elif self.current_token_tag() == TokenType.LEFTPAREN:
            node["children"].append(self.ParseGrouping())
        elif self.current_token_tag() == TokenType.LEFTFPAREN:
            node["children"].append(self.ParseOption())
        else:
            raise ValueError(f"Unexpected token {self.tokens[self.tokens_idx]}")
        return node

    # Grouping =  LPAREN Expr RPAREN.
    def ParseGrouping(self):
        node = {"name": "Grouping", "children": []}
        if self.current_token_tag() == TokenType.LEFTPAREN:
            node["children"].append(self.current_token())
            self.next_token()
            node["children"].append(self.ParseExpr())
            if self.current_token_tag() == TokenType.RIGHTPAREN:
                node["children"].append(self.current_token())
                self.next_token()
            else:
                raise ValueError(f"Expected TokenType.RIGHTPAREN, got {self.current_token().domain_name()}")
        else:
            raise ValueError(f"Expected TokenType.LEFTPAREN, got {self.current_token().domain_name()}")
        return node

    # Option = LPAREN_CURVE Expr RPAREN_CURVE.
    def ParseOption(self):
        node = {"name": "Option", "children": []}
        if self.current_token_tag() == TokenType.LEFTFPAREN:
            node["children"].append(self.current_token())
            self.next_token()
            node["children"].append(self.ParseExpr())
            if self.current_token_tag() == TokenType.RIGHTFPAREN:
                node["children"].append(self.current_token())
                self.next_token()
            else:
                raise ValueError(f"Expected TokenType.RIGHTFPAREN, got{self.current_token().domain_name()}")
        else:
            raise ValueError(f"Expected TokenType.LEFTFPAREN, got {self.current_token().domain_name()}")
        return node

    def first(self):
        self.__first = {key: {} for key in self.nterms}
        changed = True
        while changed:
            changed = False
            for left, right in self.rules.items():
                firstExpr = self.__getFirstExpr(right)
                if self.__first[left] != firstExpr:
                    changed = True
                    self.__first[left] = firstExpr
        return {key: [v for v in value.keys()] for key, value in self.__first.items()}

    def __getFirstExpr(self, exprTree):
        firstList = {}
        for child in exprTree["children"]:
            firstList.update(self.__getFirstAltern(child))
        return firstList

    def __getFirstAltern(self, alternTree, idx=0):
        if not isinstance(alternTree, dict): return {}
        if not alternTree.get("children", None): return {}
        if idx >= len(alternTree["children"]): return {}
        firstConcat = self.__getFirstConcat(alternTree["children"][idx])
        otherConcat = self.__getFirstAltern(alternTree, idx + 1)
        if not otherConcat or len(otherConcat.items()) == 0: return firstConcat
        if TokenType.EPS in [token.tag for token in firstConcat.keys()]:
            buffer = {key: value for key, value in firstConcat.items() if key.tag != TokenType.EPS}
            buffer.update(otherConcat)
            return buffer
        return firstConcat

    def __getFirstConcat(self, concatTree):
        if isinstance(concatTree["children"][0], dict):
            if concatTree["children"][0]["name"] == "Option":
                f = self.__getFirstExpr(concatTree["children"][0]["children"][1])
                if TokenType.EPS not in [token.tag for token in f.keys()]:
                    f.update({Token(TokenType.EPS, "$EPS"): True})
                return f
            elif concatTree["children"][0]["name"] == "Grouping":
                return self.__getFirstExpr(concatTree["children"][0]["children"][1])
        elif concatTree["children"][0].tag == TokenType.TERM:
            return {concatTree["children"][0]: True}
        elif concatTree["children"][0].tag == TokenType.NTERM:
            return self.__first[concatTree["children"][0].value]
        elif concatTree["children"][0].tag == TokenType.LEFTPAREN or \
                concatTree["children"][0].tag == TokenType.LEFTFPAREN:
            return self.__getFirstExpr(concatTree["children"][1])
