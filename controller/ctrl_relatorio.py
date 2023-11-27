from view.tela_relatorio import TelaRelatorio
from collections import Counter


class CtrlRelatorio():
    def __init__(self, ctrl_principal) -> None:
        self.__ctrl_principal = ctrl_principal

        self.__tela_relatorio = TelaRelatorio()
        self.__registro = 0

    @property
    def tela_relatorio(self):
        return self.__tela_relatorio

    def abre_tela(self):
        lista_opcoes = {
            'Tipo_Midia': self.gera_relatorio,
            'Voltar': self.retorna
        }

        while True:
            opcao = self.__tela_relatorio.tela_opcoes()
            escolha = lista_opcoes[opcao]
            escolha()

    def gera_relatorio(self):
        self.__registro += 1
        self.__tela_relatorio.mostra_relatorio(
            self.__ctrl_principal.ctrl_pessoa.pessoa_dao.get_all(), num_registro=self.__registro)

    def retorna(self):
        self.__ctrl_principal.abre_tela()
