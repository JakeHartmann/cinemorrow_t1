import os
from view.abstract_tela import AbstractTela
import PySimpleGUI as sg


class TelaMidia(AbstractTela):
    def __init__(self):
        super().__init__()

    def init_components(self):
        sg.theme('DarkAmber')

        titulo = 'Gerencia de Mídias'

        layout = [
            [sg.Text(f'{titulo:~^40}', font=("Helvica", 25))],
            [sg.Radio('Adicionar Mídia', "RD1", key='1')],
            [sg.Radio('Remover Mídia', "RD1", key='2')],
            [sg.Radio('Alterar Mídia', "RD1", key='3')],
            [sg.Radio('Listar Mídias', "RD1", key='4')],
            [sg.Button('Confirmar'), sg.Cancel('Retornar')]
        ]

        self.window = sg.Window('Gerencia de Mídias').Layout(layout)

    def tela_opcoes(self):
        self.init_components()

        while True:
            event, values = self.window.read()

            if event in (sg.WINDOW_CLOSED, 'Retornar'):
                opcao = 5
                break
            elif event == 'Confirmar':
                selected_option = next(
                    (key for key, value in values.items() if value), None)
                if selected_option:
                    opcao = int(selected_option)
                    break
                else:
                    self.show_message(
                        "Alerta!", "Por favor escolha uma opção antes de confirmar.")

        self.close()
        return opcao

    def seleciona_midia(self):
        sg.ChangeLookAndFeel('DarkAmber')

        titulo = 'Selecione o Tipo de Mídia'

        layout = [
            [sg.Text(f'{titulo:~^40}', font=("Helvica", 25))],
            [sg.Radio('Filme', "RD1", key='1')],
            [sg.Radio('Série', "RD1", key='2')],
            [sg.Button('Confirmar'), sg.Cancel('Retornar')]
        ]
        self.window = sg.Window(titulo).Layout(layout)

        while True:
            button, values = self.open()

            if button in (sg.WINDOW_CLOSED, 'Retornar'):
                opcao = 3
                break
            elif button == 'Confirmar':
                selected_option = next(
                    (key for key, value in values.items() if value), None)
                if selected_option:
                    opcao = int(selected_option)
                    break
                else:
                    self.show_message(
                        "Alerta!", "Por favor escolha uma opção antes de confirmar.")

        self.close()
        return opcao

    def pega_titulo_filme(self, titulo_antigo=None):
        sg.ChangeLookAndFeel('DarkAmber')

        titulo_subtela = 'Insira o título do Filme'

        layout = [
            [sg.Text(f'{titulo_subtela:~^40}', font=("Helvica", 25))]
        ]

        if titulo_antigo is not None:
            layout.append([sg.Text(f'Título atual: {titulo_antigo}')])
            layout.append([sg.Text("Insira o novo título abaixo.")])

        layout.append([sg.InputText(key='titulo')])
        layout.append([sg.Button('Confirmar'), sg.Button('Cancelar')])

        self.window = sg.Window(titulo_subtela).Layout(layout)

        while True:
            button, values = self.open()

            if button == sg.WINDOW_CLOSED or button == 'Confirmar':
                if values['titulo'].strip() == '':
                    self.show_message(
                        'Alerta!', 'O título do Filme não pode estar vazio.')
                else:
                    break
            elif button == 'Cancelar':
                titulo_filme = None
                return titulo_filme

        self.close()

        titulo_filme = values['titulo']

        return titulo_filme

    def pega_dados_serie(self, old_data=None):
        sg.ChangeLookAndFeel('DarkAmber')

        titulo_subtela = 'Insira dados da Série'

        layout = [
            [sg.Text(f'{titulo_subtela:~^40}', font=("Helvica", 25))],
        ]

        if old_data:
            layout.append([sg.Text(f'Título atual da série: {old_data[0]}')])
            layout.append(
                [sg.Text(f'Número de temporadas atual: {old_data[1]}')])
        else:
            layout.append([sg.Text("Insira título da série:"),
                          sg.InputText(key='titulo')])
            layout.append([sg.Text("Insira o número de temporadas:"),
                          sg.InputText(key='num_temporadas')])

        layout.append([sg.Button('Avançar'), sg.Button('Cancelar')])

        self.window = sg.Window(titulo_subtela).Layout(layout)

        while True:
            button, values = self.open()

            if button == sg.WINDOW_CLOSED or button == 'Cancelar':
                self.close()
                return None, None, None

            elif button == 'Avançar':
                titulo_serie = values['titulo'] if not old_data else old_data[0]
                num_temporadas = values['num_temporadas'] if not old_data else str(
                    old_data[1])

                if titulo_serie.strip() == '':
                    self.show_message(
                        "Alerta!", "Por favor, insira um título válido.")
                elif not num_temporadas.isdigit() or int(num_temporadas) <= 0:
                    self.show_message(
                        "Alerta!", "Por favor, insira um número válido de temporadas.")
                else:
                    episodios_por_temporada = self.get_num_episodios(
                        int(num_temporadas))
                    if episodios_por_temporada is not None:
                        break

        self.close()

        return titulo_serie, int(num_temporadas), episodios_por_temporada

    def get_num_episodios(self, num_temporadas):
        layout = []
        for i in range(num_temporadas):
            layout.append(
                [sg.Text(f'Temporada {i+1}'), sg.InputText(key=f'num_episodios_{i+1}')])

        layout.append([sg.Button('Confirmar')])
        window_episodes = sg.Window(
            'Insira dados dos Episódios').Layout(layout)

        while True:
            button, values = window_episodes.read()

            if button == sg.WINDOW_CLOSED:
                window_episodes.close()
                return None
            elif button == 'Confirmar':
                episodios_por_temporada = [
                    int(values[f'num_episodios_{i+1}']) for i in range(num_temporadas)]
                window_episodes.close()
                return episodios_por_temporada

    def mostra_lista_filmes(self, filmes, allow_selection=False):
        sg.ChangeLookAndFeel('DarkAmber')

        titulo_subtela = 'Lista de Filmes'

        layout = [
            [sg.Text(f'{titulo_subtela:~^40}', font=("Helvica", 25))],
        ]

        if allow_selection:
            radio_buttons = []
            for i, filme in enumerate(filmes, start=1):
                radio_buttons.append(
                    sg.Radio(filme.titulo, 'FILMES', key=f'-FILME-{i}-', enable_events=True))

            layout.append(radio_buttons)
            layout.append([sg.Button('Confirmar'), sg.Button('Cancelar')])
        else:
            layout.append([sg.Multiline('\n'.join([filme.titulo for filme in filmes]), size=(
                40, len(filmes)), key='-FILMES-', disabled=True)])
            layout.append([sg.Button('Voltar')])

        self.window = sg.Window(titulo_subtela).Layout(layout)

        if allow_selection:
            while True:
                button, values = self.open()

                if button == sg.WINDOW_CLOSED or button == 'Confirmar':
                    selected_index = next(
                        (i for i, value in enumerate(values.values()) if value), None)
                    if selected_index is not None:
                        selected_filme = filmes[selected_index]
                        break
                    else:
                        self.show_message(
                            "Alerta!", "Por favor, escolha uma opção antes de confirmar.")
                elif button == 'Cancelar':
                    selected_filme = None
                    break
            self.close()
            return selected_filme
        else:
            while True:
                button, values = self.open()

                if button == sg.WINDOW_CLOSED or button == 'Voltar':
                    break

            self.close()

    def mostra_lista_series(self, series, allow_selection=False):
        sg.ChangeLookAndFeel('DarkAmber')

        titulo_subtela = 'Lista de Séries'

        header = ['Título', 'Temporadas', 'Total Episódios']
        data = [[serie.titulo, len(serie.temporadas), sum(
            len(temporada.episodios) for temporada in serie.temporadas)] for serie in series]

        layout = [
            [sg.Text(f'{titulo_subtela:~^40}', font=("Helvica", 25))],
        ]

        if allow_selection:
            radio_buttons = []
            for i, serie in enumerate(series, start=1):
                radio_buttons.append(
                    [sg.Radio(serie.titulo, 'SERIES', key=f'-SERIE-{i}-', enable_events=True)])

            layout.extend(radio_buttons)
            layout.append([sg.Button('Confirmar'), sg.Button('Cancelar')])
        else:
            layout.append([sg.Table(values=data, headings=header, auto_size_columns=True,
                          justification='right', display_row_numbers=False, key='-SERIES-', enable_events=True)])
            layout.append([sg.Button('Voltar')])

        self.window = sg.Window(titulo_subtela).Layout(layout)

        if allow_selection:
            while True:
                button, values = self.open()

                if button == sg.WINDOW_CLOSED or button == 'Confirmar':
                    selected_index = next(
                        (i for i, value in enumerate(values.values()) if value), None)
                    if selected_index is not None:
                        selected_serie = series[selected_index]
                        break
                    else:
                        self.show_message(
                            "Alerta!", "Por favor escolha uma opção antes de confirmar.")
                elif button == 'Cancelar':
                    # Coloquei como None porque o controlador vai verificar, e
                    # caso seja None, ele só abre a tela novamente
                    selected_serie = None
                    break

            self.close()
            return selected_serie
        else:
            while True:
                button, values = self.open()

                if button == sg.WINDOW_CLOSED or button == 'Voltar':
                    break

            self.close()
