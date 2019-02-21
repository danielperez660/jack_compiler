import lexer as lex

compiled = lex.Token("Main.jack")

print(compiled.get_next_token())
print(compiled.peek_next_token())

