number =[]

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

class Token(object):

    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

class Tokenizador(object):

    def __init__(self, origem, posicao, atual):
        self.origem = origem
        self.posicao = posicao
        self.atual = atual
    
    def prePro(self):
        pos = 0
        i=[]
        f=[]
        inicio = 0
        fim = 0
        while (pos < len(self.origem)):
            if(self.origem[pos]=='/'):
                if(pos+1 < len(self.origem) and self.origem[pos+1]=='*'):
                    inicio = pos
                    pos+=1
                    while(pos+1 < len(self.origem) and fim == 0):
                        pos+=1
                        if(self.origem[pos] == '*'):
                            if(pos < len(self.origem) and self.origem[pos+1]=='/'):
                                pos+=1
                                if(pos+1 < len(self.origem) and self.origem[pos+1]==' '):
                                    while(self.origem[pos+1]==' '):
                                        pos+=1
                                fim = pos
                    if(fim != 0):
                        i.append(inicio)
                        f.append(fim)
                        inicio = 0
                        fim = 0
                        pos+=1
                    else:
                        print("Erro1")
                        return "Erro"
                else:
                    pos+=1
            else:
                pos+=1
        for c in range (len(i)-1,-1,-1):
            self.origem = self.origem[0:i[c]] + self.origem[f[c]+1:]
        return self.origem

    def selecionarProximo(self):
        if(self.posicao == len(self.origem)):
            t = Token('FIM', 'null')
            self.atual = t
        else:
            character = self.origem[self.posicao]
            
            if(character == ' '):
                while(character == ' '):
                    self.posicao = self.posicao+1
                    if(self.posicao != len(self.origem)):
                        character = self.origem[self.posicao]
                    else:
                        break
                if(self.posicao< len(self.origem)):
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
    
    def fator(self, resultado):
        if(self.tokens.atual.tipo == 'PLUS'):
            self.tokens.selecionarProximo()
            rF =  self.fator(resultado)
            resultado = resultado + rF
        elif(self.tokens.atual.tipo == 'MINUS'):
            self.tokens.selecionarProximo()
            rF =  self.fator(resultado)
            resultado = resultado - rF
        elif(self.tokens.atual.tipo == 'INT'):
            resultado = int(self.tokens.atual.valor)
            self.tokens.selecionarProximo()
        elif(self.tokens.atual.tipo == 'OPEN_P'):
            self.tokens.selecionarProximo()
            rE = self.analisarExpressao()
            resultado = rE
            if(self.tokens.atual.tipo == 'CLOSE_P'):
                self.tokens.selecionarProximo()
                return resultado
            else:
                return "Error1"
        return resultado

    def termo(self, resultado):
        resultado = self.fator(resultado)
        if(type(resultado) == str):
            return resultado
        else:
            while(self.tokens.atual.tipo == 'MULT' or self.tokens.atual.tipo == 'DIV'):
                if(self.tokens.atual.tipo == 'MULT'):
                    self.tokens.selecionarProximo()
                    rF = self.fator(resultado)
                    if(type(rF) == int):
                        resultado  = resultado * rF
                elif(self.tokens.atual.tipo == 'DIV'):
                    self.tokens.selecionarProximo()
                    rF = self.termo(resultado)
                    if(type(rF) == int):
                        resultado  = resultado // rF
                else:
                    return "Erro2" 
            
            return resultado    
           
    def analisarExpressao(self):
        resultado = 0
        resultado = self.termo(resultado)
        if(type(resultado) == str):
            return resultado
        else:
            while(self.tokens.atual.tipo == 'PLUS' or self.tokens.atual.tipo == 'MINUS'):
                if(self.tokens.atual.tipo == 'PLUS'):
                    self.tokens.selecionarProximo()
                    rT = self.termo(resultado)
                    if(type(rT) == int):
                        resultado  = resultado + rT
                elif(self.tokens.atual.tipo == 'MINUS'):
                    self.tokens.selecionarProximo()
                    rT = self.termo(resultado)
                    if(type(rT) == int):
                        resultado  = resultado - rT
                else:
                    return "Erro3" 
            return int(resultado)
        
while True:
    print("escreva uma cadeia de somas e subtracoes: ")
    exp = input()
    tokenizador = Tokenizador(exp,0,'null')
    p = tokenizador.prePro()
    if(p != "Erro"):
        tokenizador.selecionarProximo()
        analisador = Analisador(tokenizador)
        r = analisador.analisarExpressao()
        print(str(r))
