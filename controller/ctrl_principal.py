from controller.ctrl_grupo import CtrlGrupo
from controller.ctrl_midia import CtrlMidia
from controller.ctrl_pessoa import CtrlPessoa
from view.tela_principal import TelaPrincipal
from collections import Counter
import os


class CtrlPrincipal():
    def __init__(self):
        self.ctrl_grupo = CtrlGrupo(self)
        self.ctrl_midia = CtrlMidia(self)
        self.ctrl_pessoa = CtrlPessoa(self)

        self.tela_principal = TelaPrincipal()

    # @property
    # def ctrl_grupo(self):
    #     return self.__ctrl_grupo

    # @property
    # def ctrl_midia(self):
    #     return self.__ctrl_midia

    # @property
    # def ctrl_pessoa(self):
    #     return self.__ctrl_pessoa

    def inicia(self):
        self.abre_tela()

    def gerencia_midia(self):
        self.ctrl_midia.abre_tela()

    def gerencia_pessoa(self):
        self.ctrl_pessoa.abre_tela()

    def gerencia_grupo(self):
        self.ctrl_grupo.abre_tela()

    def gera_relatorio(self):
        self.tela_principal.abre_tela_relatorio()

        lista_opcoes = {
            1: self.tipo_de_midia_mais_favorita,
            2: self.pessoa_em_mais_grupos,
            3: self.grupo_com_mais_pessoas,
            4: self.tipo_de_midia_mais_assistida,
            5: self.abre_tela
        }

        while True:
            opcao = self.tela_principal.recebe_input_int(
                "\nEscolha uma opção: ", [1, 2, 3, 4, 5])
            escolha = lista_opcoes[opcao]
            escolha()

    def tipo_de_midia_mais_favorita(self):
        midias_fav = [
            pessoa.midia_fav for pessoa in self.ctrl_pessoa.pessoas if pessoa.midia_fav]

        if midias_fav:
            contagem_midias = Counter(midias_fav)
            mais_comuns = contagem_midias.most_common()

            if len(mais_comuns) > 1 and mais_comuns[0][1] == mais_comuns[1][1]:
                self.tela_principal.output_texto("Empate! Os tipos de mídia favoritos mais comuns são: ")
                for midia, quantidade in mais_comuns:
                    self.tela_principal.output_texto(f"{midia}: Quantidade: {quantidade}")

            else:
                tipo_midia_mais_comum, quantidade = mais_comuns[0]
                self.tela_principal.output_texto(
                    f"O tipo de midia favorita mais comum é: {tipo_midia_mais_comum}, Quantidade: {quantidade}")

        else:
            self.tela_principal.output_texto("Sem informações disponíveis.")

        self.standby()

    def pessoa_em_mais_grupos(self):
        if self.ctrl_grupo.grupos:
            contador_pessoa = Counter(
                [pessoa for grupo in self.ctrl_grupo.grupos for pessoa in grupo.pessoas])
            if contador_pessoa:
                quantidade_max = contador_pessoa.most_common(1)[0][1]

                pessoas_empate = [pessoa for pessoa, quantidade in contador_pessoa.items(
                ) if quantidade == quantidade_max]
                if len(pessoas_empate) == 1:
                    pessoa_mais_comum = pessoas_empate[0]
                    self.tela_principal.output_texto(
                        f"A pessoa no maior número de grupos é: {pessoa_mais_comum.nome}, Quantidade de grupos: {quantidade_max}")
                else:
                    self.tela_principal.output_texto(
                        "Empate! Pessoas com o mesmo número de ocorrência em grupos: ")
                    for pessoa in pessoas_empate:
                        self.tela_principal.output_texto(f"- {pessoa.nome}")

            else:
                self.tela_principal.output_texto("Nenhuma pessoa em grupos.")

        else:
            self.tela_principal.output_texto("Sem grupos disponíveis.")

        self.standby()

    def grupo_com_mais_pessoas(self):
        if self.ctrl_grupo.grupos:
            grupos_por_quantidade = Counter(
                len(grupo.pessoas) for grupo in self.ctrl_grupo.grupos)
            if grupos_por_quantidade:
                max_quantidade = grupos_por_quantidade.most_common(1)[0][1]

                grupos_tie = [grupo for grupo in self.ctrl_grupo.grupos if len(
                    grupo.pessoas) == max_quantidade]

                if len(grupos_tie) == 1:
                    grupo_mais_pessoas = grupos_tie[0]
                    quantidade_pessoas = len(grupo_mais_pessoas.pessoas)
                    self.tela_principal.output_texto(
                        f"O grupo com mais pessoas é: {grupo_mais_pessoas.nome}, Quantidade: {quantidade_pessoas} pessoa(s)")
                else:
                    self.tela_principal.output_texto(
                        f"Empate! Grupos com o mesmo número de pessoas ({max_quantidade}):")
                    for grupo in grupos_tie:
                        quantidade_pessoas = len(grupo.pessoas)
                        self.tela_principal.output_texto(f"- {grupo.nome} ({quantidade_pessoas} pessoas)")
            else:
                self.tela_principal.output_texto("Sem informações disponíveis.")
        else:
            self.tela_principal.output_texto("Sem grupos disponíveis.")

        self.standby()

    # def grupo_com_mais_pessoas(self):
    #     if self.ctrl_grupo.grupos:
    #         grupos_por_quantidade = Counter(len(grupo.pessoas) for grupo in self.ctrl_grupo.grupos)
    #         if grupos_por_quantidade:
    #             quantidade_max = grupos_por_quantidade.most_common(1)[0][1]

    #             empate_grupos = [grupo for grupo, quantidade in grupos_por_quantidade.items() if quantidade == quantidade_max]

    #             if len(empate_grupos) == 1:
    #                 grupo_mais_pessoas = empate_grupos[0]
    #                 quantidade_pessoas = len(grupo_mais_pessoas.pessoas)
    #                 print(f"O grupo com mais pessoas é: {grupo_mais_pessoas.nome}, Quantidade: {quantidade_pessoas}")
    #             else:
    #                 print(f"Empate! Grupos com o mesmo número de pessoas: ")
    #                 for grupo in empate_grupos:
    #                     quantidade_pessoas = len(grupo.pessoas)
    #                     print(f"- {grupo.nome} ({quantidade_pessoas} pessoas)")

    #         else:
    #             print("Sem informações disponíveis")
    #     else:
    #         print("Sem grupos disponíveis.")

    #     self.standby()

    def tipo_de_midia_mais_assistida(self):
        midias_associadas = [
            grupo.midia_associada for grupo in self.ctrl_grupo.grupos if grupo.midia_associada]

        if midias_associadas:
            midias_mais_vistas = Counter(midias_associadas).most_common()
            tipo_midia_mais_vista, quantidade = midias_mais_vistas[0]

            empate_midias = [
                midia for midia, quantidade in midias_mais_vistas[1:] if quantidade == quantidade]

            if len(empate_midias) == 0:
                self.tela_principal.output_texto(
                    f"O tipo de mídia mais visto é: {tipo_midia_mais_vista.titulo}, Quantidade: {quantidade}")
            else:
                self.tela_principal.output_texto(
                    f"Empate! Tipos de mídia com a mesma quantidade de visualizações ({quantidade}):")
                for midia in [tipo_midia_mais_vista] + empate_midias:
                    self.tela_principal.output_texto(f"- {midia.titulo}")
        else:
            self.tela_principal.output_texto("Sem informações disponíveis.")

        self.standby()

    def abre_tela(self):
        os.system('cls||clear')
        logo = '''
  ####     ####    ##  ##   ######   ##   ##   ####    ######   ######   ######   ##   ## 
 ##  ##     ##     ### ##   ##       ### ###  ##  ##   ##  ##   ##  ##   ##  ##   ##   ## 
 ##         ##     ######   ##       #######  ##  ##   ##  ##   ##  ##   ##  ##   ##   ## 
 ##         ##     ######   ####     ## # ##  ##  ##   #####    #####    ##  ##   ## # ## 
 ##         ##     ## ###   ##       ##   ##  ##  ##   ####     ####     ##  ##   ####### 
 ##  ##     ##     ##  ##   ##       ##   ##  ##  ##   ## ##    ## ##    ##  ##   ### ### 
  ####     ####    ##  ##   ######   ##   ##   ####    ##  ##   ##  ##    ####    ##   ## 
        '''
        opcoes = """
    1 - Gerenciar Mídias
    2 - Gerenciar Pessoas
    3 - Gerenciar Grupos
    4 - Relatórios
    5 - Encerrar
              """
        self.tela_principal.output_texto(logo)
        self.tela_principal.output_texto(opcoes)

        lista_opcoes = {
            1: self.gerencia_midia,
            2: self.gerencia_pessoa,
            3: self.gerencia_grupo,
            4: self.gera_relatorio,
            5: self.encerra
        }

        while True:
            opcao = self.tela_principal.recebe_input_int(
                "Escolha uma opção (principal): ", [1, 2, 3, 4, 5])
            escolha = lista_opcoes[opcao]
            escolha()

    def existem_midias(self):
        if self.ctrl_midia.filmes or self.ctrl_midia.series:
            return True
        else:
            return False

    def existem_pessoas(self):
        if self.ctrl_pessoa.pessoas:
            return True
        else:
            return False

    def pessoa_is_membro_do_grupo(self, pessoa, grupo):
        return pessoa in grupo.pessoas

    def standby(self):
        self.tela_principal.output_texto("\nAperte qualquer tecla para retornar ao menu principal.")
        input()
        self.abre_tela()

    def encerra(self):
        exit(0)
