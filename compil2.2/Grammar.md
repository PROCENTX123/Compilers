```
Program -> FuncDecl Program | COMMENT Program | eps
FuncDecl -> FUNCNAME Type DOUBLECOLON Type IS Pattern PatternList END
Type -> TYPENAME | LBRACKET Type TypeList RBRACKET | '*' Type
TypeList -> COMMA Type TypeList| eps
Pattern -> LCons ASSIGN Expr SEMI_COMMA
PatternList -> PatternList Pattern | eps
LCons -> LVal | LCons COLON LVal
LVal -> VARNAME | INT | LBRACKET LCons ListLVal RBRACKET | LFBRACKET LCons ListLVal RFBRACKET | LFBRACKET RFBRACKET 
ListLVal -> COMMA LCons ListLVal | eps
Expr -> Cons | Expr ExprOps
ExprOps -> Op Cons | ExprOps Op Cons
Op -> '+' | '-' | '*' | '/'
Cons -> Val | Cons COLON Val
Val -> FUNCNAME Val | VARNAME | INT | LSQUAREBRACKET Expr RSQUAREBRACKET | LBRACKET Cons ListVal RBRACKET | LFBRACKET Cons ListVal RFBRACKET | LFBRACET RFBRACET
ListVal -> COMMA Cons ListVal | eps
```