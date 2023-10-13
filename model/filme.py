from model.midia import Midia


class Filme(Midia):
    def __init__(self, titulo: str):
        if isinstance(titulo, str):
            super().__init__(titulo)
