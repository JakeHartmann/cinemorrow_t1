import os
from view.abstract_tela import AbstractTela


class TelaGrupo(AbstractTela):
    def __init__(self):
        pass

    def recebe_input_hora_minutos(self, mensagem):
        while True:
            try:
                entrada = input(mensagem)
                partes = entrada.split(":")
                if len(partes) == 2:
                    hora = int(partes[0])
                    minutos = int(partes[1])
                    if 0 <= hora <= 23 and 0 <= minutos <= 59:
                        return hora, minutos
                    else:
                        print(
                            "Por favor, insira uma hora válida (0-23) e minutos válidos (0-59).")
                else:
                    print("Formato inválido. Use HH:MM.")
            except ValueError:
                print("Entrada inválida. Use HH:MM.")
