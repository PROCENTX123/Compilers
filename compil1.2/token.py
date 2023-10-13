class Token:
    def __init__(self, name, coords, value):
        self.name = name
        self.coords = coords
        self.value = value

    def __str__(self):
        return f"{self.name} {self.coords}: {self.value}"
