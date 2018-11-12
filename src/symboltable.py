class SymbleTable(object):
    def __init__(self):
        self.table = {}
    
    def get(self, var):
        return self.table[var]
    
    def set(self, var, value, tipo):
        self.table[var] = [value, tipo]
    
    def check(self, var):
        return var in self.table