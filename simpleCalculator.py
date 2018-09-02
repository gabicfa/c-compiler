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
                return "Erro: parenteses nao fechados"
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
                    return "Erro" 
            
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
                    return "Erro" 
            return int(resultado)
        
while True:
    print("escreva uma cadeia de somas e subtracoes: ")
    exp = input()
    pp = PrePro.espaco(exp)
    pp = PrePro.comentarios(pp)
    if(pp[0] != "E"):
        tokenizador = Tokenizador(pp,0,'null')
        tokenizador.selecionarProximo()
        analisador = Analisador(tokenizador)
        r = analisador.analisarExpressao()
        print(str(r))
    else:
        print(pp)
