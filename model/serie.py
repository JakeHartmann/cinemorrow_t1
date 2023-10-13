from model.midia import Midia


class Serie(Midia):
    def __init__(self, titulo: str):
        self.__temporadas = []
        if isinstance(titulo, str):
            super().__init__(titulo)

    @property
    def temporadas(self):
        if self.__temporadas:
            return self.__temporadas
