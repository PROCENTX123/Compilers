from lexer import Lexer
from my_parser import Parser


if __name__ == "__main__":
    lexer = Lexer()
    tokens = lexer.tokenization(open('input.txt', 'rt').read())
    parser = Parser(tokens)
    parser.ParseGrammar()
    firsts = parser.calculate_first_set()
    for nterm, first in firsts.items():
        print(f'{nterm} - FIRST: {first}')