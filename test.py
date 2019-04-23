from compiler import lexer as lex
from compiler import parser as pars

lexer = lex.Token("Main2.jack")

for i in lexer.tokens:
    print(i)

# compiled = pars.Parser("Main2.jack")

