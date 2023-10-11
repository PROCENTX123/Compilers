from ..syntax.syntax import Term


class Token(Term):
    def __init__(self, type, image, start, follow):
        super().__init__(type, start, follow)
        self.image = image  # image.replace("[ \\t\"]*", "")

    def __str__(self):
        return f"lex_analyze.Token {super().__str__()} {self.start}-{self.follow} <{self.image}>"

    def to_dot(self):
        one, five = '\"', '\\\\\"'
        return f"[label=\"{str(self).replace(one, five)}\"],[color=red]"

    def get_image(self):
        return self.image

    def set_image(self, image):
        self.image = image