class AnalisadorSemanticoJS:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = {
            'input': {'type': 'function', 'params': []},
            'console.log': {'type': 'function', 'params': None},  # Permite múltiplos argumentos
            'prompt': {'type': 'function', 'params': ['message']},
            'true': {'type': 'boolean'},
            'false': {'type': 'boolean'}
        }
        self.errors = []

    def analyze(self):
        self.visit(self.ast)
        if self.errors:
            for error in self.errors:
                print("Erro Semântico:", error)
        else:
            print("Análise Semântica concluída sem erros.")

    def visit(self, node):
        method_name = f'visit_{node.type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Program(self, node):
        self.generic_visit(node)

    def visit_VarDeclaration(self, node):
        identifier = node.children[0]
        if identifier.value in self.symbol_table:
            self.errors.append(f"Variável '{identifier.value}' já declarada.")
        else:
            self.symbol_table[identifier.value] = {'type': 'variable', 'initialized': False}
        if len(node.children) > 1:
            self.visit(node.children[1])
            self.symbol_table[identifier.value]['initialized'] = True

    def visit_FunctionDeclaration(self, node):
        identifier = node.children[0]
        if identifier.value in self.symbol_table:
            self.errors.append(f"Função '{identifier.value}' já declarada.")
        else:
            self.symbol_table[identifier.value] = {'type': 'function', 'params': [], 'body': node.children[2]}
        params_node = node.children[1]
        for param in params_node.children:
            self.symbol_table[identifier.value]['params'].append(param.value)

    def visit_FunctionCall(self, node):
        identifier = node.value
        if identifier not in self.symbol_table or self.symbol_table[identifier]['type'] != 'function':
            self.errors.append(f"Chamada a função não declarada '{identifier}'.")
        else:
            params_count = len(node.children)
            if self.symbol_table[identifier]['params'] is not None and params_count != len(self.symbol_table[identifier]['params']):
                self.errors.append(f"Função '{identifier}' chamada com número incorreto de argumentos.")

    def visit_Identifier(self, node):
        if node.value not in self.symbol_table:
            self.errors.append(f"Uso de variável não declarada '{node.value}'.")
        else:
            if not self.symbol_table[node.value]['initialized']:
                self.errors.append(f"Uso de variável não inicializada '{node.value}'.")

    def visit_AssignmentExpression(self, node):
        identifier = node.children[0]
        if identifier.value not in self.symbol_table:
            self.errors.append(f"Atribuição a variável não declarada '{identifier.value}'.")
        else:
            self.visit(node.children[1])
            self.symbol_table[identifier.value]['initialized'] = True

    def visit_ReturnStatement(self, node):
        self.visit(node.children[0])

    def visit_BinaryExpression(self, node):
        self.visit(node.children[0])
        self.visit(node.children[1])

    def visit_IfStatement(self, node):
        self.visit(node.children[0])
        self.visit(node.children[1])
        if len(node.children) > 2:
            self.visit(node.children[2])

    def visit_WhileStatement(self, node):
        self.visit(node.children[0])
        self.visit(node.children[1])

    def visit_ForStatement(self, node):
        self.visit(node.children[0])
        self.visit(node.children[1])
        self.visit(node.children[2])
        self.visit(node.children[3])
