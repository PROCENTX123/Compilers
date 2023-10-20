from lexer import Lexer

if __name__ == "__main__":
    file_path = 'input.txt'

    with open(file_path, 'rt') as f:
        input_text = f.read()

    lexer = Lexer(input_text)

    print('Файл без ошибок')
    print('*' * 20)
    for token in lexer.tokenize():
        print(token)
    print('*' * 20)


    file_path_1 = 'input_with_error.txt'

    with open(file_path_1, 'rt') as f:
        input_text = f.read()

    lexer = Lexer(input_text)

    print('Файл с ошибками')
    print('*' * 20)
    for token in lexer.tokenize():
        print(token)
    print('*' * 20)
