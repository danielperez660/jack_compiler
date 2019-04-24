
class MethodSymbolTable:

    def __init__(self, name):
        self.name = name
        self.method_scope_table = [[['this', None, 'reference'], 0]]

        # counters for the method_scope_tables
        self.var_counter = 0
        self.argument_counter = 1

    def add(self, symbol, symb_type):

        if symb_type == 'var':
            self.method_scope_table.append([symbol, self.var_counter])
            self.var_counter += 1
        elif symb_type == 'argument':
            self.method_scope_table.append([symbol, self.argument_counter])
            self.argument_counter += 1

    def get_scope_table(self):
        return self.method_scope_table

    def print(self):
        for i in self.method_scope_table:
            print(i)
