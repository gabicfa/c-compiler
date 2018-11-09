from node import *           

class Analisador(object):

    def __init__(self,tokens,table):
        self.tokens = tokens
        self.table = table
    
    def programa(self):
        raiz_children = [] 
        while(self.tokens.atual.tipo != 'FIM'):
            func_dec_children =[]
            func_dec_children.append(self.tipo())
            if(self.tokens.atual.tipo == 'VAR'):
                name_func = self.tokens.atual.valor
                self.tokens.selecionarProximo()
                if(self.tokens.atual.tipo == 'OPEN_P'):
                    self.tokens.selecionarProximo()
                    while(self.tokens.atual.tipo != 'CLOSE_P'):
                        tipo_arg = self.tipo()
                        arg = VarVal(self.tokens.atual.valor,[])
                        vd = VarDec (tipo_arg, [arg])
                        func_dec_children.append(vd)
                        self.tokens.selecionarProximo()
                        while(self.tokens.atual.tipo == 'COLON'):
                            self.tokens.selecionarProximo()
                            tipo_arg = self.tipo()
                            arg = VarVal(self.tokens.atual.valor,[])
                            vd = VarDec (tipo_arg, [arg])
                            func_dec_children.append(vd)
                            self.tokens.selecionarProximo()
                    if(self.tokens.atual.tipo == 'CLOSE_P'):
                        self.tokens.selecionarProximo()
                        func_dec_children.append(self.comandos())
                        fd = FuncDec(name_func, func_dec_children)
                        raiz_children.append(fd)
                    else:
                        raise Exception ("Erro: Fechar Parenteses")
                else:
                    raise Exception ("Erro: Abrir Parenteses")
            else:
                raise Exception ("Erro: Func")
        fc = FuncCall('main', [])
        raiz_children.append(fc)
        return CmdsOp(None, raiz_children)
             
    def comandos(self):
        if(self.tokens.atual.tipo == 'OPEN_C'):
            self.tokens.selecionarProximo()
            comandos_children = []
            while(self.tokens.atual.tipo != 'CLOSE_C' and self.tokens.atual.tipo != 'FIM'):
                cmd = self.comando()
                comandos_children.append(cmd)
            if(self.tokens.atual.tipo == 'CLOSE_C'):
                self.tokens.selecionarProximo()
                return CmdsOp(None, comandos_children)
            elif(self.tokens.atual.tipo == 'FIM'):
                return
            else:
                raise Exception("Erro: Fechar Chaves")
        else:
            raise Exception ("Erro: Abrir Chaves")

    def tipo(self):
        if(self.tokens.atual.tipo == 'VOID'):
            tipo = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            return tipo
        elif(self.tokens.atual.tipo == 'INT'):
            tipo = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            return tipo
        elif(self.tokens.atual.tipo == 'CHAR'):
            tipo = self.tokens.atual.tipo
            self.tokens.selecionarProximo()
            return tipo
        else:
            raise Exception("Erro: Tipo")

    def comando(self):
        if(self.tokens.atual.tipo == 'VAR'):
            return self.atribuicao()
        elif(self.tokens.atual.tipo == 'PRINTF'):
            self.tokens.selecionarProximo()
            return self.print()
        elif(self.tokens.atual.tipo == 'OPEN_C'):
            resultado = self.comandos()
            return resultado
        elif(self.tokens.atual.tipo == 'IF'):
            return self.ifExp()
        elif(self.tokens.atual.tipo == 'WHILE'):
            resultado = self.whileExp()
            return resultado
        elif(self.tokens.atual.tipo == 'VOID' or self.tokens.atual.tipo == 'INT' or self.tokens.atual.tipo == 'CHAR'):
                return self.declaracao()
        elif(self.tokens.atual.tipo == 'RETURN'):
            resultado = self.returnExp()
            return resultado
        else:
            raise Exception("Erro no comando")
    
    def returnExp(self):
        self.tokens.selecionarProximo()
        if(self.tokens.atual.tipo == "OPEN_P"):
            self.tokens.selecionarProximo()
            resultado = UnOp('RETURN', [self.expressao()])
            if(self.tokens.atual.tipo=='CLOSE_P'):
                    self.tokens.selecionarProximo()
                    if(self.tokens.atual.tipo == 'SEMICOLON'):
                        self.tokens.selecionarProximo() 
                        return resultado
                    else:
                        raise Exception("Erro: Ponto e virgula")
            else:
                raise Exception("Erro: Fechar parenteses")
        else:
            raise Exception("Erro: Abrir parenteses")
    
    def declaracao(self):
        tipo = self.tokens.atual.tipo
        self.tokens.selecionarProximo()
        declaracao_children = []
        if(self.tokens.atual.tipo == 'VAR'):
            var = self.tokens.atual.valor
            self.tokens.selecionarProximo()
            if(self.tokens.atual.tipo=='OPEN_P'):
                func_dec_children =[]
                func_dec_children.append(tipo)
                name_func = var
                self.tokens.selecionarProximo()
                while(self.tokens.atual.tipo != 'CLOSE_P'):
                    tipo_arg = self.tipo()
                    arg = VarVal(self.tokens.atual.valor,[])
                    vd = VarDec (tipo_arg, [arg])
                    func_dec_children.append(vd)
                    self.tokens.selecionarProximo()
                    while(self.tokens.atual.tipo == 'COLON'):
                        self.tokens.selecionarProximo()
                        tipo_arg = self.tipo()
                        arg = VarVal(self.tokens.atual.valor,[])
                        vd = VarDec (tipo_arg, [arg])
                        func_dec_children.append(vd)
                        self.tokens.selecionarProximo()
                if(self.tokens.atual.tipo == 'CLOSE_P'):
                    self.tokens.selecionarProximo()
                    func_dec_children.append(self.comandos())
                    return FuncDec(name_func, func_dec_children)
                else:
                    raise Exception ("Erro: Fechar Parenteses")
            else:
                var = VarVal(var,[])
                declaracao_children.append(var)
                while(self.tokens.atual.tipo=='COLON'):
                    self.tokens.selecionarProximo()
                    if(self.tokens.atual.tipo == 'VAR'):
                        var = VarVal(self.tokens.atual.valor,[])
                        declaracao_children.append(var)
                        self.tokens.selecionarProximo()
                    else:
                        raise Exception("Erro declaração com virgula")
                if(self.tokens.atual.tipo == 'SEMICOLON'):
                    self.tokens.selecionarProximo()
                    return VarDec (tipo, declaracao_children)
                else:
                    raise Exception("Erro: Ponto e virgula")
        else:
            raise Exception("Erro declaração")

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
                if(self.tokens.atual.tipo == 'SEMICOLON'):
                    self.tokens.selecionarProximo() 
                    return resultado
                else:
                    raise Exception("Erro: Ponto e virgula")
            else:
                raise Exception("Erro: Fechar parenteses")
        else:
            raise Exception("Erro: Abrir parenteses")

    def atribuicao(self):
        name = VarVal(self.tokens.atual.valor,[])
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
            elif(self.tokens.atual.tipo == 'VAR'):
                peek_token = self.tokens.peek(1)
                if(peek_token.tipo == 'OPEN_P'):
                    resultado = self.funcCall()
                    self.tokens.selecionarProximo()
                else:
                    resultado = self.expressao()
            else:
                resultado = self.expressao()
            if(self.tokens.atual.tipo == 'SEMICOLON'):
                self.tokens.selecionarProximo() 
            else:
                raise Exception("Erro: Ponto e virgula")
            return BinOp('ATRI',[name, resultado])
        else:
            raise Exception("Erro: Inserir '=' ")

    def funcCall(self):
        func_call_arg =[]
        if(self.tokens.atual.tipo == 'VAR'):
            name_func = self.tokens.atual.valor
            self.tokens.selecionarProximo() 
        if(self.tokens.atual.tipo == 'OPEN_P'):
            self.tokens.selecionarProximo() 
            while(self.tokens.atual.tipo != 'CLOSE_P'):
                exp = self.expressao()
                func_call_arg.append(exp)
                while(self.tokens.atual.tipo == 'COLON'):
                    self.tokens.selecionarProximo() 
                    exp = self.expressao()
                    func_call_arg.append(exp)
                if(self.tokens.atual.tipo == 'CLOSE_P'):
                    return FuncCall(name_func, func_call_arg)
                else:
                    raise Exception("Erro: Funcao sem fechar parenteses")
        else:
            raise Exception ("Erro: Funcao sem abrir parenteses")
    
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
            peek_token = self.tokens.peek(1)
            if(peek_token.tipo == 'OPEN_P'):
                resultado = self.funcCall()
                self.tokens.selecionarProximo()
                return resultado
            else:
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
