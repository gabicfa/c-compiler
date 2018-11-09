class SymbleTable(object):
    def __init__(self, parent=None):
        self.table = {}
        self.parent=parent
    
    def get(self, var):
        if var in self.table:
            return self.table[var]
        else:
            if self.parent !=None:
                return self.parent.get(var)
            else:
                raise Exception ("Variavel "+var+" não encontrada nesse escopo")

    def set(self, var, value, tipo):
        self.table[var] = [value, tipo]
    
    def check(self, var):
        if var in self.table:
            return True
        else:
            if self.parent != None:
                return self.parent.check(var)
            else:
                return False