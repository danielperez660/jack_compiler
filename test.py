from compiler import lexer as lex
from compiler import parser as pars

lexer = lex.Token("Main2.jack")

print("\nLEXER TEST PASSED\n")

compiled = pars.Parser("Main2.jack")

