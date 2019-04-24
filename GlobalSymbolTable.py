from compiler import MethodSymbolTable as mTable
from compiler import stdLibSymbolTables as stdTable


class GlobalSymbolTable:

    def __init__(self):
        self.class_scope_table = []
        self.method_scope_tables = [[['this', None, 'reference'], 0]]
        self.method_tables = []

        self.std_lib_tables = []
        self.current_method = 0

        # counters for the class_scope_table
        self.static_counter = 0
        self.field_counter = 0

        # counters for the method_scope_tables
        self.var_counter = 0
        self.argument_counter = 1

    def std_lib_prep(self, name, libs):
        current = stdTable.stdLibSymbolTables(name, libs)
        self.std_lib_tables.append(current)

    def add_symbol(self, symbol, table, symb_type):

        # chose if it belongs to the class_scope_table or not
        if table == 'class':
            if symb_type == 'static':
                self.class_scope_table.append([symbol, self.static_counter])
                self.static_counter += 1
            elif symb_type == 'field':
                self.class_scope_table.append([symbol, self.field_counter])
                self.field_counter += 1

        elif table == 'method':
            # self.method_tables[self.current_method].add(symbol, symb_type)

            if symb_type == 'var':
                self.method_scope_tables.append([symbol, self.var_counter])
                self.var_counter += 1
            elif symb_type == 'argument':
                self.method_scope_tables.append([symbol, self.argument_counter])
                self.argument_counter += 1

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
    def find_symbol(self, symbol, table):

        if table == 'class':
            for i in self.class_scope_table:
                if symbol[0] == i[0][0]:
                    return False
            return True

        elif table == 'method':
            for i in self.method_scope_tables:
                if symbol[0] == i[0][0]:
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
        for i in self.class_scope_table:
            print(i)

        print("\nMethod Scope Table")
        for i in self.method_tables:
            print(i)