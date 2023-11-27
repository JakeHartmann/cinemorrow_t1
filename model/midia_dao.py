from model.dao import DAO
from model.midia import Midia


class MidiaDAO(DAO):
    def __init__(self):
        super().__init__('midias.pkl')

    def add(self, midia: Midia):
        if isinstance(midia, Midia) and isinstance(midia.titulo, str):
            super().add(midia.titulo, midia)

    def get(self, titulo: str):
        if isinstance(titulo, str):
            return super().get(titulo)

    def remove(self, titulo: str):
        if isinstance(titulo, str):
            super().remove(titulo)

    def save(self):
        self.dump()
