import os


class TelaPrincipal():
    def __init__(self):
        pass

    def mostra_opcoes(self):
        os.system('cls||clear')
        print(""+"-="*45)
        logo = '''
  ####     ####    ##  ##   ######   ##   ##   ####    ######   ######   ######   ##   ## 
 ##  ##     ##     ### ##   ##       ### ###  ##  ##   ##  ##   ##  ##   ##  ##   ##   ## 
 ##         ##     ######   ##       #######  ##  ##   ##  ##   ##  ##   ##  ##   ##   ## 
 ##         ##     ######   ####     ## # ##  ##  ##   #####    #####    ##  ##   ## # ## 
 ##         ##     ## ###   ##       ##   ##  ##  ##   ####     ####     ##  ##   ####### 
 ##  ##     ##     ##  ##   ##       ##   ##  ##  ##   ## ##    ## ##    ##  ##   ### ### 
  ####     ####    ##  ##   ######   ##   ##   ####    ##  ##   ##  ##    ####    ##   ## 
        '''
        print(logo)
        print(""+"-="*45)
        print("""
    1 - Gerenciar Mídias
    2 - Gerenciar Pessoas
    3 - Gerenciar Grupos
    4 - Relatórios
    5 - Encerrar
              """)

    def abre_tela_relatorio(self):
        os.system('cls||clear')
        print(" "*5+"Relatórios")
        print(""+"-="*13)

        print("""
    1 - Tipo de Mídia favorita mais comum
    2 - Pessoa em mais grupos
    3 - Grupo com mais pessoas
    4 - Mídia mais assistida
    5 - Voltar""")

    def recebe_input_int(self, mensagem: str = "", inteiros_validos: [] = None):
        while True:
            valor_lido = input(mensagem)
            try:
                inteiro = int(valor_lido)
                if inteiros_validos and inteiro not in inteiros_validos:
                    raise ValueError
                return inteiro
            except ValueError:
                print("Por favor digite um valor válido")
