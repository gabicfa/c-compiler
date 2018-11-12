number =[]
string = []

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
                while((self.posicao != len(self.origem)) and character== ' '):
                    self.posicao = self.posicao+1
                    character = self.origem[self.posicao]
                if(self.posicao == len(self.origem)):
                    t = Token('FIM', 'null')
                    self.atual = t

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
                elif(string_token == "void"):    
                    t = Token('VOID', string_token)
                elif(string_token == "int"):    
                    t = Token('INT', string_token)
                elif(string_token == "char"):    
                    t = Token('CHAR', string_token)
                elif(string_token == "main"):    
                    t = Token('MAIN', string_token)
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
            
            elif character == ',':
                t = Token('COLON','null')
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