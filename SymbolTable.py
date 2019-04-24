
class SymbolTable:

    def __init__(self, name):
        self.name = name
        self.scope_table = []

    def get_name(self):
        return self.name

    def get_table(self):
        return self.scope_table

    def print(self):
        print(self.name)
        for i in self.scope_table:
            print(i)
