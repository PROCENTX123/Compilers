```
Grammar -> NTermDecl "terminal" TERM TermList Rule RuleList "axiom" NTERM EOF
NTermDecl -> "non-terminal" NTERM NTermList | SEMI_COMA
NTermList -> COMMA NTERM NTermList | SEMI_COMA
TermList -> COMMA TERM TermList |  SEMI_COMA
Rule -> NTERM ASSIGN RightSideAlt RightSideAltListOpt
RuleList -> Rule RuleList | SEMI_COMA
RightSideAlt -> "epsilon" | ((NTERM | TERM) NTermOrTermListOpt).
NTermOrTermListOpt -> (NTERM | TERM) NTermOrTermListOpt | SEMI_COMA
RightSideAltListOpt -> ALTER RightSideAlt RightSideAltListOpt | SEMI_COMA
```

