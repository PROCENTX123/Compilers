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
                            Token(DomainTag.Error, Coords(Position(self.row, i + 1), Position(self.row, j))))
                    else:
                        self.tokens.append(Token(DomainTag.Constant, coords, str(int(line[i + 2:j + 1], base=16))))
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
                            Token(DomainTag.Error, Coords(Position(self.row, i + 1), Position(self.row, j))))
                    i = j + 1
                #Обработка идентификатора
                elif line[i].lower().isalpha():
                    last_alpha_pos = i
                    j = i + 1
                    while j < len(line) and (line[j].isalnum() or line[j].isalpha() and not line[j].isdigit()):
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
                            Token(DomainTag.Error, Coords(Position(self.row, i + 1), Position(self.row, j))))
                    i = j
            self.row += 1

    def print(self):
        for token in self.tokens:
            print(token)
