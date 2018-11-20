from symboltable import SymbleTable
from identificador import Id

class Node:
    def __init__ (self,value, children):
        self.value = value
        self.children = children
        self.id = Id.getNew()
    
    def evaluate(self, table, write):
        pass

class ProgOp(Node):
    def evaluate(self,table, write):
        self.children.evaluate(table, write)

class CmdsOp(Node):    
    def evaluate(self, table, write):
        for child in self.children:
            child.evaluate(table, write)

class VarDec(Node):    
    def evaluate(self, table, write):
        for child in self.children:
            Id.variaveis.append(str(child.value)+"_1 RESD 1")
            table.set(child.value, None, self.value)

class TriOp(Node):
    def evaluate(self, table, write):
        if(self.value == 'IF'):
            if write: Id.comandos.append("IF_"+str(self.id))
            val_exp = self.children[0].evaluate(table, write)
            if write: Id.comandos.append("CMP EBX, False")
            if(self.children[2] != None):
                if write: Id.comandos.append("JE ELSE_"+str(self.id))
                if(val_exp):
                    self.children[1].evaluate(table, write)
                    if write: Id.comandos.append("JMP EXIT_"+str(self.id))
                else:
                    if write: Id.comandos.append("ELSE_"+str(self.id))
                    self.children[2].evaluate(table, write)
            else:
                if(val_exp):
                    self.children[1].evaluate(table, write)
                    if write: Id.comandos.append("JMP EXIT_"+str(self.id))
            if write: Id.comandos.append("EXIT_"+str(self.id))
        else:
            raise Exception("Erro no Triop")
    
class BinOp(Node):
    def evaluate(self, table, write):
        if self.value ==  'ATRI':
            if table.check(self.children[0].value):
                tipo_val_esq = table.get(self.children[0].value)[1]
                val_dir = self.children[1].evaluate(table, write)
                tipo_val_dir = val_dir[1]
                 
                
                if write: Id.comandos.append("MOV ["+ str(self.children[0].value) + "_1], EBX")
                
                if(tipo_val_esq == tipo_val_dir):
                    table.set(self.children[0].value, val_dir[0],  tipo_val_esq)    
                else:
                    raise Exception("Erro: Tipos diferentes")
        
        else:
            if self.value == 'WHILE':
                if write: Id.comandos.append("LOOP_"+str(self.id))
                val_esq = self.children[0].evaluate(table, write)
                if write: Id.comandos.append("CMP EBX, False")
                if write: Id.comandos.append("JE EXIT_"+str(self.id))

                while(val_esq[0]):
                    self.children[1].evaluate(table, write)
                    write = False
                    val_esq = self.children[0].evaluate(table, write)
                    
                write = True
                if write: Id.comandos.append("JMP LOOP_"+str(self.id))
                if write: Id.comandos.append("EXIT_"+str(self.id))
                
            else:
                val_esq = self.children[0].evaluate(table, write)
                if write: Id.comandos.append("PUSH EBX")
                val_dir = self.children[1].evaluate(table, write)
                if write: Id.comandos.append("POP EAX")

                if (val_esq[1] == val_dir[1]):
                    val_esq = val_esq[0]
                    val_dir = val_dir[0]
                    if self.value == 'PLUS':

                        if write: Id.comandos.append("ADD EAX, EBX")
                        if write: Id.comandos.append("MOV EBX, EAX")

                        return [val_esq + val_dir,  'INT']
                    elif self.value == 'MINUS':

                        if write: Id.comandos.append("SUB EAX, EBX")
                        if write: Id.comandos.append("MOV EBX, EAX")

                        return [val_esq - val_dir, 'INT']
                    elif self.value == 'MULT':

                        if write: Id.comandos.append("IMUL EBX")
                        if write: Id.comandos.append("MOV EBX, EAX")

                        return [val_esq * val_dir, 'INT']
                    elif self.value == 'DIV':

                        if write: Id.comandos.append("IDIV EAX, EBX")
                        if write: Id.comandos.append("MOV EBX, EAX")

                        return [val_esq // val_dir, 'INT']
                    elif self.value == 'AND':

                        if write: Id.comandos.append("AND EAX, EBX")
                        if write: Id.comandos.append("MOV EBX, EAX")

                        return [val_esq and val_dir, 'CHAR']
                    elif self.value == 'OR':

                        if write: Id.comandos.append("OR EAX, EBX")
                        if write: Id.comandos.append("MOV EBX, EAX")

                        return [val_esq or val_dir, 'CHAR']
                    elif self.value == 'GREATER':

                        if write: Id.comandos.append("CMP EAX, EBX")
                        if write: Id.comandos.append("CALL binop_jg")

                        return [val_esq > val_dir, 'CHAR']
                    elif self.value == 'LESS':

                        if write: Id.comandos.append("CMP EAX, EBX")
                        if write: Id.comandos.append("CALL  binop_jl")

                        return [val_esq < val_dir, 'CHAR']
                    elif self.value == 'EQUAL':

                        if write: Id.comandos.append("CMP EAX, EBX")
                        if write: Id.comandos.append("CALL  binop_je")

                        return [val_esq == val_dir, 'CHAR']
                    else:
                        raise Exception("Erro no Binop")
                else:
                    raise Exception("Erro: Tipos diferentes")

class UnOp(Node):
    def evaluate(self,table,write):
        child = self.children[0].evaluate(table, write)
        if self.value == 'PLUS':
            return child[0]
        elif self.value == 'MINUS':
            return -child[0]
        elif self.value == 'PRINTF':
            if write: Id.comandos.append("PUSH EBX")
            if write: Id.comandos.append("CALL print")
            print(child[0])
        elif self.value == 'NOT':
            return not child[0]
        else:
            raise Exception("Erro no UnOp")

class IntVal(Node):
    def evaluate(self,table,write):
        if write: Id.comandos.append("MOV EBX, "+str(self.value))
        return [int(self.value), 'INT']

class VarVal(Node):
    def evaluate(self, table,write):
        if write: Id.comandos.append("MOV EBX, ["+str(self.value)+"_1]")
        v = table.get(self.value)
        return v

class Scanf(Node):
    def evaluate(self, table,write):
        return [int(input()), 'INT'] 

class NoOp(Node):
    def __init__(self):
        self.value = None
        self.children = []

    def evaluate(self, table,write):
        pass