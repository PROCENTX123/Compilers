import re
from token import Token

def find_max_match(text, regex_dict):
    max_token_name, max_end_index = None, 0

    for token_name, regex in regex_dict.items():
        submatch = regex.match(text)
        if submatch and submatch.span()[1] > max_end_index:
            max_end_index = submatch.span()[1]
            max_token_name = token_name

    return max_token_name, max_end_index

class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.tokens = {
            'COMMENT': 'REM\W.*?\\n',
            'FOR': 'FOR',
            'NEXT': 'NEXT',
            'IDENT': '[a-zA-Z_][a-zA-Z]*[%$#&!]?',
            'OPERATIONS': '[+\\-\\/\\\\]'
        }
        self.tokens_compiled = {k: re.compile(v) for k, v in self.tokens.items()}
        self.pattern = re.compile('|'.join(f'({v})' for v in self.tokens.values()))
        self.spaces = re.compile('\s+')

    def tokenize(self):
        line = 1
        line_index = -1
        current_index = -1

        while current_index < len(self.input_text) - 1:
            current_index += 1
            line_index += 1
            char = self.input_text[current_index]

            # Пропустить пробелы и переносы строк
            if char in (' ', '\t'):
                continue
            elif char == '\n':
                line += 1
                line_index = -1
                continue

            text = self.input_text[current_index:]

            max_token_name, max_end_index = find_max_match(text, self.tokens_compiled)

            if max_token_name:
                yield Token(
                    max_token_name, (line, line_index), text[:max_end_index]
                )
                current_index += max_end_index - 1
                line_index += max_end_index - 1
            else:
                print(f"Syntax error at line {line}, index {line_index}")
