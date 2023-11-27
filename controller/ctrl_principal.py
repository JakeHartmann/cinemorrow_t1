from controller.ctrl_grupo import CtrlGrupo
from controller.ctrl_midia import CtrlMidia
from controller.ctrl_pessoa import CtrlPessoa
from controller.ctrl_relatorio import CtrlRelatorio
from view.tela_principal import TelaPrincipal
from view.tela_relatorio import TelaRelatorio


class CtrlPrincipal():
    def __init__(self):
        self.ctrl_grupo = CtrlGrupo(self)
        self.ctrl_midia = CtrlMidia(self)
        self.ctrl_pessoa = CtrlPessoa(self)
        self.ctrl_relatorio = CtrlRelatorio(self)

        self.tela_principal = TelaPrincipal()
        self.tela_relatorio = TelaRelatorio()

    def inicia(self):
        self.abre_tela()

    def gerencia_midia(self):
        self.ctrl_midia.abre_tela()

    def gerencia_pessoa(self):
        self.ctrl_pessoa.abre_tela()

    def gerencia_grupo(self):
        self.ctrl_grupo.abre_tela()

    def gera_relatorio(self):
        self.ctrl_relatorio.abre_tela()

    def abre_tela(self):
        lista_opcoes = {
            1: self.gerencia_midia,
            2: self.gerencia_pessoa,
            3: self.gerencia_grupo,
            4: self.gera_relatorio,
            5: self.encerra
        }

        while True:
            opcao = self.tela_principal.tela_opcoes()
            escolha = lista_opcoes[opcao]
            escolha()

    def existem_midias(self):
        if self.ctrl_midia.midia_dao.get_all():
            return True
        else:
            return False

    def existem_pessoas(self):
        if self.ctrl_pessoa.pessoa_dao.get_all():
            return True
        else:
            return False

    # Não sei se isso funciona ainda
    def pessoa_is_membro_do_grupo(self, pessoa, grupo):
        grupo_em_questao = self.ctrl_grupo.grupo_dao.get(grupo.nome)
        return pessoa in grupo_em_questao.pessoas

    def encerra(self):
        exit(0)
