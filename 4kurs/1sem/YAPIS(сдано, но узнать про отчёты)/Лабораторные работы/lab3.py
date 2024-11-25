import re

TOKEN_SPECIFICATION = [
    ('STRING', r'"[^"]*"'),
    ('CHAR', r"'[^']'"),
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('ASSIGN', r'='),
    ('CONCAT', r'\+'),
    ('SEMI', r';'),
    ('COMMENT', r'//.*|/\*[\s\S]*?\*/'),
    ('SKIP', r'[ \t\n]+'),
    ('MISMATCH', r'.'),
]

MAX_LENGTH = 32

def tokenize(code):
    line_num = 1
    line_start = 0
    tokens = []
    
    for mo in re.finditer('|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION), code):
        kind = mo.lastgroup
        value = mo.group(kind)
        column = mo.start() - line_start
        if kind == 'SKIP' or kind == 'COMMENT':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Нераспознанный символ {value!r} в строке {line_num}')
        tokens.append((kind, value, line_num, column))
        if '\n' in value:
            line_num += 1
            line_start = mo.end()
    return tokens

def check_token_lengths(tokens):
    for token in tokens:
        kind, value, line, col = token
        if kind in ('ID', 'STRING', 'CHAR') and len(value) > MAX_LENGTH:
            print(f"Ошибка: Лексема {value} слишком длинная (строка {line}, столбец {col})")

def print_tokens(tokens):
    print(f'{"Токен":<12} {"Значение":<32} {"Строка":<6} {"Столбец":<7}')
    print('-' * 60)
    for token in tokens:
        kind, value, line, col = token
        print(f'{kind:<12} {value:<32} {line:<6} {col:<7}')

def main():
    with open('input.txt', 'r') as file:
        code = file.read()

    try:
        tokens = tokenize(code)
        check_token_lengths(tokens)
        print_tokens(tokens)
    except RuntimeError as e:
        print(e)

if __name__ == "__main__":
    main()
