import ply.lex as lex # A biblioteca PLY é utilizada para construir analisadores léxicos e sintáticos em Python

class AnalisadorLexicoJS:
    # Lista de nomes de tokens. Esta é uma variável de classe.
    tokens = (
        'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
        'LPAREN', 'RPAREN', 'IDENTIFIER', 'SEMICOLON', 'ASSIGN',
        'VAR', 'CONST', 'LET', 'LBRACE', 'RBRACE', 'CONSOLE_LOG','PROMPT', 'COMMA', # Instrucoes de entrada e saida
        'STRING', 'FOR', 'WHILE', 'BREAK', 'CONTINUE', # Logica de laços
    )

    # Regras simples de token expressas como strings regulares.
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

    # Importante: a ordem que as funções são definidas é relevante para o PLY

    # Expressão regular para números (inteiros por simplicidade)
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)  # Converte o valor de string para inteiro
        return t
    
    # Tokens para estruturas de repetição e controle
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

    # Tokens para instruções de entrada e saída
    def t_CONSOLE_LOG(self, t):
        r'console\.log'
        return t
    
    def t_PROMPT(self, t):
        r'prompt'
        return t

    # Expressão regular para strings
    def t_STRING(self, t):
        r'"([^"\\]*(\\.[^"\\]*)*)"'
        t.value = t.value[1:-1]  # Remove as aspas do início e do fim
        return t
    

    # Expressão regular para identificadores
    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        return t

    # Palavras-chave para associar variáveis
    def t_VAR(self, t):
        r'var'
        return t

    def t_CONST(self, t):
        r'const'
        return t

    def t_LET(self, t):
        r'let'
        return t

    # Regra para ignorar espaços e tabs
    t_ignore = ' \t'

    # Regra para lidar com quebras de linha
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Regra de erro para caracteres ilegais
    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    # Construtor que cria o lexer
    def __init__(self):
        self.lexer = lex.lex(module=self)

    # Método para executar a análise léxica
    def analisar(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

# Testando o analisador léxico
if __name__ == "__main__":
    analisador = AnalisadorLexicoJS()
    data = '''
    var x = 0;
    while (x < 10) {
        console.log("Count: " + x);
        x++;
        if (x == 5) break;
    }
    for (var i = 0; i < 10; i++) {
        if (i % 2 == 0) continue;
        console.log(i);
    }
    '''
    analisador.analisar(data)