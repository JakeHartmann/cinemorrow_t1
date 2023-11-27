from model.midia import Midia
from view.tela_midia import TelaMidia
from model.filme import Filme
from model.serie import Serie
from model.temporada import Temporada
from model.episodio import Episodio
from model.midia_dao import MidiaDAO
from model.titulo_duplicado_exception import TituloDuplicadoException
from model.remover_midia_associada_exception import RemoverMidiaAssociadaException


class CtrlMidia():
    def __init__(self, ctrl_principal):
        self.__ctrl_principal = ctrl_principal
        self.__tela_midia = TelaMidia()

        self.__midia_dao = MidiaDAO()

    @property
    def midia_dao(self):
        return self.__midia_dao

    def abre_tela(self):
        lista_opcoes = {
            1: self.cria_midia,
            2: self.remove_midia,
            3: self.altera_midia,
            4: self.lista_midias,
            5: self.retorna
        }

        while True:
            lista_opcoes[self.__tela_midia.tela_opcoes()]()

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
        lista_opcoes = {
            1: self.criar_filme,
            2: self.criar_serie,
            3: self.abre_tela
        }

        lista_opcoes[self.__tela_midia.seleciona_midia()]()

    def criar_filme(self):
        try:
            titulo = self.__tela_midia.pega_titulo_filme()
            if titulo is None:
                self.abre_tela()
            for filme in self.get_lista_filmes():
                if filme.titulo == titulo:
                    raise TituloDuplicadoException

        except TituloDuplicadoException:
            self.__tela_midia.show_message(
                "Alerta!", "Um filme com este título já existe.")

        else:
            filme = Filme(titulo)
            self.__midia_dao.add(filme)
            self.__tela_midia.show_message(
                "Sucesso!", f"Filme '{titulo}' criado com sucesso.")
            self.abre_tela()

    def criar_serie(self):
        try:
            titulo, num_temporadas, episodios_por_temporada = self.__tela_midia.pega_dados_serie()
            if titulo is None and num_temporadas is None and episodios_por_temporada is None:
                self.abre_tela()

            for serie in self.get_lista_series():
                if serie.titulo == titulo:
                    raise TituloDuplicadoException

        except TituloDuplicadoException:
            self.__tela_midia.show_message(
                "Alerta!", "Esse título já está sendo utilizado.")
            self.abre_tela()

        else:

            serie = Serie(titulo)
            for i, num_episodios in enumerate(episodios_por_temporada, start=1):
                temporada = self.criar_temporada(i, num_episodios)
                serie.temporadas.append(temporada)

            self.__midia_dao.add(serie)
            self.__tela_midia.show_message(
                "Sucesso!", f"Série '{titulo}' criada com sucesso.")
            self.abre_tela()

    def criar_temporada(self, numero, num_episodios):
        temporada = Temporada(numero)

        for numero_episodio in range(1, num_episodios + 1):
            episodio = Episodio(numero_episodio)
            temporada.episodios.append(episodio)

        return temporada

    def remove_midia(self):
        filmes = self.get_lista_filmes()
        series = self.get_lista_series()

        if not (filmes or series):
            self.__tela_midia.show_message(
                "Alerta!", "Não há nenhum tipo de mídia cadastrado.")
            self.abre_tela()

        tipo_midia = self.__tela_midia.seleciona_midia()

        if tipo_midia == 1:
            if not filmes:
                self.__tela_midia.show_message(
                    "Alerta!", "Não há filmes cadastrados.")
            else:
                filme_selecionado = self.__tela_midia.mostra_lista_filmes(
                    filmes, allow_selection=True)
                self.remove_filme(filme_selecionado)

        if tipo_midia == 2:
            if not series:
                self.__tela_midia.show_message(
                    "Alerta!", "Não há séries cadastradas.")
            else:
                serie_selecionada = self.__tela_midia.mostra_lista_series(
                    series, allow_selection=True)
                self.remove_serie(serie_selecionada)

    def remove_filme(self, filme_escolhido):

        if filme_escolhido is None:
            self.abre_tela()

        grupos = self.__ctrl_principal.ctrl_grupo.grupo_dao.get_all()

        try:
            for grupo in grupos:
                if grupo.midia_associada.titulo == filme_escolhido.titulo:
                    raise RemoverMidiaAssociadaException

        except RemoverMidiaAssociadaException:
            self.__tela_midia.show_message(
                "Alerta!", "Essa mídia está associada a um grupo.")
            self.abre_tela()

        else:
            self.__tela_midia.show_message(
                "Sucesso!", f"O filme '{filme_escolhido.titulo}' foi removido com sucesso.")
            self.__midia_dao.remove(filme_escolhido.titulo)
            self.abre_tela()

    def remove_serie(self, serie_escolhida):

        if serie_escolhida is None:
            self.abre_tela()

        grupos = self.__ctrl_principal.ctrl_grupo.grupo_dao.get_all()

        try:
            for grupo in grupos:
                if grupo.midia_associada.titulo == serie_escolhida.titulo:
                    raise RemoverMidiaAssociadaException

        except RemoverMidiaAssociadaException:
            self.__tela_midia.show_message(
                "Alerta!", "Essa mídia está associada a um grupo.")
            self.abre_tela()

        else:
            self.__tela_midia.show_message(
                "Sucesso!", f"A série '{serie_escolhida.titulo}' foi removida com sucesso.")
        self.__midia_dao.remove(serie_escolhida.titulo)
        self.abre_tela()

    def altera_midia(self):
        filmes = self.get_lista_filmes()
        series = self.get_lista_series()

        if not (filmes or series):
            self.__tela_midia.show_message(
                "Alerta!", "Não há nenhuma mídia cadastrada.")
            self.abre_tela()

        tipo_midia = self.__tela_midia.seleciona_midia()

        if tipo_midia == 1:
            if not filmes:
                self.__tela_midia.show_message(
                    "Alerta!", "Não há filmes cadastrados.")
            else:
                filme_selecionado = self.__tela_midia.mostra_lista_filmes(
                    filmes, allow_selection=True)
                self.altera_filme(filme_selecionado)

        if tipo_midia == 2:
            if not series:
                self.__tela_midia.show_message(
                    "Alerta!", "Não há séries cadastradas.")
            else:
                serie_selecionada = self.__tela_midia.mostra_lista_series(
                    series, allow_selection=True)
                self.altera_serie(serie_selecionada)

    def altera_filme(self, filme_escolhido):

        if filme_escolhido is None:
            self.abre_tela()

        novo_titulo = self.__tela_midia.pega_titulo_filme(
            titulo_antigo=filme_escolhido.titulo)
        if novo_titulo is None:
            self.abre_tela()

        titulo_antigo = filme_escolhido.titulo
        self.__midia_dao.remove(titulo_antigo)
        filme_escolhido.titulo = novo_titulo
        self.__ctrl_principal.ctrl_grupo.grupo_dao.dump()

        self.__midia_dao.add(filme_escolhido)

        self.__tela_midia.show_message(
            "Sucesso!", f"O título do filme '{novo_titulo}' foi alterado com sucesso.")
        self.abre_tela()

    def altera_serie(self, serie_escolhida):

        if serie_escolhida is None:
            self.abre_tela()

        num_atual_temporadas = len(serie_escolhida.temporadas)

        dados_atuais = (serie_escolhida.titulo, num_atual_temporadas)

        novo_titulo, novo_num_temporadas, novo_episodios_por_temporada = self.__tela_midia.pega_dados_serie(
            old_data=dados_atuais)

        titulo_antigo = serie_escolhida.titulo
        self.__midia_dao.remove(titulo_antigo)
        serie_escolhida.titulo = novo_titulo
        serie_escolhida.temporadas = []
        for i, num_episodios in enumerate(novo_episodios_por_temporada, start=1):
            temporada = self.criar_temporada(i, num_episodios)
            serie_escolhida.temporadas.append(temporada)

        self.__midia_dao.add(serie_escolhida)
        self.__tela_midia.show_message(
            "Sucesso!", f"Os dados da série '{serie_escolhida.titulo}' foram alterados.")
        self.abre_tela()

    def lista_midias(self):
        if self.__midia_dao.get_all():

            lista_opcoes = {
                1: self.lista_filmes,
                2: self.lista_series,
                3: self.abre_tela
            }

            lista_opcoes[self.__tela_midia.seleciona_midia()]()

        else:
            self.__tela_midia.show_message(
                "Alerta!", "Parece que não há nenhuma mídia cadastrada.")
            self.abre_tela()

    def lista_filmes(self):

        filmes = self.get_lista_filmes()

        if filmes:
            self.__tela_midia.mostra_lista_filmes(filmes)
        else:
            self.__tela_midia.show_message(
                "Alerta!", "Não há nenhum filme cadastrado.")
            self.abre_tela()

    def lista_series(self):

        series = self.get_lista_series()

        if not series:
            self.__tela_midia.show_message(
                "Alerta!", "Não há nenhuma série cadastrada.")
            self.abre_tela()
            return

        self.__tela_midia.mostra_lista_series(series)

    def retorna(self):
        self.__ctrl_principal.abre_tela()
