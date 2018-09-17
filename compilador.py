import re
inputFileList = []
number =[]
string = []

class PrePro:
    @staticmethod
    def espaco(input):
        for line in input:
            for char in line:
                if(char != "\n"):
                    inputFileList.append(char)
        inputFileString = ''.join(map(str, inputFileList))

        espaco_entre_numeros = re.search('[0-9] +[0-9]', inputFileString)
        espaco_entre_numeros_e_letras = re.search('[a-z] +[0-9]', inputFileString)

        if espaco_entre_numeros or espaco_entre_numeros_e_letras:
            raise Exception("Erro nos espaços")
        else:
            input_sem_espaco = inputFileString.replace(" ","")
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
    def __init__ (self,value, children):
        self.value = value
        self.children = children
    
    def evaluate(self, table):
        for child in self.children:
            child.evaluate(table)

class BinOp(Node):

    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def evaluate(self, table):
        if self.value ==  'EQUAL':
            table.set(self.children[0], self.children[1].evaluate(table))
        else:
            val_esq = self.children[0].evaluate(table)
            val_dir = self.children[1].evaluate(table)
            if self.value == 'PLUS':
                return val_esq + val_dir
            elif self.value == 'MINUS':
                return val_esq - val_dir
            elif self.value == 'MULT':
                return val_esq * val_dir
            elif self.value == 'DIV':
                return val_esq // val_dir
            else:
                raise Exception("Erro no Binop")

class UnOp(Node):
    def __init__ (self, value, children):
        self.value = value
        self.children = children
    
    def evaluate(self,table):
        child = self.children[0].evaluate(table)
        if self.value == 'PLUS':
            return child
        elif self.value == 'MINUS':
            return -child
        elif self.value == 'PRINTF':
            print(child)
        else:
            raise Exception("Erro no UnOp")

class IntVal(Node):
    def __init__(self,value):
        self.value = value
        self.children = []
    
    def evaluate(self,table):
        return int(self.value)

class VarVal(Node):
    def __init__(self,value):
        self.value = value
        self.children = []
    
    def evaluate(self, table):
        return table.get(self.value)

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

                numberToken = ''.join(map(str, number))
                t = Token('INT', numberToken)
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

                stringToken = ''.join(map(str, string))
                if(stringToken == "printf"):    
                    t = Token('PRINTF', stringToken)
                else:
                    t = Token('VAR', stringToken)
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
                t = Token('EQUAL','null')
                self.atual = t
                self.posicao = self.posicao+1
            
            elif character == ';':
                t = Token('SEMICOLON','null')
                self.atual = t
                self.posicao = self.posicao+1
    
class Analisador(object):

    def __init__(self,tokens,table):
        self.tokens = tokens
        self.table = table

    def comandos(self):
        if(self.tokens.atual.tipo == 'OPEN_C'):
            self.tokens.selecionarProximo()
            comandosChildren = []
            while(self.tokens.atual.tipo != 'CLOSE_C'):
                cmd = self.comando()
                comandosChildren.append(cmd)
                if(self.tokens.atual.tipo == 'SEMICOLON'):
                    self.tokens.selecionarProximo() 
                else:
                    raise Exception("Erro: Ponto e virgula")
            if(self.tokens.atual.tipo == 'CLOSE_C'):
                return CmdsOp(None, comandosChildren)
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
        else:
            raise Exception("Erro no comando")
    
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
        if(self.tokens.atual.tipo == 'EQUAL'):
            self.tokens.selecionarProximo()
            resultado = self.expressao()
            return BinOp('EQUAL',[name, resultado])
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
            resultado = IntVal(self.tokens.atual.valor)
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
            resultado = VarVal(self.tokens.atual.valor)
            self.tokens.selecionarProximo()
            return resultado
        else:
            raise Exception("Erro no fator")
    
if __name__ == "__main__":

    inputFile = open("input.c", "r")
    inputFile = PrePro.espaco(inputFile)
    inputFile = PrePro.comentarios(inputFile)

    table = SymbleTable()
    tokenizador = Tokenizador(inputFile,0,'null')
    tokenizador.selecionarProximo()
    analisador = Analisador(tokenizador, table)
    r = analisador.comandos()
    tokenizador.selecionarProximo()

    if(tokenizador.atual.tipo == 'FIM'):
        r.evaluate(table)
    else:
        raise Exception("Erro: Análise terminou antes do fim do arquivo de entrada")

