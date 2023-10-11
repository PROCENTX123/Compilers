class Coords:
    def __init__(self, row, col, pos):
        self.row = row
        self.col = col
        self.pos = pos

    def getPos(self):
        return self.pos

    def setPos(self):
        self.pos += 1
        self.col += 1

    @staticmethod
    def undefined():
        return Coords(-1, -1, -1)

    @staticmethod
    def start():
        return Coords(1, 1, 0)

    def shift(self, positions):
        return Coords(self.row, self.col + positions, self.pos + positions)

    def newline(self):
        return Coords(self.row + 1, 1, self.pos + 1)

    def __str__(self):
        return f'({self.row}, {self.col})' if self.pos > -1 else "?"