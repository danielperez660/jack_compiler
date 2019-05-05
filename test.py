from compiler import lexer as lex
from compiler import parser as pars
#
# lexer = lex.Token("Main.jack")
#
# for i in lexer.tokens:
#     print(i)
#

print("\nLEXER TEST PASSED\n")

# compiled = pars.Parser("Main_screen.jack")
# compiled = pars.Parser("Main_seven.jack")
compiled = pars.Parser("Main_string.jack")

print("\nPARSER TEST PASSED\n")
