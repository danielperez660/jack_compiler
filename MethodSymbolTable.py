from compiler import SymbolTable as sT


class MethodSymbolTable(sT.SymbolTable):

    def __init__(self, name, type, sub):
        super().__init__(name)
        self.name = name
        self.type = type
        self.sub_type = sub

        # counters for the method_scope_tables
        self.var_counter = 0
        self.argument_counter = 0

        if self.sub_type == 'method':
            self.scope_table = [['this', type, 'reference', 'argument', 0]]
        else:
            self.scope_table = []

            # Adds a new value to the symbol table
    def add(self, symbol, symb_type):

        if symb_type == 'var':
            self.scope_table.append([symbol[0], symbol[3], 'var', self.var_counter, symbol[4]])
            self.var_counter += 1
        elif symb_type == 'argument':
            self.scope_table.append([symbol[0], symbol[3], 'argument', self.argument_counter, True])
            self.argument_counter += 1

        print("Adding: ", end=" ")
        print(symbol, end=" ")
        print("to " + self.name)

    def get_type(self):
        return self.type

    def get_sub(self):
        return self.sub_type
