from symboltable import SymbleTable

class Node:
    def __init__ (self,value, children):
        self.value = value
        self.children = children
    
    def evaluate(self, table):
        pass

class FuncDec(Node):
    def evaluate(self,table):
        if(table.parent!=None):       
            table = table.parent
        table.set(self.value, self, 'FUNC') 

class FuncCall(Node):
    def evaluate(self,table):
        new_table = SymbleTable(table)
        node_declaracao = table.get(self.value)
        if (len(self.children) ==  len(node_declaracao[0].children)-2):
            if(len(node_declaracao[0].children)>2):
                for child in range(0, len(self.children)):
                    arg_call = self.children[child].evaluate(table)
                    tipo_call = arg_call[1]
                    tipo_func = node_declaracao[0].children[child+1].value
                    if(tipo_call==tipo_func):
                        new_table.set(node_declaracao[0].children[child+1].children[0].value, arg_call[0], tipo_func)
                    else:
                        raise Exception ("Erro nos tipos das variaveis")
            node_declaracao[0].children[len(node_declaracao[0].children)-1].evaluate(new_table)
            if(node_declaracao[0].children[0]!='VOID'):
                return_value = new_table.get('return')
                if(node_declaracao[0].children[0]!=return_value[1]):
                    raise Exception ("Tipo do retorno errado")
                else:
                    return return_value
        else:
            raise Exception("Número incorreto de argumentos")

class CmdsOp(Node):    
    def evaluate(self, table):
        if table == None:
            new_table = SymbleTable()
        else:
            new_table = SymbleTable(table)
        for child in self.children:
            child.evaluate(new_table)

class VarDec(Node):    
    def evaluate(self, table):
        for child in self.children:
            table.set(child.value, None, self.value)

class TriOp(Node):
    def evaluate(self, table):
        if(self.value == 'IF'):
            val_exp = self.children[0].evaluate(table)
            if(self.children[2] != None):
                if(val_exp):
                    self.children[1].evaluate(table)
                else:
                    self.children[2].evaluate(table)
            else:
                if(val_exp):
                    self.children[1].evaluate(table)
        else:
            raise Exception("Erro no Triop")
    
class BinOp(Node):
    def evaluate(self, table):
        if self.value ==  'ATRI':
            if table.check(self.children[0].value):
                tipo_val_esq = table.get(self.children[0].value)[1]
                tipo_val_dir = self.children[1].evaluate(table)[1]
                if(tipo_val_esq == tipo_val_dir): 
                    table.set(self.children[0].value, self.children[1].evaluate(table)[0],  tipo_val_esq)
                else:
                    raise Exception("Erro: Tipos diferentes")
        else:
            val_esq = self.children[0].evaluate(table)
            if self.value == 'WHILE':
                while(val_esq):
                    self.children[1].evaluate(table)
                    val_esq = self.children[0].evaluate(table)
            else:
                val_dir = self.children[1].evaluate(table)
                if (val_esq[1] == val_dir[1]):
                    val_esq = val_esq[0]
                    val_dir = val_dir[0]
                    if self.value == 'PLUS':
                        return [val_esq + val_dir,  'INT']
                    elif self.value == 'MINUS':
                        return [val_esq - val_dir, 'INT']
                    elif self.value == 'MULT':
                        return [val_esq * val_dir, 'INT']
                    elif self.value == 'DIV':
                        return [val_esq // val_dir, 'INT']
                    elif self.value == 'AND':
                        return [val_esq and val_dir, 'CHAR']
                    elif self.value == 'OR':
                        return [val_esq or val_dir, 'CHAR']
                    elif self.value == 'GREATER':
                        return [val_esq > val_dir, 'CHAR']
                    elif self.value == 'LESS':
                        return [val_esq < val_dir, 'CHAR']
                    elif self.value == 'EQUAL':
                        return [val_esq == val_dir, 'CHAR']
                    else:
                        raise Exception("Erro no Binop")
                else:
                    raise Exception("Erro: Tipos diferentes")

class UnOp(Node):
    def evaluate(self,table):
        child = self.children[0].evaluate(table)
        if self.value == 'PLUS':
            return child[0]
        elif self.value == 'MINUS':
            return -child[0]
        elif self.value == 'PRINTF':
            print(child[0])
        elif self.value == 'NOT':
            return not child[0]
        elif self.value == 'RETURN':
            table.parent.set('return', child[0], child[1])
            return child
        else:
            raise Exception("Erro no UnOp")

class IntVal(Node):
    def evaluate(self,table):
        return [int(self.value), 'INT']

class VarVal(Node):
    def evaluate(self, table):
        v = table.get(self.value)
        return v

class Scanf(Node):
    def evaluate(self, table):
        return [int(input()), 'INT'] 

class NoOp(Node):
    def __init__(self):
        self.value = None
        self.children = []

    def evaluate(self, table):
        pass