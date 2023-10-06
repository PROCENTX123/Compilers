import re
from Token import Token

class TokenAnalyzer:
    def __init__(self, states: dict):
        self.states = states

    @staticmethod
    def is_newline(buffer):
        return len(buffer) > 0 and buffer[-1] == '\n'

    def analyze_tokens(self, code):
        current_state = 'start'
        buffer = ''
        current_token_start_pos = (1, 0)
        char = code[0] if code else None
        i = 0
        j = 0
        tokens = []
        flag = 1

        while char is not None:
            next_state = self.get_next_state(char, current_state)

            if next_state is not None:

                current_state = next_state
                buffer += char
                i += 1
                j += 1

                if i < len(code):
                    char = code[i]
                else:
                    char = None
            else:
                if current_state not in ['whitespace', 'start']:
                    token = Token(current_token_start_pos, current_state, buffer.strip())
                    tokens.append(token)

                if self.is_newline(buffer):
                    current_token_start_pos = (current_token_start_pos[0] + flag, 0)
                    j = 0

                else:
                    current_token_start_pos = (current_token_start_pos[0], j)

                buffer = ''
                current_state = 'start'


        if current_state not in ['whitespace', 'start']:
            token = Token(current_token_start_pos, current_state, buffer.strip())
            tokens.append(token)

        return tokens

    def get_next_state(self, char, current_state):
        if current_state in self.states:
            for pattern, next_state in self.states[current_state].items():
                if re.fullmatch(pattern, char):
                    return next_state
        return None