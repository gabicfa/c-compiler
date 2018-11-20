from prepro import PrePro
from tokenizador import Tokenizador
from analisador import Analisador
from symboltable import SymbleTable
from identificador import Id

if __name__ == "__main__":

    with open('src/input.c', 'r') as myfile:
        input_file=myfile.read().replace('\n', '')
    input_file = PrePro.comentarios(input_file)

    table = SymbleTable()
    tokenizador = Tokenizador(input_file,0,'null')
    tokenizador.selecionarProximo()
    analisador = Analisador(tokenizador, table)
    r = analisador.programa()
    tokenizador.selecionarProximo()

    if(tokenizador.atual.tipo == 'FIM'):
        r.evaluate(table, True)
    else:
        raise Exception("Erro: Análise terminou antes do fim do arquivo de entrada")
    Id.writeAssembly()