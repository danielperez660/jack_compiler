import lexer as lex
import GlobalSymbolTable as sT


class Parser:

    def __init__(self, files):
        print("PARSER INITIALISED")

        self.types = ['int', 'char', 'boolean', 'identifier', None]

        # Initial pass to parse the std libs
        self.while_counter = -1
        self.if_counter = -1

        self.array_check = False
        self.std_check = False

        self.var_counter = []

        self.token_methods = None
        self.token_assigning = None

        self.stdLibs = ["Array.jack", "Keyboard.jack", "Math.jack", "Memory.jack",
                        "Output.jack", "Screen.jack", "String.jack", "Sys.jack"]

        self.table = sT.GlobalSymbolTable()

        self.currentClass = ""
        self.currentMethod = ""

        # Counts the number of vars per method
        for i in files:
            self.div = i.split('.')
            self.file = i
            self.Tokens = lex.Token(self.file)
            self.classDeclar()

        self.table = sT.GlobalSymbolTable()

        for i in self.stdLibs:
            print("\n" + i + "\n")
            self.div = i.split('.')
            self.Tokens = lex.Token(i)
            self.classDeclar()

        # Second pass where the std libs and the variables have been counted for methods
        for i in files:
            self.while_counter = -1
            self.if_counter = -1

            self.array_check = False
            self.std_check = True

            self.div = i.split('.')
            self.file = open(self.div[0] + '.vm', "w")

            self.Tokens = lex.Token(i)

            self.classDeclar()

        self.table.print_()
        self.file.close()

    @staticmethod
    def ok(token):
        print(token[0] + ": OK")

    @staticmethod
    def error(token, message):
        print("error in line", token[1], "at or near " + token[0] + ", " + message)
        exit(0)

    @staticmethod
    def warning(token, message):
        print("warning in line", token[1], "at or near " + token[0]+ ", " + message)

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
            self.table.new_table_gen(token[0], 'class', None, None)
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
        class_type = ""

        if token[0] == 'static' or token[0] == 'field':
            types = token[0]
            self.ok(token)
        else:
            self.error(token, "'static' or 'field' expected")

        token = self.Tokens.peek_next_token()

        if token[0] == 'int' or token[0] == 'char' or token[0] == 'boolean' or token[2] == 'identifier':
            self.type()

            if token[2] == 'identifier':
                class_type = token[0]

        else:
            self.error(token, "valid type or identifier expected")

        token = self.Tokens.get_next_token()

        # Adds the field/static to the class symbol table or checks if already there
        if token[2] == 'identifier':
            self.ok(token)
            if self.table.find_symbol(token, 'class', self.currentClass):
                if class_type != "":
                    token[3] = class_type
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

                    if self.table.find_symbol(token, 'class', self.currentClass):
                        if class_type != "":
                            token[3] = class_type
                        self.table.add_symbol_to(token, self.currentClass, types, self.currentClass)
                    else:
                        self.error(token, "redeclaration of identifier")

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
        sub = token[0]

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
            self.table.new_table_gen(token[0], 'method', self.currentClass, sub)
            self.currentMethod = token[0]
            self.if_counter = -1
            self.while_counter = -1
            print("Current method: " + self.currentMethod)

            if sub == 'method' and not self.std_check:
                self.var_counter.append([self.currentMethod, self.currentClass, 'reference', self.div[0]])

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
                if i[0] == self.currentMethod and self.currentClass == i[1] and i[2] == 'var' and i[3] == self.div[0]:
                    counter += 1

            self.write_function(self.currentClass + '.' + self.token_assigning[0], str(counter))

            if sub == 'method':
                self.write_push('argument', '0')
                self.write_pop('pointer', '0')

            if sub == 'constructor':
                self.write_push('constant', self.table.class_count(self.currentClass))
                self.write_call('Memory.alloc', '1')
                self.write_pop('pointer', '0')
        else:
            self.error(token, "')' expected")

        token = self.Tokens.peek_next_token()

        if token[0] == '{':
            self.subroutineBody()
        else:
            self.error(token, "'{' expected")

    def paramList(self):

        token = self.Tokens.peek_next_token()
        class_type = ""

        if token[0] == 'int' or token[0] == 'char' or token[0] == 'boolean' or token[2] == 'identifier':
            self.type()
            if token[2] == 'identifier':
                class_type = token[0]
        else:
            self.error(token, "valid type expected")

        token = self.Tokens.get_next_token()

        if token[2] == 'identifier':

            self.ok(token)
            if self.table.find_symbol(token, 'method', self.currentMethod):

                if class_type == '':
                    self.table.add_symbol_to(token, self.currentMethod, 'argument', self.currentClass)
                else:
                    token[3] = class_type
                    self.table.add_symbol_to(token, self.currentMethod, 'argument', self.currentClass)

                if not self.std_check:
                    self.var_counter.append([self.currentMethod, self.currentClass, 'arg', self.div[0]])
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
                    if token[2] == 'identifier':
                        class_type = token[0]
                else:
                    self.error(token, "valid type expected")

                token = self.Tokens.get_next_token()

                if token[2] == 'identifier':
                    self.ok(token)

                    if self.table.find_symbol(token, 'method', self.currentMethod):

                        if class_type == '':
                            self.table.add_symbol_to(token, self.currentMethod, 'argument', self.currentClass)
                        else:
                            token[3] = class_type
                            self.table.add_symbol_to(token, self.currentMethod, 'argument', self.currentClass)

                        if not self.std_check:
                            self.var_counter.append([self.currentMethod, self.currentClass, 'arg', self.div[0]])
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
        class_type = ''

        if token[0] == 'var':
            self.ok(token)
        else:
            self.error(token, "'var' expected")

        token = self.Tokens.peek_next_token()

        if token[0] == 'int' or token[0] == 'char' or token[0] == 'boolean' or token[2] == 'identifier':
            self.type()

            if token[2] == 'identifier':
                class_type = token[0]
        else:
            self.error(token, "valid type expected")

        token = self.Tokens.get_next_token()

        if token[2] == 'identifier':

            if self.table.find_symbol(token, 'method', self.currentMethod):

                if class_type == '':
                    self.table.add_symbol_to(token, self.currentMethod, 'var', self.currentClass)
                else:
                    token[3] = class_type
                    self.table.add_symbol_to(token, self.currentMethod, 'var', self.currentClass)

                if not self.std_check:
                    self.var_counter.append([self.currentMethod, self.currentClass, 'var', self.div[0]])
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

                        if class_type == '':
                            self.table.add_symbol_to(token, self.currentMethod, 'var', self.currentClass)
                        else:
                            token[3] = class_type
                            self.table.add_symbol_to(token, self.currentMethod, 'var', self.currentClass)

                        if not self.std_check:
                            self.var_counter.append([self.currentMethod, self.currentClass, 'var', self.div[0]])
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
                self.warning(token, "variable used has not been declared")

            elif token[3] != 'Object':
                print("Initialising: " + token[0])
                self.table.initialise(token, self.currentMethod, self.currentClass)

            self.token_assigning = token
            temp = token
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
            x, y = self.table.find_symbol_id(temp, self.currentClass, self.currentMethod)
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
            else:
                self.error(token, "'}' expected")
        else:
            self.write_label('IF_FALSE' + str(self.if_counter))

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
            self.token_assigning = None
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

            if self.table.get_type(temp[0], self.currentMethod, self.currentClass) not in self.types:
                name = self.table.get_type(temp[0], self.currentMethod, self.currentClass)
                print("Name change " + name)

            for i in self.var_counter:
                if i[0] == self.token_assigning and i[1] == name and (i[2] == 'arg' or i[2] == 'reference') \
                        and i[3] == self.div[0]:
                    if i[2] == 'reference':
                        count += 2
                    else:
                        count += 1

            if count == -1:
                count = self.table.argument_count(self.token_assigning, name)

            self.write_call(name + '.' + self.token_assigning, str(count))
            self.write_pop('temp', '0')
        else:

            # If the write call is being done for a local method/function e.g. test() and not Math.Test()
            count = -1

            for i in self.var_counter:

                if i[0] == name and i[1] == self.currentClass and (i[2] == 'arg' or i[2] == 'reference') \
                        and i[3] == self.div[0]:
                    if i[2] == 'reference':
                        count += 2
                    else:
                        count += 1

            if count == -1:
                count = self.table.argument_count(name, self.currentClass)

            self.write_push('pointer', '0')
            self.write_call(self.currentClass + "." + name, str(count))
            self.write_pop('temp', '0')

        if token[0] == ';':
            self.ok(token)
        else:
            self.error(token, "';' expected")

    def subroutineCall(self):

        token = self.Tokens.get_next_token()
        temp = token
        token = self.Tokens.peek_next_token()

        if temp[2] == 'identifier':
            if temp[3] != 'Object' and temp[0] != self.currentClass and token[0] == '.':
                x, y = self.table.find_symbol_id(temp, self.currentClass, self.currentMethod)
                self.write_push(x, y)
            self.ok(temp)
        else:
            self.error(temp, "'identifier' expected")

        if token[0] == '.':

            token = self.Tokens.get_next_token()

            if token[0] == '.':
                self.ok(token)

            token = self.Tokens.get_next_token()

            if token[2] == 'identifier':
                self.token_assigning = token[0]
                self.ok(token)
            else:
                self.error(token, "identifier expected")

        token = self.Tokens.get_next_token()

        if token[0] == '(':
            self.ok(token)
        else:
            self.error(token, "'(' expected")

        token = self.Tokens.peek_next_token()

        if token[0] == '-' or token[0] == '~' or \
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

        if token[0] == ')':
            return

        if token[0] == '-' or token[0] == '~' or token[0] == '-' or \
                token[2] == 'integerConstant' or token[2] == 'identifier' \
                or token[2] == 'stringLiteral' or token[0] == 'true' \
                or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                or token[0] == '(':
            self.expression()

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

                    self.error(token, "relational expression expected")

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
        elif temp[0] == '-':
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
                        self.warning(token, "variable has not been initialised")

            #
            # # Checks to see if the identifier has been defined previously
            # if self.table.find_symbol(token, 'method', self.currentMethod) and \
            #         self.table.find_symbol(token, 'class', self.currentClass) \
            #         and token[3] != 'Object':
            #     self.error(token, "variable used has not been declared")

            if token[0] == 'this':
                self.write_push('pointer', '0')
            if token[2] == 'integerConstant':
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
                else:
                    self.error(token, "] expected")
                return

            if token[0] == '(':
                token = self.Tokens.get_next_token()
                self.ok(token)

                token = self.Tokens.peek_next_token()

                if token[2] == 'integerConstant' or token[2] == 'identifier' \
                        or token[2] == 'stringLiteral' or token[0] == 'true' \
                        or token[0] == 'false' or token[0] == 'null' or token[0] == 'this' \
                        or token[0] == '(' or token[0] == '-' or token[0] == '~':
                    self.expressionList()
                else:
                    self.error(token, "expressionList expected")

                passed = token

                token = self.Tokens.get_next_token()

                if token[0] == ')':
                    self.ok(token)
                    if passed[2] == 'identifier':
                        x, y = self.table.find_symbol_id(passed, temp[0], methods)
                        self.write_push(x, y)

                    count = -1
                    name = temp[0]

                    for i in self.stdLibs:
                        if temp[3] == i.split('.')[0]:
                            name = temp[3]
                            print("Name change: " + name)

                    if self.table.get_type(temp[0], self.currentMethod, self.currentClass) not in self.types:
                        name = self.table.get_type(temp[0], self.currentMethod, self.currentClass)
                        print("Name change " + name)

                    for i in self.var_counter:
                        if i[0] == self.token_methods and i[1] == name and i[2] == 'arg' and i[3] == self.div[0]:
                            count += 1

                    if count == -1 or self.table.get_sub(self.token_methods, name) == 'method':
                        count = self.table.argument_count(self.token_methods, name)
                    else:
                        count += 1

                    self.write_call(name + '.' + self.token_methods, str(count))
                else:
                    self.error(token, ") expected")
                return

            if token[0] == '.':

                if token[0] == '.':
                    token = self.Tokens.get_next_token()
                    self.ok(token)
                else:
                    self.error(token, "'.' expected")

                token = self.Tokens.get_next_token()

                if token[2] == 'identifier':
                    print(temp, self.currentClass)
                    if temp[0] != self.currentClass and not self.table.exists(temp[0]) and temp[0]+'.jack' not in self.stdLibs:
                        x, y = self.table.find_symbol_id(temp, temp[0], self.currentMethod)
                        self.write_push(x, y)

                    self.ok(token)
                    self.token_methods = token[0]
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
                            or token[0] == '(' or token[0] == '-' or token[0] == '~':
                        self.expressionList()

                    token = self.Tokens.get_next_token()

                    if token[0] == ')':
                        count = 0
                        name = temp[0]
                        self.ok(token)

                        for i in self.stdLibs:
                            if i.split('.')[0] == temp[3]:
                                name = temp[3]

                        if self.table.type_of(temp[0], self.currentMethod) == self.currentClass:
                            name = self.currentClass
                            print("Name change " + name)

                        if self.table.get_type(temp[0], self.currentMethod, self.currentClass) not in self.types:
                            name = self.table.get_type(temp[0], self.currentMethod, self.currentClass)
                            print("Name change " + name)

                        for i in self.var_counter:
                            if i[0] == methods and i[1] == name and (i[2] == 'arg' or i[2] == 'reference') \
                                    and i[3] == self.div[0]:
                                count += 1

                        if count == 0:
                            count = self.table.argument_count(methods, name)

                        self.write_call(name + '.' + methods, str(count))
                    else:
                        self.error(token, ") expected")
                return
            else:
                x, y = self.table.find_symbol_id(temp, self.currentClass, self.currentMethod)
                self.write_push(x, y)
                return

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
