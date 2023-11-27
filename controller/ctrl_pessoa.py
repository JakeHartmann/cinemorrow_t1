from view.tela_pessoa import TelaPessoa
from model.pessoa import Pessoa
from model.pessoa_dao import PessoaDAO
import os


class CtrlPessoa():
    def __init__(self, ctrl_principal):
        self.__ctrl_principal = ctrl_principal

        self.__tela_pessoa = TelaPessoa()

        self.__pessoa_dao = PessoaDAO()

    @property
    def pessoa_dao(self):
        return self.__pessoa_dao

    def abre_tela(self):
        lista_opcoes = {
            1: self.cria_pessoa,
            2: self.remove_pessoa,
            3: self.altera_pessoa,
            4: self.lista_pessoas,
            5: self.retorna
        }

        while True:
            opcao = self.__tela_pessoa.tela_opcoes()
            escolha = lista_opcoes[opcao]
            escolha()

    def cria_pessoa(self):

        nome, email, midia_fav = self.__tela_pessoa.pega_dados_pessoa()
        if nome is None and email is None and midia_fav is None:
            self.abre_tela()
        email = email.lower()

        if self.__pessoa_dao.get_all():
            for pessoa in self.__pessoa_dao.get_all():
                if pessoa.email == email:
                    self.__tela_pessoa.show_message(
                        "Alerta!", "Esse e-mail já está sendo utilizado.")
                    self.abre_tela()
                    return

        nova_pessoa = Pessoa(nome, email, midia_fav)
        self.__pessoa_dao.add(nova_pessoa)
        self.__tela_pessoa.show_message(
            "Sucesso!", f"'{nome}' foi adicionado(a) com sucesso.")
        self.abre_tela()

    def remove_pessoa(self):
        pessoas = self.__pessoa_dao.get_all()
        if not pessoas:
            self.__tela_pessoa.show_message(
                "Alerta!", "Não há nenhuma pessoa cadastrada.")
            self.abre_tela()

        pessoa_escolhida = self.__tela_pessoa.mostra_lista_pessoas(
            pessoas, allow_selection=True)
        if pessoa_escolhida is None:
            self.abre_tela()

        pessoa_em_grupo = any(
            pessoa_escolhida in grupo.pessoas for grupo in self.__ctrl_principal.ctrl_grupo.grupo_dao.get_all())

        if pessoa_em_grupo:
            self.__tela_pessoa.show_message(
                "Alerta!", f"Não é possível excluir a pessoa '{pessoa_escolhida.nome}', pois ela é membro de um grupo.")
        else:
            self.__tela_pessoa.show_message(
                "Sucesso!", f"A pessoa '{pessoa_escolhida.nome}' com o E-Mail '{pessoa_escolhida.email}' foi removida com sucesso.")
            self.__pessoa_dao.remove(pessoa_escolhida.email)

        self.abre_tela()

    def altera_pessoa(self):

        pessoas = self.__pessoa_dao.get_all()

        if not pessoas:
            self.__tela_pessoa.show_message(
                "Alerta!", "Não há pessoas cadastradas.")
            self.abre_tela()

        pessoa_escolhida = self.__tela_pessoa.mostra_lista_pessoas(
            pessoas, allow_selection=True)
        if pessoa_escolhida is None:
            self.abre_tela()

        novo_nome, novo_email, nova_midia_fav = self.__tela_pessoa.pega_dados_pessoa(
            novos_dados=True)
        for pessoa in pessoas:
            if pessoa.email == novo_email:
                self.__tela_pessoa.show_message(
                    "Alerta!", "Esse email já está sendo utilizado.")
                self.abre_tela()

        self.__pessoa_dao.remove(pessoa_escolhida.email)
        pessoa_escolhida.email = novo_email
        self.__pessoa_dao.add(pessoa_escolhida)

        self.__pessoa_dao.get(pessoa_escolhida.email).nome = novo_nome
        self.__pessoa_dao.dump()

        self.__pessoa_dao.get(
            pessoa_escolhida.email).midia_fav = nova_midia_fav
        self.__pessoa_dao.dump()

        self.__tela_pessoa.show_message(
            "Sucesso!", f"Os dados da pessoa '{pessoa_escolhida.nome}' (E-Mail: {pessoa_escolhida.email}) foram alterados com sucesso.")
        self.abre_tela()

    def lista_pessoas(self):

        pessoas = self.__pessoa_dao.get_all()

        if not pessoas:
            self.__tela_pessoa.show_message(
                "Alerta!", "Não há pessoas cadastradas.")
            self.abre_tela()

        self.__tela_pessoa.mostra_lista_pessoas(pessoas)
        self.abre_tela()

    def retorna(self):
        self.__ctrl_principal.abre_tela()
