from model.midia import Midia


class Serie(Midia):
    def __init__(self, titulo: str):
        self.temporadas = []
        if isinstance(titulo, str):
            super().__init__(titulo)
