import re
input_file_list = []
number =[]
string = []

class PrePro:
    @staticmethod
    def espaco(input):
        for line in input:
            for char in line:
                if(char != "\n"):
                    input_file_list.append(char)
        input_file_string = ''.join(map(str, input_file_list))

        espaco_entre_numeros = re.search('[0-9] +[0-9]', input_file_string)
        espaco_entre_numeros_e_letras = re.search('[a-z] +[0-9]', input_file_string)

        if espaco_entre_numeros or espaco_entre_numeros_e_letras:
            raise Exception("Erro nos espaços")
        else:
            input_sem_espaco = input_file_string.replace(" ","")
            return input_sem_espaco

    @staticmethod
    def comentarios(input):
        input_sem_comentarios = re.sub('/\*(.*?)\*/', '', input)
        input_com_comentario_errado = re.search('/\*', input_sem_comentarios)
        if input_com_comentario_errado:
            raise Exception("Erro no comentario")
        return input_sem_comentarios

class Node:
    def __init__ (self,value, children):
        self.value = value
        self.children = children
    
    def evaluate(self, table):
        pass

class CmdsOp(Node):    
    def evaluate(self, table):
        for child in self.children:
            child.evaluate(table)

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
            table.set(self.children[0], self.children[1].evaluate(table))
        else:
            val_esq = self.children[0].evaluate(table)
            if self.value == 'WHILE':
                while(val_esq):
                    self.children[1].evaluate(table)
                    val_esq = self.children[0].evaluate(table)
            else:
                val_dir = self.children[1].evaluate(table)
                if self.value == 'PLUS':
                    return val_esq + val_dir
                elif self.value == 'MINUS':
                    return val_esq - val_dir
                elif self.value == 'MULT':
                    return val_esq * val_dir
                elif self.value == 'DIV':
                    return val_esq // val_dir
                elif self.value == 'AND':
                    return val_esq and val_dir
                elif self.value == 'OR':
                    return val_esq or val_dir
                elif self.value == 'GREATER':
                    return val_esq > val_dir
                elif self.value == 'LESS':
                    return val_esq < val_dir
                elif self.value == 'EQUAL':
                    return val_esq == val_dir
                else:
                    raise Exception("Erro no Binop")

class UnOp(Node):
    def evaluate(self,table):
        child = self.children[0].evaluate(table)
        if self.value == 'PLUS':
            return child
        elif self.value == 'MINUS':
            return -child
        elif self.value == 'PRINTF':
            print(child)
        elif self.value == 'NOT':
            return not child
        else:
            raise Exception("Erro no UnOp")

class IntVal(Node):
    def evaluate(self,table):
        return int(self.value)

class VarVal(Node):
    def evaluate(self, table):
        return table.get(self.value)

class Scanf(Node):
    def evaluate(self, table):
        return int(input())

class NoOp(Node):
    def __init__(self):
        self.value = None
        self.children = []

    def evaluate(self, table):
        pass

class SymbleTable(object):
    def __init__(self):
        self.table = {}
    
    def get(self, var):
        return self.table[var]
    
    def set(self, var, value):
        self.table[var] = value

class Token(object):

    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

