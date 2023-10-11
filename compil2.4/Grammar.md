# объявления тоже надо проверять
non-terminal E, T, F;
terminal '+', '-', '*', '/',
'(', ')', n;
E ::= T ( ('+' | '-') T )*;
T ::= F ( ('*' | '/') F )*;
F ::= n | '-' F | '(' E ')';

```
Grammar -> NTermDecl TermDecl {RuleDecl} EOF
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
