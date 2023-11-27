

class Episodio():
    def __init__(self, numero: int):
        if isinstance(numero, int):
            self.__numero = numero

        self.__assistido = False

    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, numero):
        if isinstance(numero, int):
            self.__numero = numero

    @property
    def assistido(self):
        return self.__assistido

    @assistido.setter
    def assistido(self, assistido):
        if isinstance(assistido, bool):
            self.__assistido = assistido
        else:
            print("O valor de assistido deve ser um booleano.")
