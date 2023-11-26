from model.dao import DAO
from model.grupo import Grupo


class GrupoDAO(DAO):
    def __init__(self):
        super().__init__('grupos.pkl')

    def add(self, grupo: Grupo):
        if isinstance(grupo, Grupo) and isinstance(grupo.nome, str):
            super().add(grupo.nome, grupo)

    def get(self, nome: str):
        if isinstance(nome, str):
            return super().get(nome)
        
    def remove(self, nome: str):
        if isinstance(nome, str):
            super().remove(nome)

    # Generalizar depois
    def save(self):
        self.dump()