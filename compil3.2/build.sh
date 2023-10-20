lex lexer.l
bison -d new_parce.y
gcc *.c
