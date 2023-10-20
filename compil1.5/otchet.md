% Лабораторная работа № 1.5 «Порождение лексического анализатора с помощью flex»
% 13 октября 2023 г.
% Григорьев Роман, ИУ9-62Б

# Цель работы
Целью данной работы является изучение генератора лексических анализаторов flex.

# Индивидуальный вариант
Идентификаторы переменных: последовательности буквенных символов
ASCII и цифр, начинающиеся на знаки «$», «@», «%».
Имена функций: последовательности буквенных символов ASCII и цифр, начинающиеся на букву.
Ключевые слова «sub», «if», «unless».


# Реализация

```lex
%option noyywrap bison-bridge bison-locations
%{

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TAG_IDENTIFIER 1
#define TAG_DEFINE 2
#define TAG_ERROR 3
#define WORD 4

const char *tag_names [] = {
    "EOF", "IDENTIFIER", "DEFINE", "ERROR", "KEY_WORD"
};

struct Position{
    int line, pos, index;
};

void print_pos(struct Position *p){
    printf("(%d,%d)", p->line, p->pos);
};

struct Fragment {
    struct Position starting, following;
};

typedef struct Fragment YYLTYPE;

void print_frag(struct Fragment *f){
    print_pos(&(f->starting));
    printf("-");
    print_pos(&(f->following));
};

union Token{
    int char *ident;
    const char *word;
};

typedef union Token YYSTYPE;

int continued;
struct Position cur;

# define YY_USER_ACTION                 \
{                                       \
    int i;                              \
    if (!continued)                     \
        yylloc->starting = cur;         \
    continued = 0;                      \
    for (i = 0; i < yyleng; i++) {      \
        if ('\n' == yytext[i]) {        \
            cur.line++;                 \
            cur.pos = 1;                \
        }                               \
        else                            \
            cur.pos++;                  \
        cur.index++;                    \
    }                                   \
    yylloc->following = cur;            \
}                                       \

struct IdentifierTable {
    int current_num;
    char *container[100];
};

typedef struct IdentifierTable IdentifierTable;

void initialize(IdentifierTable *table) {
    table->current_num = 0;
    for (int i = 0; i < 100; i++) {
        table->container[i] = NULL;
    }
}

int add(IdentifierTable *table, char *value) {
    for (int i = 0; i < table->current_num; i++) {
        if (strcmp(table->container[i], value) == 0) {
            return i;
        }
    }

    if (table->current_num < 100) {
        table->container[table->current_num] = strdup(value);
        return table->current_num++;
    }

    return -1;  // Table is full
}

void init_scanner(const char *path) {
    continued = 0;
    cur.line = 1;
    cur.pos = 1;
    cur.index = 0;
    yyin = fopen(path, "r");
}

void err(const char *msg) {
    printf("Error ");
    print_pos(&cur);
    printf(": %s\n", msg);
}
%}


IDENTIFIER [$@%][a-zA-Z0-9]+
DEFINE ^[a-zA-Z][a-zA-Z0-9]*
WORD (sub|if|unless)

%%
[\n\t ]+

{WORD} {
    yylval -> ident = yytext;
    BEGIN(0);
    return WORD;
};

{DEFINE} {
    yylval -> ident = yytext;
    BEGIN(0);
    return TAG_DEFINE;
};

{IDENTIFIER} {
    IdentifierTable table;
    initialize(&table);
    yylval -> ident = yytext;
    BEGIN(0);
    int ind = add(&table, value.ident);
    return TAG_IDENTIFIER;
};

<<EOF>> return 0;

. err("error");

%%

int main(int argc, const char **argv)
{
    int tag;
    YYSTYPE value;
    YYLTYPE coords;

    init_scanner(argv[1]);

    do {
        tag = yylex(&value, &coords);

        if (0 != tag && TAG_ERROR != tag) {
            printf("%s", tag_names[tag]);
            print_frag(&coords);
            if(tag == TAG_IDENTIFIER) {
                printf(": %d\n", value.ident);
            }
            else if(tag == TAG_DEFINE) {
                printf(": %s\n", value.ident);
            }
            else if(tag == WORD) {
                printf(": %s\n", value.ident);
            }
        };
    } while (0 != tag);

    return 0;
}
```

# Тестирование

Входные данные

```
$sdfsdf
@dsfsdfsd
%sdfsdfsd
$sdfsdf
FRRFR
krfrfr
subsdfewf
sub
if
unless
123
```

Вывод на `stdout`

```
IDENTIFIER(1,1)-(1,8): 0
IDENTIFIER(2,1)-(2,10): 1
IDENTIFIER(3,1)-(3,10): 2
IDENTIFIER(4,1)-(4,8): 0
DEFINE(5,1)-(5,6): FRRFR
DEFINE(6,1)-(6,7): krfrfr
DEFINE(7,1)-(7,10): subsdfewf
KEY_WORD(8,1)-(8,4): sub
KEY_WORD(9,1)-(9,3): if
KEY_WORD(10,1)-(10,7): unless
Error (11,2): error
Error (11,3): error
Error (11,4): error
```

# Вывод
В процессе выполнения данной лабораторной работы, я освоил генератор лексических анализаторов
flex, изучил его функциональные возможности и успешно применил
flex на практике для создания лексического анализатора на языке C.
