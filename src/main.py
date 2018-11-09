from prepro import PrePro
from tokenizador import Tokenizador
from analisador import Analisador

if __name__ == "__main__":

    with open('../input.c', 'r') as myfile:
        input_file=myfile.read().replace('\n', '')
    input_file = PrePro.comentarios(input_file)

    table = None
    tokenizador = Tokenizador(input_file,0,'null')
    tokenizador.selecionarProximo()
    analisador = Analisador(tokenizador, table)
    r = analisador.programa()
    tokenizador.selecionarProximo()

    if(tokenizador.atual.tipo == 'FIM'):
        r.evaluate(table)
    else:
        raise Exception("Erro: Análise terminou antes do fim do arquivo de entrada")
