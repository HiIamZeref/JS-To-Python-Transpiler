from arvoreSintatica import ASTNode

class Parser:
    def __init__(self, tokens):
        # Inicializa o parser com uma lista de tokens e configura o estado inicial
        self.tokens = tokens
        self.current_token = None
        self.pos = 0
        self.ast = None
        self.next_token()  # Carrega o primeiro token

    def next_token(self):
        # Avança para o próximo token na lista
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
            self.pos += 1
        else:
            self.current_token = None

    def parse(self):
        # Inicia o processo de parsing e retorna a árvore sintática abstrata (AST)
        self.ast = self.program()
        return self.ast

    def program(self):
        # Representa o nó raiz da AST e processa múltiplas declarações e expressões
        node = ASTNode("Program")
        while self.current_token:
            if self.current_token.type == 'VAR': # Declaração de variável
                node.add_child(self.var_declaration())
            elif self.current_token.type == 'WHILE': # Laço 'while'
                node.add_child(self.while_statement())
            elif self.current_token.type == 'FOR': # Laço 'for'
                node.add_child(self.for_statement())
            elif self.current_token.type == 'IF': # Declaração condicional 'if-else'
                node.add_child(self.if_statement())
            elif self.current_token.type == 'FUNCTION': # Declaração de função
                node.add_child(self.function_declaration())
            else:
                node.add_child(self.expression_statement())
        return node

    def var_declaration(self):
        # Processa uma declaração de variável
        node = ASTNode("VarDeclaration")
        self.next_token()  # Consume 'VAR'
        if self.current_token.type == 'IDENTIFIER':
            node.add_child(ASTNode("Identifier", self.current_token.value))
            self.next_token()  # Consume IDENTIFIER
            if self.current_token.type == 'ASSIGN':
                self.next_token()  # Consume '='
                node.add_child(self.expression())
            if self.current_token.type == 'SEMICOLON':
                self.next_token()  # Consume ';'
        return node

    def while_statement(self):
        # Processa uma declaração de laço 'while'
        node = ASTNode("WhileStatement")
        self.next_token()  # Consume 'WHILE'
        if self.current_token.type == 'LPAREN':
            self.next_token()  # Consume '('
            node.add_child(self.expression())
            if self.current_token.type == 'RPAREN':
                self.next_token()  # Consume ')'
                node.add_child(self.block())
        return node

    def for_statement(self):
        # Processa uma declaração de laço 'for'
        node = ASTNode("ForStatement")
        self.next_token()  # Consume 'FOR'
        if self.current_token.type == 'LPAREN':
            self.next_token()  # Consume '('
            node.add_child(self.var_declaration())
            node.add_child(self.expression())
            if self.current_token.type == 'SEMICOLON':
                self.next_token()  # Consume ';'
                node.add_child(self.expression())
            if self.current_token.type == 'RPAREN':
                self.next_token()  # Consume ')'
                node.add_child(self.block())
        return node

    def if_statement(self):
        # Processa uma declaração condicional 'if-else'
        node = ASTNode("IfStatement")
        self.next_token()  # Consume 'IF'
        if self.current_token.type == 'LPAREN':
            self.next_token()  # Consume '('
            node.add_child(self.expression())
            if self.current_token.type == 'RPAREN':
                self.next_token()  # Consume ')'
                node.add_child(self.block())
                if self.current_token and self.current_token.type == 'ELSE':
                    self.next_token()  # Consume 'ELSE'
                    node.add_child(self.block())
        return node

    def function_declaration(self):
        # Processa uma declaração de função
        node = ASTNode("FunctionDeclaration")
        self.next_token()  # Consume 'FUNCTION'
        if self.current_token.type == 'IDENTIFIER':
            node.add_child(ASTNode("Identifier", self.current_token.value))
            self.next_token()  # Consume IDENTIFIER
            if self.current_token.type == 'LPAREN':
                self.next_token()  # Consume '('
                node.add_child(self.parameters())
                if self.current_token.type == 'RPAREN':
                    self.next_token()  # Consume ')'
                    node.add_child(self.block())
        return node

    def parameters(self):
        # Processa os parâmetros de uma função
        node = ASTNode("Parameters")
        while self.current_token.type == 'IDENTIFIER':
            node.add_child(ASTNode("Identifier", self.current_token.value))
            self.next_token()  # Consume IDENTIFIER
            if self.current_token.type == 'COMMA':
                self.next_token()  # Consume ','
        return node

    def expression_statement(self):
        # Processa uma expressão seguida por um ponto e vírgula
        node = ASTNode("ExpressionStatement")
        node.add_child(self.expression())
        if self.current_token.type == 'SEMICOLON':
            self.next_token()  # Consume ';'
        return node

    def expression(self):
        # Processa uma expressão genérica
        node = self.term()
        while self.current_token and self.current_token.type in ('PLUS', 'MINUS', 'AND', 'OR'):
            operator = self.current_token
            self.next_token()  # Consume operator
            right = self.term()
            new_node = ASTNode("BinaryExpression", operator.value)
            new_node.add_child(node)
            new_node.add_child(right)
            node = new_node
        return node

    def term(self):
        # Processa um termo em uma expressão (para lidar com multiplicação e divisão)
        node = self.factor()
        while self.current_token and self.current_token.type in ('TIMES', 'DIVIDE'):
            operator = self.current_token
            self.next_token()  # Consume operator
            right = self.factor()
            new_node = ASTNode("BinaryExpression", operator.value)
            new_node.add_child(node)
            new_node.add_child(right)
            node = new_node
        return node

    def factor(self):
        # Processa um fator em uma expressão (número, string, identificador, ou expressão entre parênteses)
        if self.current_token.type == 'NUMBER':
            node = ASTNode("Number", self.current_token.value)
            self.next_token()  # Consume NUMBER
        elif self.current_token.type == 'STRING':
            node = ASTNode("String", self.current_token.value)
            self.next_token()  # Consume STRING
        elif self.current_token.type == 'IDENTIFIER':
            node = ASTNode("Identifier", self.current_token.value)
            self.next_token()  # Consume IDENTIFIER
        elif self.current_token.type == 'LPAREN':
            self.next_token()  # Consume '('
            node = self.expression()
            if self.current_token.type == 'RPAREN':
                self.next_token()  # Consume ')'
        return node

    def block(self):
        # Processa um bloco de código delimitado por chaves '{ }'
        node = ASTNode("Block")
        if self.current_token.type == 'LBRACE':
            self.next_token()  # Consume '{'
            while self.current_token and self.current_token.type != 'RBRACE':
                node.add_child(self.statement())
            if self.current_token and self.current_token.type == 'RBRACE':
                self.next_token()  # Consume '}'
        return node

    def statement(self):
        # Processa uma declaração baseada no tipo do token atual
        if self.current_token.type == 'VAR':
            return self.var_declaration()
        elif self.current_token.type == 'WHILE':
            return self.while_statement()
        elif self.current_token.type == 'FOR':
            return self.for_statement()
        elif self.current_token.type == 'IF':
            return self.if_statement()
        elif self.current_token.type == 'FUNCTION':
            return self.function_declaration()
        else:
            return self.expression_statement()
