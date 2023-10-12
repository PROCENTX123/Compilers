lex lexer.l
bison -d parser.y
gcc *.c
