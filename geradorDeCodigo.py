class GeradorDeCodigoPythonFromJS:
    def __init__(self, ast):
        self.ast = ast
        self.code = []

    def generate(self):
        self.visit(self.ast)
        return '\n'.join([line for line in self.code if line is not None])

    def visit(self, node):
        method_name = f'visit_{node.type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for child in node.children:
            self.visit(child)
            
    def visit_Program(self, node):
        self.generic_visit(node)

    def visit_ArrayLiteral(self, node):
        elements = [self.visit(child) for child in node.children]
        return f"[{', '.join(elements)}]"


    def visit_ArrayAccess(self, node):
        array_name = self.visit(node.children[0])
        index = self.visit(node.children[1])
        return f"{array_name}[{index}]"

    def visit_PropertyAccess(self, node):
        if node.value == "length":
            array_name = self.visit(node.children[0])
            return f"len({array_name})"
        else:
            raise NotImplementedError(f"Propriedade não suportada: {node.value}")

    def visit_VarDeclaration(self, node):
        identifier = node.children[0].value
        if len(node.children) > 1:  # Se houver inicialização
            value = self.visit(node.children[1])
            self.code.append(f"{identifier} = {value}")
        else:
            self.code.append(f"{identifier} = None")

    def visit_FunctionDeclaration(self, node):
        identifier = node.children[0].value
        params = ', '.join(child.value for child in node.children[1].children)
        self.code.append(f"def {identifier}({params}):")
        self.visit_Block(node.children[2])

    def visit_Block(self, node, indent=0):
        block_code = self.generate_block_code(node, indent)
        self.code.extend(block_code)

    def generate_block_code(self, node, indent=0):
        block_code = []
        for child in node.children:
            result = self.visit(child)
            if result:
                block_code.append('    ' * indent + result)
        return block_code

    def visit_FunctionCall(self, node):
        function_name = node.value
        args = ', '.join(self.visit(arg) for arg in node.children)
        if function_name == "console.log":
            return f"print({args})"
        return f"{function_name}({args})"

    def visit_Identifier(self, node):
        return node.value

    def visit_Number(self, node):
        return str(node.value)

    def visit_String(self, node):
        return f'"{node.value}"'

    def visit_Boolean(self, node):
        return str(node.value).lower()

    def visit_AssignmentExpression(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        return f"{left} = {right}"

    def visit_ReturnStatement(self, node):
        return f"return {self.visit(node.children[0])}"

    def visit_BinaryExpression(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        return f"{left} {node.value} {right}"

    def visit_LogicalExpression(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        operator = 'and' if node.value == '&&' else 'or'
        return f"{left} {operator} {right}"

    def visit_IfStatement(self, node):
        condition = self.visit(node.children[0])
        self.code.append(f"if {condition}:")
        self.visit_Block(node.children[1], 1)
        if len(node.children) > 2:
            self.code.append(f"else:")
            self.visit_Block(node.children[2], 1)

    def visit_WhileStatement(self, node):
        condition = self.visit(node.children[0])
        self.code.append(f"while {condition}:")
        self.visit_Block(node.children[1], 1)

    def visit_ForStatement(self, node):
        init = self.visit(node.children[0])
        condition = self.visit(node.children[1])
        increment = self.visit(node.children[2])
        self.code.append(init)
        self.code.append(f"while {condition}:")
        block_code = self.generate_block_code(node.children[3], 1)
        if block_code:
            self.code.extend(block_code)
        self.code.append('    ' + increment)

    def visit_ExpressionStatement(self, node):
        expr = self.visit(node.children[0])
        return expr
