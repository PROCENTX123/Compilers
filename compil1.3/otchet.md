% Лабораторная работа № 1.3. «Объектно-ориентированный лексический анализатор»
% 13 октября 2023 г.
% Григорьев Роман, ИУ9-62Б

# Цель работы
Целью данной работы является приобретение навыка реализации лексического анализатора
на объектно-ориентированном языке без применения каких-либо средств
автоматизации решения задачи лексического анализа.

# Индивидуальный вариант
Идентификаторы: последовательности буквенных символов Unicode
и цифр, начинающиеся с буквы, не чувствительны к регистру. 
Целочисленные константы: десятичные — последовательности десятичных цифр, шестнадцатеричные
— последовательности шестнадцатиричных цифр, 
начинающиеся на «&H», тоже не чувствительны к регистру.
Ключевые слова — «PRINT», «GOTO», «GOSUB» без учёта регистра.


# Реализация


Модуль analyzer.py
``` python
from Identifiertable import IdentifierTable
from Token import Coords, Position, Token
from Domaintag import DomainTag

KEYWORDS = ['print', 'goto', 'gosub']
HEX_SYMBOLS = '0123456789ABCDEFabcdef'

class LexicalAnalyzer:
    def __init__(self, file_path: str):
        with open(file_path, 'r') as file:
            self.text = file.read()
        self.lines = self.text.split('\n')
        self.row = 1
        self.tokens = []

    def analyze(self) -> None:
        identifier_table = IdentifierTable()
        for line in self.lines:
            line = line.lower()
            col = 1
            i = 0
            while i < len(line):
                #Обработка PRINT
                if line[i:i + 5].lower() == 'print' and (len(line) == i + 5 or line[i + 5] == ' '):
                    j = i + 5
                    coords = Coords(Position(self.row, col + i), Position(self.row, j))
                    self.tokens.append(Token(DomainTag.Keyword, coords, 'print'))
                    i = j
                #Обработка GOSUB
                elif line[i:i + 5].lower() == 'gosub' and (len(line) == i + 5 or line[i + 5] == ' '):
                    j = i + 5
                    coords = Coords(Position(self.row, col + i), Position(self.row, j))
                    self.tokens.append(Token(DomainTag.Keyword, coords, 'gosub'))
                    i = j
                #Обработка GOTO
                elif line[i:i + 4].lower() == 'goto' and (len(line) == i + 4 or line[i + 4] == ' '):
                    j = i + 4
                    coords = Coords(Position(self.row, col + i), Position(self.row, j))
                    self.tokens.append(Token(DomainTag.Keyword, coords, 'goto'))
                    i = j
                #Обработка шестнадцатиричной константы
                elif line[i:i + 2].lower() == '&h':
                    j = i + 2
                    while j < len(line) and (line[j].isnumeric() or line[j].lower() in HEX_SYMBOLS):
                        j += 1
                    coords = Coords(Position(self.row, i + 1), Position(self.row, j))
                    hex_value = '0x' + line[i + 2:j]
                    if hex_value == '0x':
                        self.tokens.append(
                            Token(DomainTag.Error,
                            Coords(Position(self.row, i + 1), Position(self.row, j))))
                    else:
                        self.tokens.append(Token(DomainTag.Constant,
                        coords, str(int(line[i + 2:j + 1], base=16))))
                    i = j
                #Обработка десятичной константы
                elif line[i].isnumeric():
                    j = i + 1
                    while j < len(line) and line[j] in HEX_SYMBOLS:
                        j += 1

                    coords = Coords(Position(self.row, i + 1), Position(self.row, j + 1))
                    if line[i + 1:j + 1]:
                        self.tokens.append(Token(DomainTag.Constant, coords, str(int(line[i:j]))))
                    else:
                        self.tokens.append(
                            Token(DomainTag.Error, Coords(Position(
                            self.row, i + 1), Position(self.row, j))))
                    i = j + 1
                #Обработка идентификатора
                elif line[i].lower().isalpha():
                    last_alpha_pos = i
                    j = i + 1
                    while j < len(line) and (line[j].isalnum() or
                       line[j].isalpha() and not line[j].isdigit()):
                        if line[j].isalpha():
                            last_alpha_pos = j
                        j += 1
                    coords = Coords(Position(self.row, col + i), Position(self.row, last_alpha_pos + 1))
                    self.tokens.append(
                        Token(DomainTag.Identifier, coords, identifier_table.add(line[col + i:j])))
                    i = last_alpha_pos + 1

                elif line[i] == ' ':
                    i += 1

                else:
                    j = i + 1
                    while j < len(line) and line[j:j+2] != '&H' and not line[j].isalpha():
                        j += 1
                    lexem = line[i:j]
                    if lexem:
                        self.tokens.append(
                            Token(DomainTag.Error, Coords(Position(
                                self.row, i + 1), Position(self.row, j))))
                    i = j
            self.row += 1

    def print(self):
        for token in self.tokens:
            print(token)
```
Модуль domaintag.py
``` python
from enum import Enum

class DomainTag(Enum):
    Keyword = 'Keyword'
    Constant = 'Constant'
    Identifier = 'Identifier'
    Error = 'Error'
```

