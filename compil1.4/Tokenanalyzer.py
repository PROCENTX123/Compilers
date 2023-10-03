import re
from Token import Token

class TokenAnalyzer:
    def __init__(self, states: dict):
        self.states = states

    @staticmethod
    def is_newline(char):
        return len(char) > 0 and char[0] == '\n'

    def analyze_tokens(self, code):
        current_state = 'start'
        buffer = ''
        current_token_start_pos = (1, 0)
        char = code[0] if code else None
        i = 0
        tokens = []

        while char is not None:
            next_state = self.get_next_state(char, current_state)

            if next_state is not None:
                current_state = next_state
                buffer += char
                i += 1
                if i < len(code):
                    char = code[i]
                else:
                    char = None
            else:
                if current_state not in ['whitespace', 'start']:
                    token = Token(current_token_start_pos, current_state, buffer.strip())
                    tokens.append(token)

                if self.is_newline(char):
                    current_token_start_pos = (current_token_start_pos[0] + 1, 0)
                else:
                    current_token_start_pos = (current_token_start_pos[0], current_token_start_pos[1])

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