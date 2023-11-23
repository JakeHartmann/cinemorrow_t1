import os
from view.abstract_tela import AbstractTela


class TelaPrincipal(AbstractTela):
    def __init__(self):
        pass

    def abre_tela_relatorio(self):
        os.system('cls||clear')
        nome_tela = 'Relatórios'
        print(f'{nome_tela:~^45}')
        print("""
    1 - Tipo de Mídia favorita mais comum
    2 - Pessoa em mais grupos
    3 - Grupo com mais pessoas
    4 - Mídia mais assistida
    5 - Voltar""")