class Tokenizador(object):

    def __init__(self, origem, posicao, atual):
        self.origem = origem
        self.posicao = posicao
        self.atual = atual
    
    def selecionarProximo(self):

        if(self.posicao == len(self.origem)):
            t = Token('FIM', 'null')
            self.atual = t
            
        else:
            character = self.origem[self.posicao]

            if(character.isdigit()):
                while(character.isdigit()):
                    number.append(character)
                    self.posicao = self.posicao+1
                    if(self.posicao != len(self.origem)):
                        character = self.origem[self.posicao]
                    else:
                        break

                number_token = ''.join(map(str, number))
                t = Token('INT', number_token)
                self.atual = t
                del number[:]
            
            elif(character.isalpha()):
                while(character.isalpha() or character.isdigit() or character == "_"):
                    string.append(character)
                    self.posicao = self.posicao+1
                    if(self.posicao != len(self.origem)):
                        character = self.origem[self.posicao]
                    else:
                        break

                string_token = ''.join(map(str, string))
                if(string_token == "printf"):    
                    t = Token('PRINTF', string_token)
                elif(string_token == "scanf"):    
                    t = Token('SCANF', string_token)
                elif(string_token == "if"):    
                    t = Token('IF', string_token)
                elif(string_token == "else"):    
                    t = Token('ELSE', string_token)
                elif(string_token == "while"):    
                    t = Token('WHILE', string_token)
                else:
                    t = Token('VAR', string_token)
                self.atual = t
                del string[:]
            
            elif character == "+":
                t = Token('PLUS', 'null')
                self.atual = t
                self.posicao = self.posicao+1 

            elif character is '-':
                t=Token('MINUS', 'null') 
                self.atual = t
                self.posicao = self.posicao+1 

            elif character == '/':
                t = Token('DIV', 'null')
                self.atual = t
                self.posicao = self.posicao+1

            elif character == '*':
                t = Token('MULT', 'null')
                self.atual = t
                self.posicao = self.posicao+1
            
            elif character == '(':
                t = Token('OPEN_P','null')
                self.atual = t
                self.posicao = self.posicao+1
            
            elif character == ')':
                t = Token('CLOSE_P','null')
                self.atual = t
                self.posicao = self.posicao+1

            elif character == '{':
                t = Token('OPEN_C','null')
                self.atual = t
                self.posicao = self.posicao+1
            
            elif character == '}':
                t = Token('CLOSE_C','null')
                self.atual = t
                self.posicao = self.posicao+1
            
            elif character == '=':
                if(self.origem[self.posicao+1] != '='):
                    t = Token('ATRI','null')
                    self.atual = t
                    self.posicao = self.posicao+1
                else:
                    self.posicao = self.posicao+1
                    t = Token('EQUAL','null')
                    self.atual = t
                    self.posicao = self.posicao+1
            
            elif character == ';':
                t = Token('SEMICOLON','null')
                self.atual = t
                self.posicao = self.posicao+1
            
            elif character == '&':
                if(self.origem[self.posicao+1] == '&'):
                    self.posicao = self.posicao+1
                    t = Token('AND','null')
                    self.atual = t
                    self.posicao = self.posicao+1

            elif character == '|':
                if(self.origem[self.posicao+1] == '|'):
                    self.posicao = self.posicao+1
                    t = Token('OR','null')
                    self.atual = t
                    self.posicao = self.posicao+1
            
            elif character == '!':
                t = Token('NOT','null')
                self.atual = t
                self.posicao = self.posicao+1
            
            elif character == '>':
                t = Token('GREATER','null')
                self.atual = t
                self.posicao = self.posicao+1
            
            elif character == '<':
                t = Token('LESS','null')
                self.atual = t
                self.posicao = self.posicao+1
   
