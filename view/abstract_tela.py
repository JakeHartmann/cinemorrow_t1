from abc import ABC, abstractmethod
import os


class AbstractTela(ABC):
    @abstractmethod
    def __init__(self):
        pass
        
    def output_texto(self, texto):
        print(texto)

    def recebe_input_int(self, mensagem: str = "", inteiros_validos: [] = None, limite: int = None):
        while True:
            valor_lido = input(mensagem)
            try:
                inteiro = int(valor_lido)

                if inteiros_validos and inteiro not in inteiros_validos:
                    raise ValueError

                if limite is not None and inteiro > limite:
                    confirmacao = self.recebe_input_sn(
                        "Você tem certeza? Parece um número bem grande (S/N)")
                    if not confirmacao:
                        continue

                if inteiro < 0:
                    raise ValueError

                return inteiro

            except ValueError:
                print("\nPor favor digite um número válido e que seja positivo")

    def recebe_input_sn(self, mensagem: str = ""):
        while True:
            valor_lido = input(mensagem).upper()
            if valor_lido == "S":
                return True
            elif valor_lido == "N":
                return False
            else:
                print("\nPor favor digite 'S' para Sim ou 'N' para Não.")

    def recebe_input_str(self, mensagem: str = ""):
        while True:
            valor_lido = input(mensagem)
            if valor_lido.strip():
                return valor_lido.strip()
            else:
                print("\nPor favor, digite um valor válido.")
