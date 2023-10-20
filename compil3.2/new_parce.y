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

%token VAR BEGIN_F END ASSIGN SEMICOLON COLON COMMA RECORD
%token <identifier> IDENTIFIER
%token <number> NUMBER
%token <variable> OP

%{
int yylex(YYSTYPE *yylval_param, YYLTYPE *yylloc_param, yyscan_t scanner);
void yyerror(YYLTYPE *loc, yyscan_t scanner, long env[26], const char *message);
void printTab(int length, long* env){
    for (int i = 0; i < length; i++){
        printf("\t");
        env[2]+=4;
    }
}

void checkNewLine(long* env) {
    if (env[2] > env[1]) {
        printf("\n");
        env[2] = 0;
    }
}
%}

%%

Program:
    {printf("var\n");env[0]=1;env[2]=0;}
    VAR Declarations {env[0]--;}
    ;

Declarations:
    Declaration SEMICOLON {printf(";\n");env[2]=0;}  Declarations
    |
    ;

Declaration:
    {printTab(env[0],env);} IDENTIFIER {printf("%s", $IDENTIFIER);env[2]+=strlen($IDENTIFIER);}  Decl
    ;

Decl:
     COLON {printf(": ");env[2]+=2;checkNewLine(env);}  DeclName
    |  DeclVar  COLON IDENTIFIER {printf(": ");env[2]+=2;checkNewLine(env);
                                printf("%s", $IDENTIFIER);env[2]+=strlen($IDENTIFIER);checkNewLine(env);}
    ;
DeclName:
    RECORD {printf("record\n");env[2]=0;}  NamelessVarDeclaration  {printf("\n");printTab(env[0],env);} END {printf("end");env[2]=0;}
    |  IDENTIFIER {printf("%s", $IDENTIFIER);env[2]+=strlen($IDENTIFIER);checkNewLine(env);}
    ;
DeclVar:
      COMMA IDENTIFIER  DeclVar {printf(", ");env[2]+=2;checkNewLine(env);
                                printf("%s", $IDENTIFIER);env[2]+=strlen($IDENTIFIER);checkNewLine(env);}
    |  COMMA IDENTIFIER  {printf(", ");env[2]+=2;checkNewLine(env);
                                                       printf("%s", $IDENTIFIER);env[2]+=strlen($IDENTIFIER);checkNewLine(env);}
    ;

NamelessVarDeclaration:
     {env[0]+=1;} Declaration  VariableList {env[0]-=1;}
     ;

VariableList:
     {printf(",\n");env[2]=0;} COMMA Declaration VariableList
    |
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
