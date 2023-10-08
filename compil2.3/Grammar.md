```
Grammar -> NTermDecl "terminal" TERM TermList Rule RuleList "axiom" NTERM EOF
NTermDecl -> "non-terminal" NTERM NTermList | SEMI_COMA NL
NTermList -> COMMA NTERM NTermList | SEMI_COMA NL
TermList -> COMMA TERM TermList |  SEMI_COMA NL
RuleList -> Rule RuleList | SEMI_COMA
Rule -> NTERM ASSIGN RightSideAlt RightSideAltListOpt
RightSideAlt -> "epsilon" | ((NTERM | TERM) NTermOrTermListOpt).
NTermOrTermListOpt -> (NTERM | TERM) NTermOrTermListOpt | SEMI_COMA NL
RightSideAltListOpt -> ALTER RightSideAlt RightSideAltListOpt | SEMI_COMA NL
```

