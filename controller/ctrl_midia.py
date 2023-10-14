from controller.ctrl_principal import CtrlPrincipal
from model.midia import Midia
from view.tela_midia import TelaMidia


class CtrlMidia():
    def __init__(self, ctrl_principal: CtrlPrincipal):
        if isinstance(ctrl_principal, CtrlPrincipal):
            self.__ctrl_principal = ctrl_principal
        self.__tela_midia = TelaMidia()
        
        self.__series = []
        self.__filmes = []
        
    def cria_midia():
        pass
    
    def remove_midia():
        pass
    
    def altera_midia():
        pass
    
    def lista_midias():
        pass
