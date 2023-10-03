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