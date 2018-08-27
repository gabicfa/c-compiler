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
                        character = ""

            if (character is '/'):
                marcoInicial = self.posicao
                if(self.origem[self.posicao+1] == '*'):
                    self.posicao = self.posicao+1
                    character = self.origem[self.posicao]
                    fim_comentario = False
                    while(not fim_comentario):
                        if(self.posicao+1 < len(self.origem)):
                            self.posicao = self.posicao+1
                            character = self.origem[self.posicao]
                        else:
                            character = ""
                            fim_comentario = True
                        if(self.origem[self.posicao] == '*'):
                            if(self.posicao+1 < len(self.origem)):                              
                                if(self.origem[self.posicao+1] == '/'):
                                    self.posicao = self.posicao+1
                                    fim_comentario = True 
                                    if(self.posicao+1 < len(self.origem)):
                                        marcoFinal = self.posicao+1
                                        self.origem = self.origem[0:marcoInicial] + self.origem[marcoFinal:]
                                        self.posicao = marcoInicial
                                        character = self.origem[self.posicao]
                                        if(character == ' '):
                                            while(character == ' '):
                                                self.posicao = self.posicao+1
                                                if(self.posicao != len(self.origem)):
                                                    character = self.origem[self.posicao]
                                                else:
                                                    character = ""
                                    else:
                                        t = Token('FIM', 'null')
                                        self.atual = t
                                        character = ""
                                else:
                                    t = Token('FIM', 'null')
                                    self.atual = t
                                    character = ""

                    if(self.posicao+1 > len(self.origem)):
                        t = Token('FIM', 'null')
                        self.atual = t
                        character = ""
                    
            
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

            elif character is '/':
                t = Token('DIV', 'null')
                self.atual = t
                self.posicao = self.posicao+1

            elif character is '*':
                t = Token('MULT', 'null')
                self.atual = t
                self.posicao = self.posicao+1
           
class Analisador(object):

    def __init__(self,tokens):
        self.tokens = tokens
    
    def termo(self, resultado):
        if(RepresentsInt(self.tokens.atual.valor)):
            resultado = int(self.tokens.atual.valor)
            while(self.tokens.atual.tipo != 'FIM' and self.tokens.atual.tipo != 'PLUS' and self.tokens.atual.tipo != 'MINUS'):
                self.tokens.selecionarProximo()
                if(self.tokens.atual.tipo == 'MULT'):
                    self.tokens.selecionarProximo()
                    if(self.tokens.atual.tipo == 'INT'): 
                        resultado = resultado * int(self.tokens.atual.valor)
                    else:
                        return "Erro: Need a number after operator"
                elif(self.tokens.atual.tipo == 'DIV'):
                    self.tokens.selecionarProximo()
                    if(self.tokens.atual.tipo == 'INT'):
                        resultado = resultado // int(self.tokens.atual.valor)
                    else:
                        return "Erro: Need a number after operator"
                elif(self.tokens.atual.tipo == 'INT'):
                    return "Erro: no operator found"
            return resultado
        else:
            return "Erro: Need to start with a number"
    
    def analisarExpressao(self):
        resultado = 0
        self.tokens.selecionarProximo()
        resultado = self.termo(resultado)
        if(type(resultado) == str):
            return resultado
        else:
            while(self.tokens.atual.tipo != 'FIM'):
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
                    return "Erro: no operator found" 
            
            return ("Resultado= " + str(resultado))   
        
while True:
    print("escreva uma cadeia de somas e subtracoes: ")
    exp = input()
    tokenizador = Tokenizador(exp,0,'null')
    analisador = Analisador(tokenizador)
    r = analisador.analisarExpressao()
    print(r)
