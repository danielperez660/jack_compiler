from compiler import lexer as lex
from compiler import symbolTable as sT


class Parser:

    # TODO - fix the symbol table class because im stupid and lazy

    def __init__(self, file):
        self.Tokens = lex.Token(file)
        print("PARSER INITIALISED")
        self.table = sT.SymbolTable()
        self.classDeclar()
        self.table.print()

    @staticmethod
    def ok(token):
        print(token[0] + ": OK")

    @staticmethod
    def error(token, message):
        print("error in line", token[1], "at or near " + token[0] + ", " + message)
        exit(0)

    def classDeclar(self):
        token = self.Tokens.get_next_token()

        if token[0] == 'class':
            self.ok(token)
        else:
            self.error(token, "'class' expected")

        token = self.Tokens.get_next_token()

        if token[2] == 'identifier':
            self.ok(token)
        else:
            self.error(token, "'identifier' expected")

        token = self.Tokens.get_next_token()

        if token[0] == '{':
            self.ok(token)
        else:
            self.error(token, "'{' expected")

        while self.Tokens.peek_next_token()[0] != '}':
            self.memberDeclar()

        token = self.Tokens.get_next_token()

        if token[0] == '}':
            self.ok(token)
        else:
            self.error(token, "'}' expected")

    def memberDeclar(self):

        token = self.Tokens.peek_next_token()

        if token[0] == 'static' or token[0] == 'field':
            self.classVarDeclar()
        elif token[0] == 'constructor' or token[0] == 'function' or token[0] == 'method':
            self.subroutineDeclar()
        else:
            self.error(token, "classVarDeclar or SubroutineDeclar expected")

    def classVarDeclar(self):

        token = self.Tokens.get_next_token()
        class_type = token[0]

        if token[0] == 'static' or token[0] == 'field':
            self.ok(token)
        else:
            self.error(token, "'static' or 'field' expected")

        token = self.Tokens.peek_next_token()

        if token[0] == 'int' or token[0] == 'char' or token[0] == 'boolean' or token[2] == 'identifier':
            self.type()
        else:
            self.error(token, "valid type or identifier expected")

        token = self.Tokens.get_next_token()

        if token[2] == 'identifier':
            self.ok(token)

            if self.table.find_symbol(token, 'class'):
                self.table.add_symbol(token, 'class', class_type)
            else:
                self.error(token, "redeclaration of identifier")
        else:
            self.error(token, "identifier expected")

        token = self.Tokens.peek_next_token()

        if token[0] == ',':
            while self.Tokens.peek_next_token()[0] != ';':
                token = self.Tokens.get_next_token()

                if token[0] == ',':
                    self.ok(token)
                else:
                    self.error(token, "',' expected")

                token = self.Tokens.get_next_token()

                if token[2] == 'identifier':
                    self.ok(token)
                else:
                    self.error(token, "identifier expected")

        token = self.Tokens.get_next_token()

        if token[0] == ';':
            self.ok(token)
        else:
            self.error(token, "';' expected")

    def type(self):

        token = self.Tokens.get_next_token()

        if token[0] == 'int' or token[0] == 'char' or token[0] == 'boolean' or token[2] == 'identifier':
            self.ok(token)
        else:
            self.error(token, "valid type or identifier expected")

    def subroutineDeclar(self):

        token = self.Tokens.get_next_token()

        if token[0] == 'constructor' or token[0] == 'function' or token[0] == 'method':
            self.ok(token)
        else:
            self.error(token, "'constructor' or 'function' or 'method' expected")

        token = self.Tokens.peek_next_token()

        if token[0] == 'int' or token[0] == 'char' or token[0] == 'boolean' or token[2] == 'identifier':
            self.type()
        elif token[0] == 'void':
            token = self.Tokens.get_next_token()
            self.ok(token)
        else:
            self.error(token, "valid type expected")

        token = self.Tokens.get_next_token()

        if token[2] == 'identifier':
            self.ok(token)
        else:
            self.error(token, "identifier expected")

        token = self.Tokens.get_next_token()

        if token[0] == '(':
            self.ok(token)
        else:
            self.error(token, "'(' expected")

        token = self.Tokens.peek_next_token()

        if token[0] == 'int' or token[0] == 'char' or token[0] == 'boolean' or token[2] == 'identifier':
            self.paramList()

        token = self.Tokens.get_next_token()

        if token[0] == ')':
            self.ok(token)
        else:
            self.error(token, "')' expected")

        token = self.Tokens.peek_next_token()

        if token[0] == '{':
            self.subroutineBody()
        else:
            self.error(token, "'{' expected")

    def paramList(self):

        token = self.Tokens.peek_next_token()

        if token[0] == ')':
            return

        if token[0] == 'int' or token[0] == 'char' or token[0] == 'boolean' or token[2] == 'identifier':
            self.type()
        else:
            self.error(token, "valid type expected")

        token = self.Tokens.get_next_token()

        if token[2] == 'identifier':
            self.ok(token)

            if self.table.find_symbol(token, 'method'):
                self.table.add_symbol(token, 'method', 'argument')
            else:
                self.error(token, "redeclaration of identifier")
        else:
            self.error(token, "identifier expected")

        token = self.Tokens.peek_next_token()

        if token[0] == ',':
            while self.Tokens.peek_next_token()[0] != ')':
                token = self.Tokens.get_next_token()

                if token[0] == ',':
                    self.ok(token)
                else:
                    self.error(token, "',' expected")

                token = self.Tokens.peek_next_token()

                if token[0] == 'int' or token[0] == 'char' or token[0] == 'boolean' or token[2] == 'identifier':
                    self.type()
                else:
                    self.error(token, "valid type expected")

                token = self.Tokens.get_next_token()

                if token[2] == 'identifier':
                    self.ok(token)

                    if self.table.find_symbol(token, 'method'):
                        self.table.add_symbol(token, 'method', 'argument')
                    else:
                        self.error(token, "redeclaration of identifier")
                else:
                    self.error(token, "identifier expected")

    def subroutineBody(self):

        token = self.Tokens.get_next_token()

        if token[0] == '{':
            self.ok(token)
        else:
            self.error(token, "'{' expected")

        while self.Tokens.peek_next_token()[0] != '}':
            token = self.Tokens.peek_next_token()

            if token[0] == 'var':
                self.varDeclarStatement()
            elif token[0] == 'let':
                self.letStatement()
            elif token[0] == 'if':
                self.ifStatement()
            elif token[0] == 'while':
                self.whileStatement()
            elif token[0] == 'do':
                self.doStatement()
            elif token[0] == 'return':
                self.returnStatement()
            else:
                self.error(token, "statement expected")

    def statement(self):

        token = self.Tokens.peek_next_token()

        if token[0] == 'var':
            self.varDeclarStatement()
        elif token[0] == 'let':
            self.letStatement()
        elif token[0] == 'if':
            self.ifStatement()
        elif token[0] == 'while':
            self.whileStatement()
        elif token[0] == 'do':
            self.doStatement()
        elif token[0] == 'return':
            self.returnStatement()
        else:
            self.error(token, "statement expected")

    def varDeclarStatement(self):

        token = self.Tokens.get_next_token()

        if token[0] == 'var':
            self.ok(token)
        else:
            self.error(token, "'var' expected")

        token = self.Tokens.peek_next_token()

        if token[0] == 'int' or token[0] == 'char' or token[0] == 'boolean' or token[2] == 'identifier':
            self.type()
        else:
            self.error(token, "valid type expected")

        token = self.Tokens.get_next_token()

        if token[2] == 'identifier':
            self.ok(token)

            if self.table.find_symbol(token, 'method'):
                self.table.add_symbol(token, 'method', 'var')
            else:
                self.error(token, "redeclaration of identifier")
        else:
            self.error(token, "'identifier' expected")

        token = self.Tokens.peek_next_token()

        if token[0] == ',':
            while token[0] != ';':
                token = self.Tokens.get_next_token()

                if token[0] == ',':
                    self.ok(token)
                else:
                    self.error(token, "',' expected")

                token = self.Tokens.get_next_token()

                if token[2] == 'identifier':
                    self.ok(token)
                else:
                    self.error(token, "identifier expected")

                token = self.Tokens.peek_next_token()

        token = self.Tokens.get_next_token()

        if token[0] == ';':
            self.ok(token)
        else:
            self.error(token, "';' expected")

    def letStatement(self):

        token = self.Tokens.get_next_token()

        if token[0] == 'let':
            self.ok(token)
        else:
            self.error(token, "'let' expected")

        token = self.Tokens.get_next_token()

        if token[2] == 'identifier':
            self.ok(token)
        else:
            self.error(token, "identifier expected")

        token = self.Tokens.peek_next_token()

        if token[0] == '[':
            token = self.Tokens.get_next_token()
            self.ok(token)

            token = self.Tokens.peek_next_token()

            if token[0] == '-' or token[0] == '~' or token[0] == '-' or \
                    token[2] == 'integerConstant' or token[2] == 'identifier' \
                    or token[2] == 'stringLiteral' or token[0] == 'true' \
                    or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                    or token[0] == '(':
                self.expression()
            else:
                self.error(token, "expression expected")

            token = self.Tokens.get_next_token()

            if token[0] != ']':
                self.error(token, "']' expected")

        token = self.Tokens.get_next_token()

        if token[0] == '=':
            self.ok(token)
        else:
            self.error(token, "'=' expected")

        token = self.Tokens.peek_next_token()

        if token[0] == '-' or token[0] == '~' or token[0] == '-' or \
                token[2] == 'integerConstant' or token[2] == 'identifier' \
                or token[2] == 'stringLiteral' or token[0] == 'true' \
                or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                or token[0] == '(':
            self.expression()

        token = self.Tokens.get_next_token()

        if token[0] == ';':
            self.ok(token)
        else:
            self.error(token, "';' expected")

    def ifStatement(self):

        token = self.Tokens.get_next_token()

        if token[0] == 'if':
            self.ok(token)
        else:
            self.error(token, "'if' expected")

        token = self.Tokens.get_next_token()

        if token[0] == '(':
            self.ok(token)
        else:
            self.error(token, "'(' expected")

        token = self.Tokens.peek_next_token()

        if token[0] == '-' or token[0] == '~' or token[0] == '-' or \
                token[2] == 'integerConstant' or token[2] == 'identifier' \
                or token[2] == 'stringLiteral' or token[0] == 'true' \
                or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                or token[0] == '(':
            self.expression()
        else:
            self.error(token, "expression expected")

        token = self.Tokens.get_next_token()

        if token[0] == ')':
            self.ok(token)
        else:
            self.error(token, "')' expected")

        token = self.Tokens.get_next_token()

        if token[0] == '{':
            self.ok(token)
        else:
            self.error(token, "'{' expected")

        token = self.Tokens.peek_next_token()

        while token[0] != '}':
            if token[0] == 'var':
                self.varDeclarStatement()
            elif token[0] == 'let':
                self.letStatement()
            elif token[0] == 'if':
                self.ifStatement()
            elif token[0] == 'while':
                self.whileStatement()
            elif token[0] == 'do':
                self.doStatement()
            elif token[0] == 'return':
                self.returnStatement()
            else:
                self.error(token, "statement expected")

            token = self.Tokens.peek_next_token()

        token = self.Tokens.get_next_token()

        if token[0] == '}':
            self.ok(token)
        else:
            self.error(token, "'}' expected")

        token = self.Tokens.peek_next_token()

        if token[0] == 'else':

            token = self.Tokens.get_next_token()

            if token[0] == 'else':
                self.ok(token)

            token = self.Tokens.get_next_token()

            if token[0] == '{':
                self.ok(token)
            else:
                self.error(token, "'{' expected")

            token = self.Tokens.peek_next_token()

            while token[0] != '}':
                if token[0] == 'var':
                    self.varDeclarStatement()
                elif token[0] == 'let':
                    self.letStatement()
                elif token[0] == 'if':
                    self.ifStatement()
                elif token[0] == 'while':
                    self.whileStatement()
                elif token[0] == 'do':
                    self.doStatement()
                elif token[0] == 'return':
                    self.returnStatement()
                else:
                    self.error(token, "statement expected")

                token = self.Tokens.peek_next_token()

            token = self.Tokens.get_next_token()

            if token[0] == '}':
                self.ok(token)
            else:
                self.error(token, "'}' expected")

    def whileStatement(self):

        token = self.Tokens.get_next_token()

        if token[0] == 'while':
            self.ok(token)
        else:
            self.error(token, "'while' expected")

        token = self.Tokens.get_next_token()

        if token[0] == '(':
            self.ok(token)
        else:
            self.error(token, "'(' expected")

        token = self.Tokens.peek_next_token()

        if token[0] == '-' or token[0] == '~' or token[0] == '-' or \
                token[2] == 'integerConstant' or token[2] == 'identifier' \
                or token[2] == 'stringLiteral' or token[0] == 'true' \
                or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                or token[0] == '(':
            self.expression()
        else:
            self.error(token, "expression expected")

        token = self.Tokens.get_next_token()

        if token[0] == ')':
            self.ok(token)
        else:
            self.error(token, "')' expected")

        token = self.Tokens.get_next_token()

        if token[0] == '{':
            self.ok(token)
        else:
            self.error(token, "'{' expected")

        token = self.Tokens.peek_next_token()

        while token[0] != '}':
            if token[0] == 'var':
                self.varDeclarStatement()
            elif token[0] == 'let':
                self.letStatement()
            elif token[0] == 'if':
                self.ifStatement()
            elif token[0] == 'while':
                self.whileStatement()
            elif token[0] == 'do':
                self.doStatement()
            elif token[0] == 'return':
                self.returnStatement()
            else:
                self.error(token, "statement expected")

            token = self.Tokens.peek_next_token()

        token = self.Tokens.get_next_token()

        if token[0] == '}':
            self.ok(token)
        else:
            self.error(token, "'}' expected")

    def doStatement(self):

        token = self.Tokens.get_next_token()

        if token[0] == 'do':
            self.ok(token)
        else:
            self.error(token, "'do' expected")

        token = self.Tokens.peek_next_token()

        if token[2] == 'identifier':
            self.subroutineCall()
        else:
            self.error(token, "'identifier' expected")

        token = self.Tokens.get_next_token()

        if token[0] == ';':
            self.ok(token)
        else:
            self.error(token, "';' expected")

    def subroutineCall(self):

        token = self.Tokens.get_next_token()

        if token[2] == 'identifier':
            self.ok(token)
        else:
            self.error(token, "'identifier' expected")

        token = self.Tokens.peek_next_token()

        if token[0] == '.':

            token = self.Tokens.get_next_token()

            if token[0] == '.':
                self.ok(token)

            token = self.Tokens.get_next_token()

            if token[2] == 'identifier':
                self.ok(token)
            else:
                self.error(token, "identifier expected")

        token = self.Tokens.get_next_token()

        if token[0] == '(':
            self.ok(token)
        else:
            self.error(token, "'(' expected")

        token = self.Tokens.peek_next_token()

        if token[0] == '-' or token[0] == '~' or token[0] == '-' or \
                token[2] == 'integerConstant' or token[2] == 'identifier' \
                or token[2] == 'stringLiteral' or token[0] == 'true' \
                or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                or token[0] == '(':
            self.expression()

        token = self.Tokens.get_next_token()

        if token[0] == ')':
            self.ok(token)
        else:
            self.error(token, "')' expected")

    def expressionList(self):

        token = self.Tokens.peek_next_token()

        if token[0] == '-' or token[0] == '~' or token[0] == '-' or \
                token[2] == 'integerConstant' or token[2] == 'identifier' \
                or token[2] == 'stringLiteral' or token[0] == 'true' \
                or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                or token[0] == '(':
            self.expression()
        else:
            return

        token = self.Tokens.peek_next_token()

        if token[0] == ',':
            while token[0] == ',':
                token = self.Tokens.get_next_token()

                if token[0] == ',':
                    self.ok(token)
                else:
                    self.error(token, "',' expected")

                token = self.Tokens.peek_next_token()

                if token[0] == '-' or token[0] == '~' or token[0] == '-' or \
                        token[2] == 'integerConstant' or token[2] == 'identifier' \
                        or token[2] == 'stringLiteral' or token[0] == 'true' \
                        or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                        or token[0] == '(':
                    self.expression()
                else:
                    self.error(token, "expression expected")

                token = self.Tokens.peek_next_token()

    def returnStatement(self):

        token = self.Tokens.get_next_token()

        if token[0] == 'return':
            self.ok(token)
        else:
            self.error(token, "'return' expected")

        token = self.Tokens.peek_next_token()

        if token[0] == '-' or token[0] == '~' or token[0] == '-' or \
                token[2] == 'integerConstant' or token[2] == 'identifier' \
                or token[2] == 'stringLiteral' or token[0] == 'true' \
                or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                or token[0] == '(':
            self.expression()

        token = self.Tokens.get_next_token()

        if token[0] == ';':
            self.ok(token)
        else:
            self.error(token, "';' expected")

    def expression(self):

        token = self.Tokens.peek_next_token()

        if token[0] == '-' or token[0] == '~' or token[0] == '-' or \
                token[2] == 'integerConstant' or token[2] == 'identifier' \
                or token[2] == 'stringLiteral' or token[0] == 'true' \
                or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                or token[0] == '(':
            self.relationalExpression()
        else:
            self.error(token, "relationalExpression expected")

        token = self.Tokens.peek_next_token()

        if token[0] == '&' or token[0] == '|':
            while token[0] == '&' or token[0] == '|':

                token = self.Tokens.get_next_token()

                if token[0] == '&' or token[0] == '|':
                    self.ok(token)
                else:
                    self.error(token, "'|' or '&' expected")

                token = self.Tokens.peek_next_token()

                if token[0] == '-' or token[0] == '~' or token[0] == '-' or \
                        token[2] == 'integerConstant' or token[2] == 'identifier' \
                        or token[2] == 'stringLiteral' or token[0] == 'true' \
                        or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                        or token[0] == '(':
                    self.relationalExpression()
                else:
                    self.error(token, "expression expected")

                token = self.Tokens.peek_next_token()

    def relationalExpression(self):

        token = self.Tokens.peek_next_token()

        if token[0] == '-' or token[0] == '~' or token[0] == '-' or \
                token[2] == 'integerConstant' or token[2] == 'identifier' \
                or token[2] == 'stringLiteral' or token[0] == 'true' \
                or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                or token[0] == '(':
            self.arithmeticExpression()
        else:
            self.error(token, "arithmeticExpression expected")

        token = self.Tokens.peek_next_token()

        if token[0] == '=' or token[0] == '<' or token[0] == '>':
            while token[0] == '=' or token[0] == '<' or token[0] == '>':

                token = self.Tokens.get_next_token()

                if token[0] == '=' or token[0] == '<' or token[0] == '>':
                    self.ok(token)
                else:
                    self.error(token, "'=' or '<' or '>' expected")

                token = self.Tokens.peek_next_token()

                if token[0] == '-' or token[0] == '~' or token[0] == '-' or \
                        token[2] == 'integerConstant' or token[2] == 'identifier' \
                        or token[2] == 'stringLiteral' or token[0] == 'true' \
                        or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                        or token[0] == '(':
                    self.arithmeticExpression()
                else:
                    self.error(token, "arithmeticExpression expected")

                token = self.Tokens.peek_next_token()

    def arithmeticExpression(self):

        token = self.Tokens.peek_next_token()

        if token[0] == '-' or token[0] == '~' or token[0] == '-' or \
                token[2] == 'integerConstant' or token[2] == 'identifier' \
                or token[2] == 'stringLiteral' or token[0] == 'true' \
                or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                or token[0] == '(':
            self.term()
        else:
            self.error(token, "term expected")

        token = self.Tokens.peek_next_token()

        if token[0] == '+' or token[0] == '-':
            while token[0] == '+' or token[0] == '-':

                token = self.Tokens.get_next_token()

                if token[0] == '+' or token[0] == '-':
                    self.ok(token)
                else:
                    self.error(token, "'+' or '-' expected")

                token = self.Tokens.peek_next_token()

                if token[0] == '-' or token[0] == '~' or token[0] == '-' or \
                        token[2] == 'integerConstant' or token[2] == 'identifier' \
                        or token[0] == '(':
                    self.term()
                else:
                    self.error(token, "term expected")

                token = self.Tokens.peek_next_token()

    def term(self):

        token = self.Tokens.peek_next_token()

        if token[0] == '-' or token[0] == '~' or token[0] == '-' or \
                token[2] == 'integerConstant' or token[2] == 'identifier' \
                or token[2] == 'stringLiteral' or token[0] == 'true' \
                or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                or token[0] == '(':
            self.factor()
        else:
            self.error(token, "factor expected")

        token = self.Tokens.peek_next_token()

        if token[0] == '*' or token[0] == '/':
            while token[0] == '*' or token[0] == '/':

                token = self.Tokens.get_next_token()

                if token[0] == '*' or token[0] == '/':
                    self.ok(token)
                else:
                    self.error(token, "'*' or '/' expected")

                token = self.Tokens.peek_next_token()

                if token[0] == '-' or token[0] == '~' or token[0] == '-' or \
                        token[2] == 'integerConstant' or token[2] == 'identifier' \
                        or token[2] == 'stringLiteral' or token[0] == 'true' \
                        or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                        or token[0] == '(':
                    self.factor()
                else:
                    self.error(token, "factor expected")

                token = self.Tokens.peek_next_token()

    def factor(self):
        token = self.Tokens.peek_next_token()

        if token[0] == '-' or token[0] == '~' or token[0] == '-':
            token = self.Tokens.get_next_token()
            self.ok(token)

        token = self.Tokens.peek_next_token()

        if token[2] == 'integerConstant' or token[2] == 'identifier' \
                or token[2] == 'stringLiteral' or token[0] == 'true' \
                or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                or token[0] == '(':
            self.operand()
        else:
            self.error(token, "operand expected")

    def operand(self):
        token = self.Tokens.get_next_token()

        if token[2] == 'integerConstant' or token[2] == 'identifier' \
                or token[2] == 'stringLiteral' or token[0] == 'true' \
                or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                or token[0] == '(':
            self.ok(token)
        else:
            self.error(token, "integerConstant or Identifier or stringLiteral or 'true' or 'false' or 'null' or "
                              "'this' expected")

        if token[2] == 'identifier':
            token = self.Tokens.peek_next_token()

            if token[0] == '.':
                if token[0] == '.':
                    token = self.Tokens.get_next_token()
                    self.ok(token)
                else:
                    self.error(token, "'.' expected")

                token = self.Tokens.get_next_token()

                if token[2] == 'identifier':
                    self.ok(token)
                else:
                    self.error(token, "identifier expected")

            token = self.Tokens.peek_next_token()

            if token[0] == '[':
                token = self.Tokens.get_next_token()

                if token[0] == '[':
                    self.ok(token)
                else:
                    self.error(token, "'[' expected")

                token = self.Tokens.peek_next_token()

                if token[0] == '-' or token[0] == '~' or token[0] == '-' or \
                        token[2] == 'integerConstant' or token[2] == 'identifier' \
                        or token[2] == 'stringLiteral' or token[0] == 'true' \
                        or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                        or token[0] == '(':
                    self.expression()
                else:
                    self.error(token, "expression expected")

                token = self.Tokens.get_next_token()

                if token[0] == ']':
                    self.ok(token)
                else:
                    self.error(token, "']' expected")

            if token[0] == '(':
                token = self.Tokens.get_next_token()

                if token[0] == '(':
                    self.ok(token)
                else:
                    self.error(token, "'(' expected")

                token = self.Tokens.peek_next_token()

                if token[0] == '-' or token[0] == '~' or token[0] == '-' or \
                        token[2] == 'integerConstant' or token[2] == 'identifier' \
                        or token[2] == 'stringLiteral' or token[0] == 'true' \
                        or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                        or token[0] == '(':
                    self.expressionList()
                else:
                    self.error(token, "expressionList expected")

                token = self.Tokens.get_next_token()

                if token[0] == ')':
                    self.ok(token)
                else:
                    self.error(token, "')' expected")

        if token[0] == '(':
            token = self.Tokens.get_next_token()

            if token[0] == '(':
                self.ok(token)
            else:
                self.error(token, "'(' expected")

            token = self.Tokens.peek_next_token()

            if token[0] == '-' or token[0] == '~' or token[0] == '-' or \
                    token[2] == 'integerConstant' or token[2] == 'identifier' \
                    or token[2] == 'stringLiteral' or token[0] == 'true' \
                    or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                    or token[0] == '(':
                self.expression()
            else:
                self.error(token, "expression expected")

            token = self.Tokens.get_next_token()

            if token[0] == ')':
                self.ok(token)
            else:
                self.error(token, "')' expected")
