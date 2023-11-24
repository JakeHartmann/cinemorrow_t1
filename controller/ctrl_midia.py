from model.midia import Midia
from view.tela_midia import TelaMidia
from model.filme import Filme
from model.serie import Serie
from model.temporada import Temporada
from model.episodio import Episodio
from model.midia_dao import MidiaDAO
import os


class CtrlMidia():
    def __init__(self, ctrl_principal):
        self.__ctrl_principal = ctrl_principal
        self.__tela_midia = TelaMidia()

        self.__series = []
        self.__filmes = []
        
        self.__midia_dao = MidiaDAO()

    @property
    def series(self):
        return self.__series

    @property
    def filmes(self):
        return self.__filmes

    def abre_tela(self):
        os.system('cls||clear')
        nome_tela = 'Gerencia de Midias'
        opcoes = """
    1 - Adicionar Mídia
    2 - Remover Mídia
    3 - Alterar Mídia
    4 - Listar Mídias
    5 - Voltar
    """
        self.__tela_midia.output_texto(f'{nome_tela:~^40}')
        self.__tela_midia.output_texto(opcoes)

        lista_opcoes = {
            1: self.cria_midia,
            2: self.remove_midia,
            3: self.altera_midia,
            4: self.lista_midias,
            5: self.retorna
        }

        while True:
            opcao = self.__tela_midia.recebe_input_int(
                "Escolha uma opção (midias): ", [1, 2, 3, 4, 5])

            escolha = lista_opcoes[opcao]
            escolha()

    def get_lista_filmes(self):
        filmes = []

        for value in self.__midia_dao.get_all():
            if isinstance(value, Filme):
                filmes.append(value)
        return filmes
    
    def get_lista_series(self):
        series = []
        
        for value in self.__midia_dao.get_all():
            if isinstance(value, Serie):
                series.append(value)
        return series

    def cria_midia(self):
        os.system('cls||clear')
        nome_subtela = 'Adição de Mídia'
        self.__tela_midia.output_texto(f'{nome_subtela:~^40}')

        lista_opcoes = {
            1: self.criar_filme,
            2: self.criar_serie,
            3: self.abre_tela
        }

        lista_opcoes[self.__tela_midia.recebe_input_int("""
    1 - Filme
    2 - Série
    3 - Voltar
    
Escolha uma opção (criar mídia): """, [1, 2, 3])]()

    def criar_filme(self):
        titulo = self.__tela_midia.recebe_input_str(
            "Escreva o título do filme: ")
        filme = Filme(titulo)
        self.__midia_dao.add(filme)
        self.__tela_midia.output_texto(f"Filme '{titulo}' criado com sucesso.")
        self.standby()

    def criar_serie(self):
        titulo = self.__tela_midia.recebe_input_str(
            "Escreva o título da série: ")
        num_temporadas = self.__tela_midia.recebe_input_int(
            "Escolha o número de Temporadas: ", limite=35)

        serie = Serie(titulo)
        for i in range(1, num_temporadas + 1):
            temporada = self.criar_temporada(i)
            serie.temporadas.append(temporada)

        self.__midia_dao.add(serie)
        self.__tela_midia.output_texto(f"Série '{serie.titulo}' criada com sucesso.")
        self.standby()

    def criar_temporada(self, numero):
        num_episodios = self.__tela_midia.recebe_input_int(
            f"Escreva o número de episódios para a Temporada {numero}: ")
        temporada = Temporada(numero)
        for numero_episodio in range(1, num_episodios + 1):
            episodio = Episodio(numero_episodio)
            temporada.episodios.append(episodio)

        return temporada

    def remove_midia(self):
        os.system('cls||clear')
        nome_subtela = 'Remoção de Mídia'
        self.__tela_midia.output_texto(f'{nome_subtela:~^40}')

        filmes = self.get_lista_filmes()
        series = self.get_lista_series()

        if not (filmes or series):
            self.__tela_midia.output_texto("Opa, parece que não há nem filmes e nem séries cadastrados.")
            self.standby()

        lista_opcoes = {}
        opcao = 1

        if filmes:
            lista_opcoes[opcao] = self.remove_filme
            self.__tela_midia.output_texto(f"\n    {opcao} - Filme")
            opcao += 1

        if series:
            lista_opcoes[opcao] = self.remove_serie
            self.__tela_midia.output_texto(f"    {opcao} - Série")
            opcao += 1

        lista_opcoes[opcao] = self.abre_tela
        self.__tela_midia.output_texto(f"    {opcao} - Voltar")

        opcao_escolhida = self.__tela_midia.recebe_input_int(
            "\nEscolha o tipo de mídia a ser removido: ", range(1, opcao + 1))
        if opcao_escolhida in lista_opcoes:
            escolha_tipo_midia = lista_opcoes[opcao_escolhida]
            escolha_tipo_midia()
        else:
            self.abre_tela()

    def remove_filme(self):
        os.system('cls||clear')
        nome_subtela = 'Remoção de Filmes'
        self.__tela_midia.output_texto(f'{nome_subtela:~^40}')

        filmes = self.get_lista_filmes()

        for (i, filme) in enumerate(filmes, start=1):
            self.__tela_midia.output_texto(f"[{i}] - {filme.titulo}")

        self.__tela_midia.output_texto("0 para retornar")
        validos = list(range(1, len(filmes) + 1)) + [0]

        opcao = self.__tela_midia.recebe_input_int(
            "\nEscolha o índice associado ao filme para removê-lo: ", validos)

        if opcao == 0:
            self.abre_tela()
        else:
            filme_escolhido = filmes[opcao - 1]
            self.__tela_midia.output_texto(
                f"O filme '{filme_escolhido.titulo}' foi removido com sucesso.")
            self.__midia_dao.remove(filme_escolhido.titulo)
            self.standby()

    def remove_serie(self):
        os.system('cls||clear')
        nome_subtela = 'Remoção de Séries'
        self.__tela_midia.output_texto(f'{nome_subtela:~^40}')
        
        series = self.get_lista_series()
        
        for (i, serie) in enumerate(series, start=1):
            self.__tela_midia.output_texto(f"[{i}] - {serie.titulo}")

        self.__tela_midia.output_texto("0 para retornar")
        validos = list(range(1, len(series) + 1)) + [0]

        opcao = self.__tela_midia.recebe_input_int(
            "\nEscolha o índice associado à série para removê-la: ", validos)

        if opcao == 0:
            self.abre_tela()
        else:
            serie_escolhida = series[opcao - 1]
            self.__tela_midia.output_texto(
                f"A série '{serie_escolhida.titulo}' foi removida com sucesso.")
            self.__midia_dao.remove(serie_escolhida.titulo)
            self.standby()

    def altera_midia(self):
        os.system('cls||clear')
        nome_subtela = 'Alteração de Mídias'
        self.__tela_midia.output_texto(f'{nome_subtela:~^40}')

        filmes = self.get_lista_filmes()
        series = self.get_lista_series()

        if not (filmes or series):
            self.__tela_midia.output_texto("Opa, parece que não há nem filmes e nem séries cadastrados.")
            self.standby()
            return

        lista_opcoes = {}
        opcao = 1

        if filmes:
            lista_opcoes[opcao] = self.altera_filme
            self.__tela_midia.output_texto(f"\n    {opcao} - Filme")
            opcao += 1

        if series:
            lista_opcoes[opcao] = self.altera_serie
            self.__tela_midia.output_texto(f"    {opcao} - Série")
            opcao += 1

        lista_opcoes[opcao] = self.abre_tela
        self.__tela_midia.output_texto(f"    {opcao} - Voltar")

        opcao_escolhida = self.__tela_midia.recebe_input_int(
            "\nEscolha o tipo de mídia a ser alterado: ", range(1, opcao + 1))

        if opcao_escolhida in lista_opcoes:
            escolha_tipo_midia = lista_opcoes[opcao_escolhida]
            escolha_tipo_midia()
        else:
            self.abre_tela()

    def altera_filme(self):
        os.system('cls||clear')
        nome_subtela = 'Alteração de Filmes'
        self.__tela_midia.output_texto(f'{nome_subtela:~^40}')
        
        filmes = self.get_lista_filmes()
        
        for (i, filme) in enumerate(filmes, start=1):
            self.__tela_midia.output_texto(f"[{i}] - {filme.titulo}")
        self.__tela_midia.output_texto("0 para retornar")
        validos = list(range(1, len(filmes) + 1)) + [0]

        opcao = self.__tela_midia.recebe_input_int(
            "\nEscolha o índice associado ao filme para alterá-lo: ", validos)
        if opcao == 0:
            self.abre_tela()
        else:
            filme_escolhido = filmes[opcao - 1]
            novo_titulo = self.__tela_midia.recebe_input_str(
                f"Escolha o novo título para o filme '{filme_escolhido.titulo}': ")
            print(self.__midia_dao.get(filme_escolhido.titulo))
            print(self.__midia_dao.get(filme_escolhido.titulo).titulo)
            self.__midia_dao.get(filme_escolhido.titulo).titulo = novo_titulo
            self.__midia_dao.save()
            
            self.__tela_midia.output_texto(
                f"O título do filme '{novo_titulo}' foi alterado com sucesso.")
            self.standby()

    def altera_serie(self):
        os.system('cls||clear')
        nome_subtela = 'Alteração de Séries'
        self.__tela_midia.output_texto(f'{nome_subtela:~^40}')
        
        series = self.get_lista_series()
        
        for (i, serie) in enumerate(series, start=1):
            self.__tela_midia.output_texto(f"[{i}] - {serie.titulo}")
        self.__tela_midia.output_texto("0 para retornar")
        validos = list(range(1, len(series) + 1)) + [0]

        opcao = self.__tela_midia.recebe_input_int(
            "\nEscolha o índice associado à série para alterá-la: ", validos)
        if opcao == 0:
            self.abre_tela()
        else:
            serie_escolhida = series[opcao - 1]

            mudar_titulo = self.__tela_midia.recebe_input_sn(
                f"Deseja alterar o título da série '{serie_escolhida.titulo}'? (S/N): ")
            if mudar_titulo:
                novo_titulo = self.__tela_midia.recebe_input_str(
                    f"Digite o novo título para a série '{serie_escolhida.titulo}': ")
                serie_escolhida.titulo = novo_titulo

            mudar_temporada = self.__tela_midia.recebe_input_sn(
                "Deseja alterar o número de temporadas da série? (S/N): ")
            if mudar_temporada:
                novo_numero_temporadas = self.__tela_midia.recebe_input_int(
                    "Digite o novo número de Temporadas: ")
                serie_escolhida.temporadas = [self.criar_temporada(
                    i) for i in range(1, novo_numero_temporadas + 1)]

            if mudar_titulo or mudar_temporada:
                self.__tela_midia.output_texto(
                    f"Os dados da série '{serie_escolhida.titulo}' foram alterados com sucesso.")
            else:
                self.__tela_midia.output_texto(
                    f"Não houve mudança nos dados da série '{serie_escolhida.titulo}'.")
            self.standby()

    def lista_midias(self):
        os.system('cls||clear')
        nome_subtela = 'Listagem de Mídias'
        self.__tela_midia.output_texto(f'{nome_subtela:~^40}')

        if self.__midia_dao.get_all():

            lista_opcoes = {
                1: self.lista_filmes,
                2: self.lista_series,
                3: self.abre_tela
            }

            opcao = self.__tela_midia.recebe_input_int("""
    1 - Filmes
    2 - Séries
    3 - Voltar
        
Escolha qual tipo de mídia para listar (listagem de mídia): """, [1, 2, 3])
            lista_opcoes[opcao]()
            self.standby()
        else:
            self.__tela_midia.output_texto("Opa, parece que não há nenhuma mídia cadastrada.")
            self.standby()

    def lista_filmes(self):
        os.system('cls||clear')
        nome_subtela = 'Filmes Cadastrados'
        self.__tela_midia.output_texto(f'{nome_subtela:~^40}')
        
        filmes = self.get_lista_filmes()
        
        if filmes:
            for filme in filmes:
                self.__tela_midia.output_texto(filme.titulo)
        else:
            self.__tela_midia.output_texto("Opa, parece que não há nenhum filme cadastrado.")
        self.standby()

    def lista_series(self):
        os.system('cls||clear')
        nome_subtela = 'Séries Cadastradas'
        self.__tela_midia.output_texto(f'{nome_subtela:~^40}')

        series = self.get_lista_series()

        if series:
            for serie in series:
                self.__tela_midia.output_texto(f"\n{serie.titulo}")

                for temporada in serie.temporadas:
                    num_episodios = len(temporada.episodios)
                    if num_episodios == 1:
                        self.__tela_midia.output_texto(
                            f"Temporada {temporada.numero}: {num_episodios} episódio")
                    else:
                        self.__tela_midia.output_texto(
                            f"Temporada {temporada.numero}: {num_episodios} episódios")
                self.__tela_midia.output_texto("")

        else:
            self.__tela_midia.output_texto("Opa, parece que não há nenhuma série cadastrada.")

        self.standby()

    def standby(self):
        self.__tela_midia.output_texto("\nAperte qualquer tecla para retornar à gerencia de mídias.")
        input()
        self.abre_tela()

    def retorna(self):
        self.__ctrl_principal.abre_tela()
