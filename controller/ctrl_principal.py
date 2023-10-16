from controller.ctrl_grupo import CtrlGrupo
from controller.ctrl_midia import CtrlMidia
from controller.ctrl_pessoa import CtrlPessoa
from view.tela_principal import TelaPrincipal
import os

class CtrlPrincipal():
    def __init__(self):
        self.__ctrl_grupo = CtrlGrupo(self)
        self.__ctrl_midia = CtrlMidia(self)
        self.__ctrl_pessoa = CtrlPessoa(self)
        
        self.__tela_principal = TelaPrincipal()
    
    @property
    def ctrl_grupo(self):
        return self.__ctrl_grupo
    
    @property
    def ctrl_midia(self):
        return self.__ctrl_midia
    
    @property
    def ctrl_pessoa(self):
        return self.__ctrl_pessoa
    
    def inicia(self):
        self.abre_tela()
    
    def gerencia_midia(self):
        self.__ctrl_midia.abre_tela()
    
    def gerencia_pessoa(self):
        self.__ctrl_pessoa.abre_tela()
    
    def gerencia_grupo(self):
        self.__ctrl_grupo.abre_tela()
    
    def gera_relatorio(self):
        pass
    
    def abre_tela(self):
        self.__tela_principal.mostra_opcoes()

        lista_opcoes = {1: self.gerencia_midia, 2: self.gerencia_pessoa, 3: self.gerencia_grupo, 4: self.gera_relatorio, 5: self.encerra}
        
        while True:
            opcao = self.__tela_principal.recebe_input_int("Escolha uma opção (principal): ",[1, 2, 3, 4, 5])
            escolha = lista_opcoes[opcao]
            escolha()
            
        
    def encerra(self):
        exit(0)