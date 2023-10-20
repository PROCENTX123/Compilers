from lexer import Lexer
from transition_table import TransitionTable, top_down_alg

if __name__ == "__main__":
    lexer = Lexer()
    tokens = lexer.tokenization(open('input.txt', 'rt').read())
    for token in tokens:
        print(token)
    tbl = TransitionTable("table.csv")
    v = top_down_alg(tokens, tbl)
    v.display()
