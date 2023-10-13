

class Episodio():
    def __init__(self, duracao: int):
        if isinstance(duracao, int):
            self.__duracao = duracao

    @property
    def duracao(self):
        if self.__duracao is not None:
            return self.__duracao

    @duracao.setter
    def duracao(self, duracao: int):
        if isinstance(duracao, int):
            self.__duracao = duracao
