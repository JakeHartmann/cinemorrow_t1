import os
from view.abstract_tela import AbstractTela
import PySimpleGUI as sg
from datetime import datetime


class TelaGrupo(AbstractTela):
    def __init__(self):
        super().__init__()

    def init_components(self):
        sg.theme('DarkAmber')

        titulo = 'Gerencia de Grupos'

        layout = [
            [sg.Text(f'{titulo:~^40}', font=("Helvica", 25))],
            [sg.Text(f'Escolha sua opção: ', font=("Helvica", 15))],
            [sg.Radio('Adicionar Grupo', "RD1", key='1')],
            [sg.Radio('Remover Grupo', "RD1", key='2')],
            [sg.Radio('Alterar Grupo', "RD1", key='3')],
            [sg.Radio('Listar Grupos', "RD1", key='4')],
            [sg.Button('Confirmar'), sg.Cancel('Retornar')]
        ]

        self.window = sg.Window('Gerencia de Grupos').Layout(layout)

    def tela_opcoes(self):
        self.init_components()

        while True:
            event, values = self.open()

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

    def pega_dados_grupo(self, pessoas, midias):
        sg.ChangeLookAndFeel('DarkAmber')

        titulo_subtela = 'Insira dados do Grupo'

        pessoas_options = [
            f'{pessoa.nome} ({pessoa.email})' for pessoa in pessoas]
        midias_options = [midia.titulo for midia in midias]

        layout = [
            [sg.Text(f'{titulo_subtela:~^40}', font=("Helvica", 25))],
            [sg.Text("Nome do Grupo:"), sg.InputText(key='nome_grupo')],
            [sg.Text("Escolha um integrante base:"), sg.Combo(
                pessoas_options, key='integrante_base')],
            [sg.Text("Escolha uma mídia associada:"), sg.Combo(
                midias_options, key='midia_associada')],
            [sg.Text("Insira a data (Dia-Mês-Ano):")],
            [sg.InputText(key='dia', size=(4, 1)), sg.InputText(
                key='mes', size=(4, 1)), sg.InputText(key='ano', size=(6, 1))],
            [sg.Text("Insira o horário (HH:MM):")],
            [sg.InputText(key='hora', size=(4, 1)),
             sg.InputText(key='minuto', size=(4, 1))],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]

        self.window = sg.Window(titulo_subtela).Layout(layout)

        while True:
            button, values = self.open()

            if button == sg.WINDOW_CLOSED or button == 'Cancelar':
                self.close()
                return None

            elif button == 'Confirmar':
                nome_grupo = values['nome_grupo']
                integrante_base_index = values['integrante_base']
                midia_associada_index = values['midia_associada']
                dia = values['dia']
                mes = values['mes']
                ano = values['ano']
                hora = values['hora']
                minuto = values['minuto']

                if not all([nome_grupo, integrante_base_index, midia_associada_index, dia, mes, ano, hora, minuto]):
                    self.show_message(
                        "Alerta!", "Por favor, preencha todos os campos.")
                    continue

                try:

                    data_str = f'{dia}-{mes}-{ano} {hora}:{minuto}'
                    data_hora = datetime.strptime(data_str, '%d-%m-%Y %H:%M')

                except (ValueError, IndexError, TypeError):
                    self.show_message(
                        "Alerta!", "Por favor, insira dados válidos.")
                    continue

                break

        self.close()

        return nome_grupo, integrante_base_index, midia_associada_index, data_hora

    def mostra_lista_grupos(self, grupos, allow_selection=False):
        sg.ChangeLookAndFeel('DarkAmber')

        titulo_subtela = 'Lista de Grupos'

        header = ['Nome', 'Membros', 'Mídia Associada', 'Próxima Sessão']

        data = []

        for grupo in grupos:
            membros = ', '.join(
                [f'{membro.nome} ({membro.email})' for membro in grupo.pessoas])
            proxima_sessao = grupo.data.strftime(
                '%d/%m/%Y %H:%M') if grupo.data else 'N/A'
            data.append(
                [grupo.nome, membros, grupo.midia_associada.titulo, proxima_sessao])

        max_members = max(len(grupo.pessoas) for grupo in grupos)
        for _ in range(max_members - 1):
            data.append(['', '', '', ''])

        layout = [
            [sg.Text(f'{titulo_subtela:~^40}', font=("Helvica", 25))],
        ]

        if allow_selection:
            radio_buttons = []
            for i, grupo in enumerate(grupos, start=1):
                display_text = f'{grupo.nome} - {grupo.midia_associada.titulo} ({proxima_sessao})'
                radio_buttons.append(
                    sg.Radio(display_text, 'GRUPOS', key=f'-GRUPO-{i}-', enable_events=True))

            layout.append(radio_buttons)
            layout.append([sg.Button('Avançar'), sg.Button('Retornar')])
        else:
            layout.append([sg.Table(values=data, headings=header, auto_size_columns=True,
                          justification='right', display_row_numbers=False, key='-GRUPOS-', enable_events=True)])
            layout.append([sg.Button('Retornar')])

        self.window = sg.Window(titulo_subtela).Layout(layout)

        if allow_selection:
            while True:
                button, values = self.open()

                if button == sg.WINDOW_CLOSED or button == 'Avançar' or button == 'Retornar':
                    selected_index = next(
                        (i for i, value in enumerate(values.values()) if value), None)
                    if selected_index is not None:
                        selected_grupo = grupos[selected_index]
                        break
                    elif button == sg.WINDOW_CLOSED or button == 'Retornar':
                        selected_grupo = None
                        break
                    else:
                        self.show_message(
                            "Alerta!", "Por favor, escolha uma opção antes de avançar.")

            self.close()
            return selected_grupo
        else:
            while True:
                button, values = self.open()

                if button == sg.WINDOW_CLOSED or button == 'Retornar':
                    break

            self.close()

    def mostra_opcoes_alteracao(self):
        sg.ChangeLookAndFeel('DarkAmber')

        titulo_subtela = 'Opções de Alteração'

        layout = [
            [sg.Text(f'{titulo_subtela:~^40}', font=("Helvica", 25))],
            [sg.Radio('Alterar Nome', 'OPCOES',
                      key='-ALTERAR_NOME-', enable_events=True)],
            [sg.Radio('Adicionar Membro', 'OPCOES',
                      key='-ADICIONAR_MEMBRO-', enable_events=True)],
            [sg.Radio('Remover Membro', 'OPCOES',
                      key='-REMOVER_MEMBRO-', enable_events=True)],
            [sg.Radio('Alterar Data da Próxima Sessão', 'OPCOES',
                      key='-ALTERAR_DATA_SESSAO-', enable_events=True)],
            [sg.Button('Avançar'), sg.Button('Retornar')]
        ]

        self.window = sg.Window(titulo_subtela).Layout(layout)

        while True:
            button, values = self.open()

            if button == sg.WINDOW_CLOSED or button == 'Retornar':
                opcao = None
                break

            elif button == 'Avançar':
                opcao = next(
                    (option for option, value in values.items() if value), None)
                if opcao:
                    break
                else:
                    self.show_message(
                        "Alerta!", "Por favor, escolha uma opção antes de avançar.")

        self.close()
        return opcao

    def pega_nome_grupo(self):
        sg.ChangeLookAndFeel('DarkAmber')

        titulo_subtela = 'Novo Nome para o Grupo'

        layout = [
            [sg.Text(f'{titulo_subtela:~^40}', font=("Helvica", 25))],
            [sg.Text("Digite o novo nome para o grupo:"),
             sg.InputText(key='novo_nome')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]

        self.window = sg.Window(titulo_subtela).Layout(layout)

        while True:
            button, values = self.open()

            if button == sg.WINDOW_CLOSED or button == 'Cancelar':
                self.close()
                return None

            elif button == 'Confirmar':
                novo_nome = values['novo_nome'].strip()

                if novo_nome:
                    break
                else:
                    self.show_message(
                        "Alerta!", "Por favor, insira um novo nome para o grupo.")

        self.close()
        return novo_nome

    def seleciona_pessoa(self, disponiveis):
        sg.ChangeLookAndFeel('DarkAmber')

        titulo_subtela = 'Selecione uma Pessoa'

        pessoas_options = [
            f'{pessoa.nome} ({pessoa.email})' for pessoa in disponiveis]

        layout = [
            [sg.Text(f'{titulo_subtela:~^40}', font=("Helvica", 25))],
        ]

        radio_buttons = []
        for i, pessoa_option in enumerate(pessoas_options):
            radio_buttons.append(
                sg.Radio(pessoa_option, 'PESSOAS', key=f'-PESSOA-{i}-', enable_events=True))

        layout.append(radio_buttons)
        layout.append([sg.Button('Confirmar'), sg.Button('Cancelar')])

        self.window = sg.Window(titulo_subtela).Layout(layout)

        while True:
            button, values = self.open()

            if button == sg.WINDOW_CLOSED or button == 'Cancelar':
                self.close()
                return None

            elif button == 'Confirmar':
                selected_index = next(
                    (i for i, value in enumerate(values.values()) if value), None)

                if selected_index is not None:
                    selected_pessoa = disponiveis[selected_index]
                    email = selected_pessoa.email
                    break
                else:
                    self.show_message(
                        "Alerta!", "Por favor, escolha uma pessoa antes de confirmar.")

        self.close()
        return email

    def pega_data(self):
        sg.ChangeLookAndFeel('DarkAmber')

        titulo_subtela = 'Escolha da Data e Hora'

        layout = [
            [sg.Text(f'{titulo_subtela:~^40}', font=("Helvetica", 25))],
            [sg.CalendarButton('Escolha a Data', target="-DATA-", key="-CALENDAR-", format="%Y-%m-%d"),
             sg.InputText(key='-DATA-', disabled=True, size=(12, 1)),
             sg.Text("Hora:"),
             sg.InputText(key='hora', size=(2, 1)),
             sg.Text("Minutos:"),
             sg.InputText(key='minuto', size=(2, 1))],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]

        self.window = sg.Window(titulo_subtela).Layout(layout)

        while True:
            button, values = self.open()

            if button == sg.WINDOW_CLOSED or button == 'Cancelar':
                self.close()
                return None

            elif button == 'Confirmar':
                data = values['-DATA-']
                hora = values['hora']
                minuto = values['minuto']

                try:
                    data_hora_str = f'{data} {hora.zfill(2)}:{minuto.zfill(2)}'
                    data_hora = datetime.strptime(
                        data_hora_str, '%Y-%m-%d %H:%M')
                except ValueError:
                    self.show_message(
                        "Alerta!", "Por favor, insira uma data e horário válidos.")
                    continue

                break

        self.close()
        return data_hora
