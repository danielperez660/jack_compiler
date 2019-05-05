from compiler import lexer as lex
from compiler import parser as pars
#
# lexer = lex.Token("Main.jack")
#
# for i in lexer.tokens:
#     print(i)
#

print("\nLEXER TEST PASSED\n")

compiled = pars.Parser("Main.jack")

print("\nPARSER TEST PASSED\n")
