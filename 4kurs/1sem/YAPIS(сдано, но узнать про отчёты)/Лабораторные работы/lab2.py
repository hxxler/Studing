class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.line_num = 1
        self.line_start = 0
        self.MAX_LENGTH = 32

    def next_token(self):
        while self.pos < len(self.code):
            current_char = self.code[self.pos]

            if current_char.isspace():
                if current_char == '\n':
                    self.line_num += 1
                    self.line_start = self.pos + 1
                self.pos += 1
                continue
            
            if current_char.isalpha() or current_char == '_':
                return self.identifier()
            elif current_char == '=':
                self.pos += 1
                return ('ASSIGN', '=')
            elif current_char == '+':
                self.pos += 1
                return ('CONCAT', '+')
            elif current_char == ';':
                self.pos += 1
                return ('SEMI', ';')
            elif current_char == '"':
                return self.string_literal()
            elif current_char == "'":
                return self.char_literal()
            elif current_char == '/':
                if self.peek() == '/':
                    return self.comment()
                elif self.peek() == '*':
                    return self.multi_comment()
            else:
                raise RuntimeError(f'Нераспознанный символ {current_char!r} в строке {self.line_num}')
            
            self.pos += 1
        return ('EOF', None)

    def identifier(self):
        start_pos = self.pos
        while (self.pos < len(self.code) and 
               (self.code[self.pos].isalnum() or self.code[self.pos] == '_')):
            self.pos += 1
        id_value = self.code[start_pos:self.pos]
        if len(id_value) > self.MAX_LENGTH:
            raise RuntimeError(f'Ошибка: Лексема {id_value} слишком длинная (строка {self.line_num})')
        return ('ID', id_value)

    def string_literal(self):
        start_pos = self.pos
        self.pos += 1
        while self.pos < len(self.code) and self.code[self.pos] != '"':
            self.pos += 1
        if self.pos == len(self.code):
            raise RuntimeError('Строка не закрыта кавычками')
        self.pos += 1
        return ('STRING', self.code[start_pos:self.pos])

    def char_literal(self):
        start_pos = self.pos
        self.pos += 1
        if self.pos < len(self.code) and self.code[self.pos] != "'":
            self.pos += 1
        if self.pos == len(self.code) or self.code[self.pos] != "'":
            raise RuntimeError('Символ не закрыт кавычками')
        self.pos += 1
        return ('CHAR', self.code[start_pos:self.pos])

    def comment(self):
        start_pos = self.pos
        while self.pos < len(self.code) and self.code[self.pos] != '\n':
            self.pos += 1
        return ('COMMENT', self.code[start_pos:self.pos])

    def multi_comment(self):
        start_pos = self.pos
        self.pos += 2
        while self.pos < len(self.code):
            if self.code[self.pos] == '*' and self.peek() == '/':
                self.pos += 2
                return ('COMMENT', self.code[start_pos:self.pos])
            self.pos += 1
        raise RuntimeError('Многострочный комментарий не закрыт')

    def peek(self):
        if self.pos + 1 < len(self.code):
            return self.code[self.pos + 1]
        return None

def main():
    with open('input.txt', 'r') as file:
        code = file.read()

    lexer = Lexer(code)
    tokens = []

    try:
        while True:
            token = lexer.next_token()
            if token[0] == 'EOF':
                break
            tokens.append(token)
        print_tokens(tokens)
    except RuntimeError as e:
        print(e)

def print_tokens(tokens):
    print(f'{"Токен":<12} {"Значение":<32} {"Строка":<6}')
    print('-' * 60)
    for token in tokens:
        kind, value = token
        print(f'{kind:<12} {value:<32} {value}')

if __name__ == "__main__":
    main()
