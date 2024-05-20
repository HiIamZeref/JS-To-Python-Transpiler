import ply.lex as lex

class AnalisadorLexicoJS:
    tokens = (
        'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
        'LPAREN', 'RPAREN', 'IDENTIFIER', 'SEMICOLON', 'ASSIGN',
        'VAR', 'CONST', 'LET', 'LBRACE', 'RBRACE', 'CONSOLE_LOG', 'PROMPT', 'COMMA',
        'STRING', 'FOR', 'WHILE', 'BREAK', 'CONTINUE', 'IF', 'ELSE',
        'FUNCTION', 'RETURN', 'EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE', 'AND', 'OR',
    )

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_SEMICOLON = r';'
    t_ASSIGN = r'='
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_COMMA = r','

    t_EQ = r'=='
    t_NEQ = r'!='
    t_LT = r'<'
    t_GT = r'>'
    t_LE = r'<='
    t_GE = r'>='
    t_AND = r'&&'
    t_OR = r'\|\|'

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_FOR(self, t):
        r'for'
        return t

    def t_WHILE(self, t):
        r'while'
        return t

    def t_BREAK(self, t):
        r'break'
        return t

    def t_CONTINUE(self, t):
        r'continue'
        return t

    def t_IF(self, t):
        r'if'
        return t

    def t_ELSE(self, t):
        r'else'
        return t

    def t_FUNCTION(self, t):
        r'function'
        return t

    def t_RETURN(self, t):
        r'return'
        return t

    def t_CONSOLE_LOG(self, t):
        r'console\.log'
        return t

    def t_PROMPT(self, t):
        r'prompt'
        return t

    def t_STRING(self, t):
        r'"([^"\\]*(\\.[^"\\]*)*)"'
        t.value = t.value[1:-1]
        return t

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        if t.value in ('var', 'const', 'let', 'for', 'while', 'break', 'continue', 'if', 'else', 'function', 'return'):
            t.type = t.value.upper()
        return t

    t_ignore = ' \t'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def tokenize(self, code):
        self.lexer.input(code)
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append(tok)
        return tokens

# Teste do analisador léxico
if __name__ == "__main__":
    code = '''
    var x = 0;
    '''
    lexer = AnalisadorLexicoJS()
    tokens = lexer.tokenize(code)
    print("Tokens:", tokens)
