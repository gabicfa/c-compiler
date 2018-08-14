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
           
class Analisador(object):

    def __init__(self,tokens):
        self.tokens = tokens
    
    def analisarExpressao(self):
        self.tokens.selecionarProximo()
        if(RepresentsInt(self.tokens.atual.valor)):
            resultado = int(self.tokens.atual.valor)
            self.tokens.selecionarProximo()
            while(self.tokens.atual.tipo != 'FIM'):
                if(self.tokens.atual.tipo == 'PLUS'):
                    self.tokens.selecionarProximo()
                    if(self.tokens.atual.tipo == 'INT'):    
                        resultado = resultado + int(self.tokens.atual.valor)
                    else:
                        return "Erro: Need a number after operator"
                elif(self.tokens.atual.tipo == 'MINUS'):
                    self.tokens.selecionarProximo()
                    if(self.tokens.atual.tipo == 'INT'):
                        resultado = resultado - int(self.tokens.atual.valor)
                    else:
                        return "Erro: Need a number after operator"
                else:
                    return "Erro: no operator found" 
                self.tokens.selecionarProximo()
        else:
            return "Erro: Need to start with a number"
        
        return ("Resultado= " + str(resultado))    

while True:
    print("escreva uma cadeia de somas e subtracoes: ")
    exp = input()
    tokenizador = Tokenizador(exp,0,'null')
    analisador = Analisador(tokenizador)
    r = analisador.analisarExpressao()
    print(r)
