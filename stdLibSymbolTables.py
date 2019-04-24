from compiler import MethodSymbolTable as mTable


class stdLibSymbolTables(mTable.MethodSymbolTable):

    def __init__(self, name, library):
        super().__init__(name)

        self.library = library
        self.name = name
        self.method_scope_table = [[['this', None, 'reference'], 0]]

        # counters for the method_scope_tables
        self.var_counter = 0
        self.argument_counter = 1