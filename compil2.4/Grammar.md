# объявления тоже надо проверять
non-terminal E, T, F;
terminal '+', '-', '*', '/',
'(', ')', n;
E ::= T ( ('+' | '-') T )*;
T ::= F ( ('*' | '/') F )*;
F ::= n | '-' F | '(' E ')';

```
Grammar -> NTermDecl "terminal" TERM TermList Rule RuleList EOF
NTermDecl -> "non-terminal" NTERM NTermList | SEMI_COMA
NTermList -> COMMA NTERM NTermList | SEMI_COMMA
TermList -> COMMA TERM TermList | SEMI_COMMA
Rule -> NTERM ASSIGN expr
RuleList -> Rule RuleList | SEMI_COMMA
expr -> Altern {ALTERN Altern}
Altern -> Concat {Concat}
Concat -> NTERM | TERM | Grouping | Star
Grouping -> LPAREN Expr RPAREN
Star -> Grouping*
```
