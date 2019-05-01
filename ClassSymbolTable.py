from compiler import SymbolTable as sT


class ClassSymbolTable(sT.SymbolTable):

    def __init__(self, name):
        super().__init__(name)
        self.name = name

        # counters for the method_scope_tables
        self.static_counter = 0
        self.field_counter = 0

    # Adds a new value to the symbol table
    def add(self, symbol, symb_type):

        if symb_type == 'static':
            self.scope_table.append([symbol[0], symbol[3], 'static', self.static_counter, symbol[4]])
            self.static_counter += 1
        elif symb_type == 'field':
            self.scope_table.append([symbol[0], symbol[3], 'field', self.field_counter, symbol[4]])
            self.field_counter += 1

        print("Adding: ", end=" ")
        print(symbol, end=" ")
        print("to " + self.name)
