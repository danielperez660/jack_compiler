import lexer as lex

compiled = lex.Lexer("test.txt")

print(compiled.peek_next_token())
print(compiled.get_next_token())
