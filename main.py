from analiseLexica import AnalisadorLexicoJS
from analiseSintatica import AnalisadorSintaticoJS
from analiseSemantica import AnalisadorSemanticoJS
from geradorDeCodigo import GeradorDeCodigoPythonFromJS

example01 = '''
var a = prompt("Digite um número");
var b = prompt("Digite outro número");

var soma = a + b;
console.log(soma);

''' # OK

example02 = '''
for (var i = 0; i < 10; i = i + 1) {
    console.log(i);
}

''' # OK

example03 = '''
var decider = 5;

if (decider > 10) {
    console.log("É maior que 10");
    console.log("Ainda bem!");
} else {
    console.log("É menor ou igual a 10");
}

''' # OK



example04 = '''
function soma(a, b) {
    return a + b;

}
'''

example05 = '''
const booleana = true;
const numero = 10;

if (booleana || numero > 5) {
    console.log("Verdadeiro ou numero maior que 5");
} else {
    console.log("Falso");
}
'''
example06 = '''
const myArray = [1, 2, 3, 4, 5];

for (var i = 0; i < myArray.length; i = i + 1) {
    console.log(myArray[i]);
}
'''

code = example06

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
