from view.tela_grupo import TelaGrupo
from model.grupo import Grupo
from datetime import datetime


class CtrlGrupo():
    def __init__(self, ctrl_principal):
        self.__ctrl_principal = ctrl_principal
        
        self.__tela_grupo = TelaGrupo()
        
        self.__grupos = []
    
    @property
    def grupos(self):
        return self.__grupos

    def abre_tela(self):
        self.__tela_grupo.mostra_opcoes()
        
        lista_opcoes = {1: self.cria_grupo, 2: self.remove_grupo,
                        3: self.altera_grupo, 4: self.lista_grupos, 5: self.retorna}

        while True:
            opcao = self.__tela_grupo.recebe_input_int("Escolha uma opção (grupos): ", [1, 2, 3, 4, 5])
            escolha = lista_opcoes[opcao]
            escolha()

    def cria_grupo(self):
        titulo = str(input("Digite o título do grupo: "))
        # to do: checar se existe pelo menos um objeto de pessoa já existente
        integrante = str(input("Digite o email do integrante base do grupo: "))
        # to do: checar se existe pelo menos um objeto de mídia já existente
        midia_associada = int(input("Digite o índice associado à Mídia: "))
        ano = int(input("Digite o ano da sessão do grupo: "))
        mes = int(input("Digite o mês da sessão do grupo: "))
        dia = int(input("Digite o dia da sessão do grupo: "))
        hora = int(input("Digite a hora da sessão do grupo: "))
        minutos = int(input("""Digite os minutos da sessão do grupo
                        (aperte enter caso seja uma hora em ponto): """))
        self.__grupos.append(Grupo(titulo, integrante, midia_associada, datetime(ano, mes, dia, hora, minutos)))    

    def remove_grupo(self):
        pass
    
    def altera_grupo(self):
        pass
    
    def adiciona_membro(self):
        pass
    
    def remove_membro(self):
        pass
    
    def lista_grupos(self):
        pass
    
    def imprimir_grupo(self, grupo: Grupo):
        print(f"Nome do grupo: {grupo.titulo}")
        print(f"Membros do grupo:")
        for membro in grupo.pessoas:
            print("- " + membro.nome)
        print(f"Midia associada ao grupo: {grupo.midia_associada.titulo} ({type(grupo.midia_associada).__name__})")
        print(f"Data da próxima sessão do grupo: {grupo.data.strftime('%Y-%m-%d')} às {grupo.data.strftime('%H:%M')}")
    
    def retorna(self):
        self.__ctrl_principal.abre_tela()