Модуль identyfireTable.py
``` python
class IdentifierTable:
    def __init__(self):
        self.current_num = 0
        self.container = {}

    def add(self, value: str) -> int:
        if value in self.container:
            return self.container[value]
        self.container[value] = self.current_num
        self.current_num += 1
        return self.container[value]
```

Модуль token.py
``` python
from typing import Any, Optional
from Domaintag import DomainTag

class Position:
    def __init__(self, line: int, pos: int):
        self.line = line
        self.pos = pos

    def __str__(self) -> str:
        return f'({self.line},{self.pos})'

class Coords:
    def __init__(self, start: Position, end: Position):
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f'{self.start}-{self.end}'

class Token:
    def __init__(self, tag: DomainTag, coords: Coords, attrib: Optional[Any] = None):
        self.tag = tag
        self.coords = coords
        self.attrib = attrib

    def __str__(self) -> str:
        attrib_str = f' [{self.attrib}]' if self.attrib is not None else ''
        return f'{self.tag.value} {self.coords}{attrib_str}'
```

Модуль main.py
``` python
from Analyzer import LexicalAnalyzer

if __name__ == "__main__":
    analyzer = LexicalAnalyzer('text.txt')
    analyzer.analyze()
    analyzer.print()
```

# Тестирование

Входные данные

input.txt
```
PrInTeR
9PriMe

&HA12
&Ha12

adsf 9 safd
fsdfdf
fsdfDF
10 230
goto
GoTO
gosub
print
PrInT
 printer

&H C
```
Вывод на `stdout`
```
Identifier (1,1)-(1,7) [0]
Constant (2,1)-(2,2) [9]
Identifier (2,3)-(2,6) [1]
Constant (4,1)-(4,5) [2578]
Constant (5,1)-(5,5) [2578]
Identifier (7,1)-(7,4) [2]
Constant (7,6)-(7,7) [9]
Identifier (7,8)-(7,11) [3]
Identifier (8,1)-(8,6) [4]
Identifier (9,1)-(9,6) [4]
Constant (10,1)-(10,3) [10]
Constant (10,4)-(10,7) [230]
Keyword (11,1)-(11,4) [goto]
Keyword (12,1)-(12,4) [goto]
Keyword (13,1)-(13,5) [gosub]
Keyword (14,1)-(14,5) [print]
Keyword (15,1)-(15,5) [print]
Identifier (16,2)-(16,8) [0]
Error (18,1)-(18,2)
Identifier (18,4)-(18,4) [5]
```

# Вывод
Была разработана программа, реализующая лексический анализатор
на выбранном объектно-ориентированном языке.
Программа успешно выполняет задачи по распознаванию
идентификаторов, целочисленных констант и ключевых слов,
при этом учитывая их нечувствительность к регистру.
Данная лабораторная работа позволила приобрести навыки
в области разработки лексических анализаторов,
а также освоить техники обработки текстовых данных для
распознавания различных лексических элементов в исходном коде.
