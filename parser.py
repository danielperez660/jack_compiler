from compiler import lexer as lex
from compiler import GlobalSymbolTable as sT


class Parser:

    def __init__(self, file):
        print("PARSER INITIALISED")
        self.while_counter = -1
        self.if_counter = -1

        self.array_check = False
        self.std_check = False

        div = file.split('.')
        self.file = open(div[0] + '.vm', "w")

        self.var_counter = []

        self.token_assigning = None

        self.stdLibs = ["Array.jack", "Keyboard.jack", "Math.jack", "Memory.jack",
                   "Output.jack", "Screen.jack", "String.jack", "Sys.jack"]

        self.table = sT.GlobalSymbolTable()
        self.currentClass = ""
        self.currentMethod = ""

        # Counts the number of vars per method
        self.Tokens = lex.Token(file)
        self.classDeclar()

        self.table = sT.GlobalSymbolTable()

        for i in self.stdLibs:
            print("\n" + i + "\n")
            self.Tokens = lex.Token(i)
            self.classDeclar()

        self.while_counter = -1
        self.if_counter = -1

        self.array_check = False
        self.std_check = True

        self.Tokens = lex.Token(file)
        self.classDeclar()

        self.table.print()

        self.file.close()

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

            # Generates a new table for the class and sets the current one to it
            self.table.new_table_gen(token[0], 'class', None)
            self.currentClass = token[0]

            print("Current Class: " + self.currentClass)

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
        types = ""

        if token[0] == 'static' or token[0] == 'field':
            types = token[0]
            self.ok(token)
        else:
            self.error(token, "'static' or 'field' expected")

        token = self.Tokens.peek_next_token()

        if token[0] == 'int' or token[0] == 'char' or token[0] == 'boolean' or token[2] == 'identifier':
            self.type()
        else:
            self.error(token, "valid type or identifier expected")

        token = self.Tokens.get_next_token()

        # Adds the field/static to the class symbol table or checks if already there
        if token[2] == 'identifier':
            self.ok(token)

            if self.table.find_symbol(token, 'class', self.currentClass):
                self.table.add_symbol_to(token, self.currentClass, types, self.currentClass)
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
            self.token_assigning = token
            self.table.new_table_gen(token[0], 'method', self.currentClass)
            self.currentMethod = token[0]
            print("Current method: " + self.currentMethod)

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
            counter = 0

            for i in self.var_counter:
                if i[0] == self.currentMethod and self.currentClass == i[1] and i[2] == 'var':
                    counter += 1

            self.write_function(self.currentClass + '.' + self.token_assigning[0], str(counter))
        else:
            self.error(token, "')' expected")

        token = self.Tokens.peek_next_token()

        if token[0] == '{':
            self.subroutineBody()
        else:
            self.error(token, "'{' expected")

    def paramList(self):

        token = self.Tokens.peek_next_token()

        if token[0] == 'int' or token[0] == 'char' or token[0] == 'boolean' or token[2] == 'identifier':
            self.type()
        else:
            self.error(token, "valid type expected")

        token = self.Tokens.get_next_token()

        if token[2] == 'identifier':

            self.ok(token)
            if self.table.find_symbol(token, 'method', self.currentMethod):
                self.table.add_symbol_to(token, self.currentMethod, 'argument', self.currentClass)

                self.var_counter.append([self.currentMethod, self.currentClass, 'arg'])
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

                    if self.table.find_symbol(token, 'method', self.currentMethod):
                        self.table.add_symbol_to(token, self.currentMethod, 'argument', self.currentClass)
                        self.var_counter.append([self.currentMethod, self.currentClass, 'arg'])
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

            if self.table.find_symbol(token, 'method', self.currentMethod):
                self.table.add_symbol_to(token, self.currentMethod, 'var', self.currentClass)
                self.var_counter.append([self.currentMethod, self.currentClass, 'var'])
            else:

                self.error(token, "redeclaration of identifier")

            self.ok(token)
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

                    if self.table.find_symbol(token, 'method', self.currentMethod):
                        self.table.add_symbol_to(token, self.currentMethod, 'var', self.currentClass)
                        self.var_counter.append([self.currentMethod, self.currentClass, 'var'])
                    else:
                        self.error(token, "redeclaration of identifier")

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

            # Checks to see if the identifier has been defined previously
            if self.table.find_symbol(token, 'method', self.currentMethod) and \
                    self.table.find_symbol(token, 'class', self.currentClass) \
                    and token[3] != 'Object':
                self.error(token, "variable used has not been declared")

            elif token[3] != 'Object':
                print("Initialising: " + token[0])
                self.table.initialise(token, self.currentMethod, self.currentClass)

            self.token_assigning = token
            self.ok(token)
        else:
            self.error(token, "identifier expected")

        token = self.Tokens.peek_next_token()

        if token[0] == '[':
            self.array_check = True

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

            if token[0] == ']':
                self.ok(token)
                x, y = self.table.find_symbol_id(self.token_assigning, self.currentClass, self.currentMethod)
                self.write_push(x, y)
                self.write_bool('add')
            else:
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

        if not self.array_check:
            x, y = self.table.find_symbol_id(self.token_assigning, self.currentClass, self.currentMethod)
            self.write_pop(x, y)
        else:
            self.write_pop('temp', '0')
            self.write_pop('pointer', '1')
            self.write_push('temp', '0')
            self.write_pop('that', '0')
            self.array_check = False

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
            self.if_counter += 1
            self.write_if_goto('IF_TRUE' + str(self.if_counter))
            self.write_goto('IF_FALSE' + str(self.if_counter))
            self.write_label('IF_TRUE' + str(self.if_counter))

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
                self.write_goto('IF_END' + str(self.if_counter))
                self.write_label('IF_FALSE' + str(self.if_counter))

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
                self.write_label('IF_END' + str(self.if_counter))
                self.if_counter -= 1
            else:
                self.error(token, "'}' expected")
        else:
            self.write_label('IF_FALSE' + str(self.if_counter))
            self.if_counter -= 1

    def whileStatement(self):

        token = self.Tokens.get_next_token()

        if token[0] == 'while':
            self.ok(token)
            self.while_counter += 1
            self.write_label('WHILE_EXP' + str(self.while_counter))
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
            self.write_bool('not')
            self.write_if_goto('WHILE_END' + str(self.while_counter))
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
            self.write_goto('WHILE_EXP' + str(self.while_counter))
            self.write_label('WHILE_END' + str(self.while_counter))
            self.while_counter -= 1
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
        temp = token

        if token[2] == 'identifier':
            self.subroutineCall()
        else:
            self.error(token, "'identifier' expected")

        token = self.Tokens.get_next_token()

        name = temp[0]

        if self.token_assigning is not None:
            self.ok(token)
            count = -1

            for i in self.stdLibs:
                if temp[3] == i.split('.')[0]:
                    name = temp[3]
                    print("Name change: " + name)

            for i in self.var_counter:
                if i[0] == self.token_assigning and i[1] == name and i[2] == 'arg':
                    count += 1

            if count == -1:
                count = self.table.argument_count(self.token_assigning, name)
            else:
                count += 1

            self.write_call(name + '.' + self.token_assigning, str(count))
            self.write_pop('temp', '0')
        else:
            self.write_call(name, self.table.argument_count(token[0], self.currentClass))

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
                methods = token[0]
                self.token_assigning = methods
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
            self.expressionList()

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
        ret_void = True

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
            ret_void = False
            self.expression()

        token = self.Tokens.get_next_token()

        if token[0] == ';':

            if ret_void:
                self.write_push('constant', '0')

            self.write_return()
            self.ok(token)
        else:
            self.error(token, "';' expected")

    def expression(self):

        token = self.Tokens.peek_next_token()

        if token[0] == '-' or token[0] == '~' or \
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

                temp = token

                token = self.Tokens.get_next_token()

                if token[0] == '&' or token[0] == '|':
                    self.ok(token)
                else:
                    self.error(token, "'|' or '&' expected")

                token = self.Tokens.peek_next_token()

                if token[0] == '-' or token[0] == '~' or \
                        token[2] == 'integerConstant' or token[2] == 'identifier' \
                        or token[2] == 'stringLiteral' or token[0] == 'true' \
                        or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                        or token[0] == '(':
                    self.relationalExpression()
                else:
                    self.error(token, "expression expected")

                token = self.Tokens.peek_next_token()
                if temp[0] == '&':
                    self.write_bool('and')
                elif temp[0] == '|':
                    self.write_bool('or')

    def relationalExpression(self):

        token = self.Tokens.peek_next_token()

        if token[0] == '-' or token[0] == '~' or \
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
                temp = token
                token = self.Tokens.get_next_token()

                if token[0] == '=' or token[0] == '<' or token[0] == '>':
                    self.ok(token)
                else:
                    self.error(token, "'=' or '<' or '>' expected")

                token = self.Tokens.peek_next_token()

                if token[0] == '-' or token[0] == '~' or \
                        token[2] == 'integerConstant' or token[2] == 'identifier' \
                        or token[2] == 'stringLiteral' or token[0] == 'true' \
                        or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                        or token[0] == '(':
                    self.arithmeticExpression()
                else:
                    self.error(token, "arithmeticExpression expected")

                token = self.Tokens.peek_next_token()
                if temp[0] == '<':
                    self.write_bool('lt')
                elif temp[0] == '>':
                    self.write_bool('gt')
                elif temp[0] == '=':
                    self.write_bool('eq')

    def arithmeticExpression(self):
        operation = None
        token = self.Tokens.peek_next_token()

        if token[0] == '-' or token[0] == '~' or \
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
                    operation = token[0]
                else:
                    self.error(token, "'+' or '-' expected")

                token = self.Tokens.peek_next_token()

                if token[0] == '-' or token[0] == '~' or \
                        token[2] == 'integerConstant' or token[2] == 'identifier' \
                        or token[2] == 'stringLiteral' or token[0] == 'true' \
                        or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                        or token[0] == '(':
                    self.term()
                else:
                    self.error(token, "term expected")

                token = self.Tokens.peek_next_token()

            if operation == '+':
                self.write_bool('add')
            elif operation == '-':
                self.write_bool('sub')

    def term(self):
        operation = None
        token = self.Tokens.peek_next_token()

        if token[0] == '-' or token[0] == '~' or \
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
                operation = token[0]
                token = self.Tokens.get_next_token()

                if token[0] == '*' or token[0] == '/':
                    self.ok(token)
                else:
                    self.error(token, "'*' or '/' expected")

                token = self.Tokens.peek_next_token()

                if token[0] == '-' or token[0] == '~' or \
                        token[2] == 'integerConstant' or token[2] == 'identifier' \
                        or token[2] == 'stringLiteral' or token[0] == 'true' \
                        or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                        or token[0] == '(':
                    self.factor()
                else:
                    self.error(token, "factor expected")

                token = self.Tokens.peek_next_token()

        if operation == '*':
            self.write_call('Math.multiply', '2')
        elif operation == '/':
            self.write_call('Math.divide', '2')

    def factor(self):
        token = self.Tokens.peek_next_token()
        temp = token

        if token[0] == '-' or token[0] == '~':
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

        if temp[0] == '~':
            self.write_bool('not')
        elif temp[0][0] == '-':
            self.write_bool('neg')

    def operand(self):

        token = self.Tokens.get_next_token()

        if token[2] == 'integerConstant' or token[2] == 'identifier' \
                or token[2] == 'stringLiteral' or token[0] == 'true' \
                or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                or token[0] == '(':

            self.ok(token)

            if token[2] == 'identifier' and token[3] != 'Object':
                if not self.table.init_check(token, self.currentMethod, self.currentClass):
                    if not self.table.exists(token[0]):
                        self.error(token, "variable has not been initialised or declared")

            if token[2] == 'integerConstant':
                if token[0][0] == '-':
                    self.write_push('constant', token[0][1:])
                else:
                    self.write_push('constant', token[0])
            if token[0] == 'true':
                self.write_push('constant', '0')
                self.write_bool('not')
            if token[0] == 'false':
                self.write_push('constant', '0')
            if token[2] == 'stringLiteral':
                self.write_strings(token[0])
            if token[0] == 'null':
                self.write_push('constant', '0')

        else:
            self.error(token, "integerConstant or Identifier or stringLiteral or 'true' or 'false' or 'null' or "
                              "'this' expected")

        if token[2] == 'identifier':

            temp = token
            methods = None

            token = self.Tokens.peek_next_token()

            if token[0] == '[':
                token = self.Tokens.get_next_token()
                self.ok(token)

                token = self.Tokens.peek_next_token()

                if token[2] == 'integerConstant' or token[2] == 'identifier' \
                        or token[2] == 'stringLiteral' or token[0] == 'true' \
                        or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                        or token[0] == '(':
                    self.expression()
                else:
                    self.error(token, "expression expected")

                token = self.Tokens.get_next_token()

                if token[0] == ']':
                    self.ok(token)
                    x, y = self.table.find_symbol_id(temp, self.currentClass, self.currentMethod)
                    self.write_push(x, y)
                    self.write_bool('add')
                    self.write_pop('pointer', '1')
                    self.write_push('that', '0')
                    return
                else:
                    self.error(token, "] expected")

            if token[0] == '(':
                token = self.Tokens.get_next_token()
                self.ok(token)

                token = self.Tokens.peek_next_token()

                if token[2] == 'integerConstant' or token[2] == 'identifier' \
                        or token[2] == 'stringLiteral' or token[0] == 'true' \
                        or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                        or token[0] == '(':
                    self.expressionList()
                else:
                    self.error(token, "expressionList expected")

                passed = token

                token = self.Tokens.get_next_token()

                if token[0] == ')':

                    count = self.table.argument_count(methods, temp[0])
                    self.ok(token)

                    if passed[2] == 'identifier':
                        x, y = self.table.find_symbol_id(passed, temp[0], methods)
                        self.write_push(x, y)

                    if count == '-1':
                        count = 0
                        for i in self.var_counter:
                            if i[0] == methods and i[1] == temp[0]:
                                count += 1
                                print(i)
                    self.write_call(temp[0] + '.' + methods, str(count))
                    return
                else:
                    self.error(token, ") expected")

            if token[0] == '.':
                if token[0] == '.':
                    token = self.Tokens.get_next_token()
                    self.ok(token)
                else:
                    self.error(token, "'.' expected")
                token = self.Tokens.get_next_token()

                if token[2] == 'identifier':
                    self.ok(token)
                    methods = token[0]
                else:
                    self.error(token, "identifier expected")

                token = self.Tokens.peek_next_token()

                if token[0] == '[':
                    token = self.Tokens.get_next_token()
                    self.ok(token)

                    token = self.Tokens.peek_next_token()

                    if token[2] == 'integerConstant' or token[2] == 'identifier' \
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
                        self.error(token, "] expected")

                if token[0] == '(':
                    token = self.Tokens.get_next_token()
                    self.ok(token)

                    token = self.Tokens.peek_next_token()

                    if token[2] == 'integerConstant' or token[2] == 'identifier' \
                            or token[2] == 'stringLiteral' or token[0] == 'true' \
                            or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                            or token[0] == '(':
                        self.expressionList()
                    else:
                        self.error(token, "expressionList expected")

                    # passed = token

                    token = self.Tokens.get_next_token()

                    if token[0] == ')':

                        count = self.table.argument_count(methods, temp[0])
                        self.ok(token)

                        # if passed[2] == 'identifier':
                        #     x, y = self.table.find_symbol_id(passed, temp[0], methods)
                        #     self.write_push(x, y)

                        if count == '-1':
                            count = 0
                            for i in self.var_counter:
                                if i[0] == methods and i[1] == temp[0]:
                                    count += 1
                                    print(i)
                        self.write_call(temp[0] + '.' + methods, str(count))
                        return
                    else:
                        self.error(token, ") expected")

            elif not self.table.exists(temp[0]) and token[0] != ')' and token[0] != ']':
                x, y = self.table.find_symbol_id(temp, self.currentClass, self.currentMethod)
                self.write_push(x, y)
                return

            x, y = self.table.find_symbol_id(temp, self.currentClass, self.currentMethod)
            self.write_push(x, y)

        if token[0] == '(':
            self.Tokens.peek_next_token()

            if token[2] == 'integerConstant' or token[2] == 'identifier' \
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
                self.error(token, ") expected")

    # Handles string literals
    def write_strings(self, word):

        self.write_push('constant', str(len(word)))
        self.write_call('String.new', '1')

        for i in word:
            self.write_push('constant', str(ord(i)))
            self.write_call('String.appendChar', '2')

    # Methods for writing specific commands to the file
    def write_pop(self, location, value):
        if location == 'var':
            location = 'local'
        elif location == 'field':
            location = 'this'

        if self.std_check:
            self.file.write("pop " + location + " " + value + "\n")

    def write_push(self, location, value):
        if location == 'var':
            location = 'local'
        elif location == 'field':
            location = 'this'

        if self.std_check:
            self.file.write("push " + location + " " + value + "\n")

    def write_label(self, label):
        if self.std_check:
            self.file.write("label " + label + "\n")

    def write_bool(self, command):
        if self.std_check:
            self.file.write(command + "\n")

    def write_goto(self, location):
        if self.std_check:
            self.file.write("goto " + location + "\n")

    def write_if_goto(self, location):
        if self.std_check:
            self.file.write("if-goto " + location + "\n")

    def write_function(self, name, variables):
        if self.std_check:
            self.file.write("function " + name + " " + variables + "\n")

    def write_call(self, name, variables):
        if self.std_check:
            self.file.write("call " + name + " " + variables + "\n")

    def write_return(self):
        if self.std_check:
            self.file.write("return\n")
