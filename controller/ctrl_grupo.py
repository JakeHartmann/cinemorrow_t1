from view.tela_grupo import TelaGrupo
from model.grupo import Grupo
from model.serie import Serie
from model.temporada import Temporada
from model.episodio import Episodio
from model.progresso import Progresso
from model.grupo_dao import GrupoDAO
from datetime import datetime
import os


class CtrlGrupo():
    def __init__(self, ctrl_principal):
        self.__ctrl_principal = ctrl_principal

        self.__tela_grupo = TelaGrupo()

        self.__grupos = []

        self.__grupo_dao = GrupoDAO()

    @property
    def grupos(self):
        return self.__grupos

    @property
    def grupo_dao(self):
        return self.__grupo_dao

    def abre_tela(self):
        os.system('cls||clear')
        nome_tela = 'Gerencia de Grupos'
        opcoes = """
    1 - Criar Grupo
    2 - Remover Grupo
    3 - Alterar Grupo
    4 - Listar Grupos
    5 - Voltar
    """
        self.__tela_grupo.output_texto(f'{nome_tela:~^40}')
        self.__tela_grupo.output_texto(opcoes)
        
        lista_opcoes = {
            1: self.cria_grupo,
            2: self.remove_grupo,
            3: self.altera_grupo,
            4: self.lista_grupos,
            5: self.retorna
        }

        while True:
            opcao = self.__tela_grupo.recebe_input_int(
                "Escolha uma opção (grupos): ", [1, 2, 3, 4, 5])
            escolha = lista_opcoes[opcao]
            escolha()

    def cria_grupo(self):
        os.system('cls||clear')
        nome_subtela = 'Criação de Grupos'
        self.__tela_grupo.output_texto(f'{nome_subtela:~^40}')
        
        grupos = self.__grupo_dao.get_all()
        
        if self.__ctrl_principal.existem_pessoas() and self.__ctrl_principal.existem_midias():
            confirmacao = self.__tela_grupo.recebe_input_sn(
                "Deseja criar um novo grupo? (S/N): ")

            if confirmacao:
                nome = self.__tela_grupo.recebe_input_str(
                    "Digite o nome do grupo: ")

                if grupos:
                    for grupo in grupos:
                        if grupo.nome == nome:
                            self.__tela_grupo.output_texto("Esse nome de grupo já está sendo utilizado.")
                            self.standby()
                            return

                pessoas = self.__ctrl_principal.ctrl_pessoa.pessoa_dao.get_all()

                self.__tela_grupo.output_texto("")
                # Lista todas as pessoas instanciadas, junto com o nome e o email de cada uma
                for (i, pessoa) in enumerate(pessoas , start=1):
                    self.__tela_grupo.output_texto(f"[{i}] - {pessoa.nome} (E-Mail: {pessoa.email})")
                self.__tela_grupo.output_texto("0 para retornar")
                pessoas_validas = list(
                    range(1, len(pessoas) + 1)) + [0]

                opcao_pessoa = self.__tela_grupo.recebe_input_int(
                    "\nEscolha o índice associado de uma pessoa para registrá-la como integrante base: ", pessoas_validas)
                if opcao_pessoa == 0:
                    self.abre_tela()
                else:
                    pessoa_escolhida = pessoas[opcao_pessoa - 1]
                    self.__tela_grupo.output_texto(
                        f"'{pessoa_escolhida.nome}' foi escolhida como integrante base. ")
                # Lista todas as mídias instanciadas, separadas em filmes e séries
                todas_midias = self.__ctrl_principal.ctrl_midia.midia_dao.get_all()
                self.__tela_grupo.output_texto("")
                for (i, midia) in enumerate(todas_midias, start=1):
                    self.__tela_grupo.output_texto(f"[{i}] - {midia.titulo} ({type(midia).__name__})")
                midias_validas = list(range(1, len(todas_midias) + 1)) + [0]

                opcao_midia = self.__tela_grupo.recebe_input_int(
                    "\nEscolha o índice associado de uma mídia para registrá-la como associada: ", midias_validas)
                if opcao_midia == 0:
                    self.abre_tela()
                else:
                    midia_escolhida = todas_midias[opcao_midia - 1]

                    self.__tela_grupo.output_texto(
                        f"'{midia_escolhida.titulo}' foi escolhida como a mídia associada do grupo.")

                ano = self.__tela_grupo.recebe_input_int(
                    "Digite o ano da próxima sessão do grupo: ")
                mes = self.__tela_grupo.recebe_input_int(
                    "Digite o mês (1-12): ", list(range(1, 13)))
                dia = self.__tela_grupo.recebe_input_int(
                    "Digite o dia: ", inteiros_validos=self.dias_validos(mes, ano))
                hora, minutos = self.__tela_grupo.recebe_input_hora_minutos(
                    "Digite a hora e minutos (formato: HH:MM): ")

                grupo = Grupo(nome, pessoa_escolhida, midia_escolhida, datetime(ano, mes, dia, hora, minutos))
                if isinstance(midia_escolhida, Serie):
                    progresso = Progresso(midia_escolhida, grupo)
                self.__grupo_dao.add(grupo)
                self.__tela_grupo.output_texto(f"Grupo '{nome}' foi criado com sucesso")

        else:
            if self.__ctrl_principal.existem_pessoas() and not self.__ctrl_principal.existem_midias():
                self.__tela_grupo.output_texto("Não existe nenhuma mídia cadastrada.")
            elif self.__ctrl_principal.existem_midias() and not self.__ctrl_principal.existem_pessoas():
                self.__tela_grupo.output_texto("Não existe nenhuma pessoa cadastrada.")
            else:
                self.__tela_grupo.output_texto("Não existe nenhuma mídia e nenhuma pessoa cadastrada.")

        self.standby()

    def is_ano_bissexto(self, ano):
        if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
            return True
        return False

    def dias_validos(self, mes, ano):
        if mes in [1, 3, 5, 7, 8, 10, 12]:
            return list(range(1, 32))
        elif mes in [4, 6, 9, 11]:
            return list(range(1, 31))
        elif self.is_ano_bissexto(ano):
            return list(range(1, 30))
        else:
            return list(range(1, 29))

    def remove_grupo(self):
        os.system('cls||clear')
        nome_subtela = 'Remoção de Grupos'
        self.__tela_grupo.output_texto(f'{nome_subtela:~^40}')

        grupos = self.__grupo_dao.get_all()

        if grupos:
            self.__tela_grupo.output_texto("\nGrupos disponíveis para remoção:")
            for (i, grupo) in enumerate(grupos, start=1):
                self.__tela_grupo.output_texto(f"[{i}] - {grupo.nome}")

            # Pedir confirmação
            if self.__tela_grupo.recebe_input_sn("Deseja remover um grupo? (S/N): "):
                opcao_grupo = self.__tela_grupo.recebe_input_int(
                    "\nEscolha o índice associado ao grupo que deseja remover: ", list(range(1, len(grupos) + 1)))
                grupo_escolhido = grupos[opcao_grupo - 1]

                # Confirmar novamente
                if self.__tela_grupo.recebe_input_sn(f"Tem certeza que deseja remover o grupo '{grupo_escolhido.nome}'? (S/N): "):
                    self.__grupo_dao.remove(grupo_escolhido.nome)
                    self.__tela_grupo.output_texto(
                        f"O grupo '{grupo_escolhido.nome}' foi removido com sucesso.")
                else:
                    self.__tela_grupo.output_texto("Operação cancelada.")
            else:
                self.__tela_grupo.output_texto("Operação cancelada.")
        else:
            self.__tela_grupo.output_texto("Opa, parece que não há nenhum grupo cadastrado.")

        self.standby()

    def altera_grupo(self):
        os.system('cls||clear')
        nome_subtela = 'Alteração de Grupos'
        self.__tela_grupo.output_texto(f'{nome_subtela:~^40}')
        
        grupos = self.__grupo_dao.get_all()

        if grupos:
            for (i, grupo) in enumerate(grupos, start=1):
                self.__tela_grupo.output_texto(
                    f"[{i}] - Nome: {grupo.nome} (Midia associada: {grupo.midia_associada.titulo})")
                self.__tela_grupo.output_texto(
                    f"    Data da Próxima Sessão: {grupo.data.strftime('%d/%m/%Y - %H:%M')}")
                self.__tela_grupo.output_texto("    Membros:")
                for membro in grupo.pessoas:
                    self.__tela_grupo.output_texto(f"        {membro.nome} (E-Mail: {membro.email})")
            self.__tela_grupo.output_texto("")
            self.__tela_grupo.output_texto("0 para retornar")
            validos = list(range(1, len(grupos) + 1)) + [0]
            opcao_grupo = self.__tela_grupo.recebe_input_int(
                "Escolha o índice associado a um grupo para alterá-lo: ", validos)

            if opcao_grupo == 0:
                self.abre_tela()

            grupo_escolhido = grupos[opcao_grupo - 1]

            opcao_alteracao = self.__tela_grupo.recebe_input_int("""
1 - Alterar nome
2 - Adicionar membro
3 - Remover membro
4 - Alterar data da próxima sessão
5 - Voltar

Escolha a opção de alteração: """, [1, 2, 3, 4, 5])

            if opcao_alteracao == 1:
                self.altera_nome(grupo_escolhido)

            elif opcao_alteracao == 2:
                self.adiciona_membro(grupo_escolhido)

            elif opcao_alteracao == 3:
                self.remove_membro(grupo_escolhido)

            elif opcao_alteracao == 4:
                self.altera_data_proxima_sessao(grupo_escolhido)

            elif opcao_alteracao == 5:
                self.abre_tela()

        else:
            self.__tela_grupo.output_texto("Opa, parece que não há nenhum grupo cadastrado.")

        self.standby()

    # def exibe_episodios_temporada(self, temporada):
    #     for (i, episodio) in enumerate(temporada.episodios, start=1):
    #         status_assistido = "Assistido" if episodio.assistido else "Não assistido"
    #         self.__tela_grupo.output_texto(f"[{i}] - Episódio {episodio.numero}: {status_assistido}")

    # def altera_assistido_temporada(self, temporada):
    #     indice = self.__tela_grupo.recebe_input_int(
    #         "Escolha o índice associado a um episódio para alterar seu status de assistido: ",
    #         range(len(temporada.episodios) + 1)

    #     )
    #     if indice == 0:
    #         self.abre_tela()

    #     episodio_escolhido = temporada.episodios[indice - 1]

    #     novo_status = self.__tela_grupo.recebe_input_sn(
    #         "Marcar como assistido? (S/N): ")
    #     episodio_escolhido.assistido = (novo_status)

    #     self.__tela_grupo.output_texto(
    #         f"Status de assistido do episódio {episodio_escolhido.numero} alterado para {episodio_escolhido.assistido}")

    #     continuar_alterando = self.__tela_grupo.recebe_input_sn(
    #         "Deseja alterar o status de assistido de mais episódios? (S/N): ")
    #     if continuar_alterando:
    #         self.altera_assistido_temporada(temporada)
    #     else:
    #         self.altera_grupo()

    def altera_nome(self, grupo):
        novo_nome = self.__tela_grupo.recebe_input_str(
                    "Digite o novo nome para o grupo: ")
        self.__grupo_dao.remove(grupo.nome)
        grupo.nome = novo_nome
        self.__grupo_dao.add(grupo)
        self.__tela_grupo.output_texto(
                    f"Nome do grupo '{grupo.nome}' alterado com sucesso.")

    def adiciona_membro(self, grupo):
        os.system('cls||clear')
        nome_subtela = 'Adição de Membro ao Grupo'
        self.__tela_grupo.output_texto(f'{nome_subtela:~^40}')

        disponiveis = []
        # Lista de pessoas que não estão nesse grupo
        for pessoa in self.__ctrl_principal.ctrl_pessoa.pessoa_dao.get_all():
            pessoa_emails_grupo = [p.email for p in self.__grupo_dao.get(grupo.nome).pessoas]
            if pessoa.email not in pessoa_emails_grupo:
                disponiveis.append(pessoa)

        if disponiveis:
            self.__tela_grupo.output_texto("Pessoas Disponíveis:")
            for (i, pessoa) in enumerate(disponiveis, start=1):
                self.__tela_grupo.output_texto(f"[{i}] - Nome: {pessoa.nome} (E-Mail: {pessoa.email})")
            self.__tela_grupo.output_texto("")

            opcao_pessoa = self.__tela_grupo.recebe_input_int(
                "\nEscolha o índice associado a uma pessoa para adicioná-la ao grupo: ", list(range(1, len(disponiveis) + 1)))
            pessoa_escolhida = disponiveis[opcao_pessoa - 1]

            self.__grupo_dao.get(grupo.nome).pessoas.append(pessoa_escolhida)
            self.__grupo_dao.dump()
            self.__tela_grupo.output_texto(
                f"{pessoa_escolhida.nome} foi adicionado ao grupo '{grupo.nome}' com sucesso.")
        else:
            self.__tela_grupo.output_texto("Não há pessoas disponíveis para adicionar ao grupo.")

        self.standby()

    def remove_membro(self, grupo):
        os.system('cls||clear')
        nome_subtela = 'Remoção de Membro do Grupo'
        self.__tela_grupo.output_texto(f'{nome_subtela:~^40}')
        
        if not grupo.pessoas:
            self.__tela_grupo.output_texto(f"O grupo '{grupo.nome}' não possui membros para remover.")
        else:
            self.__tela_grupo.output_texto("Membros do Grupo:")
            for (i, pessoa) in enumerate(grupo.pessoas, start=1):
                self.__tela_grupo.output_texto(f"[{i}] - Nome: {pessoa.nome} (E-Mail: {pessoa.email})")
            self.__tela_grupo.output_texto("")

            opcao_pessoa = self.__tela_grupo.recebe_input_int(
                "\nEscolha o índice associado a um membro para removê-lo do grupo: ", list(range(1, len(grupo.pessoas) + 1)))
            pessoa_escolhida = grupo.pessoas[opcao_pessoa - 1]

            self.__grupo_dao.get(grupo.nome).pessoas.remove(pessoa_escolhida)
            self.__grupo_dao.dump()
            self.__tela_grupo.output_texto(
                f"{pessoa_escolhida.nome} foi removido(a) do grupo '{grupo.nome}' com sucesso.")

        self.standby()

    def lista_grupos(self):
        os.system('cls||clear')
        nome_subtela = 'Listagem de Grupos'
        self.__tela_grupo.output_texto(f'{nome_subtela:~^40}')
        
        grupos = self.__grupo_dao.get_all()
        
        if grupos:
            confirmacao = self.__tela_grupo.recebe_input_sn(
                "Deseja listar todos os grupos? (S/N): ")
            if confirmacao:
                for grupo in grupos:
                    self.__tela_grupo.output_texto("")
                    self.__tela_grupo.output_texto("-"*30)
                    self.__tela_grupo.output_texto(f"Nome do Grupo: {grupo.nome}")
                    self.__tela_grupo.output_texto(
                        f"Data da próxima sessão do Grupo: {grupo.data.strftime('%d/%m/%Y - %H:%M')}")
                    self.__tela_grupo.output_texto(f"Membros do Grupo:")
                    for membro in grupo.pessoas:
                        self.__tela_grupo.output_texto(f"        {membro.nome} (E-Mail: {membro.email})")

                    if isinstance(grupo.midia_associada, Serie):
                        total_episodios = sum(
                            len(temporada.episodios) for temporada in grupo.midia_associada.temporadas)
                        episodios_assistidos = sum(
                            episodio.assistido for temporada in grupo.midia_associada.temporadas for episodio in temporada.episodios)

                        episodios_restantes = total_episodios - episodios_assistidos

                        porcentagem_assistido = (
                            episodios_assistidos / total_episodios) * 100
                        self.__tela_grupo.output_texto(
                            f"Porcentagem de episódios assistidos: {porcentagem_assistido:.2f}%")
                        self.__tela_grupo.output_texto(
                            f"{episodios_assistidos}/{total_episodios} episódios ({episodios_restantes} episódios restantes)")

                    self.__tela_grupo.output_texto(
                        f"Midia associada ao Grupo: {grupo.midia_associada.titulo} ({type(grupo.midia_associada).__name__})")
            self.__tela_grupo.output_texto("")

        else:
            self.__tela_grupo.output_texto("Opa, parece que não há nenhum grupo cadastrado.")

        self.standby()

    def altera_data_proxima_sessao(self, grupo):
        os.system('cls||clear')
        nome_subtela = 'Alteração de Data da Próxima Sessão do Grupo'
        self.__tela_grupo.output_texto(f'{nome_subtela:~^40}')

        self.__tela_grupo.output_texto(
            f"A data atual da próxima sessão do grupo '{grupo.nome}' é {grupo.data.strftime('%d/%m/%Y - %H:%M')}.")
        data_atual_grupo = self.__grupo_dao.get(grupo.nome).data
        # Pedir confirmação pra cada ação
        if self.__tela_grupo.recebe_input_sn("Deseja alterar o ano? (S/N): "):
            novo_ano = self.__tela_grupo.recebe_input_int(
                "Digite o novo ano: ")
            
            self.__grupo_dao.get(grupo.nome).data = data_atual_grupo.replace(year=novo_ano)
            self.__grupo_dao.dump()
            self.__tela_grupo.output_texto(f"Ano alterado para {novo_ano}.")

        if self.__tela_grupo.recebe_input_sn("Deseja alterar o mês? (S/N): "):
            novo_mes = self.__tela_grupo.recebe_input_int(
                "Digite o novo mês (1-12): ", list(range(1, 13)))
            self.__grupo_dao.get(grupo.nome).data = data_atual_grupo.replace(month=novo_mes)
            self.__grupo_dao.dump()
            self.__tela_grupo.output_texto(f"Mês alterado para {novo_mes}.")

        if self.__tela_grupo.recebe_input_sn("Deseja alterar o dia? (S/N): "):
            novo_dia = self.__tela_grupo.recebe_input_int(
                "Digite o novo dia: ", inteiros_validos=self.dias_validos(grupo.data.month, grupo.data.year))
            self.__grupo_dao.get(grupo.nome).data = data_atual_grupo.replace(day=novo_dia)
            self.__grupo_dao.dump()
            self.__tela_grupo.output_texto(f"Dia alterado para {novo_dia}.")

        if self.__tela_grupo.recebe_input_sn("Deseja alterar a hora? (S/N): "):
            nova_hora, novo_minuto = self.__tela_grupo.recebe_input_hora_minutos(
                "Digite a nova hora e minutos (formato: HH:MM): ")
            self.__grupo_dao.get(grupo.nome).data = data_atual_grupo.replace(hour=nova_hora, minute=novo_minuto)
            self.__grupo_dao.dump()
            self.__tela_grupo.output_texto(f"Hora alterada para {nova_hora}:{novo_minuto}.")

        self.__tela_grupo.output_texto(
            f"A data da próxima sessão do grupo '{grupo.nome}' foi alterada com sucesso para {grupo.data.strftime('%d/%m/%Y - %H:%M')}.")
        self.standby()

    def standby(self):
        self.__tela_grupo.output_texto("\nAperte qualquer tecla para retornar à gerencia de grupos.")
        input()
        self.abre_tela()

    def retorna(self):
        self.__ctrl_principal.abre_tela()
