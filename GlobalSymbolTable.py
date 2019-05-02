from compiler import MethodSymbolTable as mT
from compiler import ClassSymbolTable as cT


class GlobalSymbolTable:

    def __init__(self):

        # All the symbol tables for methods and functions
        self.method_tables = []
        self.class_tables = []

    # Generates new symbol table for either class or method
    def new_table_gen(self, name, meth_class, types):

        if meth_class == 'method':
            print("Created method: " + name + " " + types)
            current = mT.MethodSymbolTable(name, types)
            self.method_tables.append(current)
        else:
            print("Created class: " + name)
            current = cT.ClassSymbolTable(name)
            self.class_tables.append(current)

    # Adds symbol to a specific table
    def add_symbol_to(self, symbol, table, symb_type):

        # TODO - Fix issue where multiple functions can have same name in different classes

        # Checks if the value is added to a method or class table
        for i in self.method_tables:
            if i.get_name() == table:
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

    # Checks to see what the ID is of a specific element and returns it
    def find_symbol_id(self, symbol, class_table, method_table):

        for i in self.class_tables:
            if i.get_name() == class_table:
                for j in i.get_table():
                    if j[0] == symbol[0]:
                        print(j[2], j[3])
                        return j[2], str(j[3])

        for i in self.method_tables:
            if i.get_name() == method_table:
                for j in i.get_table():
                    if j[0] == symbol[0]:
                        return j[2], str(j[3])

    # counts the required arguments for a method call
    def argument_count(self, method_table, called_class):
        counter = -1

        print(method_table, called_class)

        for i in self.method_tables:
            if i.get_name() == method_table and i.get_table()[0][1] == called_class:
                for j in i.get_table():
                    print(j)
                    counter += 1

        return str(counter)

    def exists(self, name):
        for i in self.method_tables:
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
