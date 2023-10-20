```
Program -> Element | Program Element
Element -> COMMENT | Define 
Define -> FUNCNAME Type DOUBLECOLON Type IS Patterns END
Type -> TYPENAME | '(' Types ')' | '*' Type
Types -> Type | Types ',' Type
Patterns -> Pattern | Patterns ';' Pattern
Pattern -> LCons '=' Expr
LCons -> LVal | LCons ':' LVal
LVal -> VARNAME | INT | '(' LVals ')' | '{' LVals '}' | '{' '}'
LVals -> LCons | LVals ',' LCons
Expr -> ExprElement | Expr ExprOps
ExprOps -> ExprOp | ExprOps ExprOp
ExprOp -> ArythOp ExprElement
ExprElement -> Cons | ExprElement MulOp ExprElement
ArythOp -> '+' | '-'
MulOp -> '*' | '/'
Cons -> Val | Cons ':' Val
Val -> FUNCNAME Val | VARNAME | INT | '[' Expr ']' | '(' Vals ')' | '{' Vals '}' | '{' '}'
Vals -> Cons | Vals ',' Cons 
```