class Analisador(object):

    def __init__(self,tokens,table):
        self.tokens = tokens
        self.table = table

    def comandos(self):
        if(self.tokens.atual.tipo == 'OPEN_C'):
            self.tokens.selecionarProximo()
            comandos_children = []
            while(self.tokens.atual.tipo != 'CLOSE_C'):
                cmd = self.comando()
                comandos_children.append(cmd)
                if(self.tokens.atual.tipo == 'SEMICOLON'):
                    self.tokens.selecionarProximo() 
                else:
                    raise Exception("Erro: Ponto e virgula")
            if(self.tokens.atual.tipo == 'CLOSE_C'):
                return CmdsOp(None, comandos_children)
            else:
                raise Exception("Erro: Fechar Chaves")
        else:
            raise Exception ("Erro: Abrir Chaves")    
    
    def comando(self):
        if(self.tokens.atual.tipo == 'VAR'):
            return self.atribuicao()
        elif(self.tokens.atual.tipo == 'PRINTF'):
            self.tokens.selecionarProximo()
            return self.print()
        elif(self.tokens.atual.tipo == 'OPEN_C'):
            resultado = self.comandos()
            self.tokens.selecionarProximo()
            return resultado
        elif(self.tokens.atual.tipo == 'IF'):
            return self.ifExp()
        elif(self.tokens.atual.tipo == 'WHILE'):
            resultado = self.whileExp()
            return resultado
        else:
            raise Exception("Erro no comando")
    
    def whileExp(self):
        self.tokens.selecionarProximo()
        if(self.tokens.atual.tipo == "OPEN_P"):
            self.tokens.selecionarProximo()
            resultado1 = self.booleanExp()
            if(self.tokens.atual.tipo == "CLOSE_P"):
                self.tokens.selecionarProximo()
                resultado2 = self.comando()
                return BinOp('WHILE', [resultado1, resultado2])
            else:
                raise Exception("Erro: fechar parentases no while")
        else:
            raise Exception("Erro: abir parentases no while")

    def ifExp(self):
        self.tokens.selecionarProximo()
        if(self.tokens.atual.tipo == "OPEN_P"):
            self.tokens.selecionarProximo()
            resultado1 = self.booleanExp()
            if(self.tokens.atual.tipo == "CLOSE_P"):
                self.tokens.selecionarProximo()
                resultado2 = self.comando()
                if(self.tokens.atual.tipo == "ELSE"):
                    self.tokens.selecionarProximo()
                    resultado3 = self.comando()
                else:
                    resultado3 = None
                return TriOp('IF', [resultado1, resultado2, resultado3])
            else:
                raise Exception("Erro: fechar parentases no if")
        else:
            raise Exception("Erro: abrir parentases no if")

    def print(self):
        if(self.tokens.atual.tipo == 'OPEN_P'):
            self.tokens.selecionarProximo()
            resultado = UnOp('PRINTF', [self.expressao()])
            if(self.tokens.atual.tipo=='CLOSE_P'):
                self.tokens.selecionarProximo()
                return resultado
            else:
                raise Exception("Erro: Fechar parenteses")
        else:
            raise Exception("Erro: Abrir parenteses")

    def atribuicao(self):
        name = self.tokens.atual.valor
        self.tokens.selecionarProximo()
        if(self.tokens.atual.tipo == 'ATRI'):
            self.tokens.selecionarProximo()
            if(self.tokens.atual.tipo == 'SCANF'):
                self.tokens.selecionarProximo()
                if(self.tokens.atual.tipo == 'OPEN_P'):
                    self.tokens.selecionarProximo()
                    if(self.tokens.atual.tipo == 'CLOSE_P'):
                        self.tokens.selecionarProximo()
                        resultado = Scanf('SCANF',[])
                        return BinOp('ATRI',[name, resultado])
            else:
                resultado = self.expressao()
                return BinOp('ATRI',[name, resultado])
        else:
            raise Exception("Erro: Inserir '=' ")

    def expressao(self):
        resultado = self.termo()
        while(self.tokens.atual.tipo == 'PLUS' or self.tokens.atual.tipo == 'MINUS'):
            op = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            resultado  = BinOp(op, [resultado, self.termo()])
        return resultado
    
    def termo(self):
        resultado = self.fator()
        while(self.tokens.atual.tipo == 'MULT' or self.tokens.atual.tipo == 'DIV'):
            op = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            resultado  = BinOp(op, [resultado, self.fator()])
        return resultado 
       
    def fator(self):
        if(self.tokens.atual.tipo == 'PLUS'):
            op = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            resultado = UnOp(op, [self.fator()])
            return resultado
        elif(self.tokens.atual.tipo == 'MINUS'):
            op = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            resultado = UnOp(op, [self.fator()])
            return resultado
        elif(self.tokens.atual.tipo == 'INT'):
            resultado = IntVal(self.tokens.atual.valor,[])
            self.tokens.selecionarProximo()
            return resultado
        elif(self.tokens.atual.tipo == 'OPEN_P'):
            self.tokens.selecionarProximo()
            resultado = self.expressao()
            if(self.tokens.atual.tipo == 'CLOSE_P'):
                self.tokens.selecionarProximo()
                return resultado
            else:
                raise Exception("Erro: Fechar parenteses")
        elif(self.tokens.atual.tipo == 'VAR'):
            resultado = VarVal(self.tokens.atual.valor,[])
            self.tokens.selecionarProximo()
            return resultado
        else:
            raise Exception("Erro no fator")
    
    def booleanExp(self):
        resultado = self.booleanTerm()
        while(self.tokens.atual.tipo == 'OR'):
            op = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            resultado = BinOp(op,[resultado, self.booleanTerm()])
        return resultado
    
    def booleanTerm(self):
        resultado = self.booleanFactor()
        while(self.tokens.atual.tipo == 'AND'):
            op = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            resultado = BinOp(op,[resultado, self.booleanFactor()])
        return resultado

    def booleanFactor(self):
        if(self.tokens.atual.tipo == 'NOT'):
            op = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            return UnOp(op,[self.booleanFactor()])
        else:
            return self.relExp()
    
    def relExp(self):
        resultado = self.expressao()
        if(self.tokens.atual.tipo == 'GREATER' or self.tokens.atual.tipo == 'LESS' or self.tokens.atual.tipo == 'EQUAL'):
            op = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            return BinOp(op, [resultado, self.expressao()])
        else:
            raise Exception("Erro: relOp errado")

if __name__ == "__main__":

    input_file = open("input.c", "r")
    input_file = PrePro.espaco(input_file)
    input_file = PrePro.comentarios(input_file)

    table = SymbleTable()
    tokenizador = Tokenizador(input_file,0,'null')
    tokenizador.selecionarProximo()
    analisador = Analisador(tokenizador, table)
    r = analisador.comandos()
    tokenizador.selecionarProximo()

    if(tokenizador.atual.tipo == 'FIM'):
        r.evaluate(table)
    else:
        raise Exception("Erro: Análise terminou antes do fim do arquivo de entrada")

