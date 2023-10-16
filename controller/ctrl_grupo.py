from view.tela_grupo import TelaGrupo
from model.grupo import Grupo
from model.serie import Serie
from model.temporada import Temporada
from model.episodio import Episodio
from datetime import datetime
import os
import copy


class CtrlGrupo():
    def __init__(self, ctrl_principal):
        self.__ctrl_principal = ctrl_principal
        
        self.__tela_grupo = TelaGrupo()
        
        self.__grupos = []
    
    @property
    def grupos(self):
        return self.__grupos

    def abre_tela(self):
        self.__tela_grupo.mostra_opcoes(titulo=" "*3+"Gerencia de Grupos", spacing=""+"-="*12+"-", opcoes="""
    1 - Criar Grupo
    2 - Remover Grupo
    3 - Alterar Grupo
    4 - Listar Grupos
    5 - Voltar
    """)
        
        lista_opcoes = {
            1: self.cria_grupo,
            2: self.remove_grupo,
            3: self.altera_grupo,
            4: self.lista_grupos,
            5: self.retorna
            }

        while True:
            opcao = self.__tela_grupo.recebe_input_int("Escolha uma opção (grupos): ", [1, 2, 3, 4, 5])
            escolha = lista_opcoes[opcao]
            escolha()

    def cria_grupo(self):
        self.__tela_grupo.imprime_opcoes("Criação de Grupos")
        if self.__ctrl_principal.existem_pessoas() and self.__ctrl_principal.existem_midias():
            confirmacao = self.__tela_grupo.recebe_input_sn("Deseja criar um novo grupo? (S/N): ")

            if confirmacao:
                nome = self.__tela_grupo.recebe_input_str("Digite o nome do grupo: ")
                
                print()
                # Lista todas as pessoas instanciadas, junto com o nome e o email de cada uma
                for (i, pessoa) in enumerate(self.__ctrl_principal.ctrl_pessoa.pessoas, start=1):
                    print(f"[{i}] - {pessoa.nome} (E-Mail: {pessoa.email})")
                print("0 para retornar")
                pessoas_validas = list(range(1, len(self.__ctrl_principal.ctrl_pessoa.pessoas) + 1)) + [0]
            
                opcao_pessoa = self.__tela_grupo.recebe_input_int("\nEscolha o índice associado de uma pessoa para registrá-la como integrante base: ", pessoas_validas)
                if opcao_pessoa == 0:
                    self.abre_tela()
                else:
                    pessoa_escolhida = self.__ctrl_principal.ctrl_pessoa.pessoas[opcao_pessoa - 1]
                    print(f"'{pessoa_escolhida.nome}' foi escolhida como integrante base. ")
                # Lista todas as mídias instanciadas, separadas em filmes e séries
                todas_midias = [*self.__ctrl_principal.ctrl_midia.filmes, *self.__ctrl_principal.ctrl_midia.series]
                print()
                for (i, midia) in enumerate(todas_midias, start=1):
                    print(f"[{i}] - {midia.titulo} ({type(midia).__name__})")
                midias_validas = list(range(1, len(todas_midias) + 1)) + [0]
                
                opcao_midia = self.__tela_grupo.recebe_input_int("\nEscolha o índice associado de uma mídia para registrá-la como associada: ", midias_validas)
                if opcao_midia == 0:
                    self.abre_tela()
                else:
                    midia_escolhida = copy.deepcopy(todas_midias[opcao_midia - 1])
                    # if isinstance(midia_escolhida, Serie):
                    #     nova_serie = Serie(midia_escolhida.titulo)
                        
                    #     for temporada in midia_escolhida.temporadas:
                    #         nova_temporada = Temporada(temporada.numero)
                    #         for episodio in temporada.episodios:
                    #             novo_episodio = Episodio(episodio.numero)
                    #             nova_temporada.episodios.append(novo_episodio)
                    #     nova_serie.temporadas.append(nova_temporada)
                    #     midia_escolhida = nova_serie
                        
                    print(f"'{midia_escolhida.titulo}' foi escolhida como a mídia associada do grupo.")
                
                ano = self.__tela_grupo.recebe_input_int("Digite o ano da próxima sessão do grupo: ")
                mes = self.__tela_grupo.recebe_input_int("Digite o mês (1-12): ", list(range(1, 13)))
                dia = self.__tela_grupo.recebe_input_int("Digite o dia: ", inteiros_validos=self.dias_validos(mes, ano))
                hora, minutos = self.__tela_grupo.recebe_input_hora_minutos("Digite a hora e minutos (formato: HH:MM): ")
                
                self.__grupos.append(Grupo(nome, pessoa_escolhida, midia_escolhida, datetime(ano, mes, dia, hora, minutos)))
                print(f"Grupo '{nome}' foi criado com sucesso")
                
        else:
            if self.__ctrl_principal.existem_pessoas() and not self.__ctrl_principal.existem_midias():
                print("Não existe nenhuma mídia cadastrada.")
            elif self.__ctrl_principal.existem_midias() and not self.__ctrl_principal.existem_pessoas():
                print("Não existe nenhuma pessoa cadastrada.")
            else:
                print("Não existe nenhuma mídia e nenhuma pessoa cadastrada.")
                
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
        self.__tela_grupo.imprime_opcoes("Remoção de Grupos")

        if self.grupos:
            print("\nGrupos disponíveis para remoção:")
            for (i, grupo) in enumerate(self.__grupos, start=1):
                print(f"[{i}] - {grupo.nome}")

            # Pedir confirmação
            if self.__tela_grupo.recebe_input_sn("Deseja remover um grupo? (S/N): "):
                opcao_grupo = self.__tela_grupo.recebe_input_int("\nEscolha o índice associado ao grupo que deseja remover: ", list(range(1, len(self.__grupos) + 1)))
                grupo_escolhido = self.__grupos[opcao_grupo - 1]

                # Confirmar novamente
                if self.__tela_grupo.recebe_input_sn(f"Tem certeza que deseja remover o grupo '{grupo_escolhido.nome}'? (S/N): "):
                    self.__grupos.remove(grupo_escolhido)
                    print(f"O grupo '{grupo_escolhido.nome}' foi removido com sucesso.")
                else:
                    print("Operação cancelada.")
            else:
                print("Operação cancelada.")
        else:
            print("Opa, parece que não há nenhum grupo cadastrado.")

        self.standby()
    
    def altera_grupo(self):
        os.system('cls||clear')
        print(" "*5+"Alteração de Grupos")
        print(""+"-="*13)
    
        if self.__grupos:
            for (i, grupo) in enumerate(self.__grupos, start=1):
                print(f"[{i}] - Nome: {grupo.nome} (Midia associada: {grupo.midia_associada.titulo})")
                print(f"    Data da Próxima Sessão: {grupo.data.strftime('%Y-%m-%d %H:%M')}")
                print("    Membros:")
                for membro in grupo.pessoas:
                    print(f"        {membro.nome}")
            print()
            print("0 para retornar")
            validos = list(range(1, len(self.__grupos) + 1)) + [0]
            opcao_grupo = self.__tela_grupo.recebe_input_int("Escolha o índice associado a um grupo para alterá-lo: ", validos)
            
            if opcao_grupo == 0:
                self.abre_tela()
            
            grupo_escolhido = self.__grupos[opcao_grupo - 1]
            
            opcao_alteracao = self.__tela_grupo.recebe_input_int("""
1 - Alterar nome
2 - Adicionar membro
3 - Remover membro
4 - Alterar data da próxima sessão
5 - Alterar progresso
6 - Voltar

Escolha a opção de alteração: """, [1, 2, 3, 4, 5, 6])

            if opcao_alteracao == 1:
                # Alterar nome do grupo
                novo_nome = self.__tela_grupo.recebe_input_str("Digite o novo nome para o grupo: ")
                grupo_escolhido.nome = novo_nome
                print(f"Nome do grupo '{grupo_escolhido.nome}' alterado com sucesso.")
                
            elif opcao_alteracao == 2:
                # Adicionar um membro ao grupo
                self.adiciona_membro(grupo_escolhido)
            
            elif opcao_alteracao == 3:
                # Remover um membro do grupo
                self.remove_membro(grupo_escolhido)
            
            elif opcao_alteracao == 4:
                # Alterar data da próxima sessão
                self.altera_data_proxima_sessao(grupo_escolhido)
            
            elif opcao_alteracao == 5:
                if isinstance(grupo_escolhido.midia_associada, Serie):
                    for i, temporada in enumerate(grupo_escolhido.midia_associada.temporadas, start=1):
                        print(f"[{i}] - Temporada {temporada.numero}")
                        
                    temporada_indice = self.__tela_grupo.recebe_input_int("Escolha o índice associado a uma temporada para alterar o progresso dos episódios: ",
                    range(1, len(grupo_escolhido.midia_associada.temporadas) + 1))
                    temporada_escolhida = grupo_escolhido.midia_associada.temporadas[temporada_indice - 1]
                    
                    self.exibe_episodios_temporada(temporada_escolhida)
                    self.altera_assistido_temporada(temporada_escolhida)
                        
            
            elif opcao_alteracao == 6:
                self.abre_tela()
            
            
        else: 
            print("Opa, parece que não há nenhum grupo cadastrado.")
            
        self.standby()
    
    def exibe_episodios_temporada(self, temporada):
        for (i, episodio) in enumerate(temporada.episodios, start=1):
            status_assistido = "Assistido" if episodio.assistido else "Não assistido"
            print(f"[{i}] - Episódio {episodio.numero}: {status_assistido}")
            
    def altera_assistido_temporada(self, temporada):
        indice = self.__tela_grupo.recebe_input_int(
            "Escolha o índice associado a um episódio para alterar seu status de assistido: ",
            range(len(temporada.episodios) + 1)
        
        )
        if indice == 0:
            self.abre_tela()
        
        episodio_escolhido = temporada.episodios[indice - 1]
        
        novo_status = self.__tela_grupo.recebe_input_sn("Marcar como assistido? (S/N): ")
        episodio_escolhido.assistido = (novo_status)

        print(f"Status de assistido do episódio {episodio_escolhido.numero} alterado para {episodio_escolhido.assistido}")
    
        continuar_alterando = self.__tela_grupo.recebe_input_sn("Deseja alterar o status de assistido de mais episódios? (S/N): ")
        if continuar_alterando:
            self.altera_assistido_temporada(temporada)
        else:
            self.altera_grupo()
    
    def adiciona_membro(self, grupo):
        os.system('cls||clear')
        print(" "*5+"Adição de Membro ao Grupo")
        print(""+"-="*18)

        # Lista pessoas que não estão nesse grupo
        pessoas_disponiveis = [pessoa for pessoa in self.__ctrl_principal.ctrl_pessoa.pessoas if not self.__ctrl_principal.pessoa_is_membro_do_grupo(pessoa, grupo)]

        if pessoas_disponiveis:
            print("Pessoas Disponíveis:")
            for (i, pessoa) in enumerate(pessoas_disponiveis, start=1):
                print(f"[{i}] - Nome: {pessoa.nome} (E-Mail: {pessoa.email})")
            print()

            opcao_pessoa = self.__tela_grupo.recebe_input_int("\nEscolha o índice associado a uma pessoa para adicioná-la ao grupo: ", list(range(1, len(pessoas_disponiveis) + 1)))
            pessoa_escolhida = pessoas_disponiveis[opcao_pessoa - 1]

            grupo.pessoas.append(pessoa_escolhida)
            print(f"{pessoa_escolhida.nome} foi adicionado ao grupo '{grupo.nome}' com sucesso.")
        else:
            print("Não há pessoas disponíveis para adicionar ao grupo.")
        
        self.standby()
    
    def remove_membro(self, grupo):
        os.system('cls||clear')
        print(" "*5+"Remoção de Membro do Grupo")
        print(""+"-="*19)

        if not grupo.pessoas:
            print(f"O grupo '{grupo.nome}' não possui membros para remover.")
        else:
            print("Membros do Grupo:")
            for (i, pessoa) in enumerate(grupo.pessoas, start=1):
                print(f"[{i}] - Nome: {pessoa.nome} (E-Mail: {pessoa.email})")
            print()

            opcao_pessoa = self.__tela_grupo.recebe_input_int("\nEscolha o índice associado a um membro para removê-lo do grupo: ", list(range(1, len(grupo.pessoas) + 1)))
            pessoa_escolhida = grupo.pessoas[opcao_pessoa - 1]

            grupo.pessoas.remove(pessoa_escolhida)
            print(f"{pessoa_escolhida.nome} foi removido(a) do grupo '{grupo.nome}' com sucesso.")

        self.standby()

    
    def lista_grupos(self):
        # self.__tela_grupo.mostra_opcoes(titulo=" "*3+"Listagem de Grupos", spacing="="+"-="*12)
        self.__tela_grupo.imprime_opcoes("Listagem de Grupos")
        if self.__grupos:
            confirmacao = self.__tela_grupo.recebe_input_sn("Deseja listar todos os grupos? (S/N): ")
            if confirmacao:
                for grupo in self.__grupos:
                    print()
                    print("-"*30)
                    print(f"Nome do Grupo: {grupo.nome}")
                    print(f"Data da próxima sessão do Grupo: {grupo.data.strftime('%d/%m/%Y - %H:%M')}")
                    print(f"Membros do Grupo:")
                    for membro in grupo.pessoas:
                        print(f"        {membro.nome}")
                    
                    if isinstance(grupo.midia_associada, Serie):
                        total_episodios = sum(len(temporada.episodios) for temporada in grupo.midia_associada.temporadas)
                        episodios_assistidos = sum(episodio.assistido for temporada in grupo.midia_associada.temporadas for episodio in temporada.episodios)

                        episodios_restantes = total_episodios - episodios_assistidos
                        
                        porcentagem_assistido = (episodios_assistidos / total_episodios) * 100
                        print(f"Porcentagem de episódios assistidos: {porcentagem_assistido:.2f}%")
                        print(f"{episodios_assistidos}/{total_episodios} episódios ({episodios_restantes} episódios restantes)")
                        
                    print(f"Midia associada ao Grupo: {grupo.midia_associada.titulo} ({type(grupo.midia_associada).__name__})")
            print()
        
        else:
            print("Opa, parece que não há nenhum grupo cadastrado.")
        
        self.standby()
    
    def altera_data_proxima_sessao(self, grupo):
        os.system('cls||clear')
        print(" "*5+"Alteração de Data da Próxima Sessão do Grupo")
        print(""+"-="*26)

        print(f"A data atual da próxima sessão do grupo '{grupo.nome}' é {grupo.data}.")

        # Pedir confirmação pra cada ação
        if self.__tela_grupo.recebe_input_sn("Deseja alterar o ano? (S/N): "):
            novo_ano = self.__tela_grupo.recebe_input_int("Digite o novo ano: ")
            grupo.data = grupo.data.replace(year=novo_ano)
            print(f"Ano alterado para {novo_ano}.")

        if self.__tela_grupo.recebe_input_sn("Deseja alterar o mês? (S/N): "):
            novo_mes = self.__tela_grupo.recebe_input_int("Digite o novo mês (1-12): ", list(range(1, 13)))
            grupo.data = grupo.data.replace(month=novo_mes)
            print(f"Mês alterado para {novo_mes}.")

        if self.__tela_grupo.recebe_input_sn("Deseja alterar o dia? (S/N): "):
            novo_dia = self.__tela_grupo.recebe_input_int("Digite o novo dia: ", inteiros_validos=self.dias_validos(grupo.data.month, grupo.data.year))
            grupo.data = grupo.data.replace(day=novo_dia)
            print(f"Dia alterado para {novo_dia}.")

        if self.__tela_grupo.recebe_input_sn("Deseja alterar a hora? (S/N): "):
            nova_hora, novo_minuto = self.__tela_grupo.recebe_input_hora_minutos("Digite a nova hora e minutos (formato: HH:MM): ")
            grupo.data = grupo.data.replace(hour=nova_hora, minute=novo_minuto)
            print(f"Hora alterada para {nova_hora}:{novo_minuto}.")

        print(f"A data da próxima sessão do grupo '{grupo.nome}' foi alterada com sucesso para {grupo.data}.")
        self.standby()
    
    
    def standby(self):
        print("\nAperte qualquer tecla para retornar à gerencia de grupos.")
        input()
        self.abre_tela()
    
    def retorna(self):
        self.__ctrl_principal.abre_tela()
