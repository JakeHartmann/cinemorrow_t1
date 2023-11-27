import os
from view.abstract_tela import AbstractTela
import PySimpleGUI as sg


class TelaPrincipal(AbstractTela):
    def __init__(self):
        super().__init__()

    def init_components(self):
        sg.theme('DarkAmber')

        titulo = 'Bem-vindo ao sistema Cinemorrow'

        layout = [
            [sg.Text(f'{titulo:~^6}', font=("Helvica", 25))],
            [sg.Text(f'Escolha sua opção: ', font=("Helvica", 15))],
            [sg.Radio('Gerenciar Mídias', "RD1", key='1')],
            [sg.Radio('Gerenciar Pessoas', "RD1", key='2')],
            [sg.Radio('Gerenciar Grupos', "RD1", key='3')],
            [sg.Radio('Relatórios', "RD1", key='4')],
            [sg.Radio('Encerrar sistema', "RD1", key='5')],
            [sg.Button('Confirmar')]
        ]

        self.window = sg.Window('Cinemorrow').Layout(layout)

    def tela_opcoes(self):
        self.init_components()

        while True:
            event, values = self.open()

            if event == sg.WINDOW_CLOSED:
                opcao = None
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
