class GeradorDeCodigoPythonFromJS:
    def __init__(self, ast):
        self.ast = ast
        self.code = []

    def generate(self):
        self.visit(self.ast)
        return '\n'.join([line for line in self.code if line is not None])

    def visit(self, node, indent=0):
        method_name = f'visit_{node.type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, indent)

    def generic_visit(self, node, indent=0):
        for child in node.children:
            self.visit(child, indent)

    def visit_Program(self, node, indent=0):
        self.generic_visit(node, indent)

    def visit_ArrayLiteral(self, node, indent=0):
        elements = [self.visit(child, indent) for child in node.children]
        return f"[{', '.join(elements)}]"

    def visit_ArrayAccess(self, node, indent=0):
        array_name = self.visit(node.children[0], indent)
        index = self.visit(node.children[1], indent)
        return f"{array_name}[{index}]"

    def visit_PropertyAccess(self, node, indent=0):
        if node.value == "length":
            array_name = self.visit(node.children[0], indent)
            return f"len({array_name})"
        else:
            raise NotImplementedError(f"Propriedade não suportada: {node.value}")

    def visit_VarDeclaration(self, node, indent=0):
        identifier = node.children[0].value
        if len(node.children) > 1:  # Se houver inicialização
            value = self.visit(node.children[1], indent)
            self.code.append(f"{'    ' * indent}{identifier} = {value}")
        else:
            self.code.append(f"{'    ' * indent}{identifier} = None")

    def visit_FunctionDeclaration(self, node, indent=0):
        identifier = node.children[0].value
        params = ', '.join(child.value for child in node.children[1].children)
        self.code.append(f"{'    ' * indent}def {identifier}({params}):")
        self.visit_Block(node.children[2], indent + 1)

    def visit_Block(self, node, indent=0):
        block_code = self.generate_block_code(node, indent)
        self.code.extend(block_code)

    def generate_block_code(self, node, indent=0):
        block_code = []
        for child in node.children:
            result = self.visit(child, indent)
            if result is not None:
                block_code.append(f"{'    ' * indent}{result}")
        return block_code

    def visit_FunctionCall(self, node, indent=0):
        function_name = node.value
        args = ', '.join(self.visit(arg, indent) for arg in node.children)
        if function_name == "console.log":
            return f"print({args})"
        elif function_name == "prompt":
            return f"input({args})"
        else:
            return f"{function_name}({args})"

    def visit_Identifier(self, node, indent=0):
        return node.value

    def visit_Number(self, node, indent=0):
        return str(node.value)

    def visit_String(self, node, indent=0):
        return f'"{node.value}"'

    def visit_Boolean(self, node, indent=0):
        return 'True' if node.value else 'False'

    def visit_AssignmentExpression(self, node, indent=0):
        left = self.visit(node.children[0], indent)
        right = self.visit(node.children[1], indent)
        return f"{left} = {right}"

    def visit_ReturnStatement(self, node, indent=0):
        return f"return {self.visit(node.children[0], indent)}"

    def visit_BinaryExpression(self, node, indent=0):
        left = self.visit(node.children[0], indent)
        right = self.visit(node.children[1], indent)
        return f"{left} {node.value} {right}"

    def visit_LogicalExpression(self, node, indent=0):
        left = self.visit(node.children[0], indent)
        right = self.visit(node.children[1], indent)
        operator = 'and' if node.value == '&&' else 'or'
        return f"{left} {operator} {right}"

    def visit_IfStatement(self, node, indent=0):
        condition = self.visit(node.children[0], indent)
        self.code.append(f"{'    ' * indent}if {condition}:")
        self.visit_Block(node.children[1], indent + 1)
        if len(node.children) > 2:
            self.code.append(f"{'    ' * indent}else:")
            self.visit_Block(node.children[2], indent + 1)

    def visit_WhileStatement(self, node, indent=0):
        condition = self.visit(node.children[0], indent)
        self.code.append(f"{'    ' * indent}while {condition}:")
        self.visit_Block(node.children[1], indent + 1)

    def visit_ForStatement(self, node, indent=0):
        init = self.visit(node.children[0], indent)
        condition = self.visit(node.children[1], indent)
        increment = self.visit(node.children[2], indent)
        if init is not None:
            self.code.append(f"{'    ' * indent}{init}")
        self.code.append(f"{'    ' * indent}while {condition}:")
        self.visit_Block(node.children[3], indent + 1)
        if increment is not None:
            self.code.append(f"{'    ' * (indent + 1)}{increment}")

    def visit_ExpressionStatement(self, node, indent=0):
        expr = self.visit(node.children[0], indent)
        if expr:
            self.code.append(f"{'    ' * indent}{expr}")
