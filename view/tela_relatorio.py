from view.abstract_tela import AbstractTela
from collections import Counter
import PySimpleGUI as sg


class TelaRelatorio(AbstractTela):
    def __init__(self):
        super().__init__()

    def mostra_relatorio(self, pessoas, num_registro):
        sg.ChangeLookAndFeel('DarkAmber')

        midias_fav = [
            pessoa.midia_fav for pessoa in pessoas if pessoa.midia_fav != 'Nenhuma']

        if midias_fav:
            contagem_midias = Counter(midias_fav)
            mais_comuns = contagem_midias.most_common()

            output_text = ""
            if len(mais_comuns) > 1 and mais_comuns[0][1] == mais_comuns[1][1]:
                output_text += "Empate! Os tipos de mídia favoritos mais comuns são:\n"
                for midia, quantidade in mais_comuns:
                    output_text += f"{midia}: Quantidade: {quantidade}\n Desde que você abriu o programa, você gerou esse relatório {num_registro} vezes."
            else:
                tipo_midia_mais_comum, quantidade = mais_comuns[0]
                output_text += f"O tipo de mídia favorita mais comum é: {tipo_midia_mais_comum}\n Quantidade: {quantidade}\n Desde que você abriu o programa, você gerou esse relatório {num_registro} vezes."

            layout = [
                [sg.Text("Resultados do Tipo de Mídia Mais Favorita",
                         font=("Helvetica", 20))],
                [sg.Multiline(output_text, key="-OUTPUT-",
                              size=(50, 10), disabled=True, autoscroll=True)],
                [sg.Button("Fechar")]
            ]

            self.window = sg.Window("Resultado").Layout(layout)

            while True:
                button, _ = self.open()

                if button == sg.WINDOW_CLOSED or button == 'Fechar':
                    self.close()
                    return None

        else:
            self.show_message("Alerta!", "Sem informações disponíveis.")

        self.close()

    def init_components(self):
        sg.ChangeLookAndFeel('DarkAmber')

        titulo_subtela = 'Relatórios'

        layout = [
            [sg.Text(f'{titulo_subtela:~^40}', font=("Helvetica", 25))],
            [sg.Button("Tipo de Mídia mais favorito", key='Tipo_Midia')],
            [sg.Button("Voltar", key='Voltar')]
        ]

        self.window = sg.Window('Relatórios').Layout(layout)

    def tela_opcoes(self):
        self.init_components()
        button, values = self.open()
        if button == 'Voltar':
            opcao = 'Voltar'
        else:
            opcao = 'Tipo_Midia'

        self.close()
        return opcao
