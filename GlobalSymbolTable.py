from compiler import MethodSymbolTable as mT
from compiler import ClassSymbolTable as cT


class GlobalSymbolTable:

    def __init__(self):

        # All the symbol tables for methods and functions
        self.method_tables = []
        self.class_tables = []

    # Generates new symbol table for either class or method
    def new_table_gen(self, name, meth_class, types, sub):

        if meth_class == 'method':
            print("Created method: " + name + " " + types)
            current = mT.MethodSymbolTable(name, types, sub)
            self.method_tables.append(current)
        else:
            print("Created class: " + name)
            current = cT.ClassSymbolTable(name)
            self.class_tables.append(current)

    # Adds symbol to a specific table
    def add_symbol_to(self, symbol, table, symb_type, parent_class):

        # Checks if the value is added to a method or class table
        for i in self.method_tables:
            # Ensures that if 2 tables have same name in diff classes, it still works
            if i.get_name() == table and i.get_type() == parent_class:
                i.add(symbol, symb_type)

        for i in self.class_tables:
            if i.get_name() == table:
                i.add(symbol, symb_type)

    # Set symbol as initialised
    def initialise(self, symbol, curr_method, curr_class):

        for i in self.class_tables:
            if i.get_name() == curr_class:
                for j in i.get_table():
                    if j[0] == symbol[0]:
                        j[4] = True

        for i in self.method_tables:
            if i.get_name() == curr_method:
                for j in i.get_table():
                    if j[0] == symbol[0]:
                        j[4] = True

    # Check to see if the variable has been initialised, if so return True
    def init_check(self, symbol, curr_method, curr_class):

        for i in self.class_tables:
            if i.get_name() == curr_class:
                for j in i.get_table():
                    if j[0] == symbol[0] and j[4] != False:
                        return True

        for i in self.method_tables:
            if i.get_name() == curr_method:
                for j in i.get_table():
                    if j[0] == symbol[0] and j[4] != False:
                        return True

        return False

    # Checks to see if the identifier has been defined or not, returns false if in table
    def find_symbol(self, symbol, table, tableName):

        if table == 'class':
            for i in self.class_tables:
                if i.get_name() == tableName:
                    for j in i.get_table():
                        if j[0] == symbol[0]:
                            return False
                    return True

        elif table == 'method':
            for i in self.method_tables:
                if i.get_name() == tableName:
                    for j in i.get_table():
                        if j[0] == symbol[0]:
                            return False
                    return True
        else:
            # debugging purpose
            self.error(symbol, " identifier expected. Does not belong in symbolTable")

    # Checks to see what the ID is of a specific element and returns it + its location
    def find_symbol_id(self, symbol, class_table, method_table):

        for i in self.class_tables:
            if i.get_name() == class_table:
                tab = i.get_table()
                for j in tab:
                    if j[0] == symbol[0]:
                        return j[2], str(j[3])

        for i in self.method_tables:
            if i.get_name() == method_table:
                for j in i.get_table():
                    if j[0] == symbol[0]:
                        return j[2], str(j[3])

    # counts the required arguments for a method call
    def argument_count(self, method_table, called_class):
        counter = -1

        for i in self.method_tables:
            if i.get_name() == method_table and i.get_type() == called_class:
                counter = 0
                for j in i.get_table():
                    if j[2] == 'argument' or j[2] == 'reference':
                        counter += 1

        return str(counter)

    #  Gets the type of a specific token or argument, returns none if not found
    def get_type(self, name, table, class_table):

        for i in self.method_tables:
            if i.get_name() == table:
                tab = i.get_table()
                for j in tab:
                    if j[0] == name:
                        return j[1]

        for i in self.class_tables:
            if i.get_name() == class_table:
                tab = i.get_table()
                for j in tab:
                    if j[0] == name:
                        return j[1]
        return None

    # Counts the class variables in a class
    def class_count(self, name):
        counter = 0

        for i in self.class_tables:
            if i.get_name() == name:
                tab = i.get_table()
                for j in tab:
                    counter += 1

        return str(counter)

    # checks to see the type of a specific token
    def type_of(self, name, method):

        for i in self.method_tables:
            if i.get_name() == method:
                tab = i.get_table()
                for j in tab:
                    if j[0] == name:
                        return j[1]

    # gets the type of a specific table to see if its a method, constructor or function
    def get_sub(self, method, class_name):
        for i in self.method_tables:
            if i.get_name() == method and i.get_type() == class_name:
                return i.get_sub()

    # Checks to see if a method exists or a class exists, returns true if so
    def exists(self, name):
        for i in self.method_tables:
            if name == i.get_name():
                return True

        for i in self.class_tables:
            if name == i.get_name():
                return True

        return False

    # debugging purpose
    def print(self):

        print("\nClass Scope Table")
        for i in self.class_tables:
            i.print()

        print("\nMethod Scope Table")
        for i in self.method_tables:
            i.print()

    @staticmethod
    def error(token, message):
        print("error in line", token[1], "at or near " + token[0] + ", " + message)
        exit(0)
