import lexer as lex

compiled = lex.Lexer("Main.jack")

print(compiled.peek_next_token())
print(compiled.get_next_token())
