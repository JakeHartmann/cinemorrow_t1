from view.tela_grupo import TelaGrupo
from model.grupo import Grupo
from model.grupo_dao import GrupoDAO


class CtrlGrupo():
    def __init__(self, ctrl_principal):
        self.__ctrl_principal = ctrl_principal

        self.__tela_grupo = TelaGrupo()

        self.__grupo_dao = GrupoDAO()

    @property
    def grupo_dao(self):
        return self.__grupo_dao

    def abre_tela(self):
        lista_opcoes = {
            1: self.cria_grupo,
            2: self.remove_grupo,
            3: self.altera_grupo,
            4: self.lista_grupos,
            5: self.retorna
        }

        while True:
            opcao = self.__tela_grupo.tela_opcoes()
            escolha = lista_opcoes[opcao]
            escolha()

    def cria_grupo(self):

        grupos = self.__grupo_dao.get_all()
        pessoas = self.__ctrl_principal.ctrl_pessoa.pessoa_dao.get_all()
        midias = self.__ctrl_principal.ctrl_midia.midia_dao.get_all()

        if self.__ctrl_principal.existem_pessoas() and self.__ctrl_principal.existem_midias():

            resultado = self.__tela_grupo.pega_dados_grupo(pessoas, midias)

            if resultado is None:
                self.abre_tela()

            else:
                nome, integrante, midia_associada, data = resultado

                email_start = integrante.find("(") + 1
                email_end = integrante.find(")")
                somente_email = integrante[email_start: email_end].strip()

                pessoa_escolhida = self.__ctrl_principal.ctrl_pessoa.pessoa_dao.get(
                    somente_email)
                midia_associada = self.__ctrl_principal.ctrl_midia.midia_dao.get(
                    midia_associada)

                if grupos:
                    for grupo in grupos:
                        if grupo.nome == nome:
                            self.__tela_grupo.show_message(
                                "Alerta!", "Esse nome de grupo já está sendo utilizado.")
                            self.abre_tela()

                grupo = Grupo(nome, pessoa_escolhida, midia_associada, data)
                self.__grupo_dao.add(grupo)
                self.__tela_grupo.show_message(
                    "Sucesso!", f"Grupo '{nome}' foi criado com sucesso")

        else:
            if self.__ctrl_principal.existem_pessoas() and not self.__ctrl_principal.existem_midias():
                self.__tela_grupo.show_message(
                    "Alerta!", "Não existe nenhuma mídia cadastrada.")
                self.abre_tela()
            elif self.__ctrl_principal.existem_midias() and not self.__ctrl_principal.existem_pessoas():
                self.__tela_grupo.show_message(
                    "Alerta!", "Não existe nenhuma pessoa cadastrada.")
                self.abre_tela()
            else:
                self.__tela_grupo.show_message(
                    "Alerta!", "Não existe nenhuma pessoa e nenhuma mídia cadastrada.")
                self.abre_tela()

            self.abre_tela()

    def remove_grupo(self):

        grupos = self.__grupo_dao.get_all()

        if not grupos:
            self.__tela_grupo.show_message(
                "Alerta!", "Não há grupos cadastrados.")
            self.abre_tela()

        grupo_escolhido = self.__tela_grupo.mostra_lista_grupos(
            grupos, allow_selection=True)
        if grupo_escolhido is None:
            self.abre_tela()

        if grupos:
            self.__grupo_dao.remove(grupo_escolhido.nome)
            self.__tela_grupo.show_message(
                "Sucesso!", f"O grupo '{grupo_escolhido.nome}' foi removido com sucesso.")

        self.abre_tela()

    def altera_grupo(self):

        grupos = self.__grupo_dao.get_all()

        if grupos:

            grupo_escolhido = self.__tela_grupo.mostra_lista_grupos(
                grupos, allow_selection=True)

            if grupo_escolhido is None:
                self.abre_tela()

            lista_opcoes = {
                '-ALTERAR_NOME-': self.altera_nome,
                '-ADICIONAR_MEMBRO-': self.adiciona_membro,
                '-REMOVER_MEMBRO-': self.remove_membro,
                '-ALTERAR_DATA_SESSAO-': self.altera_data_proxima_sessao
            }

            opcao = self.__tela_grupo.mostra_opcoes_alteracao()
            if opcao is None:
                self.abre_tela()

            escolha = lista_opcoes[opcao]
            escolha(grupo_escolhido)

        else:
            self.__tela_grupo.show_message(
                "Alerta!", "Não há grupos cadastrados.")

        self.abre_tela()

    def altera_nome(self, grupo):
        novo_nome = self.__tela_grupo.pega_nome_grupo()
        if novo_nome is None:
            self.abre_tela()

        self.__grupo_dao.remove(grupo.nome)
        grupo.nome = novo_nome
        self.__grupo_dao.add(grupo)
        self.__tela_grupo.show_message(
            "Sucesso!", f"Nome do grupo '{grupo.nome}' alterado com sucesso.")
        self.abre_tela()

    def adiciona_membro(self, grupo):

        disponiveis = []
        # Lista de pessoas que não estão nesse grupo
        for pessoa in self.__ctrl_principal.ctrl_pessoa.pessoa_dao.get_all():
            pessoa_emails_grupo = [
                p.email for p in self.__grupo_dao.get(grupo.nome).pessoas]
            if pessoa.email not in pessoa_emails_grupo:
                disponiveis.append(pessoa)

        if disponiveis:
            pessoa_escolhida_email = self.__tela_grupo.seleciona_pessoa(
                disponiveis)
            if pessoa_escolhida_email is None:
                self.abre_tela()

            pessoa_escolhida = self.__ctrl_principal.ctrl_pessoa.pessoa_dao.get(
                pessoa_escolhida_email)

            self.__grupo_dao.get(grupo.nome).pessoas.append(pessoa_escolhida)
            self.__grupo_dao.dump()
            self.__tela_grupo.show_message(
                "Sucesso!", f"{pessoa_escolhida.nome} foi adicionado ao grupo '{grupo.nome}' com sucesso.")

        else:
            self.__tela_grupo.show_message(
                "Alerta!", "Não há pessoas disponíveis para adicionar ao grupo.")

        self.abre_tela()

    def remove_membro(self, grupo):

        if not grupo.pessoas:
            self.__tela_grupo.show_message(
                "Alerta!", f"O grupo '{grupo.nome}' não possui membros para remover.")
        else:
            pessoa_escolhida_email = self.__tela_grupo.seleciona_pessoa(
                grupo.pessoas)
            if pessoa_escolhida_email is None:
                self.abre_tela()
            pessoa_escolhida = self.__ctrl_principal.ctrl_pessoa.pessoa_dao.get(
                pessoa_escolhida_email)

            for pessoa in self.__grupo_dao.get(grupo.nome).pessoas:
                if pessoa.email == pessoa_escolhida_email:
                    self.__grupo_dao.get(grupo.nome).pessoas.remove(pessoa)
            self.__grupo_dao.dump()
            self.__tela_grupo.show_message(
                "Sucesso!", f"{pessoa_escolhida.nome} foi removido(a) do grupo '{grupo.nome}' com sucesso.")

        self.abre_tela()

    def lista_grupos(self):

        grupos = self.__grupo_dao.get_all()

        if not grupos:
            self.__tela_grupo.show_message(
                "Alerta!", "Não há grupos cadastrados.")
            self.abre_tela()

        self.__tela_grupo.mostra_lista_grupos(grupos)
        self.abre_tela()

    def altera_data_proxima_sessao(self, grupo):

        nova_data = self.__tela_grupo.pega_data()
        if nova_data is None:
            self.abre_tela()

        self.__grupo_dao.get(grupo.nome).data = nova_data
        self.__grupo_dao.dump()
        self.__tela_grupo.show_message(
            "Sucesso!", f"Data da próxima sessão do grupo '{grupo.nome}' foi alterada com sucesso.")

        self.abre_tela()

    def retorna(self):
        self.__ctrl_principal.abre_tela()
