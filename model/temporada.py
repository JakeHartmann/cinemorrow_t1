

class Temporada():
    def __init__(self, numero: int):
        if isinstance(numero, int):
            self.numero = numero
        self.episodios = []
