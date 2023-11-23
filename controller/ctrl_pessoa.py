from view.tela_pessoa import TelaPessoa
from model.pessoa import Pessoa
import os


class CtrlPessoa():
    def __init__(self, ctrl_principal):
        self.__ctrl_principal = ctrl_principal

        self.__tela_pessoa = TelaPessoa()

        self.__pessoas = []

    @property
    def pessoas(self):
        return self.__pessoas

    def abre_tela(self):
        os.system('cls||clear')
        nome_tela = 'Gerencia de Pessoas'
        opcoes = """
    1 - Adicionar Pessoa
    2 - Remover Pessoa
    3 - Alterar Pessoa
    4 - Listar Pessoas
    5 - Voltar
    """
        self.__tela_pessoa.output_texto(f'{nome_tela:~^40}')
        self.__tela_pessoa.output_texto(opcoes)
        
        lista_opcoes = {
            1: self.cria_pessoa,
            2: self.remove_pessoa,
            3: self.altera_pessoa,
            4: self.lista_pessoas,
            5: self.retorna
        }

        while True:
            opcao = self.__tela_pessoa.recebe_input_int(
                "Escolha uma opção (pessoas): ", [1, 2, 3, 4, 5])
            escolha = lista_opcoes[opcao]
            escolha()

    def cria_pessoa(self):
        os.system('cls||clear')
        nome_subtela = 'Criação de Pessoas'
        self.__tela_pessoa.output_texto(f'{nome_subtela:~^40}')
        
        confirmacao = self.__tela_pessoa.recebe_input_sn(
            "Deseja adicionar uma nova pessoa? (S/N): ")

        if confirmacao:
            nome = self.__tela_pessoa.recebe_input_str(
                "Digite o nome da pessoa: ")
            email = self.__tela_pessoa.recebe_input_str(
                f"Digite o email de '{nome}': ")

            if self.__pessoas:
                for pessoa in self.__pessoas:
                    if pessoa.email == email:
                        self.__tela_pessoa.output_texto("Esse email já está sendo utilizado.")
                        self.standby()
                        return

            tem_tipo_midia_fav = self.__tela_pessoa.recebe_input_sn(
                f"'{nome}' tem um tipo de mídia favorita? (S/N): ")
            if tem_tipo_midia_fav:
                midia_fav = self.__tela_pessoa.recebe_input_int(f"""
1 - Filme
2 - Série
        
Escolha o tipo de mídia favorito de '{nome}': """, [1, 2])
                if midia_fav == 1:
                    midia_fav = "Filme"
                elif midia_fav == 2:
                    midia_fav = "Série"
            else:
                midia_fav = None

            self.__pessoas.append(Pessoa(nome, email, midia_fav))
            self.__tela_pessoa.output_texto(f"'{nome}' foi adicionado(a) com sucesso.")
            self.standby()

        else:
            self.abre_tela()

    def remove_pessoa(self):
        os.system('cls||clear')
        nome_subtela = 'Remoção de Pessoa'
        self.__tela_pessoa.output_texto(f'{nome_subtela:~^40}')

        if self.__pessoas:
            # confirmacao = self.__tela_pessoa.recebe_input_sn("Deseja remover uma pessoa? (S/N): ")
            for (i, pessoa) in enumerate(self.__pessoas, start=1):
                self.__tela_pessoa.output_texto(f"[{i}] - {pessoa.nome} (E-Mail: {pessoa.email})")
            self.__tela_pessoa.output_texto("0 para retornar")
            validos = list(range(1, len(self.__pessoas) + 1)) + [0]

            opcao = self.__tela_pessoa.recebe_input_int(
                "\nEscolha o índice associado à pessoa para removê-la: ", validos)
            if opcao == 0:
                self.abre_tela()
            else:
                pessoa_escolhida = self.__pessoas[opcao - 1]

                pessoa_em_grupo = any(
                    pessoa_escolhida in grupo.pessoas for grupo in self.__ctrl_principal.ctrl_grupo.grupos)

                if pessoa_em_grupo:
                    self.__tela_pessoa.output_texto(
                        f"Não é possível excluir a pessoa '{pessoa_escolhida.nome}' pois ela é membro de um grupo.")
                else:
                    self.__tela_pessoa.output_texto(
                        f"A pessoa '{pessoa_escolhida.nome}' com o E-Mail '{pessoa_escolhida.email}' foi removida com sucesso.")
                    self.__pessoas.remove(pessoa_escolhida)

        else:
            self.__tela_pessoa.output_texto("Opa, parece que não há nenhuma pessoa cadastrada.")

        self.standby()

    def altera_pessoa(self):
        os.system('cls||clear')
        nome_subtela = 'Alteração de Pessoa'
        self.__tela_pessoa.output_texto(f'{nome_subtela:~^40}')
        
        if self.__pessoas:
            for (i, pessoa) in enumerate(self.__pessoas, start=1):
                self.__tela_pessoa.output_texto(
                    f"[{i}] - {pessoa.nome} (E-Mail: {pessoa.email}; Tipo de Midia Favorita: {pessoa.midia_fav})")
            self.__tela_pessoa.output_texto("0 para retornar")
            validos = list(range(1, len(self.__pessoas) + 1)) + [0]

            opcao = self.__tela_pessoa.recebe_input_int(
                "\nEscolha o índice associado à pessoa para alterá-la: ", validos)
            if opcao == 0:
                self.abre_tela()
            else:
                pessoa_escolhida = self.__pessoas[opcao - 1]

                quer_alterar_nome = self.__tela_pessoa.recebe_input_sn(
                    f"Deseja alterar o nome de '{pessoa_escolhida.nome}'? (S/N): ")
                if quer_alterar_nome:
                    novo_nome = self.__tela_pessoa.recebe_input_str(
                        f"Digite o novo nome para '{pessoa_escolhida.nome}': ")
                    pessoa_escolhida.nome = novo_nome

                quer_alterar_email = self.__tela_pessoa.recebe_input_sn(
                    f"Deseja alterar o E-Mail de '{pessoa_escolhida.nome}' (E-Mail atual: {pessoa_escolhida.email})? (S/N): ")
                if quer_alterar_email:
                    novo_email = self.__tela_pessoa.recebe_input_str(
                        f"Digite o novo E-Mail para '{pessoa_escolhida.nome}': ")
                    pessoa_escolhida.email = novo_email

                quer_alterar_midia_fav = self.__tela_pessoa.recebe_input_sn(
                    f"Deseja alterar o tipo de mídia favorito de '{pessoa_escolhida.nome}'? (S/N): ")
                if quer_alterar_midia_fav:
                    nova_midia_fav = self.__tela_pessoa.recebe_input_int(f"""
1 - Filme
2 - Série
3 - Nenhuma
        
Escolha o novo tipo de mídia favorito de '{pessoa_escolhida.nome}': """, [1, 2, 3])
                    if nova_midia_fav == 1:
                        pessoa_escolhida.midia_fav = "Filme"
                    elif nova_midia_fav == 2:
                        pessoa_escolhida.midia_fav = "Série"
                    elif nova_midia_fav == 3:
                        pessoa_escolhida.midia_fav = None

                if quer_alterar_nome or quer_alterar_email or quer_alterar_midia_fav:
                    self.__tela_pessoa.output_texto(
                        f"Os dados da pessoa '{pessoa_escolhida.nome}' (E-Mail: {pessoa_escolhida.email}) foram alterados com sucesso.")
                else:
                    self.__tela_pessoa.output_texto(
                        f"Não houve mudança nos dados de '{pessoa_escolhida.nome}' (E-Mail: {pessoa_escolhida.email}).")

        else:
            self.__tela_pessoa.output_texto("Opa, parece que não há nenhuma pessoa cadastrada.")

        self.standby()

    def lista_pessoas(self):
        os.system('cls||clear')
        nome_subtela = 'Listagem de Pessoas'
        self.__tela_pessoa.output_texto(f'{nome_subtela:~^40}')
        
        if self.__pessoas:
            confirmacao = self.__tela_pessoa.recebe_input_sn(
                "Deseja listar todas as pessoas cadastradas? (S/N): ")
            if confirmacao:
                for pessoa in self.__pessoas:
                    self.__tela_pessoa.output_texto(f"""
Nome: {pessoa.nome}
E-Mail: {pessoa.email}
Tipo de Midia Favorita: {pessoa.midia_fav} """)
            else:
                self.abre_tela()
        else:
            self.__tela_pessoa.output_texto("Opa, parece que não há nenhuma pessoa cadastrada.")

        self.standby()

    def standby(self):
        self.__tela_pessoa.output_texto("\nAperte qualquer tecla para retornar à gerencia de pessoas.")
        input()
        self.abre_tela()

    def retorna(self):
        self.__ctrl_principal.abre_tela()
