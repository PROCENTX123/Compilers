% "Лабораторная работа 3.2 «Форматтер исходных текстов»"
% 13 октября 2023 г.
% Григорьев Роман, ИУ9-62Б

# Цель работы
Целью данной работы является приобретение навыков использования генератора 
синтаксических анализаторов bison.

# Индивидуальный вариант
Сильный форматтер, var-блок языка Pascal (включая безымянные записи).

# Реализация

```
%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "lexer.h"
%}

%define api.pure
%locations
%lex-param {yyscan_t scanner}
%parse-param {yyscan_t scanner}
%parse-param {long env[26]}

%union {
    char* identifier;
    char variable;
    long number;
}

%token VAR BEGIN_F END ASSIGN SEMICOLON COLON LBRACKET RBRACKET COMMA POINT
%token <identifier> IDENTIFIER
%token <number> NUMBER
%token <variable> OP

%{
int yylex(YYSTYPE *yylval_param, YYLTYPE *yylloc_param, yyscan_t scanner);
void yyerror(YYLTYPE *loc, yyscan_t scanner, long env[26], const char *message);
void printTab(int length, long* env){
    for (int i = 0; i < length; i++){
        printf("    ");
        env[2]+=4;
    }
}

void checkNewLine(long* env) {
    if (env[2] > env[1]) {
        printf("\n");
        env[2] = 0;
    }
}
int getLongLen(long number) {
    char buffer[20];
    int length = snprintf(buffer, sizeof(buffer), "%ld", number);
    return length;
}
%}

%%

program:
    statement_list_begin
    ;

statement_list_begin:
    statement_begin
    | statement_list_begin statement_begin
    ;

statement_list:
    statement
    | statement_list statement
    ;

statement:
    appropriation
    ;

appropriation:
    IDENTIFIER ASSIGN
    {printTab(env[0], env); printf("%s", $1);env[2]+=strlen($1);
    checkNewLine(env);printf(" := ");env[2]+=4;checkNewLine(env);}
    expr SEMICOLON
    {printf(";\n");env[2]=0;}
    ;

expr:
    value
    | value OP {printf("%c", $OP);env[2]+=getLongLen($OP);checkNewLine(env);} expr
    ;

value:
    IDENTIFIER  {printf("%s", $IDENTIFIER);env[2]+=strlen($IDENTIFIER);checkNewLine(env);}
    |NUMBER  {printf("%ld", $NUMBER);env[2]+=getLongLen($NUMBER);checkNewLine(env);}
    | LBRACKET  {printf("\(");env[2]+=1;checkNewLine(env);}
                expr RBRACKET
                {printf("\)");env[2]+=1;checkNewLine(env);}
    ;

statement_begin:
    variable_declaration
    | compound_statement_begin
    ;

variable_declaration:
    {printf("var\n");env[0]++;env[2]=0;}
    VAR variable_list {env[0]--;}
    ;

variable_list:
    variable_declaration_line SEMICOLON  {printf(";\n");env[2]=0;}
    | variable_list  variable_declaration_line SEMICOLON  {printf(";\n");env[2]=0;}
    ;

variable_declaration_line:
    {printTab(env[0],env);} variables COLON IDENTIFIER {printf(": ");
    env[2]+=2;checkNewLine(env);printf("%s", $IDENTIFIER);
    env[2]+=strlen($IDENTIFIER);checkNewLine(env);}
    ;

variables:
    IDENTIFIER {printf("%s", $IDENTIFIER);env[2]+=strlen($IDENTIFIER);checkNewLine(env);}
    | variables COMMA IDENTIFIER {printf(", ");env[2]+=2;checkNewLine(env);
    printf("%s", $IDENTIFIER);env[2]+=strlen($IDENTIFIER);checkNewLine(env);}
    ;

compound_statement_begin:
    {printf("begin\n");env[0]++;env[2]=0;}
    BEGIN_F statement_list END POINT {env[0]--;printf("end.\n");env[2]=0;}
    ;
%%

int main(int argc, char *argv[])
{
	yyscan_t scanner;
	struct Extra extra;
	long env[26];
    env[0] = 0;
    char * buffer = 0;
    long length;
    FILE * f = fopen("input.txt", "rb");

	init_scanner(f, &scanner, &extra);
	yyparse(scanner, env);
	destroy_scanner(scanner);
    free(buffer);
	return 0;
}

```

# Тестирование

Входные данные

```
var i:integer;a,b,c:string;begin a:='a';b:='b';age:=30;end.
```

Вывод на `stdout`

```
var
    i: integer;
    a, b, c: string;
begin
    a := a;
    b := b;
    age := 30;
end.

```

# Вывод
В ходе выполнения данной лабораторной работы я освоил и приобрел опыт
в работе с генератором синтаксических анализаторов Bison. Я также изучил
и овладел методами совместного использования инструментов Flex и Bison
для создания синтаксического анализатора на языке программирования C++.
