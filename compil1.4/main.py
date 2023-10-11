from Tokenanalyzer import TokenAnalyzer

if __name__ == "__main__":
    with open('input.txt', 'r') as file:
        lines = file.read()

    states = {
        'start': {
            r'\s': 'whitespace',
            r'\d': 'digit',
            r'\(': 'ident_op_bracket',
            r'\)': 'ident_cl_bracket',
            r'{': 'ident_com_start',
            r'i': 'ident_i',
            r't': 'ident_t',
            r'e': 'ident_e',
            r'(?!ite)[a-zA-Z]': 'identifier'
        },
        'whitespace': {
            r'\s': 'whitespace'
        },
        'digit': {
            r'\d': 'digit'
        },

        'ident_op_bracket': {
            r'\s': 'op_bracket'
        },
        'op_bracket': {},

        'ident_cl_bracket': {
            r'\s': 'cl_bracet'
        },
        'cl_bracket': {},

        'ident_com_start': {
            r'[^\}]': 'comment',
            r'\}': 'comment_finished'
        },
        'comment': {
            r'[^}]': 'comment',
            r'\}': 'comment_finished'
        },
        'comment_finished': {},

        'ident_i': {
            r'f': 'ident_if',
            r'[^f]': 'identifier'
        },
        'ident_if': {
            r'[\s]': 'keyword_if',
            r'[^\sw|(|)|{]': 'identifier'
        },
        'keyword_if': {},

        'ident_e': {
            r'l': 'ident_el',
            r'[^l]': 'identifier'
        },
        'ident_el': {
            r's': 'ident_els',
            r'[^s]': 'identifier'
        },
        'ident_els': {
            r'e': 'ident_else',
            r'[^e]': 'identifier'
        },
        'ident_else': {
            r'\s': 'keyword_else',
            r'[^\sw|(|)|{]': 'identifier'
        },
        'keyword_else': {},

        'ident_t': {
            r'h': 'ident_th',
            r'[^h]': 'identifier'
        },
        'ident_th': {
            r'e': 'ident_the',
            r'[^e]': 'identifier'
        },
        'ident_the': {
            r'n': 'ident_then',
            r'[^n]': 'identifier'
        },
        'ident_then': {
            r'\s': 'keyword_then',
            r'[^\sw|(|)|{]': 'identifier'
        },
        'keyword_then': {},

        'identifier': {
            r'[a-zA-Z0-9]': 'identifier'
        }
    }

    analyzer = TokenAnalyzer(states)
    tokens = analyzer.analyze_tokens(lines)


    print('*' * 40)
    for token in tokens:
        print(
            f"{token.state} ({token.position[0]}.{token.position[1]} - {token.position[0]}.{len(token.value) + token.position[1]}) : {token.value}")
    print('*' * 40)