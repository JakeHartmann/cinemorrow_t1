from controller.ctrl_principal import CtrlPrincipal
from view.tela_grupo import TelaGrupo
from model.grupo import Grupo
from datetime import datetime


class CtrlGrupo():
    def __init__(self, ctrl_principal: CtrlPrincipal):
        if isinstance(ctrl_principal, CtrlPrincipal):
            self.__ctrl_principal = ctrl_principal
        
        self.__tela_grupo = TelaGrupo()
        
        self.__grupos = []
    
    def cria_grupo():
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
        return Grupo(titulo, integrante, midia_associada, datetime(ano, mes, dia, hora, minutos))    

    def remove_grupo():
        pass
    
    def modifica_grupo():
        pass
    
    def adiciona_membro():
        pass
    
    def remove_membro():
        pass
    
    def lista_grupos():
        pass