from model.serie import Serie
from model.grupo import Grupo


class Progresso():
    def __init__(self, serie: Serie, grupo: Grupo):
        if isinstance(serie, Serie):
            self.__serie = serie
        
        if isinstance(grupo, Grupo):
            self.__grupo = grupo

    @property
    def serie(self):
        return self.__serie
    
    @property
    def grupo(self):
        return self.__grupo
