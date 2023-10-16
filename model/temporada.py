

class Temporada():
    def __init__(self, numero: int):
        if isinstance(numero, int):
            self.numero = numero
        self.episodios = []

    # @property
    # def numero(self):
    #     return self.__numero
    # @numero.setter
    # def numero(self, numero):
    #     self.__numero = numero
