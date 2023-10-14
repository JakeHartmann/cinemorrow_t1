from controller.ctrl_principal import CtrlPrincipal
from view.tela_pessoa import TelaPessoa
from model.pessoa import Pessoa

class CtrlPessoa():
    def __init__(self, ctrl_principal: CtrlPrincipal) -> None:
        if isinstance(ctrl_principal, CtrlPrincipal):
            self.__ctrl_principal = ctrl_principal
            
        self.__tela_pessoa = TelaPessoa()
        
        self.__pessoas = []