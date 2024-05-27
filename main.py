from analiseLexica import AnalisadorLexicoJS
from analiseSintatica import AnalisadorSintaticoJS
from analiseSemantica import AnalisadorSemanticoJS
from geradorDeCodigo import GeradorDeCodigoPythonFromJS

code = '''

const n = 10;
if (n > 5) {
    console.log("Maior que 5");
} else {
    console.log("Menor ou igual a 5");

}

'''

# Analise Léxica
lexer = AnalisadorLexicoJS()
tokens = lexer.tokenize(code)
print("Tokens:", tokens)

# Analise Sintática
parser = AnalisadorSintaticoJS(tokens)
ast = parser.parse()
print("AST:", ast)

# Analise Semântica
analyzer = AnalisadorSemanticoJS(ast)
analyzer.analyze()
 
# Gerador de Código
generator = GeradorDeCodigoPythonFromJS(ast)
python_code = generator.generate()
print("Python Code:")
print(python_code)
