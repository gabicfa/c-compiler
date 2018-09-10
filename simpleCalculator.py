import re
number =[]

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

class PrePro:
    @staticmethod
    def espaco(input):
        espaco_entre_numeros = re.search('[0-9] +[0-9]', input)
        if espaco_entre_numeros:
            return "Erro: espaco entre numeros"
        else:
            input_sem_espaco = input.replace(" ","")
        return input_sem_espaco

    @staticmethod
    def comentarios(input):
        input_sem_comentarios = re.sub('/\*(.*?)\*/', '', input)
        input_com_comentario_errado = re.search('/\*', input_sem_comentarios)
        if input_com_comentario_errado:
            return "Erro no comentario"
        return input_sem_comentarios

class Node:
    def __init__ (self):
        self.value = None
        self.children = []
    
    def evaluate(self):
        pass

class BinOp(Node):

    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def evaluate(self):
        val_esq = self.children[0].evaluate()
        val_dir = self.children[1].evaluate()
        if self.value == 'PLUS':
            return val_esq + val_dir
        elif self.value == 'MINUS':
            return val_esq - val_dir
        elif self.value == 'MULT':
            return val_esq * val_dir
        elif self.value == 'DIV':
            return val_esq // val_dir

class UnOp(Node):
    def __init__ (self, value, children):
        self.value = value
        self.children = children
    
    def evaluate(self):
        child = self.children[0].evaluate()
        if self.value == 'PLUS':
            return child
        elif self.value == 'MINUS':
            return -child

class IntVal(Node):
    def __init__(self,value):
        self.value = value
        self.children = []
    
    def evaluate(self):
        return self.value

class NoOp(Node):
    def __init__(self):
        self.value = None
        self.children = []
    def evaluate(self):
        pass

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

            if(RepresentsInt(character)):
                while(RepresentsInt(character)):
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
    
class Analisador(object):

    def __init__(self,tokens):
        self.tokens = tokens
    
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
            resultado = IntVal(int(self.tokens.atual.valor))
            self.tokens.selecionarProximo()
            return resultado
        elif(self.tokens.atual.tipo == 'OPEN_P'):
            self.tokens.selecionarProximo()
            resultado = self.analisarExpressao()
            if(self.tokens.atual.tipo == 'CLOSE_P'):
                self.tokens.selecionarProximo()
                return resultado
            else:
                raise Exception("parenteses nao fechados")
        else:
            raise Exception("error no fator")

    def termo(self):
        resultado = self.fator()
        while(self.tokens.atual.tipo == 'MULT' or self.tokens.atual.tipo == 'DIV'):
            op = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            resultado  = BinOp(op, [resultado, self.fator()])
        return resultado 
           
    def analisarExpressao(self):
        resultado = self.termo()
        while(self.tokens.atual.tipo == 'PLUS' or self.tokens.atual.tipo == 'MINUS'):
            op = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            resultado  = BinOp(op, [resultado, self.termo()])
        return resultado
        
run = 1
while (run == 1):
    inputFile = open("input.c", "r")
    for line in inputFile:
        l = line.strip()
        pp = PrePro.espaco(l)
        pp = PrePro.comentarios(pp)
        print(pp)
        tokenizador = Tokenizador(pp,0,'null')
        tokenizador.selecionarProximo()
        analisador = Analisador(tokenizador)
        r = analisador.analisarExpressao()
        
        if(tokenizador.atual.tipo == 'FIM'):
            print(r.evaluate())
        else:
            raise Exception("terminou antes do fim da string")

    run=0
