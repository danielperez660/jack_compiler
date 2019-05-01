from compiler import MethodSymbolTable as mT
from compiler import ClassSymbolTable as cT


class GlobalSymbolTable:

    def __init__(self):
        self.class_scope_table = []
        self.method_scope_tables = [[['this', None, 'reference'], 0]]

        # All the symbol tables for methods and functions
        self.method_tables = []
        self.class_tables = []

        self.current_method = 0
        self.current_table = None

        # counters for the class_scope_table
        self.static_counter = 0
        self.field_counter = 0

        # counters for the method_scope_tables
        self.var_counter = 0
        self.argument_counter = 1

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

        # Checks if the value is added to a method or class table
        for i in self.method_tables:
            if i.get_name() == table:
                i.add(symbol, symb_type)

        for i in self.class_tables:
            if i.get_name() == table:
                i.add(symbol, symb_type)

    # Set symbol as initialised
    def initialise(self, symbol):
        for i in self.class_scope_table:
            if symbol[0] == i[0][0]:
                i[0][4] = True

        for i in self.method_scope_tables:
            if symbol[0] == i[0][0]:
                i[0][4] = True

    # Check to see if the variable has been initialised, if so return True
    def init_check(self, symbol):

        for i in self.class_scope_table:
            if symbol[0] == i[0][0] and i[0][4]:
                return True

        for i in self.method_scope_tables:
            if symbol[0] == i[0][0] and i[0][4]:
                return True

        return False

    # Checks to see if the identifier has been defined or not, returns false if in table
    def find_symbol(self, symbol, table, tableName):

        if table == 'class':
            for i in self.class_tables:
                if i.get_name() == tableName:
                    print("Found same table")
                    for j in i.get_table():
                        if j[0][0] == symbol[0]:
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

    @staticmethod
    def error(token, message):
        print("error in line", token[1], "at or near " + token[0] + ", " + message)
        exit(0)

    # debugging purpose
    def print(self):

        print("\nClass Scope Table")
        for i in self.class_tables:
            i.print()

        print("\nMethod Scope Table")
        for i in self.method_tables:
            i.print()
