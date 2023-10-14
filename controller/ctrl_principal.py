from controller.ctrl_grupo import CtrlGrupo
from controller.ctrl_midia import CtrlMidia
from controller.ctrl_pessoa import CtrlPessoa
from view.tela_principal import TelaPrincipal

class CtrlPrincipal():
    def __init__(self) -> None:
        self.__ctrl_grupo = CtrlGrupo(self)
        self.__ctrl_midia = CtrlMidia(self)
        self.__ctrl_pessoa = CtrlPessoa(self)
        
        self.__tela_principal = TelaPrincipal()
    
    def inicia():
        pass
    
    def gera_relatorio():
        pass