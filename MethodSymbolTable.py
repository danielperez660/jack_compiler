from compiler import SymbolTable as sT


class MethodSymbolTable(sT.SymbolTable):

    def __init__(self, name, type):
        super().__init__(name)
        self.name = name
        self.type = type

        # counters for the method_scope_tables
        self.var_counter = 0
        self.argument_counter = 1

        self.scope_table = [['this', type, 'reference', 'argument', 0]]

    # Adds a new value to the symbol table
    def add(self, symbol, symb_type):

        if symb_type == 'var':
            self.scope_table.append([symbol[0], symbol[3], 'var', self.var_counter])
            self.var_counter += 1
        elif symb_type == 'argument':
            self.scope_table.append([symbol[0], symbol[3], 'argument', self.argument_counter])
            self.argument_counter += 1
