from arvoreSintatica import ASTNode

class AnalisadorSintaticoJS:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = 0
        self.ast = None
        self.next_token()

    def next_token(self):
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
            self.pos += 1
        else:
            self.current_token = None

    def parse(self):
        self.ast = self.program()
        return self.ast

    def program(self):
        node = ASTNode("Program")
        while self.current_token:
            if self.current_token.type in ('VAR', 'LET', 'CONST'):
                node.add_child(self.var_declaration())
            elif self.current_token.type == 'WHILE':
                node.add_child(self.while_statement())
            elif self.current_token.type == 'FOR':
                node.add_child(self.for_statement())
            elif self.current_token.type == 'IF':
                node.add_child(self.if_statement())
            elif self.current_token.type == 'FUNCTION':
                node.add_child(self.function_declaration())
            else:
                node.add_child(self.expression_statement())
        return node

    def var_declaration(self):
        node = ASTNode("VarDeclaration")
        self.next_token()  # Consume 'VAR', 'LET' or 'CONST'
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

    def return_statement(self):
        node = ASTNode("ReturnStatement")
        self.next_token()  # Consume 'RETURN'
        if self.current_token and self.current_token.type != 'SEMICOLON':
            node.add_child(self.expression())
        if self.current_token and self.current_token.type == 'SEMICOLON':
            self.next_token()  # Consume ';'
        return node

    def function_declaration(self):
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
        node = ASTNode("Parameters")
        while self.current_token.type == 'IDENTIFIER':
            node.add_child(ASTNode("Identifier", self.current_token.value))
            self.next_token()  # Consume IDENTIFIER
            if self.current_token.type == 'COMMA':
                self.next_token()  # Consume ','
        return node

    def expression_statement(self):
        node = ASTNode("ExpressionStatement")
        node.add_child(self.expression())
        if self.current_token and self.current_token.type == 'SEMICOLON':
            self.next_token()  # Consume ';'
        return node

    def expression(self):
        node = self.assignment()
        return node

    def assignment(self):
        node = self.logical_or()
        while self.current_token and self.current_token.type == 'ASSIGN':
            operator = self.current_token
            self.next_token()
            right = self.assignment()
            new_node = ASTNode("AssignmentExpression", operator.value)
            new_node.add_child(node)
            new_node.add_child(right)
            node = new_node
        return node
    
    def logical_or(self):
        node = self.logical_and()
        while self.current_token and self.current_token.type == 'OR':
            operator = self.current_token
            self.next_token()
            right = self.logical_and()
            new_node = ASTNode("LogicalExpression", operator.value)
            new_node.add_child(node)
            new_node.add_child(right)
            node = new_node
        return node

    def logical_and(self):
        node = self.comparison()
        while self.current_token and self.current_token.type == 'AND':
            operator = self.current_token
            self.next_token()
            right = self.comparison()
            new_node = ASTNode("LogicalExpression", operator.value)
            new_node.add_child(node)
            new_node.add_child(right)
            node = new_node
        return node

    def comparison(self):
        node = self.term()
        while self.current_token and self.current_token.type in ('EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE'):
            operator = self.current_token
            self.next_token()
            right = self.term()
            new_node = ASTNode("BinaryExpression", operator.value)
            new_node.add_child(node)
            new_node.add_child(right)
            node = new_node
        return node

    def term(self):
        node = self.factor()
        while self.current_token and self.current_token.type in ('TIMES', 'DIVIDE', 'PLUS', 'MINUS'):
            operator = self.current_token
            self.next_token()
            right = self.factor()
            new_node = ASTNode("BinaryExpression", operator.value)
            new_node.add_child(node)
            new_node.add_child(right)
            node = new_node
        return node

    def factor(self):
        if self.current_token is None:
            raise SyntaxError("Fim inesperado do input")

        if self.current_token.type == 'NUMBER':
            node = ASTNode("Number", self.current_token.value)
            self.next_token()
        elif self.current_token.type == 'STRING':
            node = ASTNode("String", self.current_token.value)
            self.next_token()
        elif self.current_token.type == 'TRUE':
            node = ASTNode("Boolean", True)
            self.next_token()
        elif self.current_token.type == 'FALSE':
            node = ASTNode("Boolean", False)
            self.next_token()
        elif self.current_token.type == 'IDENTIFIER':
            node = ASTNode("Identifier", self.current_token.value)
            self.next_token()
            if self.current_token and self.current_token.type == 'LPAREN':
                node = self.function_call(node)
            while self.current_token and self.current_token.type == 'DOT':
                self.next_token()  # Consume '.'
                if self.current_token and self.current_token.type == 'IDENTIFIER':
                    property_node = ASTNode("PropertyAccess", self.current_token.value)
                    property_node.add_child(node)
                    node = property_node
                    self.next_token()  # Consume IDENTIFIER
                else:
                    raise SyntaxError("Esperado IDENTIFIER após '.'")
            if self.current_token and self.current_token.type == 'LBRACKET':
                node = self.array_access(node)
        elif self.current_token.type in ('CONSOLE_LOG', 'PROMPT'):
            node = self.function_call()
        elif self.current_token.type == 'LBRACKET':
            node = self.array_literal()
        elif self.current_token.type == 'LPAREN':
            self.next_token()
            node = self.expression()
            if self.current_token and self.current_token.type == 'RPAREN':
                self.next_token()
            else:
                raise SyntaxError("Esperado ')' após expressão")
        else:
            raise SyntaxError(f"Token inesperado: {self.current_token}")
        return node


    def array_literal(self):
        elements = []
        self.next_token()  # Consume '['
        while self.current_token and self.current_token.type != 'RBRACKET':
            elements.append(self.expression())
            if self.current_token and self.current_token.type == 'COMMA':
                self.next_token()  # Consume ','
        if self.current_token and self.current_token.type == 'RBRACKET':
            self.next_token()  # Consume ']'
        node = ASTNode("ArrayLiteral")
        node.children.extend(elements)
        return node

    def array_access(self, array_node):
        self.next_token()  # Consume '['
        index = self.expression()
        if self.current_token and self.current_token.type == 'RBRACKET':
            self.next_token()  # Consume ']'
        node = ASTNode("ArrayAccess")
        node.add_child(array_node)
        node.add_child(index)
        return node

    def function_call(self, node=None):
        func_name = node.value if node else self.current_token.value
        node = ASTNode("FunctionCall", func_name)
        self.next_token()  # Consume IDENTIFIER or CONSOLE_LOG or PROMPT
        if self.current_token.type == 'LPAREN':
            self.next_token()  # Consume '('
            while self.current_token and self.current_token.type != 'RPAREN':
                node.add_child(self.expression())
                if self.current_token and self.current_token.type == 'COMMA':
                    self.next_token()  # Consume ','
            if self.current_token and self.current_token.type == 'RPAREN':
                self.next_token()  # Consume ')'
        return node

    def block(self):
        node = ASTNode("Block")
        if self.current_token.type == 'LBRACE':
            self.next_token()  # Consume '{'
            while self.current_token and self.current_token.type != 'RBRACE':
                node.add_child(self.statement())
            if self.current_token and self.current_token.type == 'RBRACE':
                self.next_token()  # Consume '}'
        return node

    def statement(self):
        if self.current_token.type in ('VAR', 'LET', 'CONST'):
            return self.var_declaration()
        elif self.current_token.type == 'WHILE':
            return self.while_statement()
        elif self.current_token.type == 'FOR':
            return self.for_statement()
        elif self.current_token.type == 'IF':
            return self.if_statement()
        elif self.current_token.type == 'FUNCTION':
            return self.function_declaration()
        elif self.current_token.type == 'RETURN':
            return self.return_statement()
        else:
            return self.expression_statement()

    def peek_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        else:
            return None
