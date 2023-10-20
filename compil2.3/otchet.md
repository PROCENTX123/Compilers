% Лабораторная работа № 1.1. Раскрутка самоприменимого компилятора
% 13 октября 2023 г.
% Григорьев Роман, ИУ9-62Б

# Цель работы
Целью данной работы является ознакомление с раскруткой 
самоприменимых компиляторов
на примере модельного компилятора.

# Индивидуальный вариант
Компилятор P5. Заменить операторы div и mod на // и % соответственно.

# Реализация

Различие между файлами `pcom.pas` и `pcom2.pas`:
```diff
if not iscmte then nextch; goto 1
end;
special:
- begin sy := ssy[ch]; op := sop[ch];
+ begin
+ sy := ssy[ch]; op := sop[ch];
+ nextch;
+ if ch='/' then
+ begin
+ sy := rsy[10];
+ op := rop[10];
nextch
+ end
end;
chspace: sy := othersy
end; (*case*)
@@ -5345,7 +5352,7 @@
rw[ 1] := 'if '; rw[ 2] := 'do '; rw[ 3] := 'of ';
rw[ 4] := 'to '; rw[ 5] := 'in '; rw[ 6] := 'or ';
rw[ 7] := 'end '; rw[ 8] := 'for '; rw[ 9] := 'var ';
- rw[10] := 'div '; rw[11] := 'mod '; rw[12] := 'set ';
+ rw[10] := '// '; rw[12] := 'set ';
rw[13] := 'and '; rw[14] := 'not '; rw[15] := 'nil ';
rw[16] := 'then '; rw[17] := 'else '; rw[18] := 'with ';
rw[19] := 'goto '; rw[20] := 'case '; rw[21] := 'type ';
@@ -5378,18 +5385,18 @@
ssy[','] := comma ; ssy['.'] := period; ssy['''']:= othersy;
ssy['['] := lbrack ; ssy[']'] := rbrack; ssy[':'] := colon;
ssy['^'] := arrow ; ssy['<'] := relop; ssy['>'] := relop;
- ssy[';'] := semicolon; ssy['@'] := arrow;
+ ssy[';'] := semicolon; ssy['@'] := arrow; ssy['%'] := mulop;
end (*symbols*) ;

procedure rators;
var i: integer;
begin
for i := 1 to maxres (*nr of res words*) do rop[i] := noop;
- rop[5] := inop; rop[10] := idiv; rop[11] := imod;
+ rop[5] := inop; rop[10] := idiv;
rop[6] := orop; rop[13] := andop;
for i := ordminchar to ordmaxchar do sop[chr(i)] := noop;
sop['+'] := plus; sop['-'] := minus; sop['*'] := mul; sop['/'] := rdiv;
- sop['='] := eqop; sop['<'] := ltop; sop['>'] := gtop;
+ sop['='] := eqop; sop['<'] := ltop; sop['>'] := gtop; sop['%']:=imod;
end (*rators*) ;

procedure procmnemonics;
@@ -5487,7 +5494,7 @@
chartp['^'] := special ; chartp[';'] := special ;
chartp['<'] := chlt ; chartp['>'] := chgt ;
chartp['{'] := chlcmt ; chartp['}'] := special ;
- chartp['@'] := special ;
+ chartp['@'] := special ; chartp['%']:=special;

ordint['0'] := 0; ordint['1'] := 1; ordint['2'] := 2;
ordint['3'] := 3; ordint['4'] := 4; ordint['5'] := 5;
```


Различие между файлами `pcom2.pas` и `pcom3.pas`:

```diff
@@ -1684,7 +1684,7 @@
begin
k := alignquot(fsp);
l := flc-1;
- flc := l + k - (k+l) mod k
+ flc := l + k - (k+l) % k
end (*align*);

procedure printtables(fb: boolean);
@@ -2957,7 +2957,7 @@
end;

procedure putic;
- begin if ic mod 10 = 0 then writeln(prr,'i',ic:5) end;
+ begin if ic % 10 = 0 then writeln(prr,'i',ic:5) end;

procedure gen0(fop: oprange);
begin
@@ -3649,7 +3649,7 @@
if lsp^.form = scalar then error(399)
else
if string(lsp) then
- begin len := lsp^.size div charmax;
+ begin len := lsp^.size // charmax;
if default then
gen2(51(*ldc*),1,len);
gen2(51(*ldc*),1,len);
@@ -5319,7 +5319,7 @@
(* note in the above reservation of buffer store for 2 text files *)
ic := 3; eol := true; linecount := 0;
ch := ' '; chcnt := 0;
- mxint10 := maxint div 10;
+ mxint10 := maxint // 10;
inputhdf := false; { set 'input' not in header files }
outputhdf := false; { set 'output' not in header files }
for i := 1 to 500 do errtbl[i] := false; { initialize error tracking }
```

# Тестирование

Тестовый пример:

```pascal
program hello(output);

var a:Integer;
b:Integer;
c:Integer;
begin
    a:=5;
    b:=a // 2;
    c:= 5 % 2;
    writeln (a);
    writeln (b);
    writeln (c);
end.
```

Вывод тестового примера на `stdout`

```
P5 Pascal interpreter vs. 1.0

Assembling/loading program
Running program

P5 Pascal compiler vs. 1.0

1 40 program hello(output);
2 40
3 40 var a:Integer;
4 44 b:Integer;
5 44 c:Integer;
6 48 begin
7 3 a:=5;
8 7 b:=a // 2;
9 8 c:=a % 2
10 11 writeln (a);
11 11 writeln (b);
12 11 writeln (c);
13 18 end.

Errors in program: 0

program complete
~/Desktop/Компиляторы/lab1/p5$ mv prr prd
~/Desktop/Компиляторы/lab1/p5$ ./pint <hello.pas
P5 Pascal interpreter vs. 1.0

Assembling/loading program
Running program

5
1
1

program complete

```

# Вывод
В ходе лабораторной работы я изучил компилятор p5, предназначенный для языка Паскаль.
Мне удалось внести необходимые изменения в компилятор, чтобы он соответствовал
поставленным условиям. Далее я провел тестирование на небольшой программе.
Кроме того, был разработан новый компилятор, в котором уже изначально
учтены новые функциональные возможности.
