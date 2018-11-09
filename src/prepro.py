import re
input_file_list = []

class PrePro:
    @staticmethod
    def espaco(input):
        for line in input:
            for char in line:
                if(char != "\n"):
                    input_file_list.append(char)
        input_file_string = ''.join(map(str, input_file_list))

        espaco_entre_numeros = re.search('[0-9] +[0-9]', input_file_string)
        espaco_entre_numeros_e_letras = re.search('[a-z] +[0-9]', input_file_string)

        if espaco_entre_numeros or espaco_entre_numeros_e_letras:
            raise Exception("Erro nos espaços")
        else:
            input_sem_espaco = input_file_string.replace(" ","")
            return input_sem_espaco

    @staticmethod
    def comentarios(input):
        input_sem_comentarios = re.sub('/\*(.*?)\*/', '', input)
        input_com_comentario_errado = re.search('/\*', input_sem_comentarios)
        if input_com_comentario_errado:
            raise Exception("Erro no comentario")
        return input_sem_comentarios