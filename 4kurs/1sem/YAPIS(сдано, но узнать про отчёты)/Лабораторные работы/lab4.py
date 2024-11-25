import ply.lex as lex
import ply.yacc as yacc

# Лексический анализатор

# Список токенов
tokens = (
    'ID',          # Идентификатор
    'STRING',      # Строковая константа
    'CHAR',        # Одиночный символ
    'PLUS',        # Знак конкатенации +
    'SEMICOLON',   # Точка с запятой ;
)

# Регулярные выражения для токенов
t_PLUS = r'\+'
t_SEMICOLON = r';'

# Лексема для идентификатора
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

# Лексема для строковых констант
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

# Лексема для одиночных символов
def t_CHAR(t):
    r'\'([^\\\n]|(\\.))\''
    return t

# Игнорируем пробелы и табуляции
t_ignore = ' \t'

# Отслеживание строк и столбцов
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Обработка ошибок
def t_error(t):
    print(f"Неверный символ '{t.value[0]}'")
    t.lexer.skip(1)

# Инициализация лексера
lexer = lex.lex()

# Синтаксический анализатор

# Определим правила грамматики
def p_program(p):
    '''program : expression SEMICOLON program
               | expression'''
    if len(p) == 4:
        p[0] = ('program', p[1], p[3])
    else:
        p[0] = ('program', p[1])

def p_expression_concat(p):
    '''expression : expression PLUS element'''
    p[0] = ('concat', p[1], p[3])

def p_expression_element(p):
    '''expression : element'''
    p[0] = p[1]

def p_element_id(p):
    '''element : ID'''
    p[0] = ('id', p[1])

def p_element_string(p):
    '''element : STRING'''
    p[0] = ('string', p[1])

def p_element_char(p):
    '''element : CHAR'''
    p[0] = ('char', p[1])

# Обработка ошибок
def p_error(p):
    print(f"Ошибка синтаксиса в '{p.value}'")

# Инициализация парсера
parser = yacc.yacc()

# Пример использования программы

def main():
    # Пример входной строки
    input_data = '''"hello" + '!' + var1; "world" + var2 + 'a';'''

    # Лексический анализ
    print("Лексический анализ:")
    lexer.input(input_data)
    for token in lexer:
        print(token)

    # Синтаксический анализ
    print("\nСинтаксический анализ:")
    result = parser.parse(input_data)
    print(result)

if __name__ == '__main__':
    main()
