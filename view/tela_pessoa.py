import os
from view.abstract_tela import AbstractTela
import PySimpleGUI as sg


class TelaPessoa(AbstractTela):
    def __init__(self):
        super().__init__()

    def init_components(self):
        sg.theme('DarkAmber')

        titulo = 'Gerencia de Pessoas'

        layout = [
            [sg.Text(f'{titulo:~^40}', font=("Helvica", 25))],
            [sg.Text(f'Escolha sua opção: ', font=("Helvica", 15))],
            [sg.Radio('Adicionar Pessoa', "RD1", key='1')],
            [sg.Radio('Remover Pessoa', "RD1", key='2')],
            [sg.Radio('Alterar Pessoa', "RD1", key='3')],
            [sg.Radio('Listar Pessoas', "RD1", key='4')],
            [sg.Button('Confirmar'), sg.Cancel('Retornar')]
        ]

        self.window = sg.Window('Gerencia de Pessoas').Layout(layout)

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

    def pega_dados_pessoa(self, novos_dados=False):
        sg.ChangeLookAndFeel('DarkAmber')

        titulo_subtela = 'Insira dados da Pessoa'
        if novos_dados:
            titulo_subtela += ' - Configurando Novos Dados'

        layout = [
            [sg.Text(f'{titulo_subtela:~^40}', font=("Helvica", 25))],
            [sg.Text("Nome:"), sg.InputText(key='nome')],
            [sg.Text("E-Mail:"), sg.InputText(key='email')],
            [sg.Text("Escolha um tipo de mídia favorita:"), sg.Radio('Filme', 'TIPO_MIDIA', key='filme'), sg.Radio(
                'Série', 'TIPO_MIDIA', key='serie'), sg.Radio('Nenhuma', 'TIPO_MIDIA', key='nenhuma')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]

        self.window = sg.Window(titulo_subtela).Layout(layout)

        while True:
            button, values = self.open()

            if button == sg.WINDOW_CLOSED or button == 'Cancelar':
                self.close()
                return None, None, None

            elif button == 'Confirmar':
                nome = values['nome']
                email = values['email']
                tipo_midia_fav = 'Nenhuma'

                if values['filme']:
                    tipo_midia_fav = 'Filme'
                elif values['serie']:
                    tipo_midia_fav = 'Série'

                if nome.strip() == '' or email.strip() == '':
                    self.show_message(
                        "Alerta!", "Por favor, insira dados válidos.")
                else:
                    break

        self.close()

        return nome, email, tipo_midia_fav

    def mostra_lista_pessoas(self, pessoas, allow_selection=False):
        sg.ChangeLookAndFeel('DarkAmber')

        titulo_subtela = 'Lista de Pessoas'

        header = ['Nome', 'Email', 'Tipo Mídia Favorita']
        data = [[pessoa.nome, pessoa.email, pessoa.midia_fav]
                for pessoa in pessoas]

        layout = [
            [sg.Text(f'{titulo_subtela:~^40}', font=("Helvica", 25))],
        ]

        if allow_selection:
            radio_buttons = []
            for i, pessoa in enumerate(pessoas, start=1):
                display_text = f'{pessoa.nome} ({pessoa.email})'
                radio_buttons.append(
                    sg.Radio(display_text, 'PESSOAS', key=f'-PESSOA-{i}-', enable_events=True))

            layout.append(radio_buttons)
            layout.append([sg.Button('Confirmar'), sg.Button('Cancelar')])
        else:
            layout.append([sg.Table(values=data, headings=header, auto_size_columns=True,
                          justification='right', display_row_numbers=False, key='-PESSOAS-', enable_events=True)])
            layout.append([sg.Button('Voltar')])

        self.window = sg.Window(titulo_subtela).Layout(layout)

        if allow_selection:
            while True:
                button, values = self.open()

                if button == sg.WINDOW_CLOSED or button == 'Confirmar':
                    selected_index = next(
                        (i for i, value in enumerate(values.values()) if value), None)
                    if selected_index is not None:
                        selected_pessoa = pessoas[selected_index]
                        break
                    else:
                        self.show_message(
                            "Alerta!", "Por favor, escolha uma opção antes de confirmar.")
                elif button == 'Cancelar':
                    selected_pessoa = None
                    break
            self.close()
            return selected_pessoa
        else:
            while True:
                button, values = self.open()

                if button == sg.WINDOW_CLOSED or button == 'Voltar':
                    break

            self.close()
