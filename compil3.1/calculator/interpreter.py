class ArithmeticInterpreter:
    def __init__(self, parseTree):
        self.result = None
        self.tree = parseTree
        self.interpret_tree()

    def get_result(self):
        return self.result

    def interpret_tree(self):
        self.result = self.scan_e(self.tree.root)

    def scan_e(self, root):
        return self.scan_t(root.children[0]) + self.scan_e1(root.children[1])

    def scan_e1(self, node):
        res = 0
        while len(node.children) == 3:
            res += self.scan_t(node.children[1])
            node = node.children[2]
        return res

    def scan_t(self, node):
        return self.scan_f(node.children[0]) * self.scan_t1(node.children[1])

    def scan_t1(self, node):
        res = 1
        while len(node.children) == 3:
            res *= self.scan_f(node.children[1])
            node = node.children[2]
        return res

    def scan_f(self, node):
        if len(node.children) == 3:
            return self.scan_e(node.children[1])
        else:
            tok = node.symbols[0]
            return int(tok.image)